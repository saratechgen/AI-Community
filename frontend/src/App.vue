<template>
  <div class="app-shell">

    <!-- Mobile top header -->
    <header class="mobile-header">
      <button class="hamburger" @click="isMobileOpen = true">
        <Menu :size="22" />
      </button>
      <span class="mobile-brand">DEWA AI Adoption Community</span>
    </header>

    <!-- Mobile backdrop -->
    <Transition name="fade">
      <div v-if="isMobileOpen" class="backdrop" @click="isMobileOpen = false" />
    </Transition>

    <!-- Sidebar -->
    <aside class="sidebar" :class="{ collapsed: sidebarCollapsed, 'mobile-open': isMobileOpen }">

      <!-- Mobile-only close strip -->
      <div class="sidebar-top">
        <button class="mobile-close" @click.prevent="isMobileOpen = false">
          <X :size="18" />
        </button>
      </div>

      <nav class="sidebar-nav">

        <!-- ── Explore card ─────────────────────────────────── -->
        <div class="nav-group nav-group--explore">
          <div class="nav-group-header" v-if="!sidebarCollapsed">Explore</div>

          <RouterLink to="/" class="nav-item" @click="isMobileOpen = false">
            <span class="nav-icon-wrap icon-bg--home"><Home :size="16" class="nav-icon icon-home" /></span>
            <span class="nav-label" v-if="!sidebarCollapsed">Home</span>
          </RouterLink>

          <RouterLink to="/news" class="nav-item" @click="isMobileOpen = false">
            <span class="nav-icon-wrap icon-bg--news"><Newspaper :size="16" class="nav-icon icon-newspaper" /></span>
            <span class="nav-label" v-if="!sidebarCollapsed">AI News</span>
          </RouterLink>

          <RouterLink to="/leaderboard" class="nav-item" @click="isMobileOpen = false">
            <span class="nav-icon-wrap icon-bg--quiz"><Trophy :size="16" class="nav-icon icon-trophy" /></span>
            <span class="nav-label" v-if="!sidebarCollapsed">Test Your AI Knowledge</span>
          </RouterLink>

          <RouterLink to="/events" class="nav-item" @click="isMobileOpen = false">
            <span class="nav-icon-wrap icon-bg--events"><CalendarDays :size="16" class="nav-icon icon-calendar" /></span>
            <span class="nav-label" v-if="!sidebarCollapsed">Events</span>
          </RouterLink>
        </div>

        <!-- ── Organisation card ─────────────────────────────── -->
        <div class="nav-group nav-group--org">
          <div class="nav-group-header" v-if="!sidebarCollapsed">Organisation</div>

          <RouterLink to="/announcements" class="nav-item" @click="isMobileOpen = false">
            <span class="nav-icon-wrap icon-bg--announce"><Megaphone :size="16" class="nav-icon icon-megaphone" /></span>
            <span class="nav-label" v-if="!sidebarCollapsed">Announcements</span>
          </RouterLink>

          <RouterLink to="/leaders-message" class="nav-item" @click="isMobileOpen = false">
            <span class="nav-icon-wrap icon-bg--vision"><Quote :size="16" class="nav-icon icon-target" /></span>
            <span class="nav-label" v-if="!sidebarCollapsed">Leader's Message</span>
          </RouterLink>

          <RouterLink to="/about" class="nav-item" @click="isMobileOpen = false">
            <span class="nav-icon-wrap icon-bg--about"><Info :size="16" class="nav-icon icon-info" /></span>
            <span class="nav-label" v-if="!sidebarCollapsed">About Us</span>
          </RouterLink>

          <RouterLink to="/ask" class="nav-item" @click="isMobileOpen = false">
            <span class="nav-icon-wrap icon-bg--ask"><HelpCircle :size="16" class="nav-icon icon-ask" /></span>
            <span class="nav-label" v-if="!sidebarCollapsed">Ask AI Adoption</span>
          </RouterLink>
        </div>

      </nav>

      <button class="collapse-btn" @click="sidebarCollapsed = !sidebarCollapsed">
        <ChevronLeft :size="14" v-if="!sidebarCollapsed" />
        <ChevronRight :size="14" v-else />
      </button>
    </aside>

    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import {
  Home, Newspaper, Trophy, CalendarDays, Megaphone,
  Quote, Info, HelpCircle, ChevronLeft, ChevronRight, Menu, X,
} from 'lucide-vue-next'

const sidebarCollapsed = ref(false)
const isMobileOpen     = ref(false)
</script>

<style scoped>
/* ── Shell ───────────────────────────────────────────────────── */
.app-shell {
  display: flex;
  height: 100vh;
  background: #eeedeb;
  overflow: hidden;
}

