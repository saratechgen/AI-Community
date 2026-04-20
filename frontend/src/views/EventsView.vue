<template>
  <div class="events-view">
    <header class="events-header">
      <h1 class="events-title">Upcoming Events</h1>
      <p class="events-subtitle">AI workshops, demos and community sessions across DEWA.</p>
    </header>

    <div v-if="!data" class="state-msg">Loading events…</div>

    <div v-else-if="!data.events?.length" class="state-msg">
      No upcoming events at this time.
    </div>

    <div v-else class="events-list">
      <div v-for="event in data.events" :key="event.id" class="event-card">
        <div class="event-date">
          <span class="date-day">{{ dayOf(event.date) }}</span>
          <span class="date-month">{{ monthOf(event.date) }}</span>
        </div>
        <div class="event-body">
          <span class="event-title">{{ event.title }}</span>
          <div class="event-meta">
            <Clock :size="12" />
            {{ event.time }}
            <span class="dot">·</span>
            <MapPin :size="12" />
            {{ event.location }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Clock, MapPin } from 'lucide-vue-next'
import { useStaticJson } from '../composables/useStaticJson.js'

const { data } = useStaticJson('/data/events.json')

const dayOf   = (iso) => new Date(iso).toLocaleDateString('en-GB', { day: 'numeric' })
const monthOf = (iso) => new Date(iso).toLocaleDateString('en-GB', { month: 'short' })
</script>

<style scoped>
.events-view { padding: 32px 40px; max-width: 720px; --accent: #5bb85d; --accent-light: #d1fae5; }

.events-header {
  border-left: 4px solid var(--accent, #166534);
  border-bottom: 1px solid #e2e0dc;
  border-radius: 0 6px 0 0;
  background: #f8f7f5;
  padding: 14px 18px;
  margin-bottom: 28px;
}
.events-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 22px;
  font-weight: 700;
  color: #1a1917;
  margin: 0 0 4px;
}
.events-subtitle {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  color: #65635d;
  margin: 0;
}

.state-msg {
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  color: #65635d;
  padding: 60px 0;
}

.events-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.event-card {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  background: #ffffff;
  border: 1px solid #e2e0dc;
  border-radius: 10px;
  padding: 18px 20px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  transition: border-color 150ms, box-shadow 150ms;
}
.event-card:hover {
  border-color: var(--accent, #166534);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.event-date {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: var(--accent-light, #d1fae5);
  color: var(--accent, #166534);
  border: 1px solid var(--accent, #166534);
  border-radius: 8px;
  padding: 8px 12px;
  min-width: 46px;
  flex-shrink: 0;
}
.date-day {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 20px;
  font-weight: 700;
  line-height: 1;
}
.date-month {
  font-family: 'DM Sans', sans-serif;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  opacity: 0.8;
  margin-top: 2px;
}

.event-body { flex: 1; min-width: 0; }
.event-title {
  display: block;
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  font-weight: 600;
  color: #1a1917;
  margin-bottom: 8px;
  line-height: 1.4;
}
.event-meta {
  display: flex;
  align-items: center;
  gap: 5px;
  font-family: 'DM Sans', sans-serif;
  font-size: 11px;
  color: #85837c;
  flex-wrap: wrap;
}
.dot { opacity: 0.5; }

@media (max-width: 640px) {
  .events-view { padding: 20px; }
}
</style>
