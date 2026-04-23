<template>
  <section class="hero" v-if="data">
    <div class="hero-eyebrow">
      <span class="eyebrow-dot" />
      {{ data.mission_label }}
    </div>
    <h1 class="hero-title">{{ data.title }}</h1>
    <p class="hero-subtitle">{{ data.subtitle }}</p>
    <div class="hero-categories">
      <span v-for="cat in data.categories" :key="cat" class="hero-cat">{{ cat }}</span>
    </div>
    <div class="hero-actions">
      <RouterLink :to="data.cta_route" class="hero-cta hero-cta--primary">
        {{ data.cta_label }} <ArrowRight :size="13" />
      </RouterLink>
    </div>
    <div class="hero-pills">
      <RouterLink
        v-for="pill in data.pills"
        :key="pill.label"
        :to="pill.route"
        class="hero-pill"
      >{{ pill.label }}</RouterLink>
    </div>
  </section>
</template>

<script setup>
import { ArrowRight } from 'lucide-vue-next'
import { useStaticJson } from '../composables/useStaticJson.js'

const { data } = useStaticJson('/data/hero.json')
</script>

<style scoped>
.hero {
  background: #f8f7f5;
  border: 1px solid #e2e0dc;
  border-top: 3px solid var(--accent, #166534);
  border-radius: 10px;
  padding: 16px 32px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

.hero-eyebrow {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #166534;
}
.eyebrow-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #166534;
  flex-shrink: 0;
}

.hero-title {
  font-family: 'Satoshi', sans-serif;
  font-size: 30px;
  font-weight: 700;
  color: #1a1917;
  margin: 0;
  line-height: 1.2;
}

.hero-subtitle {
  font-family: 'Inter', sans-serif;
  font-size: 15px;
  font-weight: 500;
  color: #3a3834;
  margin: 0;
  line-height: 1.75;
  max-width: 640px;
  text-shadow: 0 1px 0 rgba(255,255,255,0.85);
}

.hero-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}
.hero-cta {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  font-weight: 600;
  padding: 8px 14px;
  border-radius: 6px;
  text-decoration: none;
  transition: background 150ms, gap 150ms;
}
.hero-cta--primary {
  background: #166534;
  color: #f0fdf4;
}
.hero-cta--primary:hover { background: #0a2e1a; gap: 10px; }

.hero-categories {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.hero-cat {
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  font-weight: 600;
  color: #166534;
  background: #dcfce7;
  border-radius: 4px;
  padding: 3px 9px;
}

.hero-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.hero-pill {
  font-family: 'Inter', sans-serif;
  font-size: 11px;
  font-weight: 500;
  color: #85837c;
  background: #fff;
  border: 1px solid #e2e0dc;
  border-radius: 20px;
  padding: 4px 12px;
  text-decoration: none;
  transition: border-color 150ms, color 150ms, background 150ms;
}
.hero-pill:hover {
  border-color: #166534;
  color: #166534;
  background: #dcfce7;
}

@media (max-width: 640px) {
  .hero { padding: 24px 20px 20px; }
  .hero-title { font-size: 24px; }
  .hero-cta { width: 100%; justify-content: center; }
}
</style>
