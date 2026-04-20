<template>
  <div class="quiz-view">
    <header class="quiz-header">
      <h1 class="quiz-title">Test Your AI Knowledge</h1>
      <p class="quiz-subtitle">Daily quiz — 5 questions on top AI tools and their use cases.</p>
    </header>

    <div v-if="loading" class="state-msg">
      <Loader2 :size="20" class="spin" /> Loading today's quiz…
    </div>
    <div v-else-if="error" class="state-msg state-error">{{ error }}</div>

    <template v-else-if="quiz">
      <div class="quiz-layout">

        <!-- ── Left: quiz flow ──────────────────────────────── -->
        <div class="quiz-main">

          <!-- Gate -->
          <div v-if="phase === 'gate'" class="card">
            <p class="gate-intro">Enter your email to begin. Only your first attempt counts officially toward the leaderboard.</p>
            <div class="field">
              <label class="field-label">Work email</label>
              <input
                v-model="email"
                type="email"
                class="field-input"
                placeholder="you@dewa.gov.ae"
                @keyup.enter="startQuiz"
              />
              <p v-if="emailError" class="field-error">{{ emailError }}</p>
            </div>
            <button class="btn-primary" @click="startQuiz">Start Quiz</button>
            <div class="gate-covers">
              <span class="covers-label">Today's quiz covers</span>
              <div class="covers-chips">
                <span class="covers-chip">AI @ Work</span>
                <span class="covers-chip">Agents</span>
                <span class="covers-chip">Quick Tips</span>
                <span class="covers-chip">Claude</span>
                <span class="covers-chip">Advancements</span>
              </div>
            </div>
          </div>

          <!-- Active quiz -->
          <div v-else-if="phase === 'quiz'" class="card">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: progressPct + '%' }" />
            </div>
            <span class="progress-label">Question {{ currentIndex + 1 }} of {{ totalQ }}</span>
            <QuizQuestion
              :question="currentQ"
              :chosen="answers[currentQ.id] ?? null"
              :answered="!!answers[currentQ.id]"
              @answer="handleAnswer"
            />
            <button
              v-if="answers[currentQ.id]"
              class="btn-primary"
              :disabled="submitting"
              @click="nextQuestion"
            >
              {{ isLastQ ? (submitting ? 'Submitting…' : 'Submit Quiz') : 'Next Question' }}
            </button>
          </div>

          <!-- Results -->
          <div v-else-if="phase === 'results' && results" class="card">
            <div class="attempt-badge" :class="results.is_official ? 'official' : 'retake'">
              {{ results.is_official ? 'Official attempt — counted on leaderboard' : 'Practice retake — not counted' }}
            </div>
            <p class="results-blurb">
              Check the panel on the right for your score and today's leaderboard.
            </p>
            <button class="btn-secondary" @click="retake">Try Again (practice)</button>
          </div>

        </div>

        <!-- ── Right: context panel ─────────────────────────── -->
        <aside class="quiz-panel">

          <!-- Gate panel -->
          <div v-if="phase === 'gate'" class="panel-card">
            <div class="panel-date">{{ formattedDate }}</div>
            <div class="panel-divider" />
            <div class="panel-count">
              <span v-if="attemptCount === 0" class="count-zero">Be the first today!</span>
              <template v-else>
                <span class="count-num">{{ attemptCount }}</span>
                <span class="count-label">
                  {{ attemptCount === 1 ? 'colleague has' : 'colleagues have' }} played today
                </span>
              </template>
            </div>
            <div class="panel-divider" />
            <p class="panel-note">Your first attempt is your official score. Retakes are practice only.</p>
          </div>

          <!-- Quiz panel -->
          <div v-else-if="phase === 'quiz'" class="panel-card">
            <div class="panel-progress-header">
              <span class="panel-q-num">
                {{ currentIndex + 1 }}<span class="panel-q-total"> / {{ totalQ }}</span>
              </span>
              <span class="panel-q-label">Questions answered</span>
            </div>
            <div class="panel-steps">
              <div
                v-for="n in totalQ"
                :key="n"
                class="step-dot"
                :class="{
                  'step-done':    answers[quiz.questions[n - 1]?.id],
                  'step-current': n - 1 === currentIndex && !answers[quiz.questions[n - 1]?.id],
                }"
              />
            </div>
            <p class="panel-tip">{{ currentTip }}</p>
          </div>

          <!-- Results panel -->
          <div v-else-if="phase === 'results' && results" class="panel-card panel-results">
            <div class="score-ring">
              <span class="score-pct">{{ Math.round(results.percentage) }}%</span>
              <span class="score-fraction">{{ results.score }}/{{ results.total }}</span>
            </div>
            <p class="band-msg">{{ bandMessage }}</p>
            <div v-if="isFirstToday" class="first-today-msg">
              You're the first one today — the leaderboard starts with you.
            </div>
          </div>

        </aside>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { Loader2 } from 'lucide-vue-next'
import QuizQuestion from '../components/QuizQuestion.vue'
import { useQuiz } from '../composables/useQuiz.js'

