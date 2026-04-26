# TSIS4 — Snake Extended

Extends Practice 10-11 snake with PostgreSQL persistence and new gameplay.

## Features
- **PostgreSQL** leaderboard via `psycopg2` (`players` + `game_sessions` tables)
- Username entry on the menu, auto-save score after game over
- Personal best shown during gameplay
- **Poison food** (dark red) — shortens the snake by 2; instant death if length ≤ 1
- 3 power-ups (8 s lifetime on board):
  - **Boost** — faster snake for 5 s
  - **Slow** — slower snake for 5 s
  - **Shield** — ignore the next wall / self / obstacle hit
- **Obstacles** appear from level 3 onward
- 4 screens: Main Menu, Game Over, Leaderboard, Settings
- Settings (`settings.json`): snake color, grid overlay, sound

## Files
- `main.py` — entry + screens
- `game.py` — gameplay loop
- `db.py` — PostgreSQL helpers (auto-creates schema on startup)
- `config.py` — DB credentials
- `settings.json` — user preferences

## Run
```bash
# create DB once:  CREATE DATABASE snake_db;
python main.py
```
