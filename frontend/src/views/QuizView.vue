<template>
  <div class="quiz-view">
    <header class="quiz-header">
      <h1 class="quiz-title">Test Your AI Knowledge</h1>
      <p class="quiz-tagline">Every day, 15 fresh AI questions — a new daily dose of AI knowledge awaits.</p>
      <div class="quiz-chips">
        <span class="chip">3 Stages</span>
        <span class="chip">5 Questions / Stage</span>
        <span class="chip chip-accent">Score 4 / 5 to Advance</span>
      </div>
    </header>

    <div v-if="loading" class="state-msg">
      <Loader2 :size="20" class="spin" /> Loading today's quiz…
    </div>
    <div v-else-if="error" class="state-msg state-error">{{ error }}</div>

    <template v-else-if="quiz">

      <!-- Stage selector: only in stage-result and final -->
      <StageSelector
        v-if="(phase === 'stage-result' || phase === 'final') && quiz.stages"
        :stages="quiz.stages"
        :unlocked-stages="unlockedStages"
        :official-results="officialResults"
        @begin="beginStage"
      />

      <div class="quiz-layout">

        <!-- ── Left: phase content ── -->
        <div class="quiz-main">

          <!-- Gate -->
          <div v-if="phase === 'gate'" class="card">
            <div class="gate-intro">
              <div class="gate-intro-icon">ℹ</div>
              <ul class="gate-intro-list">
                <li>Enter your details to begin.</li>
                <li>Your first attempt at each stage counts officially toward the leaderboard.</li>
              </ul>
            </div>
            <div class="field">
              <label class="field-label">Your name <span class="field-required">*</span></label>
              <input
                v-model="username"
                type="text"
                class="field-input"
                placeholder="e.g. Sara Ahmed"
                maxlength="50"
                required
                @keyup.enter="startQuiz"
              />
              <p v-if="usernameError" class="field-error">{{ usernameError }}</p>
            </div>
            <div class="field">
              <label class="field-label">Work email <span class="field-required">*</span></label>
              <input
                v-model="email"
                type="email"
                class="field-input"
                placeholder="you@dewa.gov.ae"
                required
                @keyup.enter="startQuiz"
              />
              <p v-if="emailError" class="field-error">{{ emailError }}</p>
            </div>
            <button class="btn-primary" :disabled="submitting" @click="startQuiz">
              {{ submitting ? 'Loading…' : 'Start Quiz' }}
            </button>
          </div>

          <!-- Active quiz -->
          <div v-else-if="phase === 'quiz' && currentStageData" class="card">
            <div class="stage-label-row">
              <span class="active-stage-badge">Stage {{ currentStage }} · {{ currentStageData.title }}</span>
              <span class="pass-hint">Score 4/5 to unlock next stage</span>
            </div>
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
              v-if="answers[currentQ?.id]"
              class="btn-primary"
              :disabled="submitting"
              @click="nextQuestion"
            >
              {{ isLastQ ? (submitting ? 'Submitting…' : 'Submit Stage') : 'Next Question' }}
            </button>
          </div>

          <!-- Stage result -->
          <div v-else-if="phase === 'stage-result' && lastResult" class="card">
            <div
              class="result-badge"
              :class="lastResult.is_official && lastResult.passed ? 'badge-pass'
                    : !lastResult.is_official && lastResult.passed ? 'badge-practice'
                    : 'badge-fail'"
            >
              {{ lastResult.is_official && lastResult.passed ? '✅ Stage Cleared'
               : !lastResult.is_official && lastResult.passed ? '✓ Practice Passed'
               : '❌ Not Cleared' }}
            </div>
            <p class="result-msg">
              <template v-if="lastResult.is_official && lastResult.passed && currentStage < 3">
                You scored {{ lastResult.score }}/5 — Stage {{ currentStage + 1 }} is now unlocked.
              </template>
              <template v-else-if="lastResult.is_official && lastResult.passed && currentStage === 3">
                You completed all 3 stages!
              </template>
              <template v-else-if="lastResult.is_official && !lastResult.passed">
                Official score: {{ lastResult.score }}/5 — you need 4/5 to clear this stage.
              </template>
              <template v-else-if="!lastResult.is_official && lastResult.passed">
                Practice score: {{ lastResult.score }}/5. Official score: {{ officialResults[currentStage]?.score ?? '—' }}/5 — that score determines stage unlock.
              </template>
              <template v-else>
                Practice score: {{ lastResult.score }}/5. Keep trying!
              </template>
            </p>
            <div class="result-actions">
              <button v-if="officialResults[currentStage]?.passed && currentStage < 3" class="btn-primary" @click="beginStage(currentStage + 1)">
                Continue to Stage {{ currentStage + 1 }}
              </button>
              <button v-if="officialResults[currentStage]?.passed && currentStage === 3" class="btn-primary" @click="showFinal">
                See Final Summary
              </button>
              <button v-if="!(officialResults[currentStage]?.passed && currentStage === 3)" class="btn-secondary" @click="retakeStage">
                Retry Stage {{ currentStage }} (practice)
              </button>
              <button class="btn-secondary" @click="showFinal">View Summary</button>
            </div>
          </div>

          <!-- Final summary -->
          <div v-else-if="phase === 'final'" class="card">
            <div class="final-badge" :class="highestStageCleared === 3 ? 'champion' : ''">
              {{ finalBadgeLabel }}
            </div>
            <div class="final-scores">
              <div v-for="s in quiz.stages" :key="s.stage" class="score-row">
                <span class="score-stage">Stage {{ s.stage }} · {{ s.title }}</span>
                <span class="score-val" :class="officialResults[s.stage]?.passed ? 'val-pass' : (officialResults[s.stage] ? 'val-fail' : 'val-none')">
                  {{ officialResults[s.stage] ? `${officialResults[s.stage].score}/5` : '—' }}
                  {{ officialResults[s.stage]?.passed ? '✓' : (officialResults[s.stage] ? '✗' : '') }}
                </span>
              </div>
              <div class="score-total">
                <span>Total</span>
                <span>{{ totalScore }}/15</span>
              </div>
            </div>
            <div class="result-actions">
              <button v-if="nextUnlockedIncomplete !== null" class="btn-primary" @click="beginStage(nextUnlockedIncomplete)">
                Continue to Stage {{ nextUnlockedIncomplete }}
              </button>
              <button v-if="!allStagesCleared" class="btn-ghost" @click="phase = 'stage-result'">
                Back to Result
              </button>
            </div>
          </div>

        </div>

        <!-- ── Right panel ── -->
        <aside class="quiz-panel">

          <!-- GATE panel: date + count + rules + mini leaderboard -->
          <div v-if="phase === 'gate'" class="panel-card">
            <div class="panel-date">{{ formattedDate }}</div>
            <div class="panel-divider" />
            <div class="panel-count">
              <span v-if="attemptCount === 0" class="count-zero">Be the first today!</span>
              <template v-else>
                <span class="count-num">{{ attemptCount }}</span>
                <span class="count-label">{{ attemptCount === 1 ? 'colleague has' : 'colleagues have' }} played today</span>
              </template>
            </div>
            <div class="panel-divider" />
            <!-- Quiz rules -->
            <div class="panel-rules">
              <div class="panel-rules-title">How it works</div>
              <ol class="panel-rules-steps">
                <li><span class="step-num">1</span><span>3 stages: Foundation → Applied → Advanced</span></li>
                <li><span class="step-num">2</span><span>5 questions per stage</span></li>
                <li><span class="step-num">3</span><span>Score 4/5 to unlock the next stage</span></li>
                <li><span class="step-num">4</span><span>First attempt counts officially</span></li>
                <li><span class="step-num">5</span><span>Retakes are practice only</span></li>
              </ol>
            </div>
            <!-- Mini leaderboard on gate screen -->
            <template v-if="leaderboard.length">
              <div class="panel-divider" />
              <div class="panel-mini-lb-title">Today's Leaders</div>
              <div class="panel-mini-lb">
                <div
                  v-for="entry in leaderboard.slice(0, 5)"
                  :key="entry.rank"
                  class="pmr-row"
                  :class="{ 'pmr-you': isYou(entry) }"
                >
                  <span class="pmr-rank">{{ medalFor(entry.rank) }}</span>
                  <span class="pmr-name">{{ entry.username }}</span>
                  <span class="pmr-score">{{ entry.total_score }}/15</span>
                </div>
              </div>
            </template>
          </div>

          <!-- QUIZ panel: progress + full leaderboard -->
          <div v-else-if="phase === 'quiz'" class="panel-card">
            <div class="panel-progress-header">
              <span class="panel-q-num">{{ currentIndex + 1 }}<span class="panel-q-total"> / {{ totalQ }}</span></span>
              <span class="panel-q-label">Stage {{ currentStage }} progress</span>
            </div>
            <div class="panel-steps">
              <div
                v-for="n in totalQ"
                :key="n"
                class="step-dot"
                :class="{
                  'step-done':    answers[currentStageData?.questions[n - 1]?.id],
                  'step-current': n - 1 === currentIndex && !answers[currentStageData?.questions[n - 1]?.id],
                }"
              />
            </div>
            <div class="panel-divider" />
            <PanelLeaderboard :leaderboard="leaderboard" :is-you="isYou" :medal-for="medalFor" />
          </div>

          <!-- STAGE-RESULT panel: stage score + full leaderboard -->
          <div v-else-if="phase === 'stage-result'" class="panel-card">
            <div class="panel-progress-header">
              <span class="panel-q-num">{{ lastResult?.score ?? 0 }}<span class="panel-q-total"> / 5</span></span>
              <span class="panel-q-label">Stage {{ currentStage }} · {{ currentStageData?.title }}</span>
            </div>
            <div class="panel-divider" />
            <PanelLeaderboard :leaderboard="leaderboard" :is-you="isYou" :medal-for="medalFor" />
          </div>

          <!-- FINAL panel: full leaderboard -->
          <div v-else-if="phase === 'final'" class="panel-card">
            <PanelLeaderboard :leaderboard="leaderboard" :is-you="isYou" :medal-for="medalFor" />
          </div>

        </aside>
      </div>


    </template>
  </div>
