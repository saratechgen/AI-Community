<template>
  <div class="placeholder-view">
    <span class="placeholder-label">Vision</span>
    <p class="placeholder-note">Coming soon</p>
  </div>
</template>

<style scoped>
.placeholder-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 60vh;
  gap: 12px;
}
.placeholder-label {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 28px;
  font-weight: 600;
  color: var(--text-primary, #1a1917);
}
.placeholder-note {
  font-family: 'DM Sans', sans-serif;
  font-size: 15px;
  color: var(--text-secondary, #65635d);
}
</style>
