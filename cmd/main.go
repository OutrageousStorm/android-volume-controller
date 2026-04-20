package main

import (
	"flag"
	"fmt"
	"os"
	"os/exec"
	"strconv"
	"strings"
)

func adb(args ...string) string {
	cmd := exec.Command("adb", args...)
	out, _ := cmd.CombinedOutput()
	return strings.TrimSpace(string(out))
}

func getVolume(stream string) int {
	out := adb("shell", "cmd", "audio", "get_volume", "--stream", stream)
	var vol int
	fmt.Sscanf(out, "%d", &vol)
	return vol
}

func setVolume(stream string, level int) {
	adb("shell", "cmd", "audio", "set_volume", "--stream", stream, "--volume", strconv.Itoa(level))
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: vol get --stream music\n       vol set --stream music --level 10")
		os.Exit(1)
	}

	getCmd := flag.NewFlagSet("get", flag.ExitOnError)
	getStream := getCmd.String("stream", "music", "audio stream")

	setCmd := flag.NewFlagSet("set", flag.ExitOnError)
	setStream := setCmd.String("stream", "music", "audio stream")
	setLevel := setCmd.Int("level", 5, "volume level")

	switch os.Args[1] {
	case "get":
		getCmd.Parse(os.Args[2:])
		level := getVolume(*getStream)
		fmt.Printf("%s volume: %d\n", *getStream, level)
	case "set":
		setCmd.Parse(os.Args[2:])
		setVolume(*setStream, *setLevel)
		fmt.Printf("Set %s to %d\n", *setStream, *setLevel)
	}
}
