"""
News fetcher — RSS feeds, categorised into 5 buckets.
Five categories:
  claude       → Claude & Anthropic news
  ai-agents    → Agentic AI, autonomous systems
  ai-at-work   → GitHub Copilot, enterprise AI, extensions, tools
  advancements → New models, research breakthroughs, open-source AI
  quick-tips   → Practical how-tos, guides, productivity
"""

import asyncio
import hashlib
import html
import re
from datetime import datetime, timezone

import feedparser
import httpx

# ── Feed catalogue (per category) ────────────────────────────────────────────

# Official AI company blogs — fetched first; highest priority in bucket filling.
# If a URL returns an error, _fetch_feed() returns [] silently — no disruption.
OFFICIAL_FEEDS = [
    {"name": "Anthropic",       "url": "https://www.anthropic.com/rss.xml"},
    {"name": "OpenAI",          "url": "https://openai.com/news/rss.xml"},
    {"name": "Google DeepMind", "url": "https://deepmind.google/blog/rss.xml"},
    {"name": "Meta AI",         "url": "https://ai.meta.com/blog/feed/"},
]

GENERAL_AI_FEEDS = [
    {"name": "MIT Technology Review AI", "url": "https://www.technologyreview.com/feed/"},
    {"name": "VentureBeat AI",           "url": "https://venturebeat.com/ai/feed/"},
    {"name": "TechCrunch AI",            "url": "https://techcrunch.com/tag/artificial-intelligence/feed/"},
    {"name": "IEEE Spectrum AI",         "url": "https://spectrum.ieee.org/feeds/topic/artificial-intelligence.rss"},
    {"name": "The Gradient",             "url": "https://thegradient.pub/rss/"},
    {"name": "Google AI Blog",           "url": "https://blog.google/innovation-and-ai/technology/ai/rss/"},
]

WORK_FEEDS = [
    {"name": "GitHub Blog",           "url": "https://github.blog/feed/"},
    {"name": "Microsoft AI Blog",     "url": "https://blogs.microsoft.com/ai/feed/"},
    {"name": "Dev.to AI",             "url": "https://dev.to/feed/tag/ai"},
    {"name": "The Verge",             "url": "https://www.theverge.com/rss/index.xml"},
]

ADVANCEMENT_FEEDS = [
    {"name": "Hugging Face Blog", "url": "https://huggingface.co/blog/feed.xml"},
    {"name": "Wired",             "url": "https://www.wired.com/feed/rss"},
    {"name": "Ars Technica",      "url": "https://feeds.arstechnica.com/arstechnica/index"},
]

TIPS_FEEDS = [
    {"name": "Dev.to AI",         "url": "https://dev.to/feed/tag/ai"},
    {"name": "Wired",             "url": "https://www.wired.com/feed/rss"},
    {"name": "Ars Technica",      "url": "https://feeds.arstechnica.com/arstechnica/index"},
]

# ── Keywords per category ─────────────────────────────────────────────────────

CLAUDE_KEYWORDS = [
    "claude", "anthropic", "claude 3", "claude 4",
    "claude sonnet", "claude opus", "claude code",
]

AGENTS_KEYWORDS = [
    "ai agent", "agentic", "multi-agent", "autonomous ai",
    "agent framework", "crewai", "autogen", "langgraph",
    "agent workflow", "agent orchestration", "ai workflow",
]

WORK_KEYWORDS = [
    "github copilot", "copilot", "cursor", "windsurf", "tabnine",
    "codewhisperer", "ai adoption", "enterprise ai",
    "vscode", "vs code", "jetbrains", "ai plugin", "ai extension",
    "workplace ai", "ai productivity", "microsoft copilot",
    "gemini workspace", "chatgpt enterprise", "ai pair",
    "developer tool", "coding assistant", "ai code",
]

ADVANCEMENT_KEYWORDS = [
    "gpt-4", "gpt-5", "gpt-o", "gemini", "llama", "mistral",
    "new model", "model release", "open source model",
    "foundation model", "ai research", "benchmark",
    "breakthrough", "multimodal", "reasoning model",
    "deepseek", "qwen", "phi-", "grok", "new ai",
    "hugging face", "model launch", "open-source ai",
    "state-of-the-art", "sota",
    "openai", "deepmind", "meta ai", "llm",
]

TIPS_KEYWORDS = [
    "how to", "tip", "tutorial", "guide", "best practice",
    "trick", "step by step", "cheat sheet", "getting started",
    "prompt engineering", "prompting", "workflow", "learn ai",
    "beginner", "quick start", "productivity hack",
]

# Source name → default category bucket for official feeds.
# Only applies when no keyword rule matches — keyword rules always take priority.
OFFICIAL_SOURCE_CATEGORY: dict[str, str] = {
    "Anthropic":       "claude",
    "OpenAI":          "advancements",
    "Google DeepMind": "advancements",
    "Meta AI":         "advancements",
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def _strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text or "")
    return html.unescape(text).strip()

def _truncate(text: str, chars: int = 280) -> str:
    text = _strip_html(text)
    return text[:chars].rsplit(" ", 1)[0] + "…" if len(text) > chars else text

