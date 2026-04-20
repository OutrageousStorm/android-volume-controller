#!/usr/bin/env python3
"""
volume.py -- Control Android volume levels via ADB
Usage: python3 volume.py get          # show all volumes
       python3 volume.py set music 10  # set music to 10/15
       python3 volume.py mute          # mute all
       python3 volume.py vibrate       # mute + disable vibration
"""
import subprocess, argparse, sys

STREAMS = {
    "voice": 0, "system": 1, "ring": 2, "music": 3,
    "alarm": 4, "notification": 5, "dtmf": 6, "accessibility": 10,
}

def adb(cmd):
    return subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True).stdout.strip()

def get_volumes():
    out = adb("dumpsys audio_service | grep 'Vol")
    print("Current volumes:")
    for line in out.splitlines()[:6]:
        print(f"  {line}")

def set_volume(stream, level):
    stream_id = STREAMS.get(stream.lower())
    if stream_id is None:
        print(f"Unknown stream: {stream}. Use: {', '.join(STREAMS.keys())}")
        sys.exit(1)
    adb(f"service call audio {stream_id} {level} {stream_id}")
    print(f"✓ {stream} → {level}")

def mute_all():
    for stream in ["ring", "music", "alarm", "notification", "system"]:
        adb(f"service call audio 1 0")
    print("✓ All streams muted")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", nargs="?", default="get")
    parser.add_argument("stream", nargs="?")
    parser.add_argument("level", nargs="?", type=int)
    args = parser.parse_args()

    if args.action == "get":
        get_volumes()
    elif args.action == "set":
        if not args.stream or args.level is None:
            print("Usage: volume.py set <stream> <level>")
            sys.exit(1)
        set_volume(args.stream, args.level)
    elif args.action == "mute":
        mute_all()
    elif args.action == "vibrate":
        adb("settings put system vibrate_on 0")
        mute_all()
        print("✓ Vibration disabled + muted")

if __name__ == "__main__":
    main()
