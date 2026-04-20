<template>
  <div class="about-view">

    <header class="page-header">
      <h1 class="page-title">About Us</h1>
      <p class="page-subtitle">Meet the team behind DEWA's AI Adoption journey.</p>
    </header>

    <div class="about-card">

      <p class="section-body">
        We are the AI Adoption team focused on helping the organisation use artificial intelligence
        in practical, secure, and impactful ways. We support teams in identifying the right use cases,
        simplifying workflows, improving productivity, and turning AI ideas into real business value.
      </p>
      <p class="section-body">
        Our role is to make AI easy to understand, easy to adopt, and useful across the organisation.
        We work closely with business teams to drive awareness, enable experimentation, and support
        responsible AI usage.
      </p>
      <div class="focus-chips">
        <span class="chip">Right Use Cases</span>
        <span class="chip">Simplified Workflows</span>
        <span class="chip">Productivity</span>
        <span class="chip">Business Value</span>
        <span class="chip">Awareness</span>
        <span class="chip">Experimentation</span>
        <span class="chip">Responsible AI</span>
      </div>

    </div>

    <!-- Contact -->
    <div class="contact-block">
      <div class="contact-row">
        <MapPin :size="14" class="contact-icon" />
        <div class="contact-text">
          <span class="contact-name">AI Adoption Department</span>
          <span class="contact-address">8th Al Shera'a Building · Dubai</span>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { MapPin } from 'lucide-vue-next'
</script>

<style scoped>
.about-view {
  padding: 16px 28px 28px;
  max-width: 780px;
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

/* ── Main card ───────────────────────────────────────────────── */
.about-card {
  background: #ffffff;
  border: 1px solid #e2e0dc;
  border-top: 3px solid #166534;
  border-radius: 10px;
  padding: 24px 28px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-bottom: 16px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}

.section-body {
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  color: #3a3834;
  margin: 0;
  line-height: 1.75;
}

/* ── Focus chips ─────────────────────────────────────────────── */
.focus-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.chip {
  font-family: 'DM Sans', sans-serif;
  font-size: 11px;
  font-weight: 600;
  color: #166534;
  background: #dcfce7;
  border-radius: 4px;
  padding: 3px 10px;
}

/* ── Contact ─────────────────────────────────────────────────── */
.contact-block {
  background: #f8f7f5;
  border: 1px solid #e2e0dc;
  border-radius: 10px;
  padding: 14px 20px;
  display: inline-flex;
  align-items: center;
}
.contact-row {
  display: flex;
  align-items: center;
  gap: 10px;
}
.contact-icon { color: #166534; flex-shrink: 0; }
.contact-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.contact-name {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 700;
  color: #1a1917;
}
.contact-address {
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  color: #65635d;
}

@media (max-width: 640px) {
  .about-view  { padding: 16px; }
  .about-card  { padding: 20px; }
}
</style>
