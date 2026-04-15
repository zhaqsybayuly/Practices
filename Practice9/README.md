# Practice 9 — Pygame Games

Three small pygame projects:

1. **mickeys_clock/** — Mickey Mouse clock where his arms rotate with system time
2. **music_player/** — keyboard-controlled music player using `pygame.mixer`
3. **moving_ball/** — red ball that moves around the window with arrow keys

## Setup

```bash
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

Each project lives in its own folder with its own `main.py`:

```bash
cd mickeys_clock && python main.py
cd ../music_player && python main.py
cd ../moving_ball  && python main.py
```

For the music player, drop `.mp3` / `.wav` / `.ogg` files into `music_player/music/` first.
