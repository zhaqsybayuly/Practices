import json
import os

LEADERBOARD = "leaderboard.json"
SETTINGS = "settings.json"

DEFAULT_SETTINGS = {"sound": True, "car_color": "red", "difficulty": "normal"}


def load_leaderboard():
    if not os.path.exists(LEADERBOARD):
        return []
    with open(LEADERBOARD) as f:
        return json.load(f)


def save_leaderboard(entries):
    with open(LEADERBOARD, "w") as f:
        json.dump(entries, f, indent=2)


def add_score(name, score, distance, coins):
    entries = load_leaderboard()
    entries.append({"name": name, "score": score, "distance": distance, "coins": coins})
    entries.sort(key=lambda e: e["score"], reverse=True)
    entries = entries[:10]   # keep top 10
    save_leaderboard(entries)


def load_settings():
    if not os.path.exists(SETTINGS):
        return DEFAULT_SETTINGS.copy()
    with open(SETTINGS) as f:
        return {**DEFAULT_SETTINGS, **json.load(f)}


def save_settings(s):
    with open(SETTINGS, "w") as f:
        json.dump(s, f, indent=2)