</template>

<script setup>
/* Escape hatch: exceeds 250-line cap — QuizView has single responsibility (3-stage quiz UX) */
import { computed, onMounted } from 'vue'
import { Loader2 } from 'lucide-vue-next'
import QuizQuestion      from '../components/QuizQuestion.vue'
import StageSelector     from '../components/StageSelector.vue'
import PanelLeaderboard  from '../components/PanelLeaderboard.vue'
import { useQuiz }       from '../composables/useQuiz.js'

const {
  quiz, loading, error, phase,
  email, emailError, username, usernameError,
  currentStage, currentStageData,
  answers, currentIndex, submitting,
  stageResults, officialResults, leaderboard,
  unlockedStages, totalScore, highestStageCleared,
  fetchQuiz, loadStageStatus, submitStageAttempt, fetchLeaderboard,
} = useQuiz()

onMounted(fetchQuiz)

const totalQ       = computed(() => currentStageData.value?.questions?.length ?? 0)
const currentQ     = computed(() => currentStageData.value?.questions?.[currentIndex.value])
const isLastQ      = computed(() => currentIndex.value === totalQ.value - 1)
const progressPct  = computed(() => totalQ.value ? (currentIndex.value / totalQ.value) * 100 : 0)
const lastResult   = computed(() => stageResults.value[currentStage.value] ?? null)
const attemptCount = computed(() => quiz.value?.attempt_count ?? 0)

