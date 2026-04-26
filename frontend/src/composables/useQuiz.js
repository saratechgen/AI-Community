import { ref, computed } from 'vue'

const API = import.meta.env.VITE_API_URL ?? 'http://localhost:8001'

// Module-level: pure data cache — safe to share across navigations
const _quiz        = ref(null)
const _leaderboard = ref([])

function getDeviceId() {
  const KEY = 'quiz_device_id'
  let id = localStorage.getItem(KEY)
  if (!id) {
    id = crypto.randomUUID()
    localStorage.setItem(KEY, id)
  }
  return id
}

export function useQuiz() {
  // Session state — local per component instance, resets cleanly on every mount
  const loading         = ref(false)
  const error           = ref(null)
  const phase           = ref('gate')   // 'gate' | 'welcome' | 'quiz' | 'stage-result' | 'final'
  const email           = ref(getDeviceId())
  const emailError      = ref('')
  const username        = ref('')
  const usernameError   = ref('')
  const currentStage    = ref(1)
  const answers         = ref({})
  const currentIndex    = ref(0)
  const submitting      = ref(false)
  const stageResults    = ref({})       // latest result per stage (includes practice)
  const officialResults = ref({})       // first (official) result per stage — server-authoritative

  const quiz        = _quiz
  const leaderboard = _leaderboard

  async function fetchQuiz() {
    if (quiz.value?.stages) {
      fetchLeaderboard(quiz.value.quiz_date)  // refresh leaderboard on re-entry
      return
    }
    loading.value = true
    error.value   = null
    try {
      const res  = await fetch(`${API}/api/quiz/today`)
      const json = await res.json()
      if (json.error) throw new Error(json.error.message)
      quiz.value = json.data
      fetchLeaderboard(json.data.quiz_date)  // pre-load so gate screen shows standings
    } catch (e) {
      error.value = e.message || "Could not load today's quiz. Please try again later."
    } finally {
      loading.value = false
    }
  }

  // Restore today's official stage results from the server for a given email.
  // Must be called before routing after email entry — makes unlockedStages
  // authoritative from DB rather than from possibly-missing local state.
  async function loadStageStatus(emailVal) {
    if (!quiz.value?.quiz_date) return
    try {
      const url  = `${API}/api/quiz/stage-status?email=${encodeURIComponent(emailVal.trim().toLowerCase())}&quiz_date=${quiz.value.quiz_date}`
      const res  = await fetch(url)
      const json = await res.json()
      if (json.error || !json.data) return
      const restored = {}
      for (const [s, st] of Object.entries(json.data)) {
        if (st.attempted) {
          restored[Number(s)] = { score: st.score, passed: st.passed, is_official: true }
        }
      }
      officialResults.value = restored
    } catch { /* network error — proceed with empty state */ }
  }

  async function submitStageAttempt(emailVal, usernameVal, stage, answersVal) {
    const res = await fetch(`${API}/api/quiz/attempt`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({
        email:     emailVal,
        username:  usernameVal,
        quiz_date: quiz.value.quiz_date,
        stage,
        answers:   answersVal,
      }),
    })
    const json = await res.json()
    if (json.error) throw new Error(json.error.message)
    const result = json.data
    stageResults.value = { ...stageResults.value, [stage]: result }
    if (result.is_official) {
      officialResults.value = { ...officialResults.value, [stage]: result }
    }
    return result
  }

  async function fetchLeaderboard(quizDate) {
    try {
      const res  = await fetch(`${API}/api/quiz/leaderboard?quiz_date=${quizDate}`)
      const json = await res.json()
      leaderboard.value = json.data ?? []
    } catch {
      leaderboard.value = []
    }
  }

  // Stage 2 unlocks only when official Stage 1 score >= 4
  // Stage 3 unlocks only when official Stage 2 score >= 4
  const unlockedStages = computed(() => {
    const unlocked = new Set([1])
    if (officialResults.value[1]?.passed) unlocked.add(2)
    if (officialResults.value[2]?.passed) unlocked.add(3)
    return unlocked
  })

  const totalScore = computed(() =>
    [1, 2, 3].reduce((sum, s) => sum + (officialResults.value[s]?.score ?? 0), 0)
  )

  const highestStageCleared = computed(() => {
    let highest = 0
    for (const s of [1, 2, 3]) {
      if (officialResults.value[s]?.passed) highest = s
    }
    return highest
  })

  const currentStageData = computed(() =>
    quiz.value?.stages?.find(s => s.stage === currentStage.value) ?? null
  )

  return {
    quiz, loading, error, phase,
    email, emailError, username, usernameError,
    currentStage, currentStageData,
    answers, currentIndex, submitting,
    stageResults, officialResults, leaderboard,
    unlockedStages, totalScore, highestStageCleared,
    fetchQuiz, loadStageStatus, submitStageAttempt, fetchLeaderboard,
  }
}
