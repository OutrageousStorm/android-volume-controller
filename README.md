# 🔊 Android Volume Controller

Control Android volume via ADB — get current level, set per-stream, mute, unmute, adjust brightness.

## Usage

```bash
python3 volume.py --get                    # get current volumes
python3 volume.py --set 15                 # set music volume to 15
python3 volume.py --stream alarm --set 10  # set alarm to 10
python3 volume.py --mute voice             # mute voice calls
python3 volume.py --unmute all             # unmute everything
```

## Streams
- `voice`: call volume
- `music`: media/music volume (default)
- `alarm`: alarm volume
- `notification`: notification sounds
- `dtmf`: dial tones
- `accessibility`: accessibility volume (Android 8+)
