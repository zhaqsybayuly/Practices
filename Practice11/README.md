# Practice 11 — Pygame Games (extends Practice 10)

Three games extended from Practice 10 with new features.

## 1. Racer
- **Weighted coins**: bronze (1 pt), silver (3 pts), gold (5 pts) — rarer = worth more
- **Enemy speeds up** every 10 collected points
- Use `← →` to move, `R` to restart on game over

## 2. Snake
- **Weighted food**: red (1), yellow (2), cyan (3) — rarer = worth more
- **Food disappears** after 5 seconds — a timer is shown in the top bar
- Same gameplay as Practice 10 (walls, levels, restart with `R`)

## 3. Paint
- All Practice 10 tools: pen, rect, circle, eraser, color palette
- New shape tools: **square**, **right triangle**, **equilateral triangle**, **rhombus**
- Click and drag to draw shapes. Live preview while dragging.

## Run
```bash
source ../Practice9/venv/bin/activate
cd racer && python main.py
cd ../snake && python main.py
cd ../paint && python main.py
```
