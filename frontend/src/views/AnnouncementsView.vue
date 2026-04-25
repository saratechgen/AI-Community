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
  padding: 0 0 20px;
  border-bottom: 1px solid #D9D5CD;
  margin-bottom: 28px;
}
.page-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 28px;
  font-weight: 700;
  color: #1F1F1B;
  margin: 0 0 6px;
  letter-spacing: -0.01em;
}
.page-subtitle {
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  color: #6E6A63;
  margin: 0;
}

.announcements-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.announcement-card {
  background: #ffffff;
  border: 1px solid #D9D5CD;
  border-radius: 12px;
  padding: 24px 28px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  box-shadow: 0 1px 4px rgba(31,31,27,0.05), 0 4px 16px rgba(31,31,27,0.04);
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
  color: #0E6B43;
  background: #DFF3E8;
  border-radius: 4px;
  padding: 3px 9px;
}
.card-platform {
  font-family: 'DM Sans', sans-serif;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: #857E76;
  background: #ECEAE3;
  border-radius: 4px;
  padding: 3px 9px;
}

.card-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: #1F1F1B;
  margin: 0;
  line-height: 1.35;
}

.card-desc {
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  color: #6E6A63;
  margin: 0;
  line-height: 1.7;
}

.card-cta {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  align-self: flex-start;
  padding: 9px 18px;
  background: #0E6B43;
  color: #f0fdf4;
  border-radius: 7px;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  transition: background 150ms, gap 150ms;
}
.card-cta:hover { background: #064022; gap: 9px; }

.card-footer {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  color: #A8A49D;
  padding-top: 10px;
  border-top: 1px solid #ECEAE3;
}
.footer-icon { color: #A8A49D; flex-shrink: 0; }

@media (max-width: 640px) {
  .announcements-view { padding: 20px; }
  .announcement-card  { padding: 20px; }
}
</style>