/* ── Sidebar ─────────────────────────────────────────────────── */
.sidebar {
  width: 240px;
  min-width: 240px;
  background: #f6f5f3;
  border-right: 1px solid #e2e0dc;
  border-top: 3px solid #166534;
  display: flex;
  flex-direction: column;
  transition: width 200ms ease-out, min-width 200ms ease-out;
  position: relative;
  z-index: 100;
}
.sidebar.collapsed {
  width: 56px;
  min-width: 56px;
}

/* ── Mobile-only close strip ─────────────────────────────────── */
.sidebar-top {
  display: none;
  justify-content: flex-end;
  padding: 8px 10px 0;
  flex-shrink: 0;
}
.mobile-close {
  background: none;
  border: none;
  color: #65635d;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  border-radius: 5px;
  transition: background 150ms;
}
.mobile-close:hover { background: #e2e0dc; }

/* ── Nav ─────────────────────────────────────────────────────── */
.sidebar-nav {
  flex: 1;
  padding: 10px 8px 16px;
  display: flex;
  flex-direction: column;
  gap: 0;
  overflow-y: auto;
  background: transparent;
}

.nav-group {
  background: transparent;
  border: none;
  border-radius: 0;
  padding: 4px 0;
  display: flex;
  flex-direction: column;
  gap: 1px;
}
.nav-group--explore { padding-top: 2px; }
.nav-group--org {
  border-top: 1px solid #e2e0dc;
  margin-top: 10px;
  padding-top: 12px;
}
.nav-group-header {
  font-family: 'DM Sans', sans-serif;
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #65635d;
  padding: 5px 8px 3px;
  user-select: none;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 10px 8px 7px;
  border-left: 3px solid transparent;
  border-radius: 8px;
  text-decoration: none;
  color: #65635d;
  font-family: 'DM Sans', sans-serif;
  font-size: 13px;
  font-weight: 500;
  transition: background 150ms ease-out, color 150ms ease-out;
  white-space: nowrap;
  overflow: hidden;
}
.nav-item:hover {
  background: #eeedeb;
  color: #23221f;
}
.nav-item.router-link-exact-active {
  background: transparent;
  color: #166534;
  font-weight: 600;
  border-left-color: #166534;
}

/* ── Icon wrap — colored per section ────────────────────────── */
.nav-icon-wrap {
  width: 30px;
  height: 30px;
  border-radius: 7px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: opacity 150ms ease-out;
}
.icon-bg--home     { background: #dcfce7; }
.icon-bg--news     { background: #dbeafe; }
.icon-bg--quiz     { background: #fee2e2; }
.icon-bg--events   { background: #d1fae5; }
.icon-bg--announce { background: #fee2e2; }
.icon-bg--vision   { background: #dbeafe; }
.icon-bg--about    { background: #d1fae5; }
.icon-bg--ask      { background: #fdf4ff; }

.nav-item:hover .nav-icon-wrap { opacity: 0.75; }
.nav-item.router-link-exact-active .nav-icon-wrap {
  opacity: 1;
}

.nav-icon { flex-shrink: 0; transition: color 200ms ease-out; }

/* Per-icon default colours */
.icon-bg--home     .nav-icon { color: #166534; }
.icon-bg--news     .nav-icon { color: #2255b0; }
.icon-bg--quiz     .nav-icon { color: #d93535; }
.icon-bg--events   .nav-icon { color: #5bb85d; }
.icon-bg--announce .nav-icon { color: #d93535; }
.icon-bg--vision   .nav-icon { color: #2255b0; }
.icon-bg--about    .nav-icon { color: #5bb85d; }
.icon-bg--ask      .nav-icon { color: #7c3aed; }

/* Hover only — keep icon colour on active so each section retains its identity */
.nav-item:hover .nav-icon { color: #166534; }

.nav-label { overflow: hidden; text-overflow: ellipsis; }

/* ── Collapse btn ────────────────────────────────────────────── */
.collapse-btn {
  position: absolute;
  bottom: 20px;
  right: -12px;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  border: 1px solid #e2e0dc;
  background: #f6f5f3;
  color: #65635d;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 150ms;
  z-index: 10;
}
.collapse-btn:hover { background: #eeedeb; }

/* ── Main content ────────────────────────────────────────────── */
.main-content {
  flex: 1;
  overflow-y: auto;
  background: #f8f7f5;
}

/* ── Mobile header ───────────────────────────────────────────── */
.mobile-header {
  display: none;
  position: fixed;
  top: 0; left: 0; right: 0;
  height: 56px;
  background: #166534;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  z-index: 50;
  align-items: center;
  padding: 0 16px;
  gap: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.2);
}
.hamburger {
  background: none;
  border: none;
  color: rgba(255,255,255,0.8);
  cursor: pointer;
  padding: 6px;
  display: flex;
  align-items: center;
  border-radius: 6px;
  transition: background 150ms;
}
.hamburger:hover { background: rgba(255,255,255,0.12); }
.mobile-brand {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 700;
  color: #f0fdf4;
  line-height: 1.3;
}

/* ── Backdrop ────────────────────────────────────────────────── */
.backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.45);
  z-index: 90;
  backdrop-filter: blur(2px);
}
.fade-enter-active, .fade-leave-active { transition: opacity 200ms ease; }
.fade-enter-from, .fade-leave-to       { opacity: 0; }

/* ── Mobile breakpoint ───────────────────────────────────────── */
@media (max-width: 960px) {
  .mobile-header  { display: flex; }
  .sidebar-top    { display: flex; }
  .collapse-btn   { display: none; }

  .main-content   { padding-top: 56px; }

  .sidebar {
    position: fixed;
    top: 0; left: 0;
    height: 100vh;
    width: 280px !important;
    min-width: 280px !important;
    transform: translateX(-100%);
    transition: transform 250ms cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 4px 0 24px rgba(0,0,0,0.15);
  }
  .sidebar.mobile-open {
    transform: translateX(0);
  }
}

/* ════════════════════════════════════════════════════════════
   NAV ICON ANIMATIONS
   ════════════════════════════════════════════════════════════ */
.icon-home {
  animation: nav-home 3s ease-in-out infinite;
  animation-delay: 0s;
}
@keyframes nav-home {
  0%, 100% { transform: scale(1) translateY(0); }
  30%       { transform: scale(1.15) translateY(-2px); }
  60%       { transform: scale(0.95) translateY(0); }
  80%       { transform: scale(1.05) translateY(-1px); }
}

.icon-newspaper {
  animation: nav-newspaper 2.5s ease-in-out infinite;
  animation-delay: 0.3s;
  transform-origin: bottom center;
}
@keyframes nav-newspaper {
  0%, 100% { transform: rotate(0deg); }
  20%       { transform: rotate(-10deg); }
  50%       { transform: rotate(10deg); }
  75%       { transform: rotate(-5deg); }
  90%       { transform: rotate(3deg); }
}

.icon-trophy {
  animation: nav-trophy 2.8s ease-in-out infinite;
  animation-delay: 0.5s;
}
@keyframes nav-trophy {
  0%, 100% { transform: scale(1) rotate(0deg); }
  25%       { transform: scale(1.1) rotate(-6deg); }
  50%       { transform: scale(1.18) rotate(6deg); }
  70%       { transform: scale(1.08) rotate(-3deg); }
  85%       { transform: scale(1.02) rotate(1deg); }
}

.icon-calendar {
  animation: nav-calendar 2s cubic-bezier(0.16, 1, 0.3, 1) infinite;
  animation-delay: 1s;
}
@keyframes nav-calendar {
  0%, 100% { transform: translateY(0) scale(1); }
  30%       { transform: translateY(-5px) scale(1.12); }
  55%       { transform: translateY(2px) scale(0.94); }
  75%       { transform: translateY(-2px) scale(1.04); }
}

.icon-megaphone {
  animation: nav-megaphone 2.3s ease-in-out infinite;
  animation-delay: 1.5s;
  transform-origin: bottom left;
}
@keyframes nav-megaphone {
  0%, 100% { transform: rotate(0deg) scale(1); }
  15%       { transform: rotate(-18deg) scale(1.08); }
  35%       { transform: rotate(18deg) scale(1.12); }
  55%       { transform: rotate(-10deg) scale(1.05); }
  75%       { transform: rotate(6deg) scale(1.02); }
}

.icon-target {
  animation: nav-target 2s ease-in-out infinite;
  animation-delay: 2s;
}
@keyframes nav-target {
  0%, 100% { transform: scale(1);    opacity: 1; }
  25%       { transform: scale(1.22); opacity: 0.75; }
  50%       { transform: scale(0.88); opacity: 1; }
  75%       { transform: scale(1.12); opacity: 0.85; }
}

.icon-info {
  animation: nav-info 3s ease-in-out infinite;
  animation-delay: 2.5s;
}
@keyframes nav-info {
  0%, 35%, 100% { transform: rotateY(0deg) scale(1); }
  15%            { transform: rotateY(90deg) scale(0.9); }
  25%            { transform: rotateY(180deg) scale(1); }
  30%            { transform: rotateY(270deg) scale(0.9); }
}

.icon-ask {
  animation: nav-ask 2.6s ease-in-out infinite;
  animation-delay: 3s;
}
@keyframes nav-ask {
  0%, 100% { transform: scale(1) rotate(0deg); }
  20%       { transform: scale(1.15) rotate(-8deg); }
  45%       { transform: scale(1.2) rotate(8deg); }
  65%       { transform: scale(1.08) rotate(-4deg); }
  82%       { transform: scale(1.03) rotate(2deg); }
}
</style>
