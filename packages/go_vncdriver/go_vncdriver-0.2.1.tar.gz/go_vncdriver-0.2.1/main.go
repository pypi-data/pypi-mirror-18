package main

/*
#define Py_LIMITED_API
#include <Python.h>
#include <stdlib.h>
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <numpy/arrayobject.h>

PyObject *get_go_vncdriver_VNCSession_type();
PyObject *GoPyArray_SimpleNew(int nd, npy_intp* dims, int typenum);
PyObject *GoPyArray_SimpleNewFromData(int nd, npy_intp* dims, int typenum, void *data);
void PyErr_SetGoVNCDriverError(char* msg);

// Workaround missing variadic function support
// https://github.com/golang/go/issues/975
static int PyArg_ParseTuple_list_O(PyObject *args, PyObject **a) {
    return PyArg_ParseTuple(args, "O", &PyList_Type, a);
}

static int PyArg_ParseTuple_list_O_bang_O_I(PyObject *args, PyObject **a, PyObject **b, int *c) {
    return PyArg_ParseTuple(args, "O!OI", &PyList_Type, a, b, c);
}

static PyObject *PyTuple_Pack_2(PyObject *a, PyObject *b) {
    return PyTuple_Pack(2, a, b);
}

static PyObject *PyObject_CallFunctionObjArgs_1(PyObject *callable, PyObject *a) {
    return PyObject_CallFunctionObjArgs(callable, a, NULL);
}

typedef struct {
      PyObject_HEAD
      PyObject *remotes;
} go_vncdriver_VNCSession_object;

// Can't access macros through cgo
static void go_vncdriver_decref(PyObject *obj) {
    Py_DECREF(obj);
}

static void go_vncdriver_incref(PyObject *obj) {
    Py_INCREF(obj);
}
*/
import "C"
import (
	"fmt"
	"sync"
	"unsafe"

	"github.com/juju/errors"
	"github.com/op/go-logging"
	"github.com/openai/gym-vnc/go-vncdriver/gymvnc"
	"github.com/openai/gym-vnc/go-vncdriver/vncclient"
)

var (
	log     = logging.MustGetLogger("go_vncdriver")
	data    = [1024 * 768 * 3]uint8{}
	Py_None = &C._Py_NoneStruct
)

var (
	vncUpdatesN          *C.PyObject = nil
	vncUpdatesPixels     *C.PyObject = nil
	vncUpdatesRectangles *C.PyObject = nil
	vncUpdatesBytes      *C.PyObject = nil
	setup                bool        = false
)

func setupOnce() {
	if setup {
		return
	}
	setup = true

	// Must hold the GIL when we init these. Thus don't need
	// Go-level locking as well.
	vncUpdatesN = C.PyUnicode_FromString(C.CString("vnc.updates.n"))
	vncUpdatesPixels = C.PyUnicode_FromString(C.CString("vnc.updates.pixels"))
	vncUpdatesRectangles = C.PyUnicode_FromString(C.CString("vnc.updates.rectangles"))
	vncUpdatesBytes = C.PyUnicode_FromString(C.CString("vnc.updates.bytes"))
}

type batchInfo struct {
	done  chan bool
	batch *gymvnc.VNCBatch

	screenPylist      *C.PyObject
	infoPylist        *C.PyObject
	infoPydicts       []*C.PyObject
	screenInfoPytuple *C.PyObject
	screenNumpy       map[*gymvnc.Screen]*C.PyObject
}

// Sets the Python error for you
func (b *batchInfo) populateScreenPylist(screens []*gymvnc.Screen) bool {
	for i, screen := range screens {
		ary, ok := b.screenNumpy[screen]
		if !ok {
			err := errors.Errorf("missing Numpy object for screen: %d", i)
			setError(errors.ErrorStack(err))
			return false
		}

		C.go_vncdriver_incref(ary)
		if C.PyList_SetItem(b.screenPylist, C.Py_ssize_t(i), ary) == C.int(-1) {
			return false
		}
	}
	return true
}