const {
  quiz, loading, error, results, leaderboard,
  phase, email, emailError, answers, currentIndex, submitting,
  fetchQuiz, submitAttempt, fetchLeaderboard,
} = useQuiz()

onMounted(() => { if (!quiz.value) fetchQuiz() })

const totalQ       = computed(() => quiz.value?.questions?.length ?? 0)
const currentQ     = computed(() => quiz.value?.questions?.[currentIndex.value])
const isLastQ      = computed(() => currentIndex.value === totalQ.value - 1)
const progressPct  = computed(() => totalQ.value ? (currentIndex.value / totalQ.value) * 100 : 0)
const attemptCount = computed(() => quiz.value?.attempt_count ?? 0)

const formattedDate = computed(() =>
  new Date().toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
)

const TIPS = [
  'Take your time — you can\'t go back.',
  'Trust your first instinct.',
  'More than halfway — keep going.',
  'Almost there — stay focused.',
]
const currentTip = computed(() => TIPS[Math.min(Math.floor(currentIndex.value / 2), TIPS.length - 1)])

const SCORE_BANDS = [
  { min: 100, msg: 'Every question right. Strong across the board.' },
  { min: 80,  msg: 'Strong result. A couple of gaps, but solid knowledge overall.' },
  { min: 60,  msg: 'Good performance. A few areas worth revisiting.' },
  { min: 40,  msg: 'A reasonable start. The gaps are worth exploring.' },
  { min: 20,  msg: "Some ground to cover — that's exactly what the daily quiz is for." },
  { min: 0,   msg: 'Tough one today. Tomorrow is a fresh set of questions.' },
]
const bandMessage = computed(() => {
  const pct = results.value?.percentage ?? 0
  return SCORE_BANDS.find(b => pct >= b.min)?.msg ?? ''
})

const userMaskedEmail = computed(() => {
  const v = email.value.trim().toLowerCase()
  if (!v.includes('@')) return null
  const [local, domain] = v.split('@')
  return `${local.slice(0, 2)}***@${domain}`
})

const isFirstToday = computed(() =>
  results.value?.is_official && leaderboard.value?.length === 1
)

function medalFor(rank) {
  return rank === 1 ? '🥇' : rank === 2 ? '🥈' : rank === 3 ? '🥉' : `#${rank}`
}

function startQuiz() {
  emailError.value = ''
  const v = email.value.trim()
  if (!v || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)) {
    emailError.value = 'Please enter a valid email address.'
    return
  }
  phase.value = 'quiz'
}

function handleAnswer(questionId, chosen) {
  if (answers.value[questionId]) return
  answers.value[questionId] = chosen
}

async function nextQuestion() {
  if (!isLastQ.value) {
    currentIndex.value++
    return
  }
  submitting.value = true
  try {
    await submitAttempt(email.value.trim(), answers.value)
    await fetchLeaderboard(quiz.value.quiz_date)
    phase.value = 'results'
  } catch (e) {
    error.value = e.message
  } finally {
    submitting.value = false
  }
}

function retake() {
  answers.value      = {}
  currentIndex.value = 0
  phase.value        = 'quiz'
}
</script>

