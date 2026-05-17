#!/usr/bin/env python3
"""
sound_profiles.py -- Preset audio profiles for Android
Profiles: silent, vibrate, normal, loud
Usage: python3 sound_profiles.py --load silent
       python3 sound_profiles.py --list
"""
import subprocess, argparse

def adb(cmd):
    subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True)

PROFILES = {
    "silent": {
        "desc": "Silent mode — all volumes to 0",
        "streams": {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0},
    },
    "vibrate": {
        "desc": "Vibrate mode — ring/notif only",
        "streams": {"0": 0, "1": 0, "2": 5, "3": 0, "4": 5, "5": 5},
    },
    "normal": {
        "desc": "Normal — balanced levels",
        "streams": {"0": 7, "1": 5, "2": 7, "3": 10, "4": 7, "5": 7},
    },
    "loud": {
        "desc": "Loud — all high",
        "streams": {"0": 15, "1": 15, "2": 15, "3": 15, "4": 15, "5": 15},
    },
}

def apply_profile(name):
    if name not in PROFILES:
        print(f"Unknown profile: {name}")
        return
    
    profile = PROFILES[name]
    print(f"Loading profile: {profile['desc']}")
    
    for stream, level in profile["streams"].items():
        adb(f"cmd audio set_volume_of_stream {stream} {level}")
        print(f"  ✓ Stream {stream} → {level}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--load", help="Load a profile")
    parser.add_argument("--list", action="store_true", help="List profiles")
    args = parser.parse_args()

    if args.list:
        print("\n🎵 Sound Profiles:\n")
        for name, profile in PROFILES.items():
            print(f"  {name:<12} {profile['desc']}")
    elif args.load:
        apply_profile(args.load)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
