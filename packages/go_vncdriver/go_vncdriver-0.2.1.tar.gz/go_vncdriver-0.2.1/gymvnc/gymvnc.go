package gymvnc

import (
	"net"
	"sync"
	"time"

	"github.com/juju/errors"
	"github.com/op/go-logging"
	"github.com/openai/gym-vnc/go-vncdriver/vncclient"
)

var log = logging.MustGetLogger("gymvnc")

type sessionMgr struct {
	Ready      sync.WaitGroup
	Done       chan bool
	Error      chan error
	Terminated sync.WaitGroup
}

func NewSessionMgr() *sessionMgr {
	return &sessionMgr{
		Done:  make(chan bool),
		Error: make(chan error, 1),
	}
}

func (s *sessionMgr) Close() {
	close(s.Done)
}

type VNCSession struct {
	address string
	mgr     *sessionMgr
	conn    *vncclient.ClientConn

	frontScreen              *Screen
	backScreen               *Screen
	backUpdated              bool
	deferredUpdates          []*vncclient.FramebufferUpdateMessage
	deferredUpdatesDiscarded bool
	lock                     sync.Mutex

	renderer       Renderer
	rendererActive bool

	compressLevel int
}

func NewVNCSession(address string, mgr *sessionMgr, compressLevel int) *VNCSession {
	if compressLevel < 0 {
		log.Warningf("[%s] Compress level %d requested, but valid values are betweeen 0 (least compression) and 9 (most compression). Using 0 intead.", address, compressLevel)
		compressLevel = 0
	} else if compressLevel > 9 {
		log.Warningf("[%s] Compress level %d requested, but valid values are betweeen 0 (least compression) and 9 (most compression). Using 9 instead.", address, compressLevel)
		compressLevel = 9
	}

	c := &VNCSession{
		address:       address,
		mgr:           mgr,
		backUpdated:   true,
		compressLevel: compressLevel,
	}
	c.start()
	return c
}

func (c *VNCSession) start() {
	updates := make(chan *vncclient.FramebufferUpdateMessage, 4096)

	// Called from main thread. Will call Done once this session
	// is fully setup.
	c.mgr.Ready.Add(1)

	// Maintains the connection to the remote
	go func() {
		err := c.connect(updates)
		if err != nil {
			// Try reporting the error
			select {
			case c.mgr.Error <- err:
			default:
			}
		}
	}()
}

func (c *VNCSession) Step(events []VNCEvent) error {
	for _, event := range events {
		err := event.Execute(c.conn)
		if err != nil {
			return errors.Annotatef(err, "could not step %s", c.address)
		}
	}
	return nil
}

func (c *VNCSession) SetRenderer(renderer Renderer) error {
	if c.rendererActive {
		return errors.New("cannot change renderer while active")
	}
	c.renderer = renderer
	return nil
}

// Must call from main thread
func (c *VNCSession) Render() error {
	if c.renderer == nil {
		return errors.New("VNCSession has no renderer. This likely means your go_vncdriver was installed without the OpenGL viewer. See https://github.com/openai/gym-vnc/tree/master/go-vncdriver for instructions on how to install with the OpenGL viewer.")
	}

	if !c.rendererActive {
		if err := c.renderer.Init(c.conn.FramebufferWidth, c.conn.FramebufferHeight, c.conn.DesktopName, c.frontScreen.Data); err != nil {
			return errors.Annotate(err, "could not render")
		}
		c.rendererActive = true
	}

	c.renderer.Render()
	return nil
}

func dummyUpdateBuffer(screen *Screen) []*vncclient.FramebufferUpdateMessage {
	return []*vncclient.FramebufferUpdateMessage{
		&vncclient.FramebufferUpdateMessage{
			Rectangles: []vncclient.Rectangle{
				vncclient.Rectangle{
					X:      0,
					Y:      0,
					Width:  screen.Width,
					Height: screen.Height,
					Enc: &vncclient.RawEncoding{
						Colors: screen.Data,
					},
				},
			},
		},
	}
}

// If rendering, must call from main thread
func (c *VNCSession) Flip() (*Screen, []*vncclient.FramebufferUpdateMessage) {
	c.lock.Lock()
	defer c.lock.Unlock()

	var updates []*vncclient.FramebufferUpdateMessage

	if c.backUpdated {
		c.frontScreen, c.backScreen = c.backScreen, c.frontScreen
		c.backUpdated = false
		updates = c.deferredUpdates
		if c.deferredUpdatesDiscarded {
			// Slow path

			// We'd discarded the pending updates, so we
			// need to copy, from the new front screen
			// (which has been kept nicely up to date)
			copy(c.backScreen.Data, c.frontScreen.Data)
			c.deferredUpdatesDiscarded = false

			if c.rendererActive {
				// Keep the GL screen fed
				updates := dummyUpdateBuffer(c.backScreen)
				c.renderer.Apply(updates)
			}
		} else {
			// Fast path: apply all the updates in the background

			go func() {
				c.lock.Lock()
				defer c.lock.Unlock()

				c.applyDeferred()
			}()

			if c.rendererActive {
				// Keep the GL screen fed
				c.renderer.Apply(updates)
			}
		}
	}

	return c.frontScreen, updates
}

