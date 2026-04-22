"""
External events fetcher — RSS (feedparser) and confs.tech JSON support.
Add entries to EXTERNAL_FEEDS to include new sources; remove to disable.
"""
import asyncio
import hashlib
import logging
import time
from datetime import date
from typing import Optional

import feedparser
import httpx

log = logging.getLogger("events_fetcher")

# ── Feed registry ─────────────────────────────────────────────────────────────
# kind "rss"            → feedparser (RSS 2.0 / Atom)
# kind "confs_tech_json" → confs.tech open GitHub dataset

EXTERNAL_FEEDS: list[dict] = [
    {
        "kind":   "confs_tech_json",
        "url":    "https://raw.githubusercontent.com/tech-conferences/conference-data/main/conferences/2026/data.json",
        "source": "confs.tech",
    },
    # Add RSS feeds here — example:
    # { "kind": "rss", "url": "https://...", "source": "Source Name" },
]

_CACHE: dict = {"events": [], "fetched_at": 0.0}
CACHE_TTL    = 3600  # 1 hour


# ── Shared helpers ────────────────────────────────────────────────────────────

def _stable_id(url: str, title: str) -> str:
    return hashlib.md5(f"{url}|{title}".encode()).hexdigest()[:12]


def _classify(title: str, summary: str = "") -> str:
    text = (title + " " + summary).lower()
    for keywords, kind in [
        (["conference", "summit", "symposium"], "conference"),
        (["workshop", "bootcamp", "training"],  "workshop"),
        (["webinar", "virtual"],                "webinar"),
        (["meetup", "meet-up"],                 "meetup"),
        (["hackathon"],                         "hackathon"),
    ]:
        if any(k in text for k in keywords):
            return kind
    return "conference"


# ── RSS normalisation ─────────────────────────────────────────────────────────

def _rss_date(entry) -> Optional[str]:
    for field in ("published_parsed", "updated_parsed"):
        t = entry.get(field)
        if t:
            try:
                return date(*t[:3]).isoformat()
            except Exception:
                pass
    return None


def _normalise_rss(entry, source: str) -> Optional[dict]:
    title = (entry.get("title") or "").strip()
    url   = (entry.get("link")  or "").strip()
    if not title or not url:
        return None
    event_date = _rss_date(entry)
    if not event_date:
        return None
    return {
        "id":        _stable_id(url, title),
        "title":     title,
        "date":      event_date,
        "endDate":   None,
        "time":      "",
        "location":  entry.get("location") or "",
        "country":   "",
        "organizer": source,
        "url":       url,
        "type":      _classify(title, entry.get("summary") or ""),
        "source":    source,
    }


async def _fetch_rss(client: httpx.AsyncClient, cfg: dict) -> list[dict]:
    try:
        resp   = await client.get(cfg["url"], timeout=10.0)
        resp.raise_for_status()
        loop   = asyncio.get_event_loop()
        parsed = await loop.run_in_executor(None, feedparser.parse, resp.text)
        valid  = [e for e in (_normalise_rss(entry, cfg["source"]) for entry in parsed.entries) if e]
        log.info(f"rss source={cfg['source']} entries={len(parsed.entries)} valid={len(valid)}")
        return valid
    except Exception as exc:
        log.warning(f"rss source={cfg['source']} error={exc}")
        return []


# ── confs.tech JSON normalisation ─────────────────────────────────────────────

def _normalise_confs_tech(raw: dict, source: str) -> Optional[dict]:
    name  = (raw.get("name") or "").strip()
    start = (raw.get("startDate") or "").strip()
    if not name or not start:
        return None
    url = (raw.get("url") or "").strip()
    loc = ", ".join(filter(None, [raw.get("city") or "", raw.get("country") or ""]))
    return {
        "id":        _stable_id(url or name, name),
        "title":     name,
        "date":      start,
        "endDate":   raw.get("endDate") or None,
        "time":      "",
        "location":  loc,
        "country":   (raw.get("country") or "").strip(),
        "organizer": source,
        "url":       url,
        "type":      "conference",
        "source":    source,
    }


async def _fetch_confs_tech(client: httpx.AsyncClient, cfg: dict) -> list[dict]:
    try:
        resp    = await client.get(cfg["url"], timeout=10.0)
        resp.raise_for_status()
        entries = resp.json()
        if not isinstance(entries, list):
            entries = entries.get("conferences", [])
        valid = [e for e in (_normalise_confs_tech(raw, cfg["source"]) for raw in entries) if e]
        log.info(f"confs.tech entries={len(entries)} valid={len(valid)}")
        return valid
    except Exception as exc:
        log.warning(f"confs.tech error={exc}")
        return []


# ── Dispatch ──────────────────────────────────────────────────────────────────

async def _fetch_one(client: httpx.AsyncClient, cfg: dict) -> list[dict]:
    if cfg["kind"] == "rss":
        return await _fetch_rss(client, cfg)
    if cfg["kind"] == "confs_tech_json":
        return await _fetch_confs_tech(client, cfg)
    log.warning(f"unknown feed kind={cfg['kind']}")
    return []


def _filter_sort_dedup(events: list[dict]) -> list[dict]:
    today = date.today().isoformat()
    seen, out = set(), []
    for e in sorted(events, key=lambda x: x["date"]):
        if e["date"] >= today and e["id"] not in seen:
            seen.add(e["id"])
            out.append(e)
    return out


async def fetch_external_events() -> list[dict]:
    """Return filtered, sorted, deduplicated external events. Cached for 1 hour."""
    if time.time() - _CACHE["fetched_at"] < CACHE_TTL:
        return _CACHE["events"]

    async with httpx.AsyncClient(
        follow_redirects=True,
        headers={"User-Agent": "AI-Community-Hub/1.0"},
    ) as client:
        results = await asyncio.gather(
            *[_fetch_one(client, cfg) for cfg in EXTERNAL_FEEDS],
            return_exceptions=True,
        )

    all_events = [e for r in results if isinstance(r, list) for e in r]
    filtered   = _filter_sort_dedup(all_events)
    _CACHE.update({"events": filtered, "fetched_at": time.time()})
    log.info(f"events_cache refreshed total={len(filtered)}")
    return filtered
