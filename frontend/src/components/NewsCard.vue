<template>
  <article class="news-card">
    <div class="card-meta">
      <span class="card-source">{{ article.source }}</span>
    </div>

    <h3 class="card-title">{{ cleanTitle }}</h3>

    <p class="card-summary">{{ cleanSummary }}</p>

    <a
      v-if="article.url"
      :href="article.url"
      target="_blank"
      rel="noopener noreferrer"
      class="read-more"
    >
      Read more
      <ExternalLink :size="13" />
    </a>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import { ExternalLink } from 'lucide-vue-next'
import { decodeHtml } from '../utils/text.js'

const props = defineProps({
  article: { type: Object, required: true },
})

const cleanTitle   = computed(() => decodeHtml(props.article.title))
const cleanSummary = computed(() => decodeHtml(props.article.summary))

</script>

<style scoped>
.news-card {
  background: #f8f7f5;
  border: 1px solid #e2e0dc;
  border-top: 3px solid var(--accent, #166534);
  border-radius: 10px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  height: 100%;
  box-sizing: border-box;
  box-shadow:
    0 1px 3px rgba(0,0,0,0.06),
    0 4px 12px rgba(0,0,0,0.07),
    0 8px 24px rgba(0,0,0,0.05);
  transition:
    border-color 180ms ease-out,
    box-shadow   180ms ease-out,
    transform    180ms ease-out;
}
.news-card:hover {
  border-color: var(--accent, #166534);
  box-shadow:
    0 2px 6px rgba(0,0,0,0.08),
    0 8px 24px rgba(0,0,0,0.1),
    0 0 0 1px rgba(15,64,36,0.15);
  transform: translateY(-3px);
}

/* Meta */
.card-meta {
  display: flex;
  align-items: center;
}
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
  max-width: 60%;
}
/* Title */
.card-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 15px;
  font-weight: 700;
  color: #1a1917;
  margin: 0;
  line-height: 1.4;
}

/* Synopsis */
.card-summary {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  color: #65635d;
  margin: 0;
  line-height: 1.7;
  flex: 1;
  overflow-wrap: break-word;
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
  transition: opacity 150ms ease-out, gap 150ms ease-out;
}
.read-more:hover {
  opacity: 0.75;
  gap: 7px;
}
</style>
