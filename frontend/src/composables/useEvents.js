import { ref, computed } from 'vue'

const BASE = import.meta.env.VITE_API_URL ?? ''

// ── Module-level cache (shared across all useEvents() instances) ──────────────
const _dewa     = ref([])
const _external = ref([])
const _loading  = ref(false)
let   _fetched  = false

// ── Date helpers ──────────────────────────────────────────────────────────────

function todayIso() {
  return new Date().toISOString().slice(0, 10)
}

function addDays(iso, n) {
  const d = new Date(iso + 'T12:00:00')
  d.setDate(d.getDate() + n)
  return d.toISOString().slice(0, 10)
}

// ── Grouping logic ────────────────────────────────────────────────────────────

function groupByWeek(events) {
  const today = todayIso()
  const in7   = addDays(today, 7)
  const in14  = addDays(today, 14)
  return {
    thisWeek: events.filter(e => e.date >= today && e.date <  in7),
    nextWeek: events.filter(e => e.date >= in7   && e.date <  in14),
    upcoming: events.filter(e => e.date >= in14),
  }
}

// ── Loaders ───────────────────────────────────────────────────────────────────

async function _loadDewa() {
  const res  = await fetch('/data/dewa-events.json')
  const json = await res.json()
  return (json.events ?? []).sort((a, b) => a.date.localeCompare(b.date))
}

async function _loadExternal() {
  const res  = await fetch(`${BASE}/api/events/external`)
  const json = await res.json()
  if (json.error) throw new Error(json.error.message)
  return json.data?.events ?? []
}

async function _loadDubaiCurated() {
  const res  = await fetch(`${BASE}/api/events/dubai`)
  const json = await res.json()
  if (json.error) throw new Error(json.error.message)
  return json.data?.events ?? []
}

// ── Public composable ─────────────────────────────────────────────────────────

export function useEvents() {
  async function fetchEvents() {
    if (_fetched) return
    _loading.value = true
    try {
      const [dewa, dubai] = await Promise.allSettled([_loadDewa(), _loadDubaiCurated()])
      _dewa.value     = dewa.status  === 'fulfilled' ? dewa.value  : []
      _external.value = dubai.status === 'fulfilled' ? dubai.value : []
      if (dewa.status  === 'rejected') console.warn('DEWA events load failed:',   dewa.reason)
      if (dubai.status === 'rejected') console.warn('Dubai events load failed:',  dubai.reason)
    } finally {
      _loading.value = false
      _fetched       = true
    }
  }

  const grouped            = computed(() => groupByWeek(_external.value))
  const homeDewaEvents     = computed(() => _dewa.value.slice(0, 3))
  const homeExternalEvents = computed(() => _external.value.slice(0, 3))

  return {
    dewaEvents:          _dewa,
    externalEvents:      _external,
    grouped,
    homeDewaEvents,
    homeExternalEvents,
    loading:             _loading,
    fetchEvents,
  }
}
