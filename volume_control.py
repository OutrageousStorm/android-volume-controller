#!/usr/bin/env python3
"""
volume_control.py -- Interactive Android audio volume mixer via ADB
Usage: python3 volume_control.py
       python3 volume_control.py --get media
       python3 volume_control.py --set media 10
"""
import subprocess, argparse

def adb(cmd):
    return subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True).stdout.strip()

STREAMS = {
    "0": "VOICE_CALL",
    "1": "SYSTEM",
    "2": "RING",
    "3": "MUSIC",
    "4": "ALARM",
    "5": "NOTIFICATION",
}

def get_volume(stream):
    """Get current volume for a stream"""
    vol = adb(f"cmd audio get_volume_of_stream {stream}")
    return vol

def set_volume(stream, level):
    """Set volume for a stream (0-15 for most streams)"""
    adb(f"cmd audio set_volume_of_stream {stream} {level}")

def get_all_volumes():
    """Get all audio streams and their levels"""
    print("\n🔊 Android Audio Volumes")
    print("=" * 40)
    for stream_id, stream_name in STREAMS.items():
        try:
            vol = get_volume(stream_id)
            print(f"  {stream_name:<15} {vol}")
        except:
            print(f"  {stream_name:<15} (unavailable)")

def interactive():
    """Interactive volume mixer"""
    while True:
        print("\n🔊 Volume Control")
        print("  0=VOICE  1=SYSTEM  2=RING  3=MUSIC  4=ALARM  5=NOTIF")
        print("  Type: stream_id volume  (e.g. '3 10' for music=10)")
        print("  Or:   'q' to quit")
        
        cmd = input("> ").strip()
        if cmd == 'q': break
        
        parts = cmd.split()
        if len(parts) != 2:
            print("  Invalid. Format: stream_id volume")
            continue
        
        try:
            stream = int(parts[0])
            level = int(parts[1])
            set_volume(stream, level)
            print(f"  ✓ {STREAMS.get(str(stream))} set to {level}")
        except Exception as e:
            print(f"  ✗ Error: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--get", type=int, help="Get volume for stream ID")
    parser.add_argument("--set", nargs=2, metavar=('STREAM','LEVEL'), help="Set stream volume")
    parser.add_argument("--list", action="store_true", help="List all volumes")
    args = parser.parse_args()

    if args.list:
        get_all_volumes()
    elif args.get is not None:
        vol = get_volume(args.get)
        print(f"Stream {args.get}: {vol}")
    elif args.set:
        stream, level = int(args.set[0]), int(args.set[1])
        set_volume(stream, level)
        print(f"✓ Set stream {stream} to {level}")
    else:
        interactive()

if __name__ == "__main__":
    main()
