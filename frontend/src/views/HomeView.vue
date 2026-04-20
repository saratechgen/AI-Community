<template>
  <div class="home-view">

    <!-- 1. Full-width hero -->
    <div class="hero-full">
      <HeroSection />
    </div>

    <!-- 2. Daily Quiz strip -->
    <div class="section-block">
      <LeaderboardPreview />
    </div>

    <!-- 4. Latest AI News + Upcoming Events -->
    <div class="section-block">
      <div class="two-col">
        <div class="news-col">
          <div class="col-header">
            <h2 class="col-title">
              <Newspaper :size="16" class="col-icon" />
              Latest AI News
            </h2>
            <span v-if="lastRefreshedLabel" class="last-refreshed">Last refreshed · {{ lastRefreshedLabel }}</span>
          </div>
          <div v-if="newsLoading" class="col-state">Loading news…</div>
          <div v-else-if="newsError" class="col-state col-error">{{ newsError }}</div>
          <div v-else class="news-stack">
            <NewsCard
              v-for="article in topNews"
              :key="article.id"
              :article="article"
            />
          </div>
          <RouterLink to="/news" class="view-all">
            View all news <ArrowRight :size="13" />
          </RouterLink>
        </div>

        <div class="events-col">
          <EventsList />
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { Newspaper, ArrowRight } from 'lucide-vue-next'

import HeroSection        from '../components/HeroSection.vue'
import NewsCard           from '../components/NewsCard.vue'
import EventsList         from '../components/EventsList.vue'
import LeaderboardPreview from '../components/LeaderboardPreview.vue'

import { useNews } from '../composables/useNews.js'

const { news, loading: newsLoading, error: newsError, fetchNews } = useNews()
const lastRefreshed = ref(null)

const topNews = computed(() => [
  ...(news.value.aiAtWork     ?.slice(0, 1) ?? []),
  ...(news.value.advancements ?.slice(0, 1) ?? []),
  ...(news.value.claude       ?.slice(0, 1) ?? []),
])

const lastRefreshedLabel = computed(() => {
  if (!lastRefreshed.value) return ''
  const d = lastRefreshed.value
  const date = d.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
  const time = d.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })
  return `${date} · ${time}`
})

fetchNews().then(() => { lastRefreshed.value = new Date() }).catch(() => {})
</script>

<style scoped>
.home-view {
  padding: 12px 40px 40px;
  max-width: 1100px;
}

/* ── Hero — full width ──────────────────────────────────────── */
.hero-full { margin-bottom: 16px; }

/* ── Section rhythm ─────────────────────────────────────────── */
.section-block { margin-bottom: 16px; }

/* ── Two-column: news + events ──────────────────────────────── */
.two-col {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 16px;
  align-items: start;
}
.news-col {
  background: #ffffff;
  border: 1px solid #e2e0dc;
  border-top: 3px solid var(--accent, #166534);
  border-radius: 10px;
  padding: 18px 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 4px 12px rgba(0,0,0,0.04);
  display: flex;
  flex-direction: column;
}
.col-header { margin-bottom: 14px; display: flex; flex-direction: column; gap: 3px; }
.last-refreshed { font-family: 'DM Sans', sans-serif; font-size: 11px; color: #a8a69f; }
.col-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 15px;
  font-weight: 700;
  color: #1a1917;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 7px;
}
.col-icon { color: #166534; }
.news-stack {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 12px;
  flex: 1;
}
.col-state {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  color: #85837c;
  padding: 20px 0;
}
.col-error { color: #d64545; }
.view-all {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  font-weight: 600;
  color: #166534;
  text-decoration: none;
  transition: gap 150ms;
}
.view-all:hover { gap: 8px; }

/* ── Responsive ─────────────────────────────────────────────── */
@media (max-width: 1000px) {
  .two-col { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
  .home-view     { padding: 20px 18px 36px; }
  .section-block { margin-bottom: 28px; }
}
</style>
