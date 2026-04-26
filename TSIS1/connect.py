import psycopg2
from config import config

def connect():
    try:
        return psycopg2.connect(**config())
    except (Exception, psycopg2.DatabaseError) as e:
        print(f"DB connection error: {e}")
        return None
