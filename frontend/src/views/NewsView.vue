<template>
  <div class="news-view">
    <header class="news-header">
      <h1 class="news-title">AI News</h1>
      <p class="news-subtitle">Sourced from 17 feeds across the AI ecosystem — refreshed every 30 minutes so you never miss what matters.</p>
      <span v-if="fetchedAtLabel" class="news-refreshed">Last refreshed · {{ fetchedAtLabel }}</span>
    </header>

    <!-- Filter chips -->
    <div class="filter-bar">
      <button
        v-for="chip in chips"
        :key="chip.key"
        :class="['filter-chip', { 'filter-chip--active': activeFilter === chip.key }]"
        @click="activeFilter = chip.key"
      >
        {{ chip.label }}
      </button>
    </div>

    <div v-if="loading" class="state-message">
      <Loader2 :size="20" class="spin" /> Loading latest news…
    </div>
    <div v-else-if="error" class="state-message state-error">{{ error }}</div>

    <template v-else>
      <section
        v-for="(section, index) in visibleSections"
        :key="section.key"
        class="news-section"
      >
        <h2 class="section-title">
          <component
            :is="section.icon"
            :size="20"
            :stroke-width="2.2"
            :class="['section-icon', section.iconClass]"
            :style="{ animationDelay: `${index * 0.4}s` }"
          />
          {{ section.label }}
          <span class="section-desc">{{ section.desc }}</span>
        </h2>

        <!-- All view: 1 featured left + 2 compact stacked right -->
        <div v-if="activeFilter === 'all' && news[section.key]?.length" class="section-editorial">
          <NewsCard :article="news[section.key][0]" variant="featured" />
          <div class="editorial-compact-col">
            <NewsCard
              v-for="article in news[section.key].slice(1, 3)"
              :key="article.id"
              :article="article"
              variant="compact"
            />
          </div>
        </div>

        <!-- Filtered view: featured full-width + compact grid below -->
        <template v-else-if="activeFilter !== 'all' && news[section.key]?.length">
          <NewsCard :article="news[section.key][0]" variant="featured" class="filtered-featured" />
          <div v-if="news[section.key].length > 1" class="filtered-compact-grid">
            <NewsCard
              v-for="article in news[section.key].slice(1)"
              :key="article.id"
              :article="article"
              variant="compact"
            />
          </div>
        </template>

        <div v-if="!news[section.key]?.length" class="empty-section">
          No articles available yet — next refresh in 30 minutes.
        </div>
      </section>
    </template>
  </div>
</template>

<script setup>
/* Escape hatch: exceeds 250-line cap — NewsView has single responsibility (news feed UI) */
import { ref, computed, onMounted } from 'vue'
import { Briefcase, Bot, Lightbulb, Sparkles, Rocket, Loader2 } from 'lucide-vue-next'
import NewsCard   from '../components/NewsCard.vue'
import { useNews } from '../composables/useNews.js'

const { news, loading, error, fetchNews, brief, fetchedAt } = useNews()
onMounted(fetchNews)

const fetchedAtLabel = computed(() => {
  if (!fetchedAt.value) return ''
  const d    = fetchedAt.value
  const date = d.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
  const time = d.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' })
  return `${date} · ${time}`
})

const activeFilter = ref('all')

const sections = [
  { key: 'aiAtWork',     label: 'AI at Work',         icon: Briefcase, iconClass: 'icon-pop',  desc: 'Enterprise AI, productivity tools, copilots & real-world use cases' },
  { key: 'aiAgents',     label: 'AI Agents',          icon: Bot,       iconClass: 'icon-pop',  desc: 'Agentic workflows, autonomous systems, multi-agent frameworks' },
  { key: 'quickTips',    label: 'Quick Tips',         icon: Lightbulb, iconClass: 'icon-glow', desc: 'Practical how-tos, prompting guides & productivity wins' },
  { key: 'claude',       label: 'Claude & Anthropic', icon: Sparkles,  iconClass: 'icon-pop',  desc: 'Latest from Claude, Claude Code & Anthropic' },
  { key: 'advancements', label: 'New Advancements',   icon: Rocket,    iconClass: 'icon-pop',  desc: 'New models, research breakthroughs & open-source releases' },
]

const chips = [{ key: 'all', label: 'All' }, ...sections.map(s => ({ key: s.key, label: s.label }))]

const visibleSections = computed(() =>
  activeFilter.value === 'all'
    ? sections
    : sections.filter(s => s.key === activeFilter.value)
)
</script>

