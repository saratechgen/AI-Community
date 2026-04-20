<template>
  <section class="events-section" v-if="data">
    <div class="section-header">
      <h2 class="section-title">
        <CalendarDays :size="17" class="title-icon" />
        Upcoming Events
      </h2>
      <RouterLink to="/events" class="view-all">
        View all <ArrowRight :size="13" />
      </RouterLink>
    </div>

    <div class="events-list">
      <div
        v-for="event in data.events"
        :key="event.id"
        class="event-row"
      >
        <div class="event-date">
          <span class="date-day">{{ dayOf(event.date) }}</span>
          <span class="date-month">{{ monthOf(event.date) }}</span>
        </div>
        <div class="event-body">
          <span class="event-title">{{ event.title }}</span>
          <div class="event-meta">
            <Clock :size="11" />
            {{ event.time }}
            <span class="dot">·</span>
            <MapPin :size="11" />
            {{ event.location }}
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { CalendarDays, Clock, MapPin, ArrowRight } from 'lucide-vue-next'
import { useStaticJson } from '../composables/useStaticJson.js'

const { data } = useStaticJson('/data/events.json')

const dayOf   = (iso) => new Date(iso).toLocaleDateString('en-GB', { day: 'numeric' })
const monthOf = (iso) => new Date(iso).toLocaleDateString('en-GB', { month: 'short' })
</script>

<style scoped>
.events-section {
  background: #ffffff;
  border: 1px solid #e2e0dc;
  border-top: 3px solid var(--accent, #166534);
  border-radius: 10px;
  padding: 20px 22px;
  box-shadow:
    0 1px 3px rgba(0,0,0,0.05),
    0 4px 12px rgba(0,0,0,0.04);
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
.section-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 15px;
  font-weight: 700;
  color: #1a1917;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 7px;
}
.title-icon { color: #166534; }

.view-all {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  font-weight: 600;
  color: #166534;
  text-decoration: none;
  transition: gap 150ms;
}
.view-all:hover { gap: 7px; }

/* Event rows */
.events-list { display: flex; flex-direction: column; }
.event-row {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 13px 0;
  border-bottom: 1px solid #f0efe9;
}
.event-row:first-child { padding-top: 0; }
.event-row:last-child { border-bottom: none; padding-bottom: 0; }

/* Date chip — larger, more presence */
.event-date {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: var(--accent-light, #dcfce7);
  color: var(--accent, #166534);
  border: 1px solid var(--accent, #166534);
  border-radius: 8px;
  padding: 6px 10px;
  min-width: 42px;
  flex-shrink: 0;
}
.date-day {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 16px;
  font-weight: 700;
  line-height: 1;
}
.date-month {
  font-family: 'DM Sans', sans-serif;
  font-size: 9px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  opacity: 0.8;
  margin-top: 2px;
}

.event-body { flex: 1; min-width: 0; }
.event-title {
  display: block;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: #1a1917;
  margin-bottom: 5px;
  line-height: 1.4;
}
.event-meta {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: 'DM Sans', sans-serif;
  font-size: 11px;
  color: #85837c;
  flex-wrap: wrap;
}
.dot { margin: 0 1px; opacity: 0.5; }
</style>
