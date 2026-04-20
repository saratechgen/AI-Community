"""
Quiz API routes.
Endpoint style mirrors app.py's /api/news pattern.
"""

import re
import logging

from fastapi import APIRouter
from pydantic import BaseModel, field_validator

from quiz_db import get_today_quiz, record_attempt, get_leaderboard as _db_leaderboard, get_attempt_count

log    = logging.getLogger("quiz")
router = APIRouter()

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class AttemptPayload(BaseModel):
    email:     str
    quiz_date: str
    answers:   dict[str, str]

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: str) -> str:
        v = v.strip().lower()
        if not _EMAIL_RE.match(v):
            raise ValueError("A valid email address is required to submit.")
        return v


def _ok(data, meta=None):
    body = {"data": data}
    if meta:
        body["meta"] = meta
    return body


def _err(code: str, message: str):
    return {"error": {"code": code, "message": message}}


@router.get("/api/quiz/today")
async def get_today():
    try:
        quiz = await get_today_quiz()
        if not quiz:
            return _err("NO_QUIZ", "No quiz published for today. Check back soon!")
        attempt_count = await get_attempt_count(quiz["quiz_date"])
        return _ok({**quiz, "attempt_count": attempt_count})
    except Exception as e:
        log.error(f"get_today failed: {e}")
        return _err("INTERNAL", "Could not load today's quiz.")


@router.post("/api/quiz/attempt")
async def submit_attempt(payload: AttemptPayload):
    try:
        quiz = await get_today_quiz(payload.quiz_date)
        if not quiz:
            return _err("NO_QUIZ", "No quiz found for the given date.")
        result = await record_attempt(
            payload.email,
            payload.quiz_date,
            payload.answers,
            quiz["questions"],
        )
        return _ok(result)
    except ValueError as e:
        return _err("VALIDATION", str(e))
    except Exception as e:
        log.error(f"submit_attempt failed: {e}")
        return _err("INTERNAL", "Could not record attempt.")


@router.get("/api/quiz/leaderboard")
async def get_leaderboard(quiz_date: str | None = None):
    try:
        board = await _db_leaderboard(quiz_date)
        return _ok(board)
    except Exception as e:
        log.error(f"get_leaderboard failed: {e}")
        return _err("INTERNAL", "Could not load leaderboard.")
