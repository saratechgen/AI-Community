"""
Quiz database — tables and operations for 3-stage daily quiz.
Same DB file (news.db), separate tables.
"""

import json
import uuid
import aiosqlite
from datetime import datetime, timezone, date as _date
from pathlib import Path

DB_PATH          = Path(__file__).parent / "news.db"
LEADERBOARD_LIMIT = 20
PASS_MARK        = 4   # out of 5 per stage

STAGE_TITLES  = {1: "Foundation", 2: "Applied", 3: "Advanced"}
STAGE_LABELS  = {0: "—", 1: "Foundation", 2: "Applied", 3: "Advanced"}
STAGE_BADGES  = {3: "AI Champion", 2: "Applied Expert", 1: "Foundation", 0: ""}


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
                stage       INTEGER NOT NULL DEFAULT 1,
                created_at  TEXT NOT NULL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS quiz_daily (
                quiz_date          TEXT PRIMARY KEY,
                question_ids       TEXT NOT NULL,
                stage_question_ids TEXT,
                published_at       TEXT NOT NULL
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id           TEXT PRIMARY KEY,
                quiz_date    TEXT NOT NULL,
                email        TEXT NOT NULL,
                username     TEXT NOT NULL DEFAULT '',
                stage        INTEGER NOT NULL DEFAULT 1,
                score        INTEGER NOT NULL,
                total        INTEGER NOT NULL,
                percentage   REAL NOT NULL,
                is_official  INTEGER NOT NULL,
                answers      TEXT NOT NULL,
                attempted_at TEXT NOT NULL
            )
        """)
        # Safe migrations for databases created before 3-stage / username update
        for sql in [
            "ALTER TABLE quiz_questions ADD COLUMN stage INTEGER NOT NULL DEFAULT 1",
            "ALTER TABLE quiz_daily     ADD COLUMN stage_question_ids TEXT",
            "ALTER TABLE quiz_attempts  ADD COLUMN stage INTEGER NOT NULL DEFAULT 1",
            "ALTER TABLE quiz_attempts  ADD COLUMN username TEXT NOT NULL DEFAULT ''",
        ]:
            try:
                await db.execute(sql)
            except Exception:
                pass  # column already exists
        await db.commit()


async def upsert_questions(questions: list[dict]) -> None:
    now = datetime.now(timezone.utc).isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        for q in questions:
            await db.execute(
                """INSERT OR REPLACE INTO quiz_questions
                   (id, question, option_a, option_b, option_c, option_d,
                    correct, explanation, category, source, stage, created_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (q["id"], q["question"], q["option_a"], q["option_b"],
                 q["option_c"], q["option_d"], q["correct"], q["explanation"],
                 q["category"], q.get("source", "local"), q.get("stage", 1), now),
            )
        await db.commit()


