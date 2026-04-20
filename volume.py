#!/usr/bin/env python3
"""
volume.py -- Control Android volume levels from CLI
Usage:
  volume.py get                    # current volume for all streams
  volume.py set music 10           # set music volume to 10
  volume.py max                    # set all to max
  volume.py mute                   # mute all non-system streams
  volume.py restore               # restore last saved state
"""
import subprocess, json, argparse, sys
from pathlib import Path

STREAMS = {
    "voice_call": 0,
    "system": 1,
    "ring": 2,
    "music": 3,
    "alarm": 4,
    "notification": 5,
}

STATE_FILE = Path.home() / ".android_volume_state.json"

def adb(cmd):
    r = subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True, text=True)
    return r.stdout.strip()

def get_current():
    """Get current volume for all streams"""
    states = {}
    for name, stream_id in STREAMS.items():
        try:
            cur = adb(f"dumpsys audio | grep 'volume_aliases' -A 20 | grep -oP '{name}' || echo '0'")
            # Fallback: use settings
            val = adb(f"settings get system volume_music")
            states[name] = int(val) if val.isdigit() else 0
        except:
            states[name] = 0
    return states

def set_volume(stream_name, level):
    """Set volume for a specific stream (0-15 typical)"""
    if stream_name not in STREAMS:
        print(f"Unknown stream: {stream_name}")
        print(f"Available: {', '.join(STREAMS.keys())}")
        return False
    
    stream_id = STREAMS[stream_name]
    # Use media_volume which maps to music stream
    if stream_name == "music":
        adb(f"settings put system volume_music {level}")
    else:
        adb(f"cmd audio set_stream_volume {stream_id} {level}")
    print(f"✓ {stream_name} → {level}")
    return True

def mute_all(exclude=["system"]):
    """Mute all streams except system"""
    for name in STREAMS.keys():
        if name not in exclude:
            adb(f"cmd audio set_stream_volume {STREAMS[name]} 0")
    print(f"✓ Muted all except {', '.join(exclude)}")

def restore():
    """Restore from last saved state"""
    if not STATE_FILE.exists():
        print("No saved state. Use: volume.py set <stream> <level> to change.")
        return
    with open(STATE_FILE) as f:
        state = json.load(f)
    for stream, level in state.items():
        set_volume(stream, level)
    print("✓ Restored")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", nargs="?", default="get",
                        help="get | set | max | mute | restore")
    parser.add_argument("stream", nargs="?")
    parser.add_argument("level", nargs="?", type=int)
    args = parser.parse_args()

    if args.action == "get":
        current = get_current()
        for stream, level in current.items():
            print(f"  {stream:<15} {level}")

    elif args.action == "set":
        if not args.stream or args.level is None:
            print("Usage: volume.py set <stream> <level>")
            sys.exit(1)
        set_volume(args.stream, args.level)
        with open(STATE_FILE, "w") as f:
            json.dump(get_current(), f)

    elif args.action == "max":
        for name in STREAMS.keys():
            set_volume(name, 15)

    elif args.action == "mute":
        mute_all()

    elif args.action == "restore":
        restore()

    else:
        print(f"Unknown action: {args.action}")
        sys.exit(1)

if __name__ == "__main__":
    main()
