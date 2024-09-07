import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome' // Importing Font Awesome CSS

axios.defaults.baseURL = process.env.VUE_APP_API_URL

const app = createApp(App)

/* register font-awesome-icon component globally */
app.component('font-awesome-icon', FontAwesomeIcon)

app.mount('#app')
