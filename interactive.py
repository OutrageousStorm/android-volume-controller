#!/usr/bin/env python3
"""
interactive.py -- Interactive Android volume mixer
Real-time volume control for all streams with visual feedback
Usage: python3 interactive.py
"""
import subprocess, sys, time
from enum import Enum

class Stream(Enum):
    VOICE = 0
    SYSTEM = 1
    RING = 2
    MUSIC = 3
    ALARM = 4
    NOTIFICATION = 5

def adb(cmd):
    subprocess.run(f"adb shell {cmd}", shell=True, capture_output=True)

def get_max_volume(stream):
    out = subprocess.run(f"adb shell media volume --get_max_volume {stream.value}",
                        shell=True, capture_output=True, text=True).stdout.strip()
    try:
        return int(out)
    except:
        return 15

def get_volume(stream):
    out = subprocess.run(f"adb shell media volume --get_volume {stream.value}",
                        shell=True, capture_output=True, text=True).stdout.strip()
    try:
        return int(out)
    except:
        return 0

def set_volume(stream, level):
    adb(f"media volume --set_volume {stream.value} {level}")

def show_bar(stream, current, max_vol):
    filled = int((current / max_vol) * 20) if max_vol > 0 else 0
    bar = "█" * filled + "░" * (20 - filled)
    pct = int((current / max_vol) * 100) if max_vol > 0 else 0
    return f"[{bar}] {pct}%"

def main():
    streams = list(Stream)
    print("\n🔊 Android Volume Mixer")
    print("=" * 50)
    print("Commands: s (system), m (music), r (ring), n (notification), u (up), d (down), q (quit)")
    print()

    current_stream = Stream.MUSIC
    
    while True:
        print("\nVOLUME STATUS:")
        for s in streams:
            vol = get_volume(s)
            max_vol = get_max_volume(s)
            bar = show_bar(s, vol, max_vol)
            marker = " ← ACTIVE" if s == current_stream else ""
            print(f"  {s.name:<12} {bar}{marker}")

        cmd = input("\nCommand (s/m/r/n/u/d/q): ").strip().lower()
        
        if cmd == 'q':
            break
        elif cmd == 's':
            current_stream = Stream.SYSTEM
        elif cmd == 'm':
            current_stream = Stream.MUSIC
        elif cmd == 'r':
            current_stream = Stream.RING
        elif cmd == 'n':
            current_stream = Stream.NOTIFICATION
        elif cmd == 'u':
            vol = get_volume(current_stream)
            max_vol = get_max_volume(current_stream)
            if vol < max_vol:
                set_volume(current_stream, vol + 1)
        elif cmd == 'd':
            vol = get_volume(current_stream)
            if vol > 0:
                set_volume(current_stream, vol - 1)

if __name__ == "__main__":
    main()
