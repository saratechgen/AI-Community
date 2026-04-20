<template>
  <div class="news-view">
    <header class="news-header">
      <h1 class="news-title">AI News</h1>
      <p class="news-subtitle">{{ brief }}</p>
    </header>

    <div v-if="loading" class="state-message">
      <Loader2 :size="20" class="spin" />
      Loading latest news…
    </div>
    <div v-else-if="error" class="state-message state-error">{{ error }}</div>

    <template v-else>
      <section
        v-for="(section, index) in sections"
        :key="section.key"
        class="news-section"
      >
        <h2 class="section-title">
          <component
            :is="section.icon"
            :size="22"
            :stroke-width="2.2"
            :class="['section-icon', section.iconClass]"
            :style="{ animationDelay: `${index * 0.4}s` }"
          />
          {{ section.label }}
          <span class="section-desc">{{ section.desc }}</span>
        </h2>

        <div class="news-grid">
          <NewsCard
            v-for="article in news[section.key]"
            :key="article.id"
            :article="article"
          />
          <div v-if="!news[section.key]?.length" class="empty-section">
            No articles available yet — next refresh in 30 minutes.
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { Briefcase, Bot, Lightbulb, Sparkles, Rocket, Loader2 } from 'lucide-vue-next'
import NewsCard from '../components/NewsCard.vue'
import { useNews } from '../composables/useNews.js'

const { news, loading, error, fetchNews, brief } = useNews()
onMounted(fetchNews)

const sections = [
  {
    key:       'aiAtWork',
    label:     'AI @ Work',
    icon:      Briefcase,
    iconClass: 'icon-pop',
    desc:      'GitHub Copilot, enterprise AI, extensions & productivity tools',
  },
  {
    key:       'aiAgents',
    label:     'AI Agents',
    icon:      Bot,
    iconClass: 'icon-pop',
    desc:      'Agentic workflows, autonomous systems, multi-agent frameworks',
  },
  {
    key:       'quickTips',
    label:     'Quick Tips',
    icon:      Lightbulb,
    iconClass: 'icon-glow',
    desc:      'Practical how-tos, prompting guides & productivity wins',
  },
  {
    key:       'claude',
    label:     'Claude & Anthropic',
    icon:      Sparkles,
    iconClass: 'icon-pop',
    desc:      'Latest from Claude, Claude Code & Anthropic',
  },
  {
    key:       'advancements',
    label:     'New Advancements',
    icon:      Rocket,
    iconClass: 'icon-pop',
    desc:      'New models, research breakthroughs & open-source releases',
  },
]
</script>

<style scoped>
.news-view {
  padding: 32px 40px;
  --accent: #2255b0;
  --accent-light: #dbeafe;
}

/* Header — matches section title style */
.news-header {
  background: #f8f7f5;
  border-left: 4px solid var(--accent, #166534);
  border-bottom: 1px solid #e2e0dc;
  border-radius: 0 6px 0 0;
  padding: 14px 18px;
  margin-bottom: 24px;
}
.news-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 22px;
  font-weight: 700;
  color: #1a1917;
  margin: 0 0 4px;
}
.news-subtitle {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  color: #65635d;
  margin: 0;
}

/* Section */
.news-section { margin-bottom: 32px; }
.section-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 18px;
  font-weight: 700;
  color: #1a1917;
  margin: 0 0 20px;
  padding: 10px 14px;
  border-left: 4px solid var(--accent, #166534);
  border-bottom: 1px solid #e2e0dc;
  background: #f8f7f5;
  border-radius: 0 6px 0 0;
  display: flex;
  align-items: center;
  gap: 10px;
}
.section-desc {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 400;
  color: var(--text-muted, #a8a69f);
  margin-left: 2px;
}

/* ── Base icon ──────────────────────────────────────────────── */
.section-icon {
  color: var(--accent, #166534);
  flex-shrink: 0;
  cursor: default;
  transition: color 200ms ease-out,
              filter 200ms ease-out,
              transform 200ms ease-out;
}

/* Hover — brighten green + glow */
.section-title:hover .section-icon {
  color: #16a34a;
  filter: drop-shadow(0 0 6px rgba(22, 163, 74, 0.55));
  transform: scale(1.2);
}

/* Pause the loop animation on hover so glow takes over cleanly */
.section-title:hover .icon-pop,
.section-title:hover .icon-glow {
  animation-play-state: paused;
}

/* ── Continuous pop (Briefcase, Bot, Sparkles, Rocket) ───── */
/* Gentle bounce-rotate loop, each section offset by 0.5s    */
.icon-pop {
  animation: icon-pop 2s cubic-bezier(0.16, 1, 0.3, 1) infinite;
}

@keyframes icon-pop {
  0%   { transform: scale(1)    rotate(0deg);  }
  20%  { transform: scale(0.78) rotate(-12deg); opacity: 0.7; }
  50%  { transform: scale(1.18) rotate(7deg);  opacity: 1;   }
  70%  { transform: scale(0.95) rotate(-3deg); }
  85%  { transform: scale(1.04) rotate(1deg);  }
  100% { transform: scale(1)    rotate(0deg);  }
}

/* ── Continuous glow (Lightbulb — Quick Tips) ────────────── */
/* Pulses amber glow on and off, smooth breathe effect       */
.icon-glow {
  animation: icon-glow 2.4s ease-in-out infinite;
}

@keyframes icon-glow {
  0%, 100% {
    color: var(--accent, #166534);
    filter: none;
  }
  40% {
    color: #d97706;
    filter: drop-shadow(0 0 5px #fbbf24);
  }
  60% {
    color: #f59e0b;
    filter: drop-shadow(0 0 10px #fbbf24) drop-shadow(0 0 20px #fde68a);
  }
}

/* ── Grid — equal height ─────────────────────────────────── */
.news-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  align-items: stretch;
}

/* Empty state */
.empty-section {
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  color: var(--text-muted, #a8a69f);
  padding: 24px;
  text-align: center;
  border: 1px dashed var(--border-light, #e2e0dc);
  border-radius: 8px;
  grid-column: 1 / -1;
}

/* Loading */
.state-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  color: var(--text-secondary, #65635d);
  padding: 60px 0;
}
.state-error { color: #d64545; }
.spin { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Responsive */
@media (max-width: 1200px) {
  .news-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
  .news-view { padding: 20px; }
  .news-grid { grid-template-columns: 1fr; }
  .section-desc { display: none; }
}
</style>
