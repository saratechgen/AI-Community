"""
FastAPI backend — AI Community Website
Endpoints: GET /api/health, GET /api/news
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db, get_articles, is_empty
from quiz_db import init_quiz_db
from dubai_events_db import init_dubai_events_db
from quiz_routes   import router as quiz_router
from events_routes import router as events_router
from ask_routes    import router as ask_router
from scheduler import refresh_news, publish_quiz, start_scheduler, stop_scheduler

logging.basicConfig(
    level=logging.INFO,
    format='{"ts":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","msg":"%(message)s"}',
)
log = logging.getLogger("app")

# ── Category configuration — single source of truth ──────────────────────────
# Add, rename, or remove entries here; the dynamic brief updates automatically.

CATEGORY_META = [
    {"key": "claude",       "tag": "Claude & Anthropic"},
    {"key": "ai-agents",    "tag": "AI Agents"},
    {"key": "ai-at-work",   "tag": "AI at Work"},
    {"key": "advancements", "tag": "New Advancements"},
    {"key": "quick-tips",   "tag": "Quick Tips"},
]

# ── Dynamic brief ─────────────────────────────────────────────────────────────
# Edit the template string here to change the wording site-wide.
# {cats} is replaced at runtime with the live category list.

BRIEF_TEMPLATE = (
    "On deck right now: {cats}. Sourced from 17 feeds across the AI "
    "ecosystem — refreshed every 30 minutes so you never miss what matters."
)


def _build_brief(active: list[dict]) -> str:
    """Build the section intro from whichever categories are currently live."""
    tags = [c["tag"] for c in active]
    n = len(tags)
    if n == 0:
        return "Your live AI news feed — refreshed every 30 minutes."
    if n == 1:
        cats_str = tags[0]
    elif n == 2:
        cats_str = f"{tags[0]} and {tags[1]}"
    else:
        cats_str = ", ".join(tags[:-1]) + f", and {tags[-1]}"
    return BRIEF_TEMPLATE.format(cats=cats_str)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("Starting up — initialising database")
    await init_db()
    await init_quiz_db()
    await init_dubai_events_db()

    log.info("Running startup news fetch")
    await refresh_news()

    await publish_quiz()
    start_scheduler()
    yield
    stop_scheduler()
    log.info("Shut down cleanly")


app = FastAPI(title="AI Community — News API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


app.include_router(quiz_router)
app.include_router(events_router)
app.include_router(ask_router)

# ── Helpers ───────────────────────────────────────────────────────────────────

def success(data, meta=None):
    body = {"data": data}
    if meta:
        body["meta"] = meta
    return body


def error(code: str, message: str):
    return {"error": {"code": code, "message": message}}


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/api/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}


@app.get("/api/news")
async def get_news():
    try:
        results = await asyncio.gather(
            get_articles("claude",       5),
            get_articles("ai-agents",    5),
            get_articles("ai-at-work",   5),
            get_articles("advancements", 5),
            get_articles("quick-tips",   5),
        )
        claude, ai_agents, ai_at_work, advancements, quick_tips = results

        if not any(results):
            return error("NO_CONTENT", "No news available yet. Please try again shortly.")

        # Determine which categories returned content — brief reflects only those
        by_key = {c["key"]: r for c, r in zip(CATEGORY_META, results)}
        active = [c for c in CATEGORY_META if by_key.get(c["key"])]

        return success(
            data={
                "claude":       claude,
                "aiAgents":     ai_agents,
                "aiAtWork":     ai_at_work,
                "advancements": advancements,
                "quickTips":    quick_tips,
            },
            meta={
                "fetched_at": datetime.now(timezone.utc).isoformat(),
                "brief":      _build_brief(active),
                "categories": [c["tag"] for c in active],
            },
        )
    except Exception as e:
        log.error(f"get_news failed: {e}")
        return error("INTERNAL", "Could not retrieve news. Please try again later.")
