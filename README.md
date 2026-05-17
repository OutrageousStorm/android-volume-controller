# 🔊 Android Volume Controller

Control all audio volumes from PC via ADB — no touching the device.

## Tools

| Tool | What it does |
|------|-------------|
| `volume_control.py` | Interactive volume mixer |
| `sound_profiles.py` | Switch between sound profiles (silent, vibrate, normal, loud) |
| `audio_route.py` | Route audio to speaker, headphones, Bluetooth |

## Usage

```bash
# Interactive mixer
python3 volume_control.py

# Set specific volume
python3 volume_control.py --set media 15  # max=15

# Load a preset
python3 sound_profiles.py --load silent
```
