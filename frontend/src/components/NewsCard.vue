<template>
  <article :class="['news-card', variant !== 'default' && `news-card--${variant}`]">
    <div class="card-meta">
      <span class="card-source">{{ article.source }}</span>
      <span v-if="pubDate" class="card-date">{{ pubDate }}</span>
    </div>
    <h3 class="card-title">{{ cleanTitle }}</h3>
    <p v-if="variant !== 'compact'" class="card-summary">{{ cleanSummary }}</p>
    <a
      v-if="article.url"
      :href="article.url"
      target="_blank"
      rel="noopener noreferrer"
      class="read-more"
    >
      Read more <ExternalLink :size="variant === 'compact' ? 11 : 13" />
    </a>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import { ExternalLink } from 'lucide-vue-next'
import { decodeHtml } from '../utils/text.js'

const props = defineProps({
  article: { type: Object, required: true },
  variant: { type: String, default: 'default' }, // 'default' | 'featured' | 'compact'
})

const cleanTitle   = computed(() => decodeHtml(props.article.title   ?? ''))
const cleanSummary = computed(() => decodeHtml(props.article.summary ?? ''))

const pubDate = computed(() => {
  if (!props.article.published) return ''
  const d = new Date(props.article.published)
  if (isNaN(d.getTime())) return ''
  return d.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' })
})
</script>

<style scoped>
/* ── Base card ─────────────────────────────────────────────── */
.news-card {
  background: #f8f7f5;
  border: 1px solid #e2e0dc;
  border-top: 3px solid var(--accent, #166534);
  border-radius: 10px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  height: 100%;
  box-sizing: border-box;
  transition: border-color 180ms ease-out, box-shadow 180ms ease-out, transform 180ms ease-out;
}
.news-card:hover {
  border-color: var(--accent, #166534);
  box-shadow: 0 4px 16px rgba(0,0,0,0.08), 0 0 0 1px rgba(34,85,176,0.1);
  transform: translateY(-2px);
}

/* Meta row */
.card-meta  { display: flex; align-items: center; gap: 8px; }
.card-source {
  font-family: 'DM Sans', sans-serif;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--accent, #166534);
  background: var(--accent-light, #dcfce7);
  padding: 3px 8px;
  border-radius: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 55%;
}
.card-date {
  font-family: 'DM Sans', sans-serif;
  font-size: 11px;
  color: #a8a69f;
  white-space: nowrap;
}

/* Title — 3-line clamp by default */
.card-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 14px;
  font-weight: 700;
  color: #1a1917;
  margin: 0;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Summary — 2-line clamp */
.card-summary {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  color: #65635d;
  margin: 0;
  line-height: 1.6;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Read more */
.read-more {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  font-weight: 700;
  color: var(--accent, #166534);
  text-decoration: none;
  margin-top: auto;
  padding-top: 10px;
  border-top: 1px solid #e2e0dc;
  transition: opacity 150ms, gap 150ms;
}
.read-more:hover { opacity: 0.75; gap: 7px; }

/* ── Featured variant ──────────────────────────────────────── */
.news-card--featured {
  background: #fff;
  border-top: none;
  border-left: 4px solid var(--accent, #166534);
  padding: 20px;
  gap: 12px;
}
.news-card--featured .card-title {
  font-size: 17px;
  -webkit-line-clamp: 4;
}
.news-card--featured .card-summary {
  -webkit-line-clamp: 3;
}

/* ── Compact variant ───────────────────────────────────────── */
.news-card--compact {
  padding: 12px 14px;
  gap: 7px;
  background: #faf9f7;
}
.news-card--compact .card-title {
  font-size: 13px;
  -webkit-line-clamp: 2;
}
.news-card--compact .read-more {
  font-size: 11px;
  padding-top: 8px;
}
</style>