// Apply any deferred updates *while holding the lock*
func (c *VNCSession) applyDeferred() error {
	if c.backUpdated {
		return nil
	}
	c.backUpdated = true

	for _, update := range c.deferredUpdates {
		c.applyUpdate(update)
	}
	c.deferredUpdates = nil
	return nil
}

// Apply an update *while holding the lock*
func (c *VNCSession) applyUpdate(update *vncclient.FramebufferUpdateMessage) error {
	var bytes uint32
	start := time.Now().UnixNano()
	for _, rect := range update.Rectangles {
		switch enc := rect.Enc.(type) {
		case *vncclient.RawEncoding:
			bytes += c.applyRect(c.conn, rect, enc.Colors)
		case *vncclient.ZRLEEncoding:
			bytes += c.applyRect(c.conn, rect, enc.Colors)
		default:
			return errors.Errorf("unsupported encoding: %T", enc)
		}
	}
	delta := time.Now().UnixNano() - start
	log.Debugf("[%s] Update complete: time=%dus type=%T rectangles=%+v bytes=%d", c.address, delta/1000, update, len(update.Rectangles), bytes)
	return nil
}

func (c *VNCSession) applyRect(conn *vncclient.ClientConn, rect vncclient.Rectangle, colors []vncclient.Color) uint32 {
	var bytes uint32
	// var wg sync.WaitGroup
	// wg.Add(int(rect.Height))
	for y := uint32(0); y < uint32(rect.Height); y++ {
		// go func(y uint32) {
		encStart := uint32(rect.Width) * y
		encEnd := encStart + uint32(rect.Width)

		screenStart := uint32(conn.FramebufferWidth)*(uint32(rect.Y)+y) + uint32(rect.X)
		screenEnd := screenStart + uint32(rect.Width)

		bytes += encEnd - encStart
		copy(c.backScreen.Data[screenStart:screenEnd], colors[encStart:encEnd])
		// wg.Done()
		// }(y)
	}
	// wg.Wait()
	return bytes
}

func (c *VNCSession) maintainFrameBuffer(updates chan *vncclient.FramebufferUpdateMessage) error {
	done := false

	// While the VNC protocol supports more exotic formats, we
	// only want straight RGB with 1 byte per color.
	c.frontScreen = NewScreen(c.conn.FramebufferWidth, c.conn.FramebufferHeight)
	c.backScreen = NewScreen(c.conn.FramebufferWidth, c.conn.FramebufferHeight)

	for {
		select {
		case update := <-updates:
			c.lock.Lock()
			if err := c.applyDeferred(); err != nil {
				c.lock.Unlock()
				return errors.Annotate(err, "when applying deferred updates")
			}

			if err := c.applyUpdate(update); err != nil {
				c.lock.Unlock()
				return errors.Annotate(err, "when applying new update")
			}

			// If we queue more than 20 updates, the user
			// is falling far behind and we should just
			// pay for a copy on the next flip.
			if c.deferredUpdatesDiscarded {
				// Nothing to do
			} else if len(c.deferredUpdates) < 20 {
				c.deferredUpdates = append(c.deferredUpdates, update)
			} else {
				log.Debugf("[%s] exceeded 20 pending updates; next flip will result in a copy", c.address)
				c.deferredUpdatesDiscarded = true
				c.deferredUpdates = nil
			}
			c.lock.Unlock()
		case <-c.mgr.Done:
			log.Debugf("[%s] shutting down frame buffer thread", c.address)
			return nil
		}

		if !done {
			c.mgr.Ready.Done()
			done = true
		}
	}
}

