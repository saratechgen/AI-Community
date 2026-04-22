<template>
  <section class="events-section">
    <div class="section-header">
      <h2 class="section-title">
        <CalendarDays :size="17" class="title-icon" />
        Upcoming Events
      </h2>
      <RouterLink to="/events" class="view-all">
        View all <ArrowRight :size="13" />
      </RouterLink>
    </div>

    <div v-if="loading" class="ev-state">Loading events…</div>

    <template v-else>

      <!-- DEWA Events ─────────────────────────────────────── -->
      <div class="ev-label">
        <Building2 :size="11" /> DEWA
      </div>

      <div v-if="homeDewaEvents.length" class="events-list">
        <div v-for="e in homeDewaEvents" :key="e.id" class="event-row">
          <div class="event-date">
            <span class="date-day">{{ dayOf(e.date) }}</span>
            <span class="date-month">{{ monthOf(e.date) }}</span>
          </div>
          <div class="event-body">
            <span class="event-title">{{ e.title }}</span>
            <div class="event-meta">
              <Clock :size="11" /> {{ e.time }}
              <span class="dot">·</span>
              <MapPin :size="11" /> {{ e.location }}
            </div>
          </div>
        </div>
      </div>
      <p v-else class="ev-empty">No DEWA events scheduled yet.</p>

      <div class="ev-divider" />

      <!-- External Events ──────────────────────────────────── -->
      <div class="ev-label ev-label--blue">
        <Globe :size="11" /> Outside DEWA
      </div>

      <div v-if="homeExternalEvents.length" class="events-list">
        <a
          v-for="e in homeExternalEvents"
          :key="e.id"
          :href="e.url || '#'"
          target="_blank"
          rel="noopener noreferrer"
          class="event-row event-row--link"
        >
          <div class="event-date event-date--blue">
            <span class="date-day">{{ dayOf(e.date) }}</span>
            <span class="date-month">{{ monthOf(e.date) }}</span>
          </div>
          <div class="event-body">
            <span class="event-title">{{ e.title }}</span>
            <div class="event-meta">
              <span class="ev-org">{{ e.organizer }}</span>
              <span class="dot">·</span>
              <MapPin :size="11" /> {{ e.location || 'TBC' }}
              <ExternalLink :size="10" class="ev-ext-icon" />
            </div>
          </div>
        </a>
      </div>
      <p v-else class="ev-empty">No upcoming external events.</p>

    </template>
  </section>
</template>

<script setup>
import { onMounted } from 'vue'
import { CalendarDays, Clock, MapPin, ArrowRight, Building2, Globe, ExternalLink } from 'lucide-vue-next'
import { useEvents } from '../composables/useEvents.js'

const { homeDewaEvents, homeExternalEvents, loading, fetchEvents } = useEvents()
onMounted(fetchEvents)

const toDate  = (iso) => new Date(iso + 'T12:00:00')
const dayOf   = (iso) => toDate(iso).toLocaleDateString('en-GB', { day: 'numeric' })
const monthOf = (iso) => toDate(iso).toLocaleDateString('en-GB', { month: 'short' })
</script>

<style scoped>
.events-section {
  background: #ffffff;
  border: 1px solid #e2e0dc;
  border-top: 3px solid var(--accent, #166534);
  border-radius: 10px;
  padding: 20px 22px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 4px 12px rgba(0,0,0,0.04);
}

.section-header   { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.section-title    { font-family: 'Space Grotesk', sans-serif; font-size: 15px; font-weight: 700; color: #1a1917; margin: 0; display: flex; align-items: center; gap: 7px; }
.title-icon       { color: #166534; }
.view-all         { display: inline-flex; align-items: center; gap: 3px; font-family: 'DM Sans', sans-serif; font-size: 12px; font-weight: 600; color: #166534; text-decoration: none; transition: gap 150ms; }
.view-all:hover   { gap: 7px; }

/* Group labels */
.ev-label {
  display: flex;
  align-items: center;
  gap: 5px;
  font-family: 'DM Sans', sans-serif;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: #166534;
  margin-bottom: 8px;
}
.ev-label--blue { color: #2255b0; }

.ev-divider { border: none; border-top: 1px solid #f0efe9; margin: 12px 0; }

/* Event rows */
.events-list  { display: flex; flex-direction: column; }
.event-row {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid #f0efe9;
  text-decoration: none;
}
.event-row:last-child { border-bottom: none; padding-bottom: 0; }
.event-row--link { cursor: pointer; transition: padding-left 140ms; }
.event-row--link:hover { padding-left: 3px; }
.event-row--link:hover .event-title { color: #2255b0; }

/* Date chip */
.event-date {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #dcfce7;
  color: #166534;
  border: 1px solid #166534;
  border-radius: 7px;
  padding: 5px 9px;
  min-width: 38px;
  flex-shrink: 0;
}
.event-date--blue { background: #dbeafe; color: #2255b0; border-color: #2255b0; }

.date-day   { font-family: 'Space Grotesk', sans-serif; font-size: 15px; font-weight: 700; line-height: 1; }
.date-month { font-family: 'DM Sans', sans-serif; font-size: 9px; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.8; margin-top: 2px; }

/* Body */
.event-body  { flex: 1; min-width: 0; }
.event-title { display: block; font-family: 'DM Sans', sans-serif; font-size: 12px; font-weight: 600; color: #1a1917; margin-bottom: 4px; line-height: 1.4; transition: color 140ms; }
.event-meta  { display: flex; align-items: center; gap: 5px; font-family: 'DM Sans', sans-serif; font-size: 11px; color: #85837c; flex-wrap: wrap; }
.ev-org      { font-weight: 600; color: #2255b0; }
.ev-ext-icon { margin-left: 2px; color: #a8a69f; flex-shrink: 0; }
.dot         { opacity: 0.4; }

/* States */
.ev-state { font-family: 'DM Sans', sans-serif; font-size: 13px; color: #85837c; padding: 16px 0; }
.ev-empty { font-family: 'DM Sans', sans-serif; font-size: 12px; color: #a8a69f; margin: 4px 0 0; padding-bottom: 2px; }
</style>
