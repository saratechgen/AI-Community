<template>
  <div class="leaders-view">

    <header class="page-header">
      <h1 class="page-title">Leader's Message</h1>
      <p class="page-subtitle">Perspectives from DEWA leadership on our AI journey.</p>
    </header>

    <div class="messages-grid">

      <!-- CAIO Message -->
      <div class="message-card">
        <div class="card-label">Chief Artificial Intelligence Office</div>
        <div class="card-body">
          <Quote :size="24" class="quote-icon" />
          <div class="message-text">
            <p>DEWA is on a clear path to become the world's first AI utility. Every decision, initiative, and investment points toward that goal. I encourage every employee to engage, keep learning, and be part of this transformation — for Dubai and for the world.</p>
          </div>
        </div>
        <div class="card-author">
          <div class="author-avatar"><UserCircle :size="20" /></div>
          <div class="author-info">
            <span class="author-name">Chief Artificial Intelligence Officer</span>
            <span class="author-org">DEWA — Dubai Electricity and Water Authority</span>
          </div>
        </div>
      </div>

      <!-- AI Adoption Dept Message -->
      <div class="message-card">
        <div class="card-label">AI Adoption Department Office</div>
        <div class="card-body">
          <Quote :size="24" class="quote-icon" />
          <div class="message-text">
            <p>Our purpose is simple — ensure every DEWA employee has the knowledge and support to make AI work for them. Through training, daily learning, and community initiatives, we are building a culture where AI becomes second nature. Explore, participate, and reach out. We are here.</p>
          </div>
        </div>
        <div class="card-author">
          <div class="author-avatar"><UserCircle :size="20" /></div>
          <div class="author-info">
            <span class="author-name">AI Adoption Department Head</span>
            <span class="author-org">DEWA — Dubai Electricity and Water Authority</span>
          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { Quote, UserCircle } from 'lucide-vue-next'
</script>

<style scoped>
.leaders-view {
  padding: 16px 28px 28px;
  max-width: 1100px;
}

/* ── Header ─────────────────────────────────────────────────── */
.page-header {
  border-left: 4px solid #166534;
  border-bottom: 1px solid #e2e0dc;
  border-radius: 0 6px 0 0;
  background: #f8f7f5;
  padding: 12px 16px;
  margin-bottom: 16px;
}
.page-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 20px;
  font-weight: 700;
  color: #1a1917;
  margin: 0 0 3px;
}
.page-subtitle {
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  color: #65635d;
  margin: 0;
}

/* ── Grid ───────────────────────────────────────────────────── */
.messages-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  align-items: stretch;
}

/* ── Card ───────────────────────────────────────────────────── */
.message-card {
  background: #ffffff;
  border: 1px solid #e2e0dc;
  border-top: 3px solid #166534;
  border-radius: 10px;
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}

.card-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #166534;
}

.card-body {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  flex: 1;
}
.quote-icon {
  color: #dcfce7;
  flex-shrink: 0;
  margin-top: 2px;
}

.message-text p {
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  color: #3a3834;
  margin: 0;
  line-height: 1.7;
}

/* ── Author ─────────────────────────────────────────────────── */
.card-author {
  display: flex;
  align-items: center;
  gap: 10px;
  padding-top: 12px;
  border-top: 1px solid #f0efe9;
}
.author-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #dcfce7;
  color: #166534;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.author-info {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.author-name {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 12px;
  font-weight: 700;
  color: #1a1917;
}
.author-org {
  font-family: 'DM Sans', sans-serif;
  font-size: 11px;
  color: #a8a69f;
}

@media (max-width: 860px) {
  .messages-grid { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
  .leaders-view { padding: 16px; }
  .message-card { padding: 16px; }
  .card-body    { flex-direction: column; gap: 8px; }
}
</style>
