"""
Quiz API routes — 3-stage gated daily quiz.
"""

import re
import logging

from fastapi import APIRouter
from pydantic import BaseModel, field_validator

from quiz_db import (
    get_today_quiz, record_stage_attempt, get_stage_status,
    get_leaderboard as _db_leaderboard, get_attempt_count,
)

log    = logging.getLogger("quiz")
router = APIRouter()

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class AttemptPayload(BaseModel):
    email:     str
    username:  str = ''
    quiz_date: str
    stage:     int = 1
    answers:   dict[str, str]

    @field_validator("email")
    @classmethod
    def email_valid(cls, v: str) -> str:
        v = v.strip().lower()
        if not _EMAIL_RE.match(v):
            raise ValueError("A valid email address is required to submit.")
        return v

    @field_validator("username")
    @classmethod
    def username_clean(cls, v: str) -> str:
        return v.strip()[:50]

    @field_validator("stage")
    @classmethod
    def stage_valid(cls, v: int) -> int:
        if v not in (1, 2, 3):
            raise ValueError("Stage must be 1, 2, or 3.")
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

        stage_data = next(
            (s for s in quiz["stages"] if s["stage"] == payload.stage), None
        )
        if not stage_data:
            return _err("INVALID_STAGE", f"Stage {payload.stage} not found.")

        result = await record_stage_attempt(
            payload.email,
            payload.quiz_date,
            payload.stage,
            payload.answers,
            stage_data["questions"],
            payload.username,
        )
        return _ok(result)
    except ValueError as e:
        return _err("STAGE_LOCKED", str(e))
    except Exception as e:
        log.error(f"submit_attempt failed: {e}")
        return _err("INTERNAL", "Could not record attempt.")


@router.get("/api/quiz/stage-status")
async def get_stage_status_endpoint(email: str, quiz_date: str):
    try:
        status = await get_stage_status(email.strip().lower(), quiz_date)
        return _ok(status)
    except Exception as e:
        log.error(f"stage_status failed: {e}")
        return _err("INTERNAL", "Could not load stage status.")


@router.get("/api/quiz/leaderboard")
async def get_leaderboard(quiz_date: str | None = None):
    try:
        board = await _db_leaderboard(quiz_date)
        return _ok(board)
    except Exception as e:
        log.error(f"get_leaderboard failed: {e}")
        return _err("INTERNAL", "Could not load leaderboard.")
