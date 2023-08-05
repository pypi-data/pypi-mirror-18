// +build !no_gl

package main

import "github.com/openai/gym-vnc/go-vncdriver/vncgl"

func (b *batchInfo) initBatch() error {
	return b.batch.SetRenderer(&vncgl.VNCGL{})
}
