"""
Quiz feature tests.
Run: pytest test_quiz.py -v
"""

import pytest
import pytest_asyncio
from pathlib import Path

# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest_asyncio.fixture
async def db(tmp_path, monkeypatch):
    """Isolated in-memory DB for each test."""
    test_db = tmp_path / "test.db"
    monkeypatch.setattr("quiz_db.DB_PATH", test_db)
    from quiz_db import init_quiz_db
    await init_quiz_db()
    yield test_db


@pytest.fixture
def questions():
    from quiz_source import get_questions_for_quiz
    return get_questions_for_quiz(n=5, seed=42)


# ── Helpers ───────────────────────────────────────────────────────────────────

async def _publish(questions, quiz_date="2026-04-18"):
    from quiz_db import upsert_questions, publish_daily_quiz
    await upsert_questions(questions)
    await publish_daily_quiz([q["id"] for q in questions], quiz_date=quiz_date)


def _all_correct(questions):
    return {q["id"]: q["correct"] for q in questions}


# ── Tests ─────────────────────────────────────────────────────────────────────

@pytest.mark.asyncio
async def test_email_required_to_submit(db, questions):
    """Pydantic rejects empty or invalid email before any DB write."""
    from quiz_routes import AttemptPayload
    import pydantic

    with pytest.raises(pydantic.ValidationError):
        AttemptPayload(email="", quiz_date="2026-04-18", answers={})

    with pytest.raises(pydantic.ValidationError):
        AttemptPayload(email="not-an-email", quiz_date="2026-04-18", answers={})


@pytest.mark.asyncio
async def test_first_attempt_is_official(db, questions):
    """First completed attempt for an email on a quiz date is marked official."""
    await _publish(questions)
    from quiz_db import record_attempt
    result = await record_attempt(
        "user@example.com", "2026-04-18", _all_correct(questions), questions
    )
    assert result["is_official"] is True


@pytest.mark.asyncio
async def test_retake_not_official(db, questions):
    """Second attempt by same email on same date is not official."""
    await _publish(questions)
    from quiz_db import record_attempt
    answers = _all_correct(questions)
    await record_attempt("user@example.com", "2026-04-18", answers, questions)
    retake = await record_attempt("user@example.com", "2026-04-18", answers, questions)
    assert retake["is_official"] is False


@pytest.mark.asyncio
async def test_retake_does_not_overwrite_official_score(db, questions):
    """A perfect retake does not replace a low official score."""
    await _publish(questions)
    from quiz_db import record_attempt, get_leaderboard

    # First attempt — all wrong
    wrong = {q["id"]: "a" if q["correct"] != "a" else "b" for q in questions}
    first = await record_attempt("user@example.com", "2026-04-18", wrong, questions)
    assert first["is_official"] is True

    # Retake — all correct
    await record_attempt(
        "user@example.com", "2026-04-18", _all_correct(questions), questions
    )

    board = await get_leaderboard("2026-04-18")
    assert len(board) == 1
    assert board[0]["score"] == first["score"]   # original low score preserved


@pytest.mark.asyncio
async def test_explanations_in_results(db, questions):
    """Every result item contains an explanation field after submission."""
    await _publish(questions)
    from quiz_db import record_attempt
    result = await record_attempt(
        "user@example.com", "2026-04-18", _all_correct(questions), questions
    )
    assert all("explanation" in r and r["explanation"] for r in result["results"])


@pytest.mark.asyncio
async def test_leaderboard_excludes_retakes(db, questions):
    """Leaderboard only contains one entry per email (the official attempt)."""
    await _publish(questions)
    from quiz_db import record_attempt, get_leaderboard

    answers = _all_correct(questions)
    await record_attempt("a@test.com", "2026-04-18", answers, questions)
    await record_attempt("a@test.com", "2026-04-18", answers, questions)  # retake
    await record_attempt("b@test.com", "2026-04-18", answers, questions)

    board = await get_leaderboard("2026-04-18")
    emails_on_board = [e["email"] for e in board]
    assert len(board) == 2
    assert all(e.count("***") == 1 for e in emails_on_board)  # emails masked


@pytest.mark.asyncio
async def test_daily_quiz_publishing(db, questions):
    """Publishing a quiz stores it and get_today_quiz returns the correct questions."""
    from quiz_db import publish_daily_quiz, upsert_questions, get_today_quiz, has_quiz_today

    assert not await has_quiz_today("2026-04-18")
    await upsert_questions(questions)
    await publish_daily_quiz([q["id"] for q in questions], quiz_date="2026-04-18")
    assert await has_quiz_today("2026-04-18")

    quiz = await get_today_quiz("2026-04-18")
    assert quiz is not None
    assert quiz["quiz_date"] == "2026-04-18"
    assert len(quiz["questions"]) == len(questions)
