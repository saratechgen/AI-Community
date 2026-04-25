<template>
  <div class="events-view">
    <header class="events-header">
      <h1 class="events-title">Events</h1>
      <p class="events-subtitle">DEWA internal sessions and external AI events worth exploring.</p>
    </header>

    <div v-if="loading" class="state-msg">
      <Loader2 :size="18" class="spin" /> Loading events…
    </div>

    <template v-else>

      <!-- ── DEWA Events ────────────────────────────────────────── -->
      <section class="ev-section">
        <h2 class="ev-section-title">
          <Building2 :size="17" class="ev-section-icon" />
          DEWA Events
        </h2>

        <div v-if="dewaEvents.length" class="ev-list">
          <div v-for="e in dewaEvents" :key="e.id" class="ev-card">
            <div class="ev-date">
              <span class="ev-day">{{ dayOf(e.date) }}</span>
              <span class="ev-month">{{ monthOf(e.date) }}</span>
            </div>
            <div class="ev-body">
              <div class="ev-card-top">
                <span class="ev-card-title">{{ e.title }}</span>
                <span class="ev-type-chip ev-type-chip--green">{{ e.type }}</span>
              </div>
              <div class="ev-meta">
                <Clock :size="12" /> {{ e.time }}
                <span class="dot">·</span>
                <MapPin :size="12" /> {{ e.location }}
              </div>
              <p v-if="e.description" class="ev-desc">{{ e.description }}</p>
              <a
                v-if="e.registrationUrl"
                :href="e.registrationUrl"
                target="_blank"
                rel="noopener noreferrer"
                class="ev-register"
              >
                Register <ExternalLink :size="12" />
              </a>
            </div>
          </div>
        </div>
        <div v-else class="ev-empty-state">No DEWA events scheduled. Check back soon.</div>
      </section>

      <!-- ── External Events ────────────────────────────────────── -->
      <section class="ev-section ev-section--ext">
        <h2 class="ev-section-title ev-section-title--blue">
          <Globe :size="17" class="ev-section-icon ev-section-icon--blue" />
          Events to Explore Outside DEWA
        </h2>

        <template v-if="externalEvents.length">
          <template v-for="group in visibleGroups" :key="group.key">
            <div class="ev-week-label">{{ group.label }}</div>
            <div class="ev-list">
              <a
                v-for="e in grouped[group.key]"
                :key="e.id"
                :href="e.url || '#'"
                target="_blank"
                rel="noopener noreferrer"
                class="ev-card ev-card--ext"
              >
                <div class="ev-date ev-date--blue">
                  <span class="ev-day">{{ dayOf(e.date) }}</span>
                  <span class="ev-month">{{ monthOf(e.date) }}</span>
                  <span v-if="e.endDate && e.endDate !== e.date" class="ev-end-day">
                    – {{ dayOf(e.endDate) }}
                  </span>
                </div>
                <div class="ev-body">
                  <div class="ev-card-top">
                    <span class="ev-card-title">{{ e.title }}</span>
                    <span class="ev-type-chip ev-type-chip--blue">{{ e.type }}</span>
                  </div>
                  <div class="ev-meta">
                    <span class="ev-org">{{ e.organizer }}</span>
                    <span v-if="e.location" class="dot">·</span>
                    <MapPin v-if="e.location" :size="12" /> {{ e.location }}
                    <ExternalLink :size="11" class="ev-ext-icon" />
                  </div>
                </div>
              </a>
            </div>
          </template>
        </template>

        <div v-else class="ev-empty-state">No upcoming external events at this time.</div>
      </section>

    </template>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { Building2, Globe, Clock, MapPin, ExternalLink, Loader2 } from 'lucide-vue-next'
import { useEvents } from '../composables/useEvents.js'

const { dewaEvents, externalEvents, grouped, loading, fetchEvents } = useEvents()
onMounted(fetchEvents)

const GROUP_DEFS = [
  { key: 'thisWeek', label: 'This Week' },
  { key: 'nextWeek', label: 'Next Week' },
  { key: 'upcoming', label: 'Upcoming'  },
]

const visibleGroups = computed(() =>
  GROUP_DEFS.filter(g => grouped.value[g.key]?.length)
)

const toDate  = (iso) => new Date(iso + 'T12:00:00')
const dayOf   = (iso) => toDate(iso).toLocaleDateString('en-GB', { day: 'numeric' })
const monthOf = (iso) => toDate(iso).toLocaleDateString('en-GB', { month: 'short' })
</script>

