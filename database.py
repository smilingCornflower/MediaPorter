import sqlite3
from datetime import UTC
from datetime import datetime
from pathlib import Path
from sqlite3 import Connection

from config import DB_DSN

DB_PATH = Path(DB_DSN)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection() -> Connection:
    return sqlite3.connect(DB_PATH)


def init_database():
    with get_connection() as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS downloads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT NOT NULL,
            url TEXT NOT NULL,
            format TEXT NOT NULL,
            downloaded_at TEXT NOT NULL
        )
        """)
        print("Database initialized.")


def log_download(platform: str, url: str, fmt: str):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO downloads (platform, url, format, downloaded_at) VALUES (?, ?, ?, ?)",
            (platform, url, fmt, datetime.now(tz=UTC).isoformat())
        )


init_database()
