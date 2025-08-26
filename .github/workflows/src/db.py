import sqlite3
from typing import Iterable, Dict, Any

def get_conn(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn

def init_db(conn: sqlite3.Connection):
    conn.executescript(
        '''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            url TEXT UNIQUE,
            title TEXT,
            published_at TEXT,
            summary TEXT,
            raw_text TEXT
        );
        '''
    )
    conn.commit()

def insert_articles(conn, rows: Iterable[Dict[str, Any]]):
    cur = conn.cursor()
    for r in rows:
        try:
            cur.execute(
                "INSERT OR IGNORE INTO articles (source, url, title, published_at, summary, raw_text) VALUES (?, ?, ?, ?, ?, ?)",
                (r["source"], r["url"], r["title"], r["published_at"], r.get("summary", ""), r.get("raw_text", "")),
            )
        except:
            pass
    conn.commit()

def fetch_recent_articles(conn, since_iso: str):
    cur = conn.cursor()
    cur.execute("SELECT id, source, url, title, published_at, summary, raw_text FROM articles WHERE published_at >= ? ORDER BY published_at DESC", (since_iso,))
    cols = [d[0] for d in cur.description]
    return [dict(zip(cols, row)) for row in cur.fetchall()]
