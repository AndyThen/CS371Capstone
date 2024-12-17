import axios from 'axios'
axios.defaults.baseURL = 'http://127.0.0.1:5000'
import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