// Preallocate all needed Python objects, so we don't need to
// generate a lot of garbage.
func (b *batchInfo) preallocatePythonObjects() bool {
	// Create holder for info dictionaries. Populate those now.
	n := b.batch.N()
	b.infoPylist = C.PyList_New(C.Py_ssize_t(n))

	for i := 0; i < n; i++ {
		infoPydict := C.PyDict_New()
		b.infoPydicts = append(b.infoPydicts, infoPydict)

		if C.PyList_SetItem(b.infoPylist, C.Py_ssize_t(i), infoPydict) == C.int(-1) {
			return false
		}
	}

	// Create holder for numpy screens. Populate it at flip/peek
	// time using the front screens.
	b.screenPylist = C.PyList_New(C.Py_ssize_t(b.batch.N()))
	// Create numpy screens
	screens := append(b.batch.Peek(), b.batch.PeekBack()...)
	b.screenNumpy = make(map[*gymvnc.Screen]*C.PyObject)
	for _, screen := range screens {
		dims := []C.npy_intp{C.npy_intp(screen.Height), C.npy_intp(screen.Width), 3}
		ary := C.GoPyArray_SimpleNewFromData(3, &dims[0], C.NPY_UINT8, unsafe.Pointer(&screen.Data[0]))
		b.screenNumpy[screen] = ary
	}

	b.screenInfoPytuple = C.PyTuple_Pack_2(b.screenPylist, b.infoPylist)
	return true
}

var (
	batchMgr  = map[uintptr]batchInfo{}
	batchLock sync.Mutex
)

//export GoVNCDriver_VNCSession_c_init
func GoVNCDriver_VNCSession_c_init(self *C.go_vncdriver_VNCSession_object, args *C.PyObject) C.int {
	setupOnce()

	listObj := new(*C.PyObject)
	errorCallable := new(*C.PyObject)
	compressLevelC := new(C.int)

	if C.PyArg_ParseTuple_list_O_bang_O_I(args, listObj, errorCallable, compressLevelC) == 0 {
		return C.int(-1)
	}

	// Going to keep a pointer around
	C.go_vncdriver_incref(*errorCallable)

	remotes := []string{}
	size := C.PyList_Size(*listObj)
	for i := 0; i < int(size); i++ {
		// Look at the i'th item and convert to a Go string
		listItem := C.PyList_GetItem(*listObj, C.Py_ssize_t(i))
		if listItem == nil {
			return C.int(-1)
		}
		unicodeObj := C.PyUnicode_FromObject(listItem)
		if unicodeObj == nil {
			return C.int(-1)
		}
		byteObj := C.PyUnicode_AsASCIIString(unicodeObj)
		if byteObj == nil {
			return C.int(-1)
		}
		strObj := C.PyBytes_AsString(byteObj)
		if strObj == nil {
			return C.int(-1)
		}
		str := C.GoString(strObj)
		remotes = append(remotes, str)
	}
	compressLevel := int(*compressLevelC)

	errCh := make(chan error, 10)
	done := make(chan bool)
	batch, err := gymvnc.NewVNCBatch(remotes, compressLevel, done, errCh)
	if err != nil {
		close(done)
		setError(errors.ErrorStack(err))
		return C.int(-1)
	}

	info := batchInfo{
		done:  done,
		batch: batch,
	}
	if err := info.initBatch(); err != nil {
		close(done)
		reportBestError(batch, err)
		return C.int(-1)
	}

	info.preallocatePythonObjects()
	go func() {
		select {
		case err := <-errCh:
			if *errorCallable != Py_None {
				errString := C.CString(errors.ErrorStack(err))
				var gstate C.PyGILState_STATE
				gstate = C.PyGILState_Ensure()
				pystring := C.PyUnicode_FromString(errString)
				res := C.PyObject_CallFunctionObjArgs_1(*errorCallable, pystring)
				if res == nil {
					log.Infof("wasn't able to make python call with error: %s", err)
					C.PyErr_Print()
				}
				C.go_vncdriver_decref(pystring)
				C.PyGILState_Release(gstate)
				C.free(unsafe.Pointer(errString))
			} else {
				log.Infof("error in go-vncdriver: %v", err)
			}

			GoVNCDriver_VNCSession_c_close(self)
		case <-done:
		}

		// And now its watch is done
		C.go_vncdriver_decref(*errorCallable)
	}()

	batchLock.Lock()
	defer batchLock.Unlock()

	ptr := uintptr(unsafe.Pointer(self))
	batchMgr[ptr] = info

	return C.int(0)
}

