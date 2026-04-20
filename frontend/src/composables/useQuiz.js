import { ref } from 'vue'

const API = import.meta.env.VITE_API_URL ?? 'http://localhost:8001'

// Module-level singletons — persist across route navigation until hard refresh
const quiz         = ref(null)
const loading      = ref(false)
const error        = ref(null)
const results      = ref(null)
const leaderboard  = ref([])
const phase        = ref('gate')
const email        = ref('')
const emailError   = ref('')
const answers      = ref({})
const currentIndex = ref(0)
const submitting   = ref(false)

export function useQuiz() {
  async function fetchQuiz() {
    if (quiz.value) return
    loading.value = true
    error.value   = null
    try {
      const res  = await fetch(`${API}/api/quiz/today`)
      const json = await res.json()
      if (json.error) throw new Error(json.error.message)
      quiz.value = json.data
    } catch (e) {
      error.value = e.message || "Could not load today's quiz. Please try again later."
    } finally {
      loading.value = false
    }
  }

  async function submitAttempt(emailVal, answersVal) {
    const res = await fetch(`${API}/api/quiz/attempt`, {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ email: emailVal, quiz_date: quiz.value.quiz_date, answers: answersVal }),
    })
    const json = await res.json()
    if (json.error) throw new Error(json.error.message)
    results.value = json.data
    return json.data
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

  return {
    quiz, loading, error, results, leaderboard,
    phase, email, emailError, answers, currentIndex, submitting,
    fetchQuiz, submitAttempt, fetchLeaderboard,
  }
}
