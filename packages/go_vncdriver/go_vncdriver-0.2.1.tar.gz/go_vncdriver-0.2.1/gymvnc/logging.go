package gymvnc

import "github.com/op/go-logging"

func ConfigureLogging() {
	logging.SetLevel(logging.INFO, "")
	logging.SetFormatter(logging.MustStringFormatter("%{level:.1s}%{time:0102 15:04:05.999999} %{pid} %{shortfile}] %{message}"))
}
