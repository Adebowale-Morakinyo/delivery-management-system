import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome' // Importing Font Awesome CSS

import { fas } from "@fortawesome/free-solid-svg-icons";
    
library.add(fas);

axios.defaults.baseURL = process.env.VUE_APP_API_URL

const app = createApp(App)

/* register font-awesome-icon component globally */
app.component('font-awesome-icon', FontAwesomeIcon)

app.mount('#app')
