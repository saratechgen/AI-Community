<template>
  <section class="quiz-strip">
    <div class="strip-left">
      <div class="strip-icon">
        <BrainCircuit :size="20" />
      </div>
      <div class="strip-text">
        <div class="strip-title-row">
          <h2 class="strip-title">Test Your AI Knowledge</h2>
          <span class="new-badge">Daily NEW QUIZ</span>
        </div>
        <p class="strip-hook">A new quiz, every morning.</p>
        <p class="strip-rule">Your first attempt is your official score.</p>
      </div>
    </div>

    <div class="strip-right">
      <div class="strip-stats">
        <div class="stat">
          <span class="stat-num">5</span>
          <span class="stat-label">Questions</span>
        </div>
        <div class="stat-divider" />
        <div class="stat">
          <span class="stat-num">Daily</span>
          <span class="stat-label">New</span>
        </div>
      </div>
      <RouterLink to="/leaderboard" class="strip-cta">
        Take today's quiz <ArrowRight :size="14" />
      </RouterLink>
    </div>
  </section>
</template>

<script setup>
import { BrainCircuit, ArrowRight } from 'lucide-vue-next'
</script>

<style scoped>
.quiz-strip {
  background: #ffffff;
  border: 1px solid #D9D5CD;
  border-radius: 12px;
  padding: 20px 24px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  gap: 24px;
  box-shadow: 0 1px 4px rgba(31,31,27,0.05), 0 4px 16px rgba(31,31,27,0.04);
}

/* Left: icon + text */
.strip-left {
  display: flex;
  align-items: center;
  gap: 14px;
  min-width: 0;
}
.strip-icon {
  width: 40px;
  height: 40px;
  border-radius: 9px;
  background: #DFF3E8;
  color: #0E6B43;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.strip-title {
  font-family: 'Satoshi', sans-serif;
  font-size: 15px;
  font-weight: 700;
  color: #1F1F1B;
  margin: 0 0 3px;
}
.strip-hook {
  font-family: 'Satoshi', sans-serif;
  font-size: 13px;
  font-weight: 600;
  color: #1F1F1B;
  margin: 4px 0 2px;
}
.strip-rule {
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  color: #A8A49D;
  margin: 0;
}

/* Right: stats + CTA */
.strip-right {
  display: flex;
  align-items: center;
  gap: 24px;
  flex-shrink: 0;
}
.strip-stats {
  display: flex;
  align-items: center;
  gap: 16px;
}
.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
}
.stat-num {
  font-family: 'Satoshi', sans-serif;
  font-size: 17px;
  font-weight: 700;
  color: #0E6B43;
  line-height: 1;
}
.stat-label {
  font-family: 'Inter', sans-serif;
  font-size: 10px;
  color: #85837c;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.stat-divider {
  width: 1px;
  height: 30px;
  background: #D9D5CD;
}
.strip-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.new-badge {
  font-family: 'Inter', sans-serif;
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  background: #0E6B43;
  color: #f0fdf4;
  padding: 2px 8px;
  border-radius: 10px;
  animation: badge-pulse 1.8s ease-in-out infinite;
  flex-shrink: 0;
}
@keyframes badge-pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.4; }
}

.strip-cta {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  background: #DFF3E8;
  color: #0E6B43;
  border: 1.5px solid #0E6B43;
  border-radius: 7px;
  font-family: 'Inter', sans-serif;
  font-size: 12px;
  font-weight: 600;
  text-decoration: none;
  white-space: nowrap;
  transition: background 150ms, gap 150ms;
}
.strip-cta:hover { background: #bbf7d0; gap: 10px; }

/* Stack on narrow screens */
@media (max-width: 860px) {
  .quiz-strip    { flex-direction: column; align-items: flex-start; }
  .strip-right   { width: 100%; justify-content: space-between; }
}
@media (max-width: 480px) {
  .strip-right   { flex-direction: column; align-items: flex-start; gap: 14px; }
  .strip-cta     { width: 100%; justify-content: center; }
}
</style>