def _article_id(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()[:10]

def _parse_date(entry) -> str:
    for field in ("published", "updated"):
        raw = getattr(entry, field, None)
        if raw:
            return raw
    return datetime.now(timezone.utc).isoformat()

def _matches(text: str, keywords: list[str]) -> bool:
    lower = text.lower()
    return any(kw in lower for kw in keywords)

def _to_card(entry: dict, source: str, category: str) -> dict:
    title   = _strip_html(entry.get("title", ""))
    summary = _truncate(entry.get("summary", entry.get("description", "")), chars=380)
    url     = entry.get("link", "")
    return {
        "id":        _article_id(url or title),
        "title":     title,
        "summary":   summary,
        "source":    source,
        "url":       url,
        "published": _parse_date(entry),
        "category":  category,
    }

# ── Feed fetcher ──────────────────────────────────────────────────────────────

async def _fetch_feed(client: httpx.AsyncClient, feed: dict) -> list[dict]:
    try:
        resp   = await client.get(feed["url"], timeout=8)
        parsed = feedparser.parse(resp.text)
        items  = []
        for e in parsed.entries[:8]:
            entry = dict(e)
            # feedparser stores link as attribute — extract explicitly
            entry["link"] = e.get("link") or e.get("id") or ""
            items.append({"entry": entry, "source": feed["name"]})
        return items
    except Exception:
        return []

async def _fetch_feeds(client: httpx.AsyncClient, feeds: list[dict]) -> list[dict]:
    results = await asyncio.gather(*[_fetch_feed(client, f) for f in feeds])
    return [item for feed_items in results for item in feed_items]

# ── Category classifier ───────────────────────────────────────────────────────

def _classify(item: dict) -> str | None:
    e    = item["entry"]
    text = (e.get("title", "") + " " + e.get("summary", "")).lower()

    if _matches(text, CLAUDE_KEYWORDS):      return "claude"
    if _matches(text, AGENTS_KEYWORDS):      return "ai-agents"
    if _matches(text, WORK_KEYWORDS):        return "ai-at-work"
    if _matches(text, ADVANCEMENT_KEYWORDS): return "advancements"
    if _matches(text, TIPS_KEYWORDS):        return "quick-tips"
    # Official sources that matched no keyword fall back to their default bucket
    return OFFICIAL_SOURCE_CATEGORY.get(item["source"])

def _fill_bucket(
    bucket: list,
    items: list[dict],
    category: str,
    seen_ids: set,
    limit: int = 3,
) -> None:
    """Fill bucket from items list up to limit, skipping seen IDs."""
    for item in items:
        if len(bucket) >= limit:
            break
        e   = item["entry"]
        aid = _article_id(e.get("link", e.get("title", "")))
        if aid in seen_ids:
            continue
        seen_ids.add(aid)
        bucket.append(_to_card(e, item["source"], category))

# ── Main fetch ────────────────────────────────────────────────────────────────

async def fetch_all_news() -> dict:
    buckets: dict[str, list] = {
        "claude":       [],
        "ai-agents":    [],
        "ai-at-work":   [],
        "advancements": [],
        "quick-tips":   [],
    }

    async with httpx.AsyncClient(follow_redirects=True) as client:

        # Fetch all feed groups in parallel — official feeds prepended so they
        # get first pick of category slots before general sources
        official_items, ai_items, work_items, adv_items, tips_items = await asyncio.gather(
            _fetch_feeds(client, OFFICIAL_FEEDS),
            _fetch_feeds(client, GENERAL_AI_FEEDS),
            _fetch_feeds(client, WORK_FEEDS),
            _fetch_feeds(client, ADVANCEMENT_FEEDS),
            _fetch_feeds(client, TIPS_FEEDS),
        )

        all_items = official_items + ai_items + work_items + adv_items + tips_items
        seen_ids: set[str] = set()

        # Pass 1 — classify every article by keyword
        for item in all_items:
            e   = item["entry"]
            aid = _article_id(e.get("link", e.get("title", "")))
            if aid in seen_ids:
                continue

            category = _classify(item)
            if category and len(buckets[category]) < 3:
                seen_ids.add(aid)
                buckets[category].append(_to_card(e, item["source"], category))

        # Pass 2 — fill gaps from targeted feed pools (no keyword required)
        if len(buckets["ai-at-work"]) < 4:
            _fill_bucket(buckets["ai-at-work"], work_items, "ai-at-work", seen_ids)

        if len(buckets["advancements"]) < 4:
            _fill_bucket(buckets["advancements"], adv_items, "advancements", seen_ids)

        if len(buckets["quick-tips"]) < 4:
            _fill_bucket(buckets["quick-tips"], tips_items, "quick-tips", seen_ids)

        # Pass 3 — any remaining empties filled from general pool
        for category in ["claude", "ai-agents"]:
            if len(buckets[category]) < 4:
                _fill_bucket(buckets[category], ai_items, category, seen_ids)

    return {
        "claude":       buckets["claude"][:3],
        "aiAgents":     buckets["ai-agents"][:3],
        "aiAtWork":     buckets["ai-at-work"][:3],
        "advancements": buckets["advancements"][:3],
        "quickTips":    buckets["quick-tips"][:3],
    }
