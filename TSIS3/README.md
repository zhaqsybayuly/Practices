# TSIS3 — Racer Extended

Extends Practice 10-11 racer with:
- Enemy traffic + oil-spill obstacles + difficulty scaling
- 3 power-ups: **Nitro** (speed boost), **Shield** (1 free hit), **Repair** (clears obstacle)
- Score = coins × 10 + distance / 10
- Distance meter
- Persistent **leaderboard** in `leaderboard.json` (top 10)
- Username entry on every play
- 4 screens: Main Menu, Game Over, Leaderboard, Settings
- Settings (`settings.json`): sound, car color, difficulty

## Files
- `main.py` — game screens + main menu
- `racer.py` — gameplay loop
- `ui.py` — small UI helpers (button, text input)
- `persistence.py` — settings + leaderboard JSON I/O

## Run
```bash
python main.py
```
