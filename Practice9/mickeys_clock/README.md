# Mickey's Clock

A Mickey Mouse themed clock where his arms rotate to show the current time.

- **Right arm** = minutes hand
- **Left arm** = seconds hand

## Files

- `main.py` — window setup and game loop
- `clock.py` — `MickeyClock` class with the rotation logic
- `images/` — SVG pieces (clock face, body, arms, center pin)

## Run

```bash
python main.py
```

The window updates every frame, reading the system time via `datetime.now()`.