<style scoped>
.quiz-view { padding: 20px 40px; max-width: 1020px; --accent: #d93535; --accent-light: #fee2e2; }

.quiz-header { border-left: 4px solid var(--accent, #166534); border-bottom: 1px solid #e2e0dc; border-radius: 0 6px 0 0; background: #f8f7f5; padding: 14px 18px; margin-bottom: 20px; }
.quiz-title    { font-family: 'Space Grotesk', sans-serif; font-size: 22px; font-weight: 700; color: #1a1917; margin: 0 0 4px; }
.quiz-subtitle { font-family: 'DM Sans', sans-serif; font-size: 13px; color: #65635d; margin: 0; }

.state-msg   { display: flex; align-items: center; gap: 10px; font-family: 'DM Sans', sans-serif; font-size: 15px; color: #65635d; padding: 60px 0; }
.state-error { color: #d64545; }
.spin        { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Two-column layout ──────────────────────────────────────── */
.quiz-layout {
  display: grid;
  grid-template-columns: 1fr 280px;
  gap: 24px;
  align-items: start;
}

/* ── Left: main cards ───────────────────────────────────────── */
.card {
  background: #f8f7f5;
  border: 1px solid #e2e0dc;
  border-top: 3px solid var(--accent, #166534);
  border-radius: 10px;
  padding: 28px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.gate-intro  { font-family: 'DM Sans', sans-serif; font-size: 14px; color: #65635d; margin: 0; line-height: 1.6; }

.gate-covers { display: flex; flex-direction: column; gap: 8px; padding-top: 16px; border-top: 1px solid #e2e0dc; }
.covers-label { font-family: 'DM Sans', sans-serif; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: #a8a69f; }
.covers-chips { display: flex; flex-wrap: wrap; gap: 6px; }
.covers-chip  { font-family: 'DM Sans', sans-serif; font-size: 12px; font-weight: 500; color: #65635d; background: #f0efe9; border: 1px solid #e2e0dc; border-radius: 20px; padding: 4px 12px; }
.field       { display: flex; flex-direction: column; gap: 6px; }
.field-label { font-family: 'DM Sans', sans-serif; font-size: 12px; font-weight: 700; color: #3a3834; text-transform: uppercase; letter-spacing: 0.05em; }
.field-input { padding: 10px 14px; border: 1.5px solid #e2e0dc; border-radius: 7px; font-family: 'DM Sans', sans-serif; font-size: 14px; background: #fff; outline: none; transition: border-color 150ms; }
.field-input:focus { border-color: #166534; }
.field-error { font-family: 'DM Sans', sans-serif; font-size: 12px; color: #dc2626; margin: 0; }

.progress-bar  { height: 4px; background: #e2e0dc; border-radius: 2px; overflow: hidden; }
.progress-fill { height: 100%; background: #166534; transition: width 300ms ease; }
.progress-label { font-family: 'DM Sans', sans-serif; font-size: 11px; color: #a8a69f; margin-top: -12px; }

.btn-primary  { padding: 11px 24px; background: #166534; color: #fff; border: none; border-radius: 7px; font-family: 'DM Sans', sans-serif; font-size: 14px; font-weight: 600; cursor: pointer; transition: opacity 150ms; align-self: flex-start; }
.btn-primary:hover:not(:disabled) { opacity: 0.85; }
.btn-primary:disabled { opacity: 0.5; cursor: default; }
.btn-secondary { padding: 9px 20px; background: transparent; color: #166534; border: 1.5px solid #166534; border-radius: 7px; font-family: 'DM Sans', sans-serif; font-size: 13px; font-weight: 600; cursor: pointer; transition: background 150ms; align-self: flex-start; }
.btn-secondary:hover { background: #f0fdf4; }

.attempt-badge { align-self: flex-start; font-family: 'DM Sans', sans-serif; font-size: 12px; font-weight: 700; padding: 5px 14px; border-radius: 20px; }
.attempt-badge.official { background: #dcfce7; color: #16a34a; }
.attempt-badge.retake   { background: #fef9c3; color: #a16207; }

.results-blurb { font-family: 'DM Sans', sans-serif; font-size: 13px; color: #85837c; margin: 0; line-height: 1.6; }

/* ── Right: context panel ───────────────────────────────────── */
.quiz-panel { position: sticky; top: 20px; }

.panel-card {
  background: #ffffff;
  border: 1px solid #e2e0dc;
  border-top: 3px solid var(--accent, #166534);
  border-radius: 10px;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.panel-date {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: #1a1917;
  text-align: center;
}
.panel-divider { height: 1px; background: #f0efe9; }

.panel-count  { display: flex; flex-direction: column; align-items: center; gap: 4px; text-align: center; }
.count-zero {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 17px;
  font-weight: 700;
  color: #1a1917;
}
.count-num {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 40px;
  font-weight: 700;
  color: #1a1917;
  line-height: 1;
}
.count-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  color: #65635d;
  line-height: 1.4;
}
.panel-note {
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  color: #a8a69f;
  margin: 0;
  line-height: 1.6;
}

/* Quiz progress panel */
.panel-progress-header { display: flex; flex-direction: column; gap: 4px; }
.panel-q-num {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 44px;
  font-weight: 700;
  color: #166534;
  line-height: 1;
}
.panel-q-total { font-size: 22px; color: #a8a69f; }
.panel-q-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 11px;
  font-weight: 600;
  color: #a8a69f;
  text-transform: uppercase;
  letter-spacing: 0.07em;
}
.panel-steps { display: flex; flex-wrap: wrap; gap: 6px; }
.step-dot {
  width: 26px;
  height: 6px;
  border-radius: 3px;
  background: #e2e0dc;
  transition: background 250ms;
}
.step-done    { background: #166534; }
.step-current { background: #86efac; }
.panel-tip {
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  color: #a8a69f;
  margin: 0;
  line-height: 1.6;
  font-style: italic;
}

/* Results panel */
.panel-results   { gap: 20px; }
.score-ring      { text-align: center; padding: 12px 0 4px; }
.score-pct       { display: block; font-family: 'Space Grotesk', sans-serif; font-size: 56px; font-weight: 700; color: #166534; line-height: 1; }
.score-fraction  { display: block; font-family: 'DM Sans', sans-serif; font-size: 15px; color: #a8a69f; margin-top: 6px; }
.band-msg        { font-family: 'DM Sans', sans-serif; font-size: 13px; color: #1a1917; text-align: center; margin: 0; line-height: 1.6; }
.first-today-msg {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 15px;
  font-weight: 700;
  color: #166534;
  text-align: center;
  line-height: 1.5;
  padding-top: 14px;
  border-top: 2px solid #dcfce7;
}

/* ── Responsive ─────────────────────────────────────────────── */
@media (max-width: 860px) {
  .quiz-layout { grid-template-columns: 1fr; }
  .quiz-panel  { position: static; order: -1; }
}
@media (max-width: 640px) {
  .quiz-view { padding: 20px; }
}
</style>
