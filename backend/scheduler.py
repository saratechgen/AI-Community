"""
Scheduler — news refresh (every 30 min) + daily quiz publish.
Quiz publishes at 20:01 UTC = 00:01 UAE time (UTC+4).
"""

import logging
from datetime import date
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import save_articles, cleanup_old_articles
from news_fetcher import fetch_all_news
from quiz_source import get_questions_for_stage
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

        saved = await save_articles(all_articles)
        log.info(f"refresh_news: saved {saved} new articles")

        deleted = await cleanup_old_articles()
        if deleted:
            log.info(f"refresh_news: cleaned up {deleted} articles older than 30 days")

    except Exception as e:
        log.error(f"refresh_news: failed — {e}")


async def publish_quiz() -> None:
    """Publish today's 3-stage quiz if not already done."""
    today = date.today().isoformat()
    if await has_quiz_today():
        log.info("publish_quiz: quiz already published for today")
        return

    seed = int(today.replace("-", ""))

    # 5 questions per stage, seeded by date for daily consistency
    stage_questions: dict[int, list[dict]] = {}
    all_questions: list[dict] = []
    for s in [1, 2, 3]:
        qs = get_questions_for_stage(stage=s, n=5, seed=seed)
        stage_questions[s] = qs
        all_questions.extend(qs)

    await upsert_questions(all_questions)

    stage_ids = {str(s): [q["id"] for q in qs] for s, qs in stage_questions.items()}
    await publish_daily_quiz(stage_ids)
    log.info(f"publish_quiz: published 15 questions (3 × 5) for {today}")


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
        hour=20,    # 20:01 UTC = 00:01 UAE (UTC+4)
        minute=1,
        id="quiz_publish",
        replace_existing=True,
    )
    _scheduler.start()
    log.info("Scheduler started — news every 30 min, quiz daily at 20:01 UTC (00:01 UAE)")


def stop_scheduler() -> None:
    _scheduler.shutdown(wait=False)
    log.info("Scheduler stopped")