func (c *VNCSession) connect(updates chan *vncclient.FramebufferUpdateMessage) error {
	log.Infof("[%s] connecting", c.address)

	target, err := net.Dial("tcp", c.address)
	if err != nil {
		return errors.Annotate(err, "could not connect to server")
	}

	errorCh := make(chan error)
	serverMessageCh := make(chan vncclient.ServerMessage)
	conn, err := vncclient.Client(target, &vncclient.ClientConfig{
		Auth: []vncclient.ClientAuth{
			&vncclient.PasswordAuth{
				Password: "openai",
			},
		},
		ServerMessageCh: serverMessageCh,
		ErrorCh:         errorCh,
	})
	if err != nil {
		return errors.Annotate(err, "could not establish VNC connection to server")
	}

	go func() {
		select {
		case err := <-errorCh:
			c.mgr.Error <- errors.Annotatef(err, "[%s] vnc error", c.address)
		case <-c.mgr.Done:
		}
	}()

	c.conn = conn
	log.Infof("[%s] connection established", c.address)

	// Spin up a screenbuffer thread
	go func() {
		err := c.maintainFrameBuffer(updates)
		if err != nil {
			// Report the error, if any
			select {
			case c.mgr.Error <- err:
			default:
			}
		}
	}()

	conn.SetPixelFormat(&vncclient.PixelFormat{
		BPP:        32,
		Depth:      24,
		BigEndian:  false,
		TrueColor:  true,
		RedMax:     255,
		GreenMax:   255,
		BlueMax:    255,
		RedShift:   0,
		GreenShift: 8,
		BlueShift:  16,
	})

	conn.SetEncodings([]vncclient.Encoding{
		&vncclient.ZRLEEncoding{},
		&vncclient.RawEncoding{},
		&vncclient.CompressLevel{uint32(c.compressLevel)},
	})

	conn.FramebufferUpdateRequest(true, 0, 0, conn.FramebufferWidth, conn.FramebufferHeight)

	for {
		select {
		case msg := <-serverMessageCh:
			log.Debugf("[%s] Just received: %T %+v", c.address, msg, msg)
			switch msg := msg.(type) {
			case *vncclient.FramebufferUpdateMessage:
				updates <- msg
				// Keep re-requesting!
				conn.FramebufferUpdateRequest(true, 0, 0, conn.FramebufferWidth, conn.FramebufferHeight)
			}
		case <-c.mgr.Done:
			log.Debugf("[%s] terminating VNC connection as requested", c.address)
			if err := conn.Close(); err != nil {
				return err
			}
			return nil
		}
	}
}

type VNCBatch struct {
	lock     sync.Mutex
	error    error
	sessions []*VNCSession
}

func (v *VNCBatch) Check() error {
	v.lock.Lock()
	defer v.lock.Unlock()
	return v.error
}

func (v *VNCBatch) setError(err error) {
	v.lock.Lock()
	defer v.lock.Unlock()
	v.error = err
}

func (v *VNCBatch) N() int {
	return len(v.sessions)
}

func (v *VNCBatch) Step(actions [][]VNCEvent) error {
	for i, action := range actions {
		session := v.sessions[i]

		err := session.Step(action)
		if err != nil {
			return errors.Annotate(err, "could not step")
		}
	}
	return nil
}

func (v *VNCBatch) SetRenderer(renderer Renderer) error {
	return v.sessions[0].SetRenderer(renderer)
}

func (v *VNCBatch) Render() error {
	return v.sessions[0].Render()
}

func (v *VNCBatch) Flip() (screens []*Screen, updates [][]*vncclient.FramebufferUpdateMessage) {
	for _, session := range v.sessions {
		screen, update := session.Flip()
		screens = append(screens, screen)
		updates = append(updates, update)
	}
	return
}

func (v *VNCBatch) Peek() (screens []*Screen) {
	for _, session := range v.sessions {
		screens = append(screens, session.frontScreen)
	}
	return
}

func (v *VNCBatch) PeekBack() (screens []*Screen) {
	for _, session := range v.sessions {
		screens = append(screens, session.backScreen)
	}
	return
}

func NewVNCBatch(remotes []string, compressLevel int, done chan bool, errCh chan error) (*VNCBatch, error) {
	batch := &VNCBatch{}
	mgr := NewSessionMgr()

	for _, address := range remotes {
		batch.sessions = append(batch.sessions, NewVNCSession(address, mgr, compressLevel))
	}

	allReady := make(chan bool)
	go func() {
		mgr.Ready.Wait()
		allReady <- true
	}()

	select {
	case <-allReady:
		go func() {
			select {
			case <-done:
				log.Debugf("Closing VNC batch due to user request")
				// Translate 'done' closing into closing down
				// this pipeline.
				close(mgr.Done)
			case err := <-mgr.Error:
				log.Debugf("Closing VNCBatch due to error: %s", err)

				// Capture the relevant error, and let
				// the user know.
				batch.setError(err)
				errCh <- err
				close(mgr.Done)
			}
		}()

		return batch, nil
	case err := <-mgr.Error:
		return nil, err
	case <-done:
		// upstream requested a cancelation
		mgr.Close()
		return nil, nil
	}
}
