import { createRouter, createWebHistory } from 'vue-router'
import HomeView          from '../views/HomeView.vue'
import AboutView         from '../views/AboutView.vue'
import LeadersMessageView from '../views/LeadersMessageView.vue'
import LeaderboardView   from '../views/LeaderboardView.vue'
import QuizView          from '../views/QuizView.vue'
import EventsView        from '../views/EventsView.vue'
import NewsView          from '../views/NewsView.vue'
import AnnouncementsView from '../views/AnnouncementsView.vue'
import AskView           from '../views/AskView.vue'

const routes = [
  { path: '/',              component: HomeView          },
  { path: '/news',          component: NewsView          },
  { path: '/leaderboard',   component: LeaderboardView   },
  { path: '/events',        component: EventsView        },
  { path: '/announcements', component: AnnouncementsView },
  { path: '/ask',           component: AskView           },
  { path: '/leaders-message', component: LeadersMessageView },
  { path: '/about',         component: AboutView         },
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
