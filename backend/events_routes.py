"""Events API routes."""
import logging
from datetime import datetime, timezone

from fastapi import APIRouter
from events_fetcher import fetch_external_events
from dubai_events_db import get_upcoming_dubai_events

log    = logging.getLogger("events_routes")
router = APIRouter(prefix="/api/events")


@router.get("/external")
async def get_external_events():
    try:
        events = await fetch_external_events()
        return {
            "data": {"events": events, "total": len(events)},
            "meta": {"fetched_at": datetime.now(timezone.utc).isoformat()},
        }
    except Exception as exc:
        log.error(f"get_external_events failed: {exc}")
        return {"error": {"code": "INTERNAL", "message": "Could not retrieve events."}}


@router.get("/dubai")
async def get_dubai_events():
    try:
        events = await get_upcoming_dubai_events()
        return {"data": {"events": events, "total": len(events)}}
    except Exception as exc:
        log.error(f"get_dubai_events failed: {exc}")
        return {"error": {"code": "INTERNAL", "message": "Could not retrieve Dubai events."}}
