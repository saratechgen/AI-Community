"""Dubai curated events — SQLite storage and seed data."""
import aiosqlite
from datetime import date
from database import DB_PATH

_SEED = [
    ("dxb-world-ai-expo-2026",  "World AI Expo Dubai 2026",  "2026-10-07", "2026-10-08", "Dubai, UAE",                          "UAE", "World AI Expo",   "https://worldaiexpo.io"),
    ("dxb-ai-festival-2026",    "Dubai AI Festival 2026",    "2026-10-26", "2026-10-27", "Dubai World Trade Centre, Dubai",     "UAE", "Dubai AI Campus", "https://dubaiaifestival.com"),
    ("dxb-gitex-global-2026",   "GITEX Global 2026",         "2026-12-07", "2026-12-11", "Dubai Exhibition Centre, Expo City",  "UAE", "GITEX",           "https://www.gitex.com"),
]

async def init_dubai_events_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS dubai_events (
                id        TEXT PRIMARY KEY,
                title     TEXT NOT NULL,
                date      TEXT NOT NULL,
                end_date  TEXT,
                location  TEXT DEFAULT '',
                country   TEXT DEFAULT 'UAE',
                organizer TEXT DEFAULT '',
                url       TEXT DEFAULT '',
                type      TEXT DEFAULT 'conference'
            )
        """)
        for row in _SEED:
            await db.execute(
                "INSERT OR IGNORE INTO dubai_events (id,title,date,end_date,location,country,organizer,url) VALUES (?,?,?,?,?,?,?,?)",
                row,
            )
        await db.commit()

async def get_upcoming_dubai_events() -> list[dict]:
    today = date.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT * FROM dubai_events WHERE date >= ? ORDER BY date ASC", (today,)
        )
        return [dict(r) for r in await cur.fetchall()]