//export GoVNCDriver_VNCSession_render
func GoVNCDriver_VNCSession_render(self, args *C.PyObject) *C.PyObject {
	batchLock.Lock()
	defer batchLock.Unlock()

	ptr := uintptr(unsafe.Pointer(self))
	info, ok := batchMgr[ptr]
	if !ok {
		setError("No screens (perhaps you've already closed that VNCSession?)")
		return nil
	}

	err := info.batch.Render()
	if err != nil {
		reportBestError(info.batch, err)
		return nil
	}

	C.go_vncdriver_incref(Py_None)
	return Py_None
}

//export GoVNCDriver_VNCSession_step
func GoVNCDriver_VNCSession_step(self, actionIterable *C.PyObject) (rep *C.PyObject) {
	// defer func() {
	// 	if r := recover(); r != nil {
	// 		stack := debug.Stack()
	// 		setError(string(stack))
	// 		rep = nil
	// 	}
	// }()

	batchLock.Lock()
	defer batchLock.Unlock()

	ptr := uintptr(unsafe.Pointer(self))
	info, ok := batchMgr[ptr]
	if !ok {
		setError("No screens (perhaps you've already closed that VNCSession?)")
		return nil
	}

	actionIter := C.PyObject_GetIter(actionIterable)
	if actionIter == nil {
		return nil
	}

	// Iterate over all actions in the batch
	batchEvents := [][]gymvnc.VNCEvent{}
	errOccurred := false
	for action := C.PyIter_Next(actionIter); !errOccurred && action != nil; action = C.PyIter_Next(actionIter) {
		events := []gymvnc.VNCEvent{}

		// Iterate over all events in the action
		eventsIter := C.PyObject_GetIter(action)
		for eventPy := C.PyIter_Next(eventsIter); !errOccurred && eventPy != nil; eventPy = C.PyIter_Next(eventsIter) {
			event, ok := convertEventPy(eventPy)
			if !ok {
				errOccurred = true
			}
			C.go_vncdriver_decref(eventPy)

			events = append(events, event)
		}

		C.go_vncdriver_decref(action)
		batchEvents = append(batchEvents, events)

		if !errOccurred {
			errOccurred = C.PyErr_Occurred() != nil
		}
	}

	C.go_vncdriver_decref(actionIter)
	if C.PyErr_Occurred() != nil {
		return nil
	}

	err := info.batch.Step(batchEvents)
	if err != nil {
		reportBestError(info.batch, err)
		return nil
	}

	return flipHelper(info)
}

func reportBestError(batch *gymvnc.VNCBatch, err error) {
	var report string

	checkErr := batch.Check()
	if checkErr != nil {
		report = fmt.Sprintf("Error: %s\n\nOriginal error: %s", errors.ErrorStack(err), errors.ErrorStack(checkErr))
	} else {
		report = fmt.Sprintf("Error: %s", errors.ErrorStack(err))
	}

	setError(report)
}

