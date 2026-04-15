# Moving Ball

A red ball on a white background that moves when you press the arrow keys. Each key press shifts the ball by 20 pixels, and it can't leave the window.

## Files

- `main.py` — window and input loop
- `ball.py` — `Ball` class holding position, draw method and boundary check

## Controls

- **← ↑ → ↓** — move the ball

Moves that would push the ball off-screen are simply ignored.

## Run

```bash
python main.py
```
