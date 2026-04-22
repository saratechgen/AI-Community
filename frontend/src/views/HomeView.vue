<template>
  <div class="home-view">

    <!-- Hero -->
    <div class="hero-full">
      <HeroSection />
    </div>

    <!-- Quiz strip -->
    <div class="section-block">
      <LeaderboardPreview />
    </div>

    <!-- Latest AI News + Events -->
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

          <template v-else-if="featuredArticle">
            <div class="home-news-grid">
              <NewsCard :article="featuredArticle" variant="featured" />
              <div class="home-highlights">
                <a
                  v-for="h in highlights"
                  :key="h.key"
                  :href="h.article.url"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="highlight-row"
                >
                  <span class="hl-cat">{{ h.label }}</span>
                  <span class="hl-title">{{ decodeHtml(h.article.title) }}</span>
                  <span class="hl-meta">{{ h.article.source }}</span>
                </a>
              </div>
            </div>
          </template>
          <div v-else class="col-state">No news available yet.</div>

          <RouterLink to="/news" class="view-all">
            View all AI News <ArrowRight :size="13" />
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

import { useNews }    from '../composables/useNews.js'
import { decodeHtml } from '../utils/text.js'

const { news, loading: newsLoading, error: newsError, fetchNews } = useNews()
const lastRefreshed = ref(null)

const CATEGORY_LABEL = {
  claude:       'Claude & Anthropic',
  aiAgents:     'AI Agents',
  aiAtWork:     'AI at Work',
  advancements: 'New Advancements',
  quickTips:    'Quick Tips',
}

// Pick the most recently published article across all categories as the featured story
const featuredArticle = computed(() => {
  const all = Object.values(news.value).flat()
  if (!all.length) return null
  return [...all].sort((a, b) => new Date(b.published) - new Date(a.published))[0]
})

// 4 category highlights — one per category, skipping the featured article
const highlights = computed(() => {
  const featId = featuredArticle.value?.id
  return Object.entries(CATEGORY_LABEL)
    .map(([key, label]) => {
      const article = (news.value[key] ?? []).find(a => a.id !== featId)
      return article ? { key, label, article } : null
    })
    .filter(Boolean)
    .slice(0, 4)
})

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
.home-view     { padding: 12px 40px 40px; max-width: 1100px; }
.hero-full     { margin-bottom: 16px; }
.section-block { margin-bottom: 16px; }

/* Two-column: news + events */
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
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.col-header     { display: flex; flex-direction: column; gap: 3px; }
.col-title      { font-family: 'Space Grotesk', sans-serif; font-size: 15px; font-weight: 700; color: #1a1917; margin: 0; display: flex; align-items: center; gap: 7px; }
.col-icon       { color: #166534; }
.last-refreshed { font-family: 'DM Sans', sans-serif; font-size: 11px; color: #a8a69f; }

/* Featured + highlights grid */
.home-news-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  align-items: start;
}
.home-highlights { display: flex; flex-direction: column; }

/* Category highlight rows */
.highlight-row {
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding: 10px 0;
  border-bottom: 1px solid #f0efe9;
  text-decoration: none;
  transition: padding-left 150ms;
}
.highlight-row:last-child { border-bottom: none; }
.highlight-row:hover      { padding-left: 4px; }
.highlight-row:hover .hl-title { color: #166534; }
.hl-cat {
  font-family: 'DM Sans', sans-serif;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #166534;
}
.hl-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 12px;
  font-weight: 600;
  color: #1a1917;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  transition: color 150ms;
}
.hl-meta { font-family: 'DM Sans', sans-serif; font-size: 11px; color: #a8a69f; }

.col-state  { font-family: 'DM Sans', sans-serif; font-size: 13px; color: #85837c; padding: 20px 0; }
.col-error  { color: #d64545; }
.view-all   { display: inline-flex; align-items: center; gap: 4px; font-family: 'DM Sans', sans-serif; font-size: 12px; font-weight: 600; color: #166534; text-decoration: none; transition: gap 150ms; }
.view-all:hover { gap: 8px; }

/* Responsive */
@media (max-width: 1000px) {
  .two-col        { grid-template-columns: 1fr; }
  .home-news-grid { grid-template-columns: 1fr; }
}
@media (max-width: 640px) {
  .home-view     { padding: 20px 18px 36px; }
  .section-block { margin-bottom: 28px; }
}
</style>