// Sets python error
func convertEventPy(eventPy *C.PyObject) (event gymvnc.VNCEvent, ok bool) {
	// eventPy: ("PointerEvent", x, y, buttonmask) or ("KeyEvent", key, down)

	// if PyTuple_Check(eventPy) == 0 {
	// 	setError("event was not a tuple")
	// 	ok = false
	// 	return
	// }
	t := C.PyTuple_GetItem(eventPy, C.Py_ssize_t(0))
	if t == nil {
		C.PyErr_Clear()
		repr, isOk := PyObject_Repr(eventPy)
		if !isOk {
			return
		}
		setError(fmt.Sprintf("Expected non-empty tuple rather than: %s", repr))
		return
	}

	unicodePystr := C.PyUnicode_FromObject(t)
	if unicodePystr == nil {
		return
	}
	bytePystr := C.PyUnicode_AsASCIIString(unicodePystr)
	if bytePystr == nil {
		return
	}
	typePystr := C.PyBytes_AsString(bytePystr)
	if typePystr == nil {
		return
	}

	eventType := C.GoString(typePystr)
	if eventType == "PointerEvent" {
		x, isOk := getIntFromTuple(eventPy, 1)
		if !isOk {
			return
		}

		y, isOk := getIntFromTuple(eventPy, 2)
		if !isOk {
			return
		}

		mask, isOk := getIntFromTuple(eventPy, 3)
		if !isOk {
			return
		}

		event = &gymvnc.PointerEvent{
			Mask: vncclient.ButtonMask(mask),
			X:    uint16(x),
			Y:    uint16(y),
		}
	} else if eventType == "KeyEvent" {
		keysym, isOk := getIntFromTuple(eventPy, 1)
		if !isOk {
			return
		}

		down, isOk := getBoolFromTuple(eventPy, 2)
		if !isOk {
			return
		}

		event = &gymvnc.KeyEvent{
			Keysym: uint32(keysym),
			Down:   down,
		}
	} else {
		setError(fmt.Sprintf("invalid event type: %s", eventType))
	}

	ok = true
	return
}

func getIntFromTuple(eventPy *C.PyObject, i int) (int, bool) {
	iPyint := C.PyTuple_GetItem(eventPy, C.Py_ssize_t(i))
	if iPyint == nil {
		return 0, false
	}

	tup := C.PyLong_AsLong(iPyint)
	if tup == -1 && C.PyErr_Occurred() != nil {
		return 0, false
	}

	return int(tup), true
}

func getBoolFromTuple(eventPy *C.PyObject, i int) (bool, bool) {
	iPyint := C.PyTuple_GetItem(eventPy, C.Py_ssize_t(i))
	if iPyint == nil {
		return false, false
	}

	t := C.PyObject_IsTrue(iPyint)
	if t == -1 {
		return false, false
	}

	if t == 1 {
		return true, true
	} else {
		return false, true
	}
}

func PyObject_Repr(obj *C.PyObject) (string, bool) {
	res := C.PyObject_Repr(obj)
	if res == nil {
		return "", false
	}

	unicodeObj := C.PyUnicode_FromObject(res)
	if unicodeObj == nil {
		return "", false
	}

	byteObj := C.PyUnicode_AsASCIIString(unicodeObj)
	if byteObj == nil {
		return "", false
	}

	strObj := C.PyBytes_AsString(byteObj)
	if strObj == nil {
		return "", false
	}

	str := C.GoString(strObj)
	return str, true
}

//export GoVNCDriver_VNCSession_flip
func GoVNCDriver_VNCSession_flip(self, args *C.PyObject) *C.PyObject {
	batchLock.Lock()
	defer batchLock.Unlock()

	ptr := uintptr(unsafe.Pointer(self))
	info, ok := batchMgr[ptr]
	if !ok {
		setError("No screens (perhaps you've already closed that VNCSession?)")
		return nil
	}

	return flipHelper(info)
}

//export GoVNCDriver_VNCSession_peek
func GoVNCDriver_VNCSession_peek(self, args *C.PyObject) *C.PyObject {
	batchLock.Lock()
	defer batchLock.Unlock()

	ptr := uintptr(unsafe.Pointer(self))
	info, ok := batchMgr[ptr]
	if !ok {
		setError("No screens (perhaps you've already closed that VNCSession?)")
		return nil
	}

	screens := info.batch.Peek()
	info.populateScreenPylist(screens)

	// Ownership will transfer away when we return
	C.go_vncdriver_incref(info.screenPylist)
	return info.screenPylist
}

