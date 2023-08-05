package main

import (
	"log"
	"os"
	"runtime/pprof"
	"time"

	"github.com/openai/gym-vnc/go-vncdriver/gymvnc"
)
import _ "net/http/pprof"

type foo struct {
	bar string
}

func main() {
	f, err := os.Create("/tmp/profile-zrle.pprof")
	if err != nil {
		panic(err)
	}
	pprof.StartCPUProfile(f)
	defer pprof.StopCPUProfile()

	batch := gymvnc.NewVNCBatch()
	err = batch.Open("conn", gymvnc.VNCSessionConfig{
		Address:          "127.0.0.1:5900",
		Password:         "openai",
		Encoding:         "tight",
		FineQualityLevel: 100,
	})
	if err != nil {
		panic(err)
	}
	for i := 0; i < 2000; i++ {
		batchEvents := map[string][]gymvnc.VNCEvent{
			"conn": []gymvnc.VNCEvent{
				gymvnc.KeyEvent{
					Keysym: 71,
					Down:   true,
				},
				gymvnc.KeyEvent{
					Keysym: 71,
					Down:   false,
				},
			},
		}
		observationN, updatesN, errN := batch.Step(batchEvents)
		log.Println(observationN, updatesN, errN)
		time.Sleep(16 * time.Millisecond)
	}

	// f, err := os.Create("/tmp/hi.prof")
	// if err != nil {
	//     log.Fatal("could not create memory profile: ", err)
	// }
	// runtime.GC() // get up-to-date statistics
	// if err := pprof.WriteHeapProfile(f); err != nil {
	//     log.Fatal("could not write memory profile: ", err)
	// }
	// f.Close()
}
