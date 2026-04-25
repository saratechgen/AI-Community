<template>
  <div class="quiz-question">
    <p class="q-text">{{ question.question }}</p>

    <div class="options">
      <button
        v-for="opt in options"
        :key="opt.key"
        class="option-btn"
        :class="optionClass(opt.key)"
        :disabled="answered"
        @click="$emit('answer', question.id, opt.key)"
      >
        <span class="opt-label">{{ opt.key.toUpperCase() }}</span>
        <span class="opt-text">{{ opt.text }}</span>
      </button>
    </div>

    <Transition name="fade">
      <div v-if="answered" class="feedback">
        <div class="feedback-verdict" :class="isCorrect ? 'correct' : 'incorrect'">
          {{ isCorrect ? 'Correct!' : 'Incorrect — the right answer is ' + question.correct.toUpperCase() }}
        </div>
        <p class="feedback-explanation">{{ question.explanation }}</p>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  question:  { type: Object,  required: true },
  chosen:    { type: String,  default: null  },
  answered:  { type: Boolean, default: false },
})

defineEmits(['answer'])

const options = computed(() => [
  { key: 'a', text: props.question.option_a },
  { key: 'b', text: props.question.option_b },
  { key: 'c', text: props.question.option_c },
  { key: 'd', text: props.question.option_d },
])

const isCorrect = computed(() => props.chosen === props.question.correct)

function optionClass(key) {
  if (!props.answered) return ''
  if (key === props.question.correct) return 'opt-correct'
  if (key === props.chosen)           return 'opt-wrong'
  return 'opt-dim'
}
</script>

<style scoped>
.quiz-question { display: flex; flex-direction: column; gap: 12px; }

.q-text {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 17px;
  font-weight: 600;
  color: #1F1F1B;
  line-height: 1.5;
  margin: 0;
}

.options { display: flex; flex-direction: column; gap: 7px; }

.option-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 14px;
  background: #F6F5F2;
  border: 1.5px solid #D9D5CD;
  border-radius: 8px;
  cursor: pointer;
  text-align: left;
  transition: border-color 150ms, background 150ms;
  width: 100%;
}
.option-btn:not(:disabled):hover {
  border-color: #0E6B43;
  background: #f0fdf4;
}
.option-btn:disabled { cursor: default; }

.opt-label {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 700;
  color: #0E6B43;
  background: #dcfce7;
  border-radius: 4px;
  padding: 2px 7px;
  flex-shrink: 0;
}
.opt-text {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  color: #3a3834;
}

.opt-correct { border-color: #16a34a !important; background: #f0fdf4 !important; }
.opt-correct .opt-label { background: #16a34a; color: #fff; }

.opt-wrong   { border-color: #dc2626 !important; background: #fef2f2 !important; }
.opt-wrong .opt-label { background: #dc2626; color: #fff; }

.opt-dim { opacity: 0.45; }

.feedback { padding: 14px 16px; background: #F6F5F2; border-radius: 8px; border-left: 4px solid var(--accent, #0E6B43); }
.feedback-verdict {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 700;
  margin-bottom: 6px;
}
.feedback-verdict.correct   { color: #16a34a; }
.feedback-verdict.incorrect { color: #dc2626; }
.feedback-explanation {
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  color: #6E6A63;
  margin: 0;
  line-height: 1.6;
}

.fade-enter-active, .fade-leave-active { transition: opacity 250ms ease; }
.fade-enter-from, .fade-leave-to       { opacity: 0; }
</style>
