# CONVENTIONS.md — AI Community Website

> Read this at the start of every session. These are the naming, structure, and pattern rules for this project.

---

## Project Structure

```
AI Community/
├── frontend/
│   ├── src/
│   │   ├── views/              # One file per route (page-level)
│   │   ├── components/         # Reusable UI components
│   │   ├── composables/        # Shared logic (useNews.js, etc.)
│   │   ├── router/
│   │   │   └── index.js        # Vue Router config
│   │   ├── assets/             # Static assets (fonts, icons)
│   │   ├── App.vue             # Root — sidebar + router-view
│   │   └── main.js             # Entry point
│   ├── public/
│   └── index.html
├── backend/
│   ├── app.py                  # FastAPI app, routes, middleware
│   ├── news_fetcher.py         # MCP news fetch logic
│   └── requirements.txt
├── CLAUDE.md
├── CONVENTIONS.md
└── PROJECT.md
```

---

## Naming Rules

### Files
| Type | Convention | Example |
|---|---|---|
| Vue views (pages) | PascalCase + `View` suffix | `NewsView.vue`, `AboutView.vue` |
| Vue components | PascalCase | `NewsCard.vue`, `SidebarNav.vue` |
| Composables | camelCase + `use` prefix | `useNews.js`, `useEvents.js` |
| Python modules | snake_case | `news_fetcher.py`, `app.py` |
| Python functions | snake_case | `fetch_news()`, `get_claude_articles()` |

### Routes (Vue Router)
| Section | Route |
|---|---|
| About Us | `/about` |
| Vision | `/vision` |
| AI Adoption Leaderboard | `/leaderboard` |
| Events | `/events` |
| AI News | `/news` |
| Announcements | `/announcements` |

Default redirect: `/` → `/news` (AI News is the landing section for pilot)

### API Endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Liveness check |
| GET | `/api/news` | Fetch all news categories |

All endpoints prefixed with `/api/`. No verbs in URLs.

---

## Component Rules

- Max **250 lines** per Vue SFC (template + script + style combined)
- Max **50 lines** per function
- Max **200 lines** per composable
- One responsibility per component — if you can't name it in one word, split it
- No inline styles — use CSS variables from the design system
- No modals — use slide-in panels if detail view is needed later

---

## Design System Rules

Import once in `main.js`:
```js
import './assets/design-tokens.css'
```

| Token | Value | Use for |
|---|---|---|
| Background | `#faf9f7` | Page background |
| Text primary | `#23221f` | Body copy |
| Accent | `#0f4024` | Active nav, badges, highlights |
| Border | `#e2e0dc` | Card borders, dividers |
| Font headings | Space Grotesk | Section titles, card titles |
| Font body | DM Sans | Summaries, labels, body text |

**Never use** `#000`, `#fff`, Tailwind, Bootstrap, or any component library theme.

---

## News Section Conventions

### Card Data Shape
```js
{
  id: String,
  title: String,
  summary: String,       // 2–3 sentences max displayed
  source: String,        // e.g. "MIT Technology Review"
  published: String,     // ISO date string
  category: String       // "claude" | "ai-agents" | "quick-tips"
}
```

### Category Labels (display)
| Internal key | Display label |
|---|---|
| `claude` | Claude News |
| `ai-agents` | AI Agents |
| `quick-tips` | Quick Tips |

### Fetch Strategy
1. `GET /api/news` on page load — no caching in pilot
2. Backend Layer 1: `get_news_by_category("ai")` — split results into claude / ai-agents
3. Backend Layer 2: `search_global_news("Claude Anthropic")` — only if claude results < 2
4. Backend Layer 3: `get_news_by_category("tech")` — for quick-tips

---

## Python Conventions

- Use `httpx` or `subprocess` to call the MCP server from FastAPI
- Return standardised response: `{ "data": [...], "meta": { "fetched_at": "..." } }`
- Never expose raw MCP JSON to the frontend — always transform first
- Log errors with a reference ID, never expose stack traces

---

## Git Conventions (when repo is initialised)

- Branch naming: `feature/section-name`, `fix/issue-description`
- Commit style: imperative present tense — "Add NewsCard component", "Fix sidebar collapse"
- Never commit `.env`, `node_modules/`, `venv/`, `__pycache__/`

---

## Content Sanitisation Rules (Mandatory)

Every piece of text that comes from an external feed (RSS, API, GDELT) **must** be cleaned before storage and again before display. No exceptions.

### Backend — `news_fetcher.py`
All text fields must pass through `_strip_html()` which:
1. Removes HTML tags via regex
2. Decodes HTML entities via `html.unescape()` (handles `&#8230;` → `…`, `&amp;` → `&`, etc.)

**Rule:** Never store raw RSS text. Always call `_strip_html()` on title, summary, and any other display field.

```python
# Correct
title = _strip_html(entry.get("title", ""))

# Wrong — never do this
title = entry.get("title", "")
```

### Frontend — `NewsCard.vue` and any future card component
All text from the API must pass through `decodeHtml()` from `src/utils/text.js` before rendering. This is the second line of defence — catches anything that survives the backend pass.

```js
// Correct
const cleanTitle = computed(() => decodeHtml(props.article.title))

// Wrong — never render raw feed text directly
<h3>{{ article.title }}</h3>
```

**`decodeHtml()`** uses the browser's `DOMParser` — handles every named and numeric HTML entity automatically. No manual replacement lists needed.

### When adding a new feed or data source
- Add `_strip_html()` to every new field in `_to_card()` or equivalent
- Add `decodeHtml()` to every new display field in the card component
- Test with a feed that uses smart quotes, em-dashes, and ellipsis characters

---

## What NOT to Do

- No static HTML files as pages
- No hardcoded news articles
- No Tailwind, Bootstrap, or third-party CSS frameworks
- No modals (use panels)
- No pure black `#000` or pure white `#fff`
- No glassmorphism, gradient text, glow borders
- No duplicating helpers — grep before creating a new one
- No appending to a file past its line cap — extract first
