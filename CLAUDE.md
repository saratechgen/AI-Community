# AI Community Website — Project Instructions

## Collaboration Rules (Non-negotiable)

### Step-by-Step Approval
Before every implementation step:
1. Brief the user on **what** the next action is
2. Explain **why** it is needed
3. Wait for **explicit approval** before proceeding

No exceptions — not for small steps, not for obvious steps. One step at a time.

### Memory
Project memory lives at:
`~/.claude/projects/C--Users-DELL-Documents-AI-Community/memory/`

Read `MEMORY.md` index at the start of every session to restore full context.

---

## Project Overview

**AI Community Website** — A hub for AI professionals built with the DAK stack.

### Sections
| Route | Section | Status |
|---|---|---|
| /about | About Us | Placeholder |
| /vision | Vision | Placeholder |
| /leaderboard | AI Adoption Leaderboard | Placeholder |
| /events | Events | Placeholder |
| /news | AI News | Pilot — building first |
| /announcements | Announcements | Placeholder |

### Current Pilot
Building the **AI News** section first:
- Claude News (4 cards)
- AI Agents News (4 cards)
- Quick Tips (4 cards)

News refreshes **on page load only** for the pilot.

---

## Tech Stack (DAK Standard)
- **Frontend:** Vue 3 + Vite + Vue Router
- **Styling:** EZ Design System (`~/design-system/index.css`)
- **Backend:** FastAPI + Python
- **News Data:** `news-aggregator-mcp-server` (already configured, no API key needed)

## Guides to Read Before Coding
| Guide | Location |
|---|---|
| Tech stack | `~/.claude/stack.md` |
| Design system | `~/design-system/guide.md` |
| API patterns | `~/.claude/api-patterns.md` |
| Project template | `~/.claude/project-management-template.md` |
| Conventions template | `~/.claude/conventions-template.md` |

---

## Content Sanitisation — Non-Negotiable Rule

Every text field from an external feed must be cleaned at TWO layers:

1. **Backend (`news_fetcher.py`):** All fields pass through `_strip_html()` — strips tags + `html.unescape()` decodes entities
2. **Frontend (`NewsCard.vue` and any future card):** All fields pass through `decodeHtml()` from `src/utils/text.js`

Never render raw feed text. Never store uncleaned text. See `CONVENTIONS.md § Content Sanitisation Rules` for full detail.

---

## News Fetch Strategy
- **Layer 1:** `get_news_by_category("ai")` — covers Claude + AI Agents
- **Layer 2:** `search_global_news("Claude Anthropic")` — fallback only if <2 Claude articles found in Layer 1
- **Quick Tips:** `get_news_by_category("tech")` filtered for practical/tips content
