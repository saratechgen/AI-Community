<template>
  <section class="glance" v-if="data">
    <div class="glance-grid">
      <RouterLink
        v-for="item in data.highlights"
        :key="item.label"
        :to="item.route"
        class="glance-tile"
      >
        <div class="icon-circle">
          <component :is="iconFor(item.icon)" :size="20" />
        </div>
        <div class="tile-body">
          <span class="tile-value">{{ item.value }}</span>
          <span class="tile-label">{{ item.label }}</span>
        </div>
        <ChevronRight :size="14" class="tile-arrow" />
      </RouterLink>
    </div>
  </section>
</template>

<script setup>
import * as Icons from 'lucide-vue-next'
import { ChevronRight } from 'lucide-vue-next'
import { useStaticJson } from '../composables/useStaticJson.js'

const { data } = useStaticJson('/data/weekly-highlights.json')

const iconFor = (name) => Icons[name] || Icons.Circle
</script>

<style scoped>
.glance { margin-bottom: 0; }

.glance-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 14px;
}

.glance-tile {
  display: flex;
  align-items: center;
  gap: 14px;
  background: #ffffff;
  border: 1px solid #e2e0dc;
  border-radius: 10px;
  padding: 18px 16px;
  text-decoration: none;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 4px 10px rgba(0,0,0,0.04);
  transition: border-color 180ms, box-shadow 180ms, transform 180ms;
}
.glance-tile:hover {
  border-color: #0f4024;
  box-shadow: 0 2px 6px rgba(0,0,0,0.06), 0 8px 20px rgba(15,64,36,0.1);
  transform: translateY(-2px);
}

.icon-circle {
  width: 42px;
  height: 42px;
  border-radius: 10px;
  background: #dcfce7;
  color: #0f4024;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.tile-body {
  display: flex;
  flex-direction: column;
  gap: 3px;
  flex: 1;
  min-width: 0;
}
.tile-value {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 15px;
  font-weight: 700;
  color: #1a1917;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.tile-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 11px;
  font-weight: 500;
  color: #85837c;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
.tile-arrow {
  color: #a8a69f;
  flex-shrink: 0;
  transition: color 150ms, transform 150ms;
}
.glance-tile:hover .tile-arrow {
  color: #0f4024;
  transform: translateX(2px);
}

@media (max-width: 640px) {
  .glance-grid { grid-template-columns: 1fr; }
}
</style>
