<template>
  <div class="stage-selector">
    <div
      v-for="s in stages"
      :key="s.stage"
      class="stage-card"
      :class="cardClass(s.stage)"
    >
      <div class="stage-top">
        <span class="stage-num">Stage {{ s.stage }}</span>
        <span class="stage-icon">{{ statusIcon(s.stage) }}</span>
      </div>

      <div class="stage-title">{{ s.title }}</div>
      <div class="stage-meta">5 Questions · Pass mark: 4/5</div>

      <!-- Score if officially attempted -->
      <div v-if="officialResult(s.stage)" class="stage-score" :class="officialResult(s.stage).passed ? 'score-pass' : 'score-fail'">
        {{ officialResult(s.stage).score }}/5
        {{ officialResult(s.stage).passed ? '✓ Cleared' : '✗ Not cleared' }}
      </div>

      <!-- Action -->
      <button
        v-if="isUnlocked(s.stage) && !isCleared(s.stage)"
        class="stage-btn"
        @click="$emit('begin', s.stage)"
      >
        {{ hasAttempted(s.stage) ? 'Retry (practice)' : 'Begin' }}
      </button>

      <div v-else-if="isCleared(s.stage)" class="stage-cleared">
        Stage cleared
      </div>

      <div v-else class="stage-locked">
        🔒 Clear Stage {{ s.stage - 1 }} first
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  stages:          { type: Array,  required: true },
  unlockedStages:  { type: Object, required: true }, // Set
  officialResults: { type: Object, required: true }, // { 1: result, 2: result, ... }
})

defineEmits(['begin'])

function officialResult(stage) {
  return props.officialResults[stage] ?? null
}

function isUnlocked(stage) {
  return props.unlockedStages.has(stage)
}

function isCleared(stage) {
  return props.officialResults[stage]?.passed === true
}

function hasAttempted(stage) {
  return !!props.officialResults[stage]
}

function statusIcon(stage) {
  if (isCleared(stage))   return '✅'
  if (hasAttempted(stage) && !isCleared(stage)) return '❌'
  if (isUnlocked(stage))  return '▶'
  return '🔒'
}

function cardClass(stage) {
  if (isCleared(stage))   return 'card-cleared'
  if (hasAttempted(stage)) return 'card-failed'
  if (isUnlocked(stage))  return 'card-unlocked'
  return 'card-locked'
}
</script>

<style scoped>
.stage-selector {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.stage-card {
  background: #f8f7f5;
  border: 1px solid #e2e0dc;
  border-top: 3px solid #e2e0dc;
  border-radius: 10px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: border-color 200ms;
}

.card-unlocked { border-top-color: var(--accent, #166534); }
.card-cleared  { border-top-color: #16a34a; background: #f0fdf4; }
.card-failed   { border-top-color: #d93535; background: #fff5f5; }
.card-locked   { opacity: 0.6; }

.stage-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stage-num {
  font-family: 'DM Sans', sans-serif;
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: #a8a69f;
}

.stage-icon { font-size: 18px; }

.stage-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 16px;
  font-weight: 700;
  color: #1a1917;
}

.stage-meta {
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  color: #85837c;
}

.stage-score {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 700;
  padding: 4px 0;
}
.score-pass { color: #16a34a; }
.score-fail { color: #d93535; }

.stage-btn {
  margin-top: auto;
  padding: 9px 16px;
  background: var(--accent, #166534);
  color: #fff;
  border: none;
  border-radius: 7px;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 150ms;
}
.stage-btn:hover { opacity: 0.85; }

.stage-cleared {
  margin-top: auto;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: #16a34a;
}

.stage-locked {
  margin-top: auto;
  font-family: 'DM Sans', sans-serif;
  font-size: 12px;
  color: #a8a69f;
}

@media (max-width: 640px) {
  .stage-selector { grid-template-columns: 1fr; }
}
</style>
