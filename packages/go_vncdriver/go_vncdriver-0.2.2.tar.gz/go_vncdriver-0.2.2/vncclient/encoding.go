package vncclient

import (
	"bytes"
	"encoding/binary"
	"io"

	"github.com/juju/errors"
	"github.com/op/go-logging"
)

var log = logging.MustGetLogger("vncclient")

// An Encoding implements a method for encoding pixel data that is
// sent by the server to the client.
type Encoding interface {
	// The number that uniquely identifies this encoding type.
	Type() uint32

	// Read reads the contents of the encoded pixel data from the reader.
	// This should return a new Encoding implementation that contains
	// the proper data.
	Read(*ClientConn, *Rectangle, io.Reader) (Encoding, error)

	Size() int
}

type CompressLevel struct {
	Level uint32
}

func (r *CompressLevel) Size() int {
	return 0
}

func (r *CompressLevel) Type() uint32 {
	return 0xFFFFFF00 + r.Level
}

func (*CompressLevel) Read(c *ClientConn, rect *Rectangle, r io.Reader) (Encoding, error) {
	return &CompressLevel{}, errors.New("Not implemented")
}

// RawEncoding is raw pixel data sent by the server.
//
// See RFC 6143 Section 7.7.1
type RawEncoding struct {
	Colors []Color
}

func (r *RawEncoding) Size() int {
	return len(r.Colors) * 3
}

func (*RawEncoding) Type() uint32 {
	return 0
}

func (*RawEncoding) Read(c *ClientConn, rect *Rectangle, r io.Reader) (Encoding, error) {
	bytesPerPixel := c.PixelFormat.BPP / 8

	// Various housekeeping helpers
	pixelBytes := make([]uint8, bytesPerPixel)
	var byteOrder binary.ByteOrder = binary.LittleEndian
	if c.PixelFormat.BigEndian {
		byteOrder = binary.BigEndian
	}

	// Output buffer
	colors := make([]Color, int(rect.Height)*int(rect.Width))

	// Read all needed bytes: this improves performance so we
	// don't have to do piecemeal unbuffered reads.
	buf := make([]byte, int(rect.Height)*int(rect.Width)*int(bytesPerPixel))
	if _, err := io.ReadFull(r, buf); err != nil {
		return nil, err
	}
	r = bytes.NewBuffer(buf)

	for y := uint16(0); y < rect.Height; y++ {
		for x := uint16(0); x < rect.Width; x++ {
			if _, err := io.ReadFull(r, pixelBytes); err != nil {
				return nil, err
			}

			var rawPixel uint32
			if c.PixelFormat.BPP == 8 {
				rawPixel = uint32(pixelBytes[0])
			} else if c.PixelFormat.BPP == 16 {
				rawPixel = uint32(byteOrder.Uint16(pixelBytes))
			} else if c.PixelFormat.BPP == 32 {
				rawPixel = byteOrder.Uint32(pixelBytes)
			}

			color := &colors[int(y)*int(rect.Width)+int(x)]
			if c.PixelFormat.TrueColor {
				color.R = uint8((rawPixel >> c.PixelFormat.RedShift) & uint32(c.PixelFormat.RedMax))
				color.G = uint8((rawPixel >> c.PixelFormat.GreenShift) & uint32(c.PixelFormat.GreenMax))
				color.B = uint8((rawPixel >> c.PixelFormat.BlueShift) & uint32(c.PixelFormat.BlueMax))
			} else {
				*color = c.ColorMap[rawPixel]
			}
		}
	}

	return &RawEncoding{colors}, nil
}

// ZRLEEncoding is Zlib run-length encoded pixel data
//
// See RFC 6143 Section 7.7.6
type ZRLEEncoding struct {
	Colors []Color
	size   int32
}

func (*ZRLEEncoding) Type() uint32 {
	return 16
}

func (z *ZRLEEncoding) Size() int {
	return int(z.size)
}

func (z *ZRLEEncoding) Read(c *ClientConn, rect *Rectangle, r io.Reader) (Encoding, error) {
	var length int32
	if err := binary.Read(r, binary.BigEndian, &length); err != nil {
		return nil, err
	}

	// Could maybe get by without the copy
	compressed := make([]uint8, length)
	if err := binary.Read(r, binary.BigEndian, &compressed); err != nil {
		return nil, err
	}

	inflated, err := c.inflator.Inflate(compressed)
	if err != nil {
		return nil, errors.Annotate(err, "could not inflate")
	}

	// It's now safe to start reading other ZRLE messages if desired
	log.Debugf("expanded zlib: %d bytes -> %d bytes", len(compressed), len(inflated))

	// TODO: other format checks here
	if c.PixelFormat.BPP < 24 {
		return nil, errors.Errorf("unsupported bitsPerPixel: %d", c.PixelFormat.BPP)
	}

	// data := base64.StdEncoding.EncodeToString(inflated)
	// log.Infof("payload %v %v %v %v: %v", rect.X, rect.Y, rect.Width, rect.Height, data)

	buf := NewQuickBuf(inflated)
	colors, err := z.parse(rect, buf)
	if err != nil {
		return nil, errors.Annotatef(err, "could not parse ZRLEEncoding colors")
	}

	if buf.Len() != 0 {
		return nil, errors.Errorf("BUG: buffer still had %d unread bytes", buf.Len())
	}

	// buf := bytes.NewBuffer(inflated)
	return &ZRLEEncoding{colors, length}, nil
}