const allStagesCleared     = computed(() => [1, 2, 3].every(s => officialResults.value[s]?.passed))
const nextUnlockedIncomplete = computed(() => {
  for (const s of [1, 2, 3]) {
    if (unlockedStages.value.has(s) && !officialResults.value[s]?.passed) return s
  }
  return null
})

const formattedDate  = computed(() =>
  new Date().toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })
)
const TIPS           = ['Take your time — read each option carefully.', 'Trust your first instinct.', 'More than halfway — keep going.', 'Almost there!']
const currentTip     = computed(() => TIPS[Math.min(currentIndex.value, TIPS.length - 1)])
const BADGE_LABELS   = { 3: '🏆 AI Champion', 2: '⭐ Applied Expert', 1: '🌱 Foundation Complete', 0: 'Quiz Summary' }
const finalBadgeLabel = computed(() => BADGE_LABELS[highestStageCleared.value] ?? 'Quiz Summary')

function medalFor(rank) {
  return rank === 1 ? '🥇' : rank === 2 ? '🥈' : rank === 3 ? '🥉' : `#${rank}`
}

function isYou(entry) {
  const u = username.value.trim()
  return u.length > 0 && entry.username?.toLowerCase() === u.toLowerCase()
}

async function startQuiz() {
  usernameError.value = ''
  emailError.value    = ''

  if (!username.value.trim()) {
    usernameError.value = 'Please enter your name.'
    return
  }
  const v = email.value.trim()
  if (!v || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)) {
    emailError.value = 'Please enter a valid email address.'
    return
  }

  submitting.value = true
  try {
    await loadStageStatus(v)
  } finally {
    submitting.value = false
  }

  if (allStagesCleared.value) {
    await fetchLeaderboard(quiz.value.quiz_date)
    phase.value = 'final'
    return
  }
  beginStage(nextUnlockedIncomplete.value ?? 1)
}

