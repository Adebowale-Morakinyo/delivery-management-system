import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import '@fortawesome/fontawesome-free/css/all.css'  // Importing Font Awesome CSS

axios.defaults.baseURL = process.env.VUE_APP_API_URL

createApp(App).mount('#app')
