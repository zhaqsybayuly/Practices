import psycopg2
from config import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS players (
    id       SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS game_sessions (
    id            SERIAL PRIMARY KEY,
    player_id     INTEGER REFERENCES players(id),
    score         INTEGER NOT NULL,
    level_reached INTEGER NOT NULL,
    played_at     TIMESTAMP DEFAULT NOW()
);
"""


def connect():
    try:
        return psycopg2.connect(**config())
    except Exception as e:
        print(f"DB error: {e}")
        return None


def init_schema():
    conn = connect()
    if not conn:
        return
    with conn, conn.cursor() as cur:
        cur.execute(SCHEMA)
    conn.close()


def get_or_create_player(username):
    conn = connect()
    with conn, conn.cursor() as cur:
        cur.execute("SELECT id FROM players WHERE username=%s", (username,))
        row = cur.fetchone()
        if row:
            pid = row[0]
        else:
            cur.execute("INSERT INTO players(username) VALUES(%s) RETURNING id", (username,))
            pid = cur.fetchone()[0]
    conn.close()
    return pid


def save_session(player_id, score, level):
    conn = connect()
    with conn, conn.cursor() as cur:
        cur.execute("""INSERT INTO game_sessions(player_id, score, level_reached)
                       VALUES (%s, %s, %s)""", (player_id, score, level))
    conn.close()


def personal_best(player_id):
    conn = connect()
    with conn, conn.cursor() as cur:
        cur.execute("SELECT COALESCE(MAX(score), 0) FROM game_sessions WHERE player_id=%s", (player_id,))
        best = cur.fetchone()[0]
    conn.close()
    return best


def top_10():
    conn = connect()
    with conn, conn.cursor() as cur:
        cur.execute("""
            SELECT p.username, gs.score, gs.level_reached, gs.played_at
            FROM game_sessions gs JOIN players p ON p.id = gs.player_id
            ORDER BY gs.score DESC LIMIT 10
        """)
        rows = cur.fetchall()
    conn.close()
    return rows