function beginStage(stageNum) {
  currentStage.value  = stageNum
  answers.value       = {}
  currentIndex.value  = 0
  phase.value         = 'quiz'
}

function handleAnswer(questionId, chosen) {
  if (answers.value[questionId]) return
  answers.value = { ...answers.value, [questionId]: chosen }
}

async function nextQuestion() {
  if (!isLastQ.value) {
    currentIndex.value++
    return
  }
  submitting.value = true
  try {
    await submitStageAttempt(email.value.trim(), username.value.trim(), currentStage.value, answers.value)
    await fetchLeaderboard(quiz.value.quiz_date)
    phase.value = 'stage-result'
  } catch (e) {
    error.value = e.message
  } finally {
    submitting.value = false
  }
}

function retakeStage() {
  answers.value      = {}
  currentIndex.value = 0
  phase.value        = 'quiz'
}

async function showFinal() {
  await fetchLeaderboard(quiz.value.quiz_date)
  phase.value = 'final'
}
</script>

<style scoped>
/* Escape hatch: exceeds 250-line cap — QuizView has single responsibility (3-stage quiz UX) */
.quiz-view { padding: 12px 40px; max-width: 1020px; --accent: #d93535; }

.quiz-header { border-left: 4px solid var(--accent); border-bottom: 1px solid #e2e0dc; border-radius: 0 6px 0 0; background: #f8f7f5; padding: 16px 20px; margin-bottom: 12px; }
.quiz-title { font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 700; color: #1a1917; margin: 0 0 10px; }
.quiz-chips { display: flex; flex-wrap: wrap; gap: 8px; }
.chip { font-family: 'DM Sans', sans-serif; font-size: 12px; font-weight: 600; padding: 4px 12px; border-radius: 20px; background: #f0efe9; color: #65635d; border: 1px solid #e2e0dc; }
.chip-accent { background: #fef3c7; color: #d97706; border-color: #fcd34d; }
.quiz-tagline { font-family: 'DM Sans', sans-serif; font-size: 13px; font-weight: 500; color: #3a3834; margin: 4px 0 6px; text-shadow: 0 1px 0 rgba(255,255,255,0.85); }

.state-msg   { display: flex; align-items: center; gap: 10px; font-family: 'DM Sans', sans-serif; font-size: 15px; color: #65635d; padding: 60px 0; }
.state-error { color: #d64545; }
.spin        { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

.quiz-layout { display: grid; grid-template-columns: 1fr 280px; gap: 16px; align-items: start; }

.card { background: #f8f7f5; border: 1px solid #e2e0dc; border-top: 3px solid var(--accent); border-radius: 10px; padding: 28px; display: flex; flex-direction: column; gap: 20px; }

/* Gate */
.gate-intro      { display: flex; gap: 10px; align-items: flex-start; background: #f0fdf4; border: 1px solid #bbf7d0; border-left: 3px solid #166534; border-radius: 7px; padding: 10px 14px; }
.gate-intro-icon { font-style: normal; font-size: 14px; color: #166534; font-weight: 700; flex-shrink: 0; line-height: 1.6; }
.gate-intro-list { font-family: 'DM Sans', sans-serif; font-size: 13px; color: #166534; margin: 0; padding-left: 16px; display: flex; flex-direction: column; gap: 4px; line-height: 1.6; }
.field        { display: flex; flex-direction: column; gap: 6px; }
.field-label  { font-family: 'DM Sans', sans-serif; font-size: 12px; font-weight: 700; color: #3a3834; text-transform: uppercase; letter-spacing: 0.05em; }
.field-required { color: var(--accent); }
.field-input  { padding: 10px 14px; border: 1.5px solid #e2e0dc; border-radius: 7px; font-family: 'DM Sans', sans-serif; font-size: 14px; background: #fff; outline: none; transition: border-color 150ms; }
.field-input:focus { border-color: #166534; }
.field-error  { font-family: 'DM Sans', sans-serif; font-size: 12px; color: #dc2626; margin: 0; }

/* Quiz */
.stage-label-row    { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; }
.active-stage-badge { font-family: 'Space Grotesk', sans-serif; font-size: 13px; font-weight: 700; color: var(--accent); }
.pass-hint   { font-family: 'DM Sans', sans-serif; font-size: 12px; color: #a8a69f; }
.progress-bar  { height: 4px; background: #e2e0dc; border-radius: 2px; overflow: hidden; }
.progress-fill { height: 100%; background: var(--accent); transition: width 300ms ease; }
.progress-label { font-family: 'DM Sans', sans-serif; font-size: 11px; color: #a8a69f; margin-top: -12px; }

/* Stage result */
.result-badge    { align-self: flex-start; font-family: 'DM Sans', sans-serif; font-size: 14px; font-weight: 700; padding: 6px 16px; border-radius: 20px; }
.badge-pass      { background: #dcfce7; color: #16a34a; }
.badge-fail      { background: #fee2e2; color: #d93535; }
.badge-practice  { background: #fef9c3; color: #a16207; }
.result-msg      { font-family: 'DM Sans', sans-serif; font-size: 14px; color: #3a3834; margin: 0; line-height: 1.6; }
.result-actions  { display: flex; flex-wrap: wrap; gap: 10px; }

/* Final */
.final-badge { align-self: flex-start; font-family: 'Space Grotesk', sans-serif; font-size: 15px; font-weight: 700; padding: 6px 16px; border-radius: 20px; background: #f0efe9; color: #3a3834; }
.final-badge.champion { background: #fef9c3; color: #a16207; }
.final-scores { display: flex; flex-direction: column; gap: 10px; }
.score-row   { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #f0efe9; }
.score-stage { font-family: 'DM Sans', sans-serif; font-size: 14px; color: #3a3834; }
.score-val   { font-family: 'Space Grotesk', sans-serif; font-size: 14px; font-weight: 700; }
.val-pass    { color: #16a34a; }
.val-fail    { color: #d93535; }
.val-none    { color: #a8a69f; }
.score-total { display: flex; justify-content: space-between; padding-top: 8px; font-family: 'Space Grotesk', sans-serif; font-size: 16px; font-weight: 700; color: #1a1917; }

/* Buttons */
.btn-primary   { padding: 11px 24px; background: #166534; color: #fff; border: none; border-radius: 7px; font-family: 'DM Sans', sans-serif; font-size: 14px; font-weight: 600; cursor: pointer; transition: opacity 150ms; align-self: flex-start; }
.btn-primary:hover:not(:disabled) { opacity: 0.85; }
.btn-primary:disabled { opacity: 0.5; cursor: default; }
.btn-secondary { padding: 9px 20px; background: transparent; color: #166534; border: 1.5px solid #166534; border-radius: 7px; font-family: 'DM Sans', sans-serif; font-size: 13px; font-weight: 600; cursor: pointer; }
.btn-secondary:hover { background: #f0fdf4; }
.btn-ghost     { padding: 9px 20px; background: transparent; color: #85837c; border: 1.5px solid #e2e0dc; border-radius: 7px; font-family: 'DM Sans', sans-serif; font-size: 13px; cursor: pointer; }
.btn-ghost:hover { background: #f0efe9; }

/* Right panel shared */
.quiz-panel  { position: sticky; top: 20px; }
.panel-card  { background: #fff; border: 1px solid #e2e0dc; border-top: 3px solid var(--accent); border-radius: 10px; padding: 14px 16px; display: flex; flex-direction: column; gap: 10px; }
.panel-date  { font-family: 'Space Grotesk', sans-serif; font-size: 13px; font-weight: 600; color: #1a1917; text-align: center; }
.panel-divider { height: 1px; background: #f0efe9; flex-shrink: 0; }
.panel-count { display: flex; flex-direction: column; align-items: center; gap: 2px; text-align: center; }
.count-zero  { font-family: 'Space Grotesk', sans-serif; font-size: 14px; font-weight: 700; color: #1a1917; }
.count-num   { font-family: 'Space Grotesk', sans-serif; font-size: 30px; font-weight: 700; color: #1a1917; line-height: 1; }
.count-label { font-family: 'DM Sans', sans-serif; font-size: 11px; color: #65635d; }
.panel-note  { font-family: 'DM Sans', sans-serif; font-size: 12px; color: #a8a69f; margin: 0; line-height: 1.5; }

/* Rules section in gate panel */
.panel-rules        { display: flex; flex-direction: column; gap: 8px; background: #faf9f7; border: 1px solid #f0efe9; border-radius: 7px; padding: 10px 12px; }
.panel-rules-title  { font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 700; color: #1a1917; letter-spacing: 0.02em; }
.panel-rules-steps  { list-style: none; margin: 0; padding: 0; display: flex; flex-direction: column; gap: 7px; }
.panel-rules-steps li { display: flex; align-items: flex-start; gap: 8px; font-family: 'DM Sans', sans-serif; font-size: 12px; color: #3a3834; line-height: 1.45; }
.step-num { flex-shrink: 0; width: 18px; height: 18px; border-radius: 50%; background: #166534; color: #fff; font-family: 'Space Grotesk', sans-serif; font-size: 10px; font-weight: 700; display: flex; align-items: center; justify-content: center; margin-top: 1px; }

/* Gate panel mini leaderboard (top 5, no stage column) */
.panel-mini-lb-title { font-family: 'DM Sans', sans-serif; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: #a8a69f; }
.panel-mini-lb       { display: flex; flex-direction: column; gap: 6px; }
.pmr-row    { display: grid; grid-template-columns: 24px 1fr auto; gap: 6px; align-items: center; padding: 4px 6px; border-radius: 5px; }
.pmr-row:hover { background: #f8f7f5; }
.pmr-you    { background: #fef9c3 !important; }
.pmr-rank   { font-family: 'Space Grotesk', sans-serif; font-size: 13px; font-weight: 700; }
.pmr-name   { font-family: 'DM Sans', sans-serif; font-size: 12px; color: #3a3834; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.pmr-score  { font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 700; color: #166534; white-space: nowrap; }

/* Quiz progress panel */
.panel-progress-header { display: flex; flex-direction: column; gap: 4px; }
.panel-q-num   { font-family: 'Space Grotesk', sans-serif; font-size: 44px; font-weight: 700; color: #166534; line-height: 1; }
.panel-q-total { font-size: 22px; color: #a8a69f; }
.panel-q-label { font-family: 'DM Sans', sans-serif; font-size: 11px; font-weight: 600; color: #a8a69f; text-transform: uppercase; letter-spacing: 0.07em; }
.panel-steps   { display: flex; flex-wrap: wrap; gap: 6px; }
.step-dot      { width: 26px; height: 6px; border-radius: 3px; background: #e2e0dc; transition: background 250ms; }
.step-done     { background: #166534; }
.step-current  { background: #86efac; }
.panel-tip     { font-family: 'DM Sans', sans-serif; font-size: 12px; color: #a8a69f; margin: 0; line-height: 1.5; font-style: italic; }


@media (max-width: 860px) {
  .quiz-layout { grid-template-columns: 1fr; }
  .quiz-panel  { position: static; order: -1; }
}
@media (max-width: 640px) { .quiz-view { padding: 16px; } }
</style>
