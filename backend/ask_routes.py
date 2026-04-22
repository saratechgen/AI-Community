"""Ask AI Adoption — lightweight query submission.
Stores submissions in ask_submissions.json.
Future: route to mailbox, SharePoint, admin panel, status tracking.
"""
import json
import logging
import re
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel, field_validator

log    = logging.getLogger("ask_routes")
router = APIRouter(prefix="/api/ask")

SUBMISSIONS_FILE = Path(__file__).parent / "ask_submissions.json"
_LOCK            = threading.Lock()

QueryType = Literal["Tools", "Trainings", "Team Related", "Others"]


class AskPayload(BaseModel):
    name:       str
    email:      str
    division:   str
    department: str
    query_type: QueryType
    message:    str

    @field_validator("name", "division", "department", "message", mode="before")
    @classmethod
    def strip_and_require(cls, v: str) -> str:
        v = str(v).strip()
        if not v:
            raise ValueError("This field is required.")
        return v

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, v: str) -> str:
        v = str(v).strip()
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v):
            raise ValueError("Please enter a valid email address.")
        return v


def _load() -> dict:
    if SUBMISSIONS_FILE.exists():
        try:
            return json.loads(SUBMISSIONS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"counter": 0, "submissions": []}


def _save(store: dict) -> None:
    SUBMISSIONS_FILE.write_text(
        json.dumps(store, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def _ack(n: int) -> str:
    return f"AIADQ{n:03d}"


@router.post("")
def submit_ask(payload: AskPayload):
    """Accept a query and persist it with a unique acknowledgment number."""
    try:
        with _LOCK:
            store = _load()
            store["counter"] += 1
            ack = _ack(store["counter"])
            record = {
                "ack_number":   ack,
                "name":         payload.name,
                "email":        payload.email,
                "division":     payload.division,
                "department":   payload.department,
                "query_type":   payload.query_type,
                "message":      payload.message,
                "submitted_at": datetime.now(timezone.utc).isoformat(),
                "status":       "pending",
            }
            store["submissions"].append(record)
            _save(store)

        log.info(f"ask_submit ack={ack} email={payload.email} query_type={payload.query_type}")
        return {
            "data": {
                "ack_number":   ack,
                "submitted_at": record["submitted_at"],
            },
            "meta": {"message": "Query submitted successfully."},
        }
    except Exception as exc:
        log.error(f"ask_submit failed: {exc}")
        return {"error": {"code": "INTERNAL", "message": "Submission failed. Please try again."}}
