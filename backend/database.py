"""
SQLite database — article storage, retrieval, and 30-day cleanup.
"""

import aiosqlite
from datetime import datetime, timezone, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent / "news.db"
RETENTION_DAYS = 30
MIN_NEW_ARTICLES = 2  # threshold: skip refresh if fewer new articles per category


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id          TEXT PRIMARY KEY,
                title       TEXT NOT NULL,
                summary     TEXT,
                source      TEXT,
                url         TEXT,
                published   TEXT,
                category    TEXT NOT NULL,
                fetched_at  TEXT NOT NULL
            )
        """)
        # Add url column to existing DBs that predate this change
        try:
            await db.execute("ALTER TABLE articles ADD COLUMN url TEXT")
        except Exception:
            pass  # Column already exists — safe to ignore
        await db.commit()


async def count_existing(ids: list[str]) -> int:
    """Return how many of the given IDs already exist in the DB."""
    if not ids:
        return 0
    placeholders = ",".join("?" * len(ids))
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            f"SELECT COUNT(*) FROM articles WHERE id IN ({placeholders})", ids
        )
        row = await cur.fetchone()
        return row[0] if row else 0


async def count_new(articles: list[dict]) -> int:
    """Return how many articles are not yet in the DB."""
    ids = [a["id"] for a in articles]
    existing = await count_existing(ids)
    return len(ids) - existing


async def save_articles(articles: list[dict]) -> int:
    """Insert new articles, skip duplicates. Returns count saved."""
    if not articles:
        return 0
    now = datetime.now(timezone.utc).isoformat()
    saved = 0
    async with aiosqlite.connect(DB_PATH) as db:
        for a in articles:
            try:
                await db.execute(
                    """
                    INSERT OR REPLACE INTO articles
                        (id, title, summary, source, url, published, category, fetched_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (a["id"], a["title"], a["summary"], a["source"],
                     a.get("url", ""), a["published"], a["category"], now),
                )
                saved += 1
            except Exception:
                pass
        await db.commit()
    return saved


async def get_articles(category: str, limit: int = 3) -> list[dict]:
    """Return the most recent articles for a category."""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            """
            SELECT id, title, summary, source, url, published, category
            FROM articles
            WHERE category = ?
            ORDER BY fetched_at DESC, published DESC
            LIMIT ?
            """,
            (category, limit),
        )
        rows = await cur.fetchall()
        return [dict(r) for r in rows]


async def is_empty() -> bool:
    """True if no articles stored yet."""
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute("SELECT COUNT(*) FROM articles")
        row = await cur.fetchone()
        return (row[0] if row else 0) == 0


async def cleanup_old_articles() -> int:
    """Delete articles older than RETENTION_DAYS. Returns count deleted."""
    cutoff = (datetime.now(timezone.utc) - timedelta(days=RETENTION_DAYS)).isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "DELETE FROM articles WHERE fetched_at < ?", (cutoff,)
        )
        await db.commit()
        return cur.rowcount