<style scoped>
.events-view { padding: 32px 40px; --accent: #0E6B43; --accent-light: #DFF3E8; }

/* Header */
.events-header {
  padding: 0 0 20px;
  border-bottom: 1px solid #D9D5CD;
  margin-bottom: 28px;
}
.events-title    { font-family: 'Space Grotesk', sans-serif; font-size: 28px; font-weight: 700; color: #1F1F1B; margin: 0 0 6px; letter-spacing: -0.01em; }
.events-subtitle { font-family: 'DM Sans', sans-serif; font-size: 14px; color: #6E6A63; margin: 0; }

/* Loading */
.state-msg { display: flex; align-items: center; gap: 10px; font-family: 'DM Sans', sans-serif; font-size: 15px; color: #6E6A63; padding: 60px 0; }
.spin      { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Sections */
.ev-section       { margin-bottom: 36px; }
.ev-section--ext  { margin-bottom: 0; }

.ev-section-title {
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
  gap: 9px;
}
.ev-section-title--blue  { border-bottom-color: #0E6B43; }
.ev-section-icon         { color: var(--accent); }
.ev-section-icon--blue   { color: #0E6B43; }

/* Week group labels */
.ev-week-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: #0E6B43;
  margin: 16px 0 8px;
}
.ev-week-label:first-of-type { margin-top: 0; }

/* Card list */
.ev-list { display: flex; flex-direction: column; gap: 10px; margin-bottom: 4px; }

/* Cards */
.ev-card {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  background: #ffffff;
  border: 1px solid #D9D5CD;
  border-radius: 10px;
  padding: 16px 18px;
  transition: border-color 150ms, box-shadow 150ms, transform 150ms;
  cursor: pointer;
}
.ev-card:hover { border-color: var(--accent); box-shadow: 0 6px 20px rgba(0,0,0,0.12); transform: translateY(-3px); }
.ev-card:hover .ev-card-title { color: var(--accent); }
.ev-card--ext  { text-decoration: none; }
.ev-card--ext:hover { border-color: #0E6B43; }

/* Date chip */
.ev-date {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: var(--accent-light);
  color: var(--accent);
  border: 1px solid var(--accent);
  border-radius: 8px;
  padding: 8px 12px;
  min-width: 46px;
  flex-shrink: 0;
}
.ev-date--blue   { background: #DFF3E8; color: #0E6B43; border-color: #0E6B43; }
.ev-day          { font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 700; line-height: 1; }
.ev-month        { font-family: 'DM Sans', sans-serif; font-size: 10px; text-transform: uppercase; letter-spacing: 0.05em; opacity: 0.8; margin-top: 2px; }
.ev-end-day      { font-family: 'DM Sans', sans-serif; font-size: 9px; opacity: 0.7; margin-top: 2px; white-space: nowrap; }

/* Card body */
.ev-body      { flex: 1; min-width: 0; }
.ev-card-top  { display: flex; align-items: flex-start; justify-content: space-between; gap: 8px; margin-bottom: 6px; }
.ev-card-title {
  font-family: 'DM Sans', sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: #1F1F1B;
  line-height: 1.4;
  flex: 1;
}
.ev-card--ext:hover .ev-card-title { color: #0E6B43; }

/* Type chips */
.ev-type-chip {
  font-family: 'DM Sans', sans-serif;
  font-size: 10px;
  font-weight: 700;
  text-transform: capitalize;
  padding: 2px 8px;
  border-radius: 4px;
  white-space: nowrap;
  flex-shrink: 0;
}
.ev-type-chip--green { background: #dcfce7; color: #166534; }
.ev-type-chip--blue  { background: #DFF3E8; color: #0E6B43; }

.ev-meta { display: flex; align-items: center; gap: 5px; font-family: 'DM Sans', sans-serif; font-size: 11px; color: #85837c; flex-wrap: wrap; }
.ev-org  { font-weight: 600; color: #0E6B43; }
.ev-ext-icon { margin-left: auto; color: #a8a69f; flex-shrink: 0; }
.dot     { opacity: 0.4; }

.ev-desc { font-family: 'DM Sans', sans-serif; font-size: 12px; color: #6E6A63; margin: 8px 0 0; line-height: 1.5; }

.ev-register {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin-top: 10px;
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  font-weight: 700;
  color: var(--accent);
  text-decoration: none;
  transition: opacity 150ms;
}
.ev-register:hover { opacity: 0.75; }

/* Empty state */
.ev-empty-state {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  color: #a8a69f;
  padding: 24px;
  text-align: center;
  border: 1px dashed #D9D5CD;
  border-radius: 8px;
}

@media (max-width: 640px) {
  .events-view { padding: 20px; }
  .ev-card     { padding: 14px; gap: 12px; }
}
</style>