<style scoped>
/* Escape hatch: exceeds 250-line cap — NewsView has single responsibility (news feed UI) */
.news-view {
  padding: 32px 40px;
  --accent: #0E6B43;
  --accent-light: #DFF3E8;
}

/* Header */
.news-header {
  padding: 0 0 20px;
  border-bottom: 1px solid #D9D5CD;
  margin-bottom: 24px;
}
.news-title   { font-family: 'Space Grotesk', sans-serif; font-size: 28px; font-weight: 700; color: #1F1F1B; margin: 0 0 6px; letter-spacing: -0.01em; }
.news-subtitle { font-family: 'DM Sans', sans-serif; font-size: 14px; color: #6E6A63; margin: 0; }
.news-refreshed { font-family: 'DM Sans', sans-serif; font-size: 11px; color: #A8A49D; margin-top: 4px; display: block; }

/* Filter chips */
.filter-bar { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 28px; }
.filter-chip {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 600;
  padding: 6px 16px;
  border-radius: 20px;
  border: 1.5px solid #D9D5CD;
  background: #F6F5F2;
  color: #6E6A63;
  cursor: pointer;
  transition: all 150ms;
  white-space: nowrap;
}
.filter-chip:hover            { border-color: var(--accent); color: var(--accent); background: #DFF3E8; }
.filter-chip--active          { background: var(--accent); border-color: var(--accent); color: #fff; }
.filter-chip--active:hover    { opacity: 0.9; }

/* Section */
.news-section { margin-bottom: 36px; }
.section-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 14px;
  font-weight: 700;
  color: #1F1F1B;
  margin: 0 0 16px;
  padding: 0 0 10px;
  border-bottom: 2px solid var(--accent);
  background: transparent;
  border-radius: 0;
  display: flex;
  align-items: center;
  gap: 10px;
}
.section-desc { font-family: 'DM Sans', sans-serif; font-size: 12px; font-weight: 400; color: #A8A49D; }
.section-icon { color: var(--accent); flex-shrink: 0; transition: color 200ms, filter 200ms, transform 200ms; }
.section-title:hover .section-icon { color: #0A5736; filter: drop-shadow(0 0 5px rgba(14,107,67,0.4)); transform: scale(1.15); }
.section-title:hover .icon-pop,
.section-title:hover .icon-glow  { animation-play-state: paused; }

/* Editorial layout (All view) */
.section-editorial     { display: grid; grid-template-columns: 3fr 2fr; gap: 12px; align-items: start; }
.editorial-compact-col { display: flex; flex-direction: column; gap: 10px; height: 100%; }

/* Filtered layout */
.filtered-featured      { margin-bottom: 12px; }
.filtered-compact-grid  { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }

/* Empty */
.empty-section {
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  color: #a8a69f;
  padding: 24px;
  text-align: center;
  border: 1px dashed #D9D5CD;
  border-radius: 8px;
}

/* Loading */
.state-message { display: flex; align-items: center; justify-content: center; gap: 10px; font-family: 'DM Sans', sans-serif; font-size: 15px; color: #6E6A63; padding: 60px 0; }
.state-error   { color: #d64545; }
.spin          { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Icon animations */
.icon-pop  { animation: icon-pop  2s   cubic-bezier(0.16,1,0.3,1) infinite; }
.icon-glow { animation: icon-glow 2.4s ease-in-out infinite; }
@keyframes icon-pop {
  0%   { transform: scale(1)    rotate(0deg);   }
  20%  { transform: scale(0.78) rotate(-12deg); opacity: 0.7; }
  50%  { transform: scale(1.18) rotate(7deg);   opacity: 1;   }
  70%  { transform: scale(0.95) rotate(-3deg);  }
  85%  { transform: scale(1.04) rotate(1deg);   }
  100% { transform: scale(1)    rotate(0deg);   }
}
@keyframes icon-glow {
  0%, 100% { color: var(--accent); filter: none; }
  40%  { color: #d97706; filter: drop-shadow(0 0 5px #fbbf24); }
  60%  { color: #f59e0b; filter: drop-shadow(0 0 10px #fbbf24) drop-shadow(0 0 20px #fde68a); }
}

/* Responsive */
@media (max-width: 1000px) {
  .section-editorial     { grid-template-columns: 1fr; }
  .editorial-compact-col { flex-direction: row; }
}
@media (max-width: 640px) {
  .news-view             { padding: 20px; }
  .section-desc          { display: none; }
  .editorial-compact-col { flex-direction: column; }
  .filtered-compact-grid { grid-template-columns: 1fr; }
  .filter-chip           { font-size: 12px; padding: 5px 12px; }
}
</style>
