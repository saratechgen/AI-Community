<template>
  <div class="announcements-view">
    <header class="page-header">
      <h1 class="page-title">Announcements</h1>
      <p class="page-subtitle">Updates and resources from the AI Adoption Department.</p>
    </header>

    <div class="announcements-list">

      <div class="announcement-card">
        <div class="card-top">
          <span class="card-tag">Featured Course</span>
          <span class="card-platform">Udemy</span>
        </div>

        <h2 class="card-title">AI Coder: Vibe Coder to Agentic Engineer in 3 Weeks</h2>

        <p class="card-desc">
          The Complete Course on Coding Agents — Claude Code, Copilot, Codex, Cursor, Antigravity.
          Covering Skills, MCP, Plugins, and Subagents.
        </p>

        <a
          href="https://www.udemy.com/course/ai-coder-from-vibe-coder-to-agentic-engineer"
          target="_blank"
          rel="noopener noreferrer"
          class="card-cta"
        >
          Check out on Udemy <ExternalLink :size="13" />
        </a>

        <div class="card-footer">
          <Info :size="13" class="footer-icon" />
          For any queries, reach out to the AI Adoption Department.
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ExternalLink, Info } from 'lucide-vue-next'
</script>

<style scoped>
.announcements-view {
  padding: 32px 40px;
  max-width: 780px;
}

.page-header {
  border-left: 4px solid #166534;
  border-bottom: 1px solid #e2e0dc;
  border-radius: 0 6px 0 0;
  background: #f8f7f5;
  padding: 14px 18px;
  margin-bottom: 28px;
}
.page-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 22px;
  font-weight: 700;
  color: #1a1917;
  margin: 0 0 4px;
}
.page-subtitle {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 500;
  color: #3a3834;
  text-shadow: 0 1px 0 rgba(255,255,255,0.85);
  margin: 0;
}

.announcements-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.announcement-card {
  background: #ffffff;
  border: 1px solid #e2e0dc;
  border-top: 3px solid #166534;
  border-radius: 10px;
  padding: 24px 28px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}

.card-top {
  display: flex;
  align-items: center;
  gap: 8px;
}
.card-tag {
  font-family: 'DM Sans', sans-serif;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: #166534;
  background: #dcfce7;
  border-radius: 4px;
  padding: 3px 9px;
}
.card-platform {
  font-family: 'DM Sans', sans-serif;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: #85837c;
  background: #f0efe9;
  border-radius: 4px;
  padding: 3px 9px;
}

.card-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: #1a1917;
  margin: 0;
  line-height: 1.35;
}

.card-desc {
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  color: #65635d;
  margin: 0;
  line-height: 1.7;
}

.card-cta {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  align-self: flex-start;
  padding: 9px 18px;
  background: #166534;
  color: #f0fdf4;
  border-radius: 7px;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  transition: background 150ms, gap 150ms;
}
.card-cta:hover { background: #0a2e1a; gap: 9px; }

.card-footer {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  color: #a8a69f;
  padding-top: 10px;
  border-top: 1px solid #f0efe9;
}
.footer-icon { color: #a8a69f; flex-shrink: 0; }

@media (max-width: 640px) {
  .announcements-view { padding: 20px; }
  .announcement-card  { padding: 20px; }
}
</style>