func (z *ZRLEEncoding) parse(rect *Rectangle, r *QuickBuf) ([]Color, error) {
	colors := make([]Color, int(rect.Height)*int(rect.Width))

	// We pass in a scratch buffer so that parseTile doesn't need
	// to allocate its own. A better implementation would probably
	// write directly into the colors buffer.
	scratch := make([]Color, 64*64)

	for tileY := uint16(0); tileY < rect.Height; tileY += 64 {
		tileHeight := min(64, rect.Height-tileY)
		for tileX := uint16(0); tileX < rect.Width; tileX += 64 {
			tileWidth := min(64, rect.Width-tileX)

			err := z.parseTile(rect, colors, r, tileX, tileY, tileWidth, tileHeight, scratch[:int(tileHeight)*int(tileWidth)])
			if err != nil {
				return nil, err
			}
		}
	}

	return colors, nil
}

func (*ZRLEEncoding) parseTile(rect *Rectangle, colors []Color, r *QuickBuf, tileX, tileY, tileWidth, tileHeight uint16, scratch []Color) error {
	// Each tile begins with a subencoding type byte.  The top bit of this
	// byte is set if the tile has been run-length encoded, clear otherwise.
	// The bottom 7 bits indicate the size of the palette used: zero means
	// no palette, 1 means that the tile is of a single color, and 2 to 127
	// indicate a palette of that size.  The special subencoding values 129
	// and 127 indicate that the palette is to be reused from the last tile
	// that had a palette, with and without RLE, respectively.
	subencoding, err := r.ReadByte()
	if err != nil {
		return errors.Annotate(err, "failed to read subencoding")
	}

	runLengthEncoded := subencoding&128 != 0
	paletteSize := subencoding & 127

	paletteData, err := r.ReadColors(int(paletteSize))
	if err != nil {
		return errors.Annotatef(err, "failed to read palette: runLengthEncoded:%v paletteSize:%v", runLengthEncoded, paletteSize)
	}

	if paletteSize == 0 && !runLengthEncoded {
		// 0: Raw pixel data. width*height pixel values follow (where width and
		// height are the width and height of the tile):
		//
		//  +-----------------------------+--------------+-------------+
		//  | No. of bytes                | Type [Value] | Description |
		//  +-----------------------------+--------------+-------------+
		//  | width*height*BytesPerCPixel | CPIXEL array | pixels      |
		//  +-----------------------------+--------------+-------------+

		colors, err := r.ReadColors(len(scratch))
		if err != nil {
			return errors.Annotate(err, "failed to read raw colors")
		}
		// Don't bother with the scratch buffer
		scratch = colors
	} else if paletteSize == 1 && !runLengthEncoded {
		// 1: A solid tile consisting of a single color.  The pixel value
		// follows:
		//
		// +----------------+--------------+-------------+
		// | No. of bytes   | Type [Value] | Description |
		// +----------------+--------------+-------------+
		// | bytesPerCPixel | CPIXEL       | pixelValue  |
		// +----------------+--------------+-------------+
		pixelValue := paletteData[0]
		fillColor(scratch, pixelValue)
	} else if !runLengthEncoded {
		// 2 to 16:  Packed palette types.  The paletteSize is the value of the
		// subencoding, which is followed by the palette, consisting of
		// paletteSize pixel values.  The packed pixels follow, with each
		// pixel represented as a bit field yielding a zero-based index into
		// the palette.  For paletteSize 2, a 1-bit field is used; for
		// paletteSize 3 or 4, a 2-bit field is used; and for paletteSize
		// from 5 to 16, a 4-bit field is used.  The bit fields are packed
		// into bytes, with the most significant bits representing the
		// leftmost pixel (i.e., big endian).  For tiles not a multiple of 8,
		// 4, or 2 pixels wide (as appropriate), padding bits are used to
		// align each row to an exact number of bytes.

		//   +----------------------------+--------------+--------------+
		//   | No. of bytes               | Type [Value] | Description  |
		//   +----------------------------+--------------+--------------+
		//   | paletteSize*bytesPerCPixel | CPIXEL array | palette      |
		//   | m                          | U8 array     | packedPixels |
		//   +----------------------------+--------------+--------------+

		//  where m is the number of bytes representing the packed pixels.
		//  For paletteSize of 2, this is div(width+7,8)*height; for
		//  paletteSize of 3 or 4, this is div(width+3,4)*height; or for
		//  paletteSize of 5 to 16, this is div(width+1,2)*height.

		var bitsPerPackedPixel uint8
		if paletteSize > 16 {
			// No palette reuse in zrle
			bitsPerPackedPixel = 8
		} else if paletteSize > 4 {
			bitsPerPackedPixel = 4
		} else if paletteSize > 2 {
			bitsPerPackedPixel = 2
		} else {
			bitsPerPackedPixel = 1
		}

		for j := uint16(0); j < tileHeight; j++ {
			// We discard any leftover bits for each new line
			var b uint8
			var nbits uint8

			for i := uint16(0); i < tileWidth; i++ {
				if nbits == 0 {
					b, err = r.ReadByte()
					if err != nil {
						return errors.Annotate(err, "failed to read nbits byte")
					}
					nbits = 8
				}
				nbits -= bitsPerPackedPixel
				paletteIdx := (b >> nbits) & ((1 << bitsPerPackedPixel) - 1) & 127
				pixelValue := paletteData[paletteIdx]
				scratch[j*tileWidth+i] = pixelValue
			}
		}
	} else if runLengthEncoded && paletteSize == 0 {
		// 128:  Plain RLE.  The data consists of a number of runs, repeated
		// until the tile is done.  Runs may continue from the end of one row
		// to the beginning of the next.  Each run is represented by a single
		// pixel value followed by the length of the run.  The length is
		// represented as one or more bytes.  The length is calculated as one
		// more than the sum of all the bytes representing the length.  Any
		// byte value other than 255 indicates the final byte.  So for
		// example, length 1 is represented as [0], 255 as [254], 256 as
		// [255,0], 257 as [255,1], 510 as [255,254], 511 as [255,255,0], and
		// so on.
		//
		// +-------------------------+--------------+-----------------------+
		// | No. of bytes            | Type [Value] | Description           |
		// +-------------------------+--------------+-----------------------+
		// | bytesPerCPixel          | CPIXEL       | pixelValue            |
		// | div(runLength - 1, 255) | U8 array     | 255                   |
		// | 1                       | U8           | (runLength-1) mod 255 |
		// +-------------------------+--------------+-----------------------+

		for pos := 0; pos < len(scratch); {
			pixelValue, err := r.ReadColor()
			if err != nil {
				return err
			}

			count := 1
			for b := uint8(255); b == 255; {
				b, err = r.ReadByte()
				if err != nil {
					return errors.Annotate(err, "failed to read rle byte")
				}
				count += int(b)
			}

			fillColor2(scratch[pos:pos+count], pixelValue)
			pos += count
		}
	} else if runLengthEncoded && paletteSize > 1 {
		// 130 to 255:  Palette RLE.  Followed by the palette, consisting of
		// paletteSize = (subencoding - 128) pixel values:
		//
		//   +----------------------------+--------------+-------------+
		//   | No. of bytes               | Type [Value] | Description |
		//   +----------------------------+--------------+-------------+
		//   | paletteSize*bytesPerCPixel | CPIXEL array | palette     |
		//   +----------------------------+--------------+-------------+
		//
		// Following the palette is, as with plain RLE, a number of runs,
		// repeated until the tile is done.  A run of length one is
		// represented simply by a palette index:
		//
		//         +--------------+--------------+--------------+
		//         | No. of bytes | Type [Value] | Description  |
		//         +--------------+--------------+--------------+
		//         | 1            | U8           | paletteIndex |
		//         +--------------+--------------+--------------+
		//
		// A run of length more than one is represented by a palette index
		// with the top bit set, followed by the length of the run as for
		// plain RLE.
		//
		// +-------------------------+--------------+-----------------------+
		// | No. of bytes            | Type [Value] | Description           |
		// +-------------------------+--------------+-----------------------+
		// | 1                       | U8           | paletteIndex + 128    |
		// | div(runLength - 1, 255) | U8 array     | 255                   |
		// | 1                       | U8           | (runLength-1) mod 255 |
		// +-------------------------+--------------+-----------------------+
		for pos := 0; pos < len(scratch); {
			paletteIdx, err := r.ReadByte()
			if err != nil {
				return errors.Annotate(err, "failed to read palette index")
			}

			count := 1
			if paletteIdx&128 != 0 {
				for b := uint8(255); b == 255; {
					b, err = r.ReadByte()
					if err != nil {
						return errors.Annotate(err, "failed to read byte")
					}
					count += int(b)
				}
			}

			paletteIdx &= 127
			pixelValue := paletteData[paletteIdx]
			fillColor(scratch[pos:pos+count], pixelValue)
			pos += count
		}
	} else {
		return errors.Errorf("Unhandled case: runLengthEncoded=%v paletteSize=%v", runLengthEncoded, paletteSize)
	}

	for j := 0; j < int(tileHeight); j++ {
		off := int(tileY)*int(rect.Width) + int(tileX)
		start := j*int(rect.Width) + off
		copy(colors[start:start+int(tileWidth)], scratch[j*int(tileWidth):])
	}

	return nil
}

func min(x, y uint16) uint16 {
	if x > y {
		return y
	} else {
		return x
	}
}

func fillColor(dst []Color, pixelValue Color) {
	dst[0] = pixelValue
	for bp := 1; bp < len(dst); {
		copy(dst[bp:], dst[:bp])
		bp *= 2
	}
}

func fillColor2(dst []Color, pixelValue Color) {
	for i := range dst {
		dst[i] = pixelValue
	}
}
