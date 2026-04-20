<template>
  <section class="quick-access" v-if="data">
    <div class="links-row">
      <RouterLink
        v-for="link in data.links"
        :key="link.route"
        :to="link.route"
        class="quick-link"
      >
        <component :is="iconFor(link.icon)" :size="18" class="link-icon" />
        <span class="link-label">{{ link.label }}</span>
      </RouterLink>
    </div>
  </section>
</template>

<script setup>
import * as Icons from 'lucide-vue-next'
import { useStaticJson } from '../composables/useStaticJson.js'

const { data } = useStaticJson('/data/quick-links.json')
const iconFor  = (name) => Icons[name] || Icons.Circle
</script>

<style scoped>
.quick-access { margin-bottom: 36px; }
.section-label {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #0f4024;
  margin: 0 0 12px;
}
.links-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.quick-link {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 8px 14px;
  border: 1px solid #e2e0dc;
  border-radius: 20px;
  background: #f8f7f5;
  text-decoration: none;
  color: #65635d;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 500;
  transition: border-color 150ms, color 150ms, background 150ms;
}
.quick-link:hover {
  border-color: #0f4024;
  color: #0f4024;
  background: #dcfce7;
}
.link-icon { flex-shrink: 0; }
</style>
