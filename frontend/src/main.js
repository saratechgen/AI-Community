import { createApp } from 'vue'
import './design-system/tokens.css'
import './design-system/index.css'
import router from './router/index.js'
import App from './App.vue'

createApp(App).use(router).mount('#app')
