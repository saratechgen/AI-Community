"""
Quiz database — tables and operations for daily quiz and attempts.
Structure mirrors database.py for news articles.
Same DB file (news.db), separate tables.
"""

import json
import uuid
import aiosqlite
from datetime import datetime, timezone, date as _date
from pathlib import Path

DB_PATH = Path(__file__).parent / "news.db"
QUIZ_QUESTIONS_PER_DAY = 5
LEADERBOARD_LIMIT = 10


async def init_quiz_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS quiz_questions (
                id          TEXT PRIMARY KEY,
                question    TEXT NOT NULL,
                option_a    TEXT NOT NULL,
                option_b    TEXT NOT NULL,
                option_c    TEXT NOT NULL,
                option_d    TEXT NOT NULL,
                correct     TEXT NOT NULL,
                explanation TEXT NOT NULL,
                category    TEXT NOT NULL,
                source      TEXT NOT NULL,
                created_at  TEXT NOT NULL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS quiz_daily (
                quiz_date    TEXT PRIMARY KEY,
                question_ids TEXT NOT NULL,
                published_at TEXT NOT NULL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id           TEXT PRIMARY KEY,
                quiz_date    TEXT NOT NULL,
                email        TEXT NOT NULL,
                score        INTEGER NOT NULL,
                total        INTEGER NOT NULL,
                percentage   REAL NOT NULL,
                is_official  INTEGER NOT NULL,
                answers      TEXT NOT NULL,
                attempted_at TEXT NOT NULL
            )
        """)
        await db.commit()


async def upsert_questions(questions: list[dict]) -> None:
    """Insert or replace questions in the bank. Mirrors save_articles()."""
    now = datetime.now(timezone.utc).isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        for q in questions:
            await db.execute(
                """INSERT OR REPLACE INTO quiz_questions
                   (id, question, option_a, option_b, option_c, option_d,
                    correct, explanation, category, source, created_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (q["id"], q["question"], q["option_a"], q["option_b"],
                 q["option_c"], q["option_d"], q["correct"], q["explanation"],
                 q["category"], q.get("source", "local"), now),
            )
        await db.commit()


async def publish_daily_quiz(
    question_ids: list[str],
    quiz_date: str | None = None,
) -> None:
    """Publish today's quiz by storing the ordered question ID list."""
    if quiz_date is None:
        quiz_date = _date.today().isoformat()
    now = datetime.now(timezone.utc).isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT OR REPLACE INTO quiz_daily (quiz_date, question_ids, published_at)
               VALUES (?, ?, ?)""",
            (quiz_date, json.dumps(question_ids), now),
        )
        await db.commit()


async def has_quiz_today(quiz_date: str | None = None) -> bool:
    """Return True if a quiz is already published for the given date."""
    if quiz_date is None:
        quiz_date = _date.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT 1 FROM quiz_daily WHERE quiz_date = ?", (quiz_date,)
        )
        return await cur.fetchone() is not None


async def get_today_quiz(quiz_date: str | None = None) -> dict | None:
    """Return full quiz with questions. Returns None if no quiz published."""
    if quiz_date is None:
        quiz_date = _date.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT question_ids FROM quiz_daily WHERE quiz_date = ?", (quiz_date,)
        )
        row = await cur.fetchone()
        if not row:
            return None
        qids = json.loads(row["question_ids"])
        placeholders = ",".join("?" * len(qids))
        cur2 = await db.execute(
            f"""SELECT id, question, option_a, option_b, option_c, option_d,
                       correct, explanation, category
                FROM quiz_questions WHERE id IN ({placeholders})""",
            qids,
        )
        questions = [dict(r) for r in await cur2.fetchall()]
        order = {qid: i for i, qid in enumerate(qids)}
        questions.sort(key=lambda q: order.get(q["id"], 999))
        return {"quiz_date": quiz_date, "questions": questions}


async def record_attempt(
    email: str,
    quiz_date: str,
    answers: dict[str, str],
    questions: list[dict],
) -> dict:
    """Score the attempt server-side, store it, and return the result."""
    results = []
    score = 0
    for q in questions:
        chosen = answers.get(q["id"], "")
        is_correct = chosen == q["correct"]
        if is_correct:
            score += 1
        results.append({
            "question_id": q["id"],
            "question":    q["question"],
            "chosen":      chosen,
            "correct":     q["correct"],
            "is_correct":  is_correct,
            "explanation": q["explanation"],
        })

    total      = len(questions)
    percentage = round((score / total) * 100, 1) if total else 0.0

    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT 1 FROM quiz_attempts WHERE email=? AND quiz_date=? AND is_official=1",
            (email.lower(), quiz_date),
        )
        is_official = (await cur.fetchone()) is None

        now = datetime.now(timezone.utc).isoformat()
        await db.execute(
            """INSERT INTO quiz_attempts
               (id, quiz_date, email, score, total, percentage, is_official, answers, attempted_at)
               VALUES (?,?,?,?,?,?,?,?,?)""",
            (str(uuid.uuid4()), quiz_date, email.lower(), score, total,
             percentage, 1 if is_official else 0, json.dumps(answers), now),
        )
        await db.commit()

    return {
        "score":       score,
        "total":       total,
        "percentage":  percentage,
        "is_official": is_official,
        "results":     results,
    }


async def get_attempt_count(quiz_date: str | None = None) -> int:
    """Return count of official attempts for the given date."""
    if quiz_date is None:
        quiz_date = _date.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT COUNT(*) FROM quiz_attempts WHERE quiz_date=? AND is_official=1",
            (quiz_date,),
        )
        row = await cur.fetchone()
        return row[0] if row else 0


def _mask_email(email: str) -> str:
    local, _, domain = email.partition("@")
    return f"{local[:2]}***@{domain}" if len(local) > 2 else f"***@{domain}"


async def get_leaderboard(
    quiz_date: str | None = None,
    limit: int = LEADERBOARD_LIMIT,
) -> list[dict]:
    """Return top official attempts. Mirrors get_articles()."""
    if quiz_date is None:
        quiz_date = _date.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            """SELECT email, score, total, percentage, attempted_at
               FROM quiz_attempts
               WHERE quiz_date=? AND is_official=1
               ORDER BY percentage DESC, attempted_at ASC
               LIMIT ?""",
            (quiz_date, limit),
        )
        rows = await cur.fetchall()
        return [
            {
                "rank":        i + 1,
                "email":       _mask_email(dict(r)["email"]),
                "score":       r["score"],
                "total":       r["total"],
                "percentage":  r["percentage"],
                "attempted_at": r["attempted_at"],
            }
            for i, r in enumerate(rows)
        ]
