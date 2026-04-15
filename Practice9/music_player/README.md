# Music Player

A keyboard-controlled music player built with pygame.

## Controls

- **P** — Play
- **S** — Stop
- **N** — Next track
- **B** — Back (previous track)
- **Q** — Quit

## Files

- `main.py` — window, input loop, UI
- `player.py` — `Player` class that wraps `pygame.mixer` and manages the playlist
- `music/` — drop your `.mp3`, `.wav` or `.ogg` files here

## Run

```bash
python main.py
```

The app scans the `music/` folder at startup and builds the playlist from whatever audio files it finds there.
