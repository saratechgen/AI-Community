<template>
  <div class="plb">
    <div class="plb-title">Today's Leaderboard ⚡🦸‍♂️</div>
    <template v-if="leaderboard.length">
      <div class="plb-header">
        <span class="plb-col-rank">Rank</span>
        <span class="plb-col-name">Username</span>
        <span class="plb-col-stage">Stage</span>
        <span class="plb-col-score">Score</span>
      </div>
      <div class="plb-body">
        <div
          v-for="entry in leaderboard"
          :key="entry.rank"
          class="plb-row"
          :class="{ 'plb-you': isYou(entry) }"
        >
          <span class="plb-col-rank">{{ medalFor(entry.rank) }}</span>
          <span class="plb-col-name">{{ entry.username }}</span>
          <span class="plb-col-stage">{{ entry.stage_label }}</span>
          <span class="plb-col-score">{{ entry.total_score }}/15</span>
        </div>
      </div>
    </template>
    <p v-else class="plb-empty">No entries yet today.</p>
  </div>
</template>

<script setup>
defineProps({
  leaderboard: { type: Array, required: true },
  isYou:       { type: Function, required: true },
  medalFor:    { type: Function, required: true },
})
</script>

<style scoped>
.plb        { display: flex; flex-direction: column; gap: 0; background: #f0fdf4; border: 1px solid #dcfce7; border-radius: 7px; padding: 10px 12px; }
.plb-title  { font-family: 'DM Sans', sans-serif; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: #15803d; margin-bottom: 8px; text-align: center; }
.plb-empty  { font-family: 'DM Sans', sans-serif; font-size: 12px; color: #6E6A63; margin: 0; text-align: center; }

/* grid: rank | name | stage | score */
.plb-header,
.plb-row    { display: grid; grid-template-columns: 30px 1fr 56px 38px; gap: 4px; align-items: center; padding: 5px 4px; }

.plb-header { border-bottom: 1px solid #D9D5CD; margin-bottom: 2px; }
.plb-header span { font-family: 'DM Sans', sans-serif; font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #a8a69f; }

.plb-row          { border-radius: 5px; }
.plb-row:hover    { background: #F6F5F2; }
.plb-you          { background: #fef9c3 !important; }

.plb-col-rank  { font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 700; }
.plb-col-name  { font-family: 'DM Sans', sans-serif; font-size: 11px; color: #3A3730; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.plb-col-stage { font-family: 'DM Sans', sans-serif; font-size: 10px; color: #6E6A63; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.plb-col-score { font-family: 'Space Grotesk', sans-serif; font-size: 11px; font-weight: 700; color: #0E6B43; text-align: right; }

.plb-body { max-height: 340px; overflow-y: auto; display: flex; flex-direction: column; gap: 1px; }
</style>
