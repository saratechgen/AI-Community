"""
Scheduler — news refresh (every 30 min) + daily quiz publish (00:01 UTC).
"""

import logging
from datetime import date
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import MIN_NEW_ARTICLES, count_new, save_articles, cleanup_old_articles
from news_fetcher import fetch_all_news
from quiz_source import get_questions_for_quiz
from quiz_db import upsert_questions, publish_daily_quiz, has_quiz_today

log = logging.getLogger("scheduler")

_scheduler = AsyncIOScheduler()


async def refresh_news() -> None:
    log.info("refresh_news: starting fetch")
    try:
        fetched = await fetch_all_news()

        all_articles = (
            fetched["claude"] +
            fetched["aiAgents"] +
            fetched["aiAtWork"] +
            fetched["advancements"] +
            fetched["quickTips"]
        )

        # Per-category new-article counts (all 5 categories)
        counts = {}
        for category, key in [
            ("claude",       "claude"),
            ("ai-agents",    "aiAgents"),
            ("ai-at-work",   "aiAtWork"),
            ("advancements", "advancements"),
            ("quick-tips",   "quickTips"),
        ]:
            counts[category] = await count_new(fetched[key])

        min_new = min(counts.values()) if counts else 0
        log.info(f"refresh_news: new article counts per category — {counts}")

        if min_new < MIN_NEW_ARTICLES:
            log.info(
                f"refresh_news: skipping save — "
                f"min new articles ({min_new}) below threshold ({MIN_NEW_ARTICLES})"
            )
        else:
            saved = await save_articles(all_articles)
            log.info(f"refresh_news: saved {saved} new articles")

        deleted = await cleanup_old_articles()
        if deleted:
            log.info(f"refresh_news: cleaned up {deleted} articles older than 30 days")

    except Exception as e:
        log.error(f"refresh_news: failed — {e}")


async def publish_quiz() -> None:
    """Publish today's quiz if not already done. Mirrors refresh_news() pattern."""
    today = date.today().isoformat()
    if await has_quiz_today():
        log.info("publish_quiz: quiz already published for today")
        return
    seed = int(today.replace("-", ""))
    questions = get_questions_for_quiz(n=5, seed=seed)
    await upsert_questions(questions)
    await publish_daily_quiz([q["id"] for q in questions])
    log.info(f"publish_quiz: published 5 questions for {today}")


def start_scheduler() -> None:
    _scheduler.add_job(
        refresh_news,
        trigger="interval",
        minutes=30,
        id="news_refresh",
        replace_existing=True,
    )
    _scheduler.add_job(
        publish_quiz,
        trigger="cron",
        hour=0,
        minute=1,
        id="quiz_publish",
        replace_existing=True,
    )
    _scheduler.start()
    log.info("Scheduler started — news every 30 min, quiz daily at 00:01 UTC")


def stop_scheduler() -> None:
    _scheduler.shutdown(wait=False)
    log.info("Scheduler stopped")
