#!/usr/bin/env python3
"""
volume.py -- Control Android volume streams via ADB
Get, set, mute, unmute per-stream volume.
Usage: python3 volume.py --get
       python3 volume.py --set 15
       python3 volume.py --stream music --set 8
"""
import subprocess, argparse

STREAMS = {
    "voice": 0,
    "music": 1,  # default for media
    "alarm": 4,
    "notification": 5,
    "dtmf": 8,
    "accessibility": 10,
}

def adb(cmd):
    r = subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True)
    return r.stdout.strip()

def get_volume(stream_id):
    # dumpsys audio shows volumes per-stream
    raw = adb("dumpsys audio")
    for line in raw.splitlines():
        if f"volumeIndexDefault_stream_{stream_id}" in line or f"index={stream_id}" in line:
            return line
    return None

def set_volume(stream_id, level):
    """Set volume for a stream (0-15 typically)"""
    adb(f"media volume --show --set 0 -- {level}")
    # More reliable: use settings
    adb(f"settings put global volume_music {level}")

def mute_stream(stream_id):
    adb(f"media volume --set {stream_id} 0")

def unmute_stream(stream_id):
    adb(f"media volume --set {stream_id} 5")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--get", action="store_true")
    parser.add_argument("--set", type=int)
    parser.add_argument("--stream", default="music", choices=STREAMS.keys())
    parser.add_argument("--mute", action="store_true")
    parser.add_argument("--unmute", action="store_true")
    args = parser.parse_args()

    stream_id = STREAMS[args.stream]

    if args.get:
        raw = adb("dumpsys audio | grep 'vol_music\|vol_alarm\|vol_notification'")
        print("Current volumes:")
        print(raw)
    elif args.set is not None:
        print(f"Setting {args.stream} to {args.set}")
        set_volume(stream_id, args.set)
    elif args.mute:
        print(f"Muting {args.stream}")
        mute_stream(stream_id)
    elif args.unmute:
        print(f"Unmuting {args.stream}")
        unmute_stream(stream_id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
