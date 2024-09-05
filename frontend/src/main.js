import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'

axios.defaults.baseURL = 'https://delivery-management-system-production.up.railway.app/'

createApp(App).mount('#app')