//export GoVNCDriver_VNCSession_close
func GoVNCDriver_VNCSession_close(self, args *C.PyObject) *C.PyObject {
	// t := C.get_go_vncdriver_VNCSession_type()
	// check := C.PyObject_IsInstance(self, t)
	// if check == C.int(-1) {
	// 	return nil
	// } else if check == C.int(0) {
	// 	setError("Must pass an VNCSession instance")
	// 	return nil
	// }

	cast := (*C.go_vncdriver_VNCSession_object)(unsafe.Pointer(self))
	GoVNCDriver_VNCSession_c_close(cast)

	// Acquire the GIL
	var gstate C.PyGILState_STATE
	gstate = C.PyGILState_Ensure()
	defer C.PyGILState_Release(gstate)

	C.go_vncdriver_incref(Py_None)
	return Py_None
}

//export GoVNCDriver_VNCSession_c_close
func GoVNCDriver_VNCSession_c_close(self *C.go_vncdriver_VNCSession_object) {
	batchLock.Lock()
	defer batchLock.Unlock()

	ptr := uintptr(unsafe.Pointer(self))
	info, ok := batchMgr[ptr]
	if !ok {
		return
	}

	var gstate C.PyGILState_STATE
	gstate = C.PyGILState_Ensure()
	defer C.PyGILState_Release(gstate)

	close(info.done)
	if info.screenInfoPytuple != nil {
		C.go_vncdriver_decref(info.screenInfoPytuple)
	}
	if info.infoPylist != nil {
		C.go_vncdriver_decref(info.infoPylist)
	}
	if info.screenPylist != nil {
		C.go_vncdriver_decref(info.screenPylist)
	}

	// Lists have taken ownership of our Numpy references and info
	// dictionaries
	// (https://docs.python.org/2.7/extending/extending.html#ownership-rules)
	delete(batchMgr, ptr)
}

//export GoVNCDriver_setup
func GoVNCDriver_setup(self, args *C.PyObject) *C.PyObject {
	gymvnc.ConfigureLogging()
	// Expansion of Py_None
	C.go_vncdriver_incref(Py_None)
	return Py_None
}

func flipHelper(info batchInfo) *C.PyObject {
	screens, updates := info.batch.Flip()
	if ok := info.populateScreenPylist(screens); !ok {
		return nil
	}

	for i, update := range updates {
		dict := info.infoPydicts[i]

		// Get rid of any extra stuff that may have been added
		C.PyDict_Clear(dict)

		// Retain our reference!
		C.go_vncdriver_incref(vncUpdatesN)
		ok := C.PyDict_SetItem(dict, vncUpdatesN, C.PyLong_FromLong(C.long(len(update))))
		if ok != C.int(0) {
			return nil
		}

		// Count up number of pixels changed
		pixels := 0
		rectangles := 0
		bytes := 0 // TODO: should we just compute this from the byte stream directly?
		for _, updateI := range update {
			for _, rect := range updateI.Rectangles {
				pixels += int(rect.Width) * int(rect.Height)
				rectangles++
				// Each rectangle consists of X, Y,
				// Width, Height (each 2 bytes) and an
				// encoding.
				//
				// Technically, we should consider
				// including other control messages in
				// bytes, but this is ok for now.
				bytes += rect.Enc.Size() + 8
			}
		}

		C.go_vncdriver_incref(vncUpdatesPixels)
		ok = C.PyDict_SetItem(dict, vncUpdatesPixels, C.PyLong_FromLong(C.long(pixels)))
		if ok != C.int(0) {
			return nil
		}

		C.go_vncdriver_incref(vncUpdatesRectangles)
		ok = C.PyDict_SetItem(dict, vncUpdatesRectangles, C.PyLong_FromLong(C.long(rectangles)))
		if ok != C.int(0) {
			return nil
		}

		C.go_vncdriver_incref(vncUpdatesBytes)
		ok = C.PyDict_SetItem(dict, vncUpdatesBytes, C.PyLong_FromLong(C.long(bytes)))
		if ok != C.int(0) {
			return nil
		}
	}

	// Ownership will transfer away when we return
	C.go_vncdriver_incref(info.screenInfoPytuple)
	return info.screenInfoPytuple
}

func setError(str string) {
	C.PyErr_SetGoVNCDriverError(C.CString(str))
}

func main() {
}