async def publish_daily_quiz(
    stage_ids: dict[str, list[str]],
    quiz_date: str | None = None,
) -> None:
    """Publish today's quiz. stage_ids = {"1": [...5 ids], "2": [...], "3": [...]}"""
    if quiz_date is None:
        quiz_date = _date.today().isoformat()
    all_ids = stage_ids["1"] + stage_ids["2"] + stage_ids["3"]
    now     = datetime.now(timezone.utc).isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT OR REPLACE INTO quiz_daily
               (quiz_date, question_ids, stage_question_ids, published_at)
               VALUES (?, ?, ?, ?)""",
            (quiz_date, json.dumps(all_ids), json.dumps(stage_ids), now),
        )
        await db.commit()


async def has_quiz_today(quiz_date: str | None = None) -> bool:
    """True only if a 3-stage quiz is published for this date."""
    if quiz_date is None:
        quiz_date = _date.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            "SELECT stage_question_ids FROM quiz_daily WHERE quiz_date = ?",
            (quiz_date,),
        )
        row = await cur.fetchone()
        return bool(row and row[0])  # None/empty = old format, needs re-publish


async def _fetch_questions_by_ids(db: aiosqlite.Connection, ids: list[str]) -> list[dict]:
    if not ids:
        return []
    placeholders = ",".join("?" * len(ids))
    cur = await db.execute(
        f"""SELECT id, question, option_a, option_b, option_c, option_d,
                   correct, explanation, category
            FROM quiz_questions WHERE id IN ({placeholders})""",
        ids,
    )
    rows      = [dict(r) for r in await cur.fetchall()]
    order_map = {qid: i for i, qid in enumerate(ids)}
    rows.sort(key=lambda q: order_map.get(q["id"], 999))
    return rows


async def get_today_quiz(quiz_date: str | None = None) -> dict | None:
    """Return stage-structured quiz. Returns None if not published."""
    if quiz_date is None:
        quiz_date = _date.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cur = await db.execute(
            "SELECT stage_question_ids FROM quiz_daily WHERE quiz_date = ?",
            (quiz_date,),
        )
        row = await cur.fetchone()
        if not row or not row["stage_question_ids"]:
            return None

        stage_ids = json.loads(row["stage_question_ids"])
        stages    = []
        for s in [1, 2, 3]:
            ids       = stage_ids.get(str(s), [])
            questions = await _fetch_questions_by_ids(db, ids)
            stages.append({
                "stage":     s,
                "title":     STAGE_TITLES[s],
                "pass_mark": PASS_MARK,
                "questions": questions,
            })
        return {"quiz_date": quiz_date, "stages": stages}


async def get_stage_status(email: str, quiz_date: str) -> dict:
    """Return official attempt results per stage for email+date."""
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            """SELECT stage, score FROM quiz_attempts
               WHERE email=? AND quiz_date=? AND is_official=1 AND stage IN (1,2,3)""",
            (email.lower(), quiz_date),
        )
        rows   = await cur.fetchall()
    status = {s: {"attempted": False, "score": 0, "passed": False} for s in [1, 2, 3]}
    for row in rows:
        s = row[0]
        if s in status:
            status[s] = {"attempted": True, "score": row[1], "passed": row[1] >= PASS_MARK}
    return status


async def record_stage_attempt(
    email:     str,
    quiz_date: str,
    stage:     int,
    answers:   dict[str, str],
    questions: list[dict],
    username:  str = '',
) -> dict:
    """Validate unlock, score attempt, persist, return result."""
    email = email.lower()
    async with aiosqlite.connect(DB_PATH) as db:
        # Server-side unlock gate
        if stage > 1:
            cur = await db.execute(
                """SELECT score FROM quiz_attempts
                   WHERE email=? AND quiz_date=? AND stage=? AND is_official=1""",
                (email, quiz_date, stage - 1),
            )
            prev = await cur.fetchone()
            if not prev or prev[0] < PASS_MARK:
                raise ValueError(
                    f"Stage {stage - 1} must be cleared with at least {PASS_MARK}/5 first."
                )

        # Score
        results = []
        score   = 0
        for q in questions:
            chosen     = answers.get(q["id"], "")
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
        passed     = score >= PASS_MARK

        # First attempt for this email+stage+date is official
        cur = await db.execute(
            "SELECT 1 FROM quiz_attempts WHERE email=? AND quiz_date=? AND stage=? AND is_official=1",
            (email, quiz_date, stage),
        )
        is_official = (await cur.fetchone()) is None

        now      = datetime.now(timezone.utc).isoformat()
        uname    = (username or '').strip()[:50]
        await db.execute(
            """INSERT INTO quiz_attempts
               (id, quiz_date, email, username, stage, score, total, percentage,
                is_official, answers, attempted_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (str(uuid.uuid4()), quiz_date, email, uname, stage, score, total,
             percentage, 1 if is_official else 0, json.dumps(answers), now),
        )
        await db.commit()

    return {
        "stage":       stage,
        "score":       score,
        "total":       total,
        "percentage":  percentage,
        "passed":      passed,
        "is_official": is_official,
        "results":     results,
    }


async def get_attempt_count(quiz_date: str | None = None) -> int:
    """Count distinct players who officially started today (stage 1 attempts)."""
    if quiz_date is None:
        quiz_date = _date.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            """SELECT COUNT(DISTINCT email) FROM quiz_attempts
               WHERE quiz_date=? AND is_official=1 AND stage=1""",
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
    """Rank by: highest stage cleared → total score → completion time → first attempt."""
    if quiz_date is None:
        quiz_date = _date.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(
            """SELECT
                 email,
                 MAX(username)                                        AS username,
                 MAX(CASE WHEN score >= ? THEN stage ELSE 0 END)     AS highest_stage,
                 SUM(score)                                          AS total_score,
                 MIN(CASE WHEN stage=3 THEN attempted_at ELSE NULL END) AS completed_at,
                 MIN(attempted_at)                                   AS first_attempt
               FROM quiz_attempts
               WHERE quiz_date=? AND is_official=1 AND stage IN (1,2,3)
               GROUP BY email
               ORDER BY
                 highest_stage DESC,
                 total_score   DESC,
                 COALESCE(completed_at, '9999') ASC,
                 first_attempt ASC
               LIMIT ?""",
            (PASS_MARK, quiz_date, limit),
        )
        rows = await cur.fetchall()

    return [
        {
            "rank":           i + 1,
            "username":       row[1] or _mask_email(row[0]),
            "email":          _mask_email(row[0]),
            "highest_stage":  row[2],
            "stage_label":    STAGE_LABELS.get(row[2], "—"),
            "total_score":    row[3],
            "total_possible": 15,
            "badge":          STAGE_BADGES.get(row[2], ""),
            "attempted_at":   row[5],
        }
        for i, row in enumerate(rows)
    ]
