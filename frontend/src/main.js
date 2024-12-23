import axios from "axios";
import { createApp } from 'vue'
import App from './App.vue'
import router from './router.js';
import '@picocss/pico'

axios.defaults.baseURL = 'http://127.0.0.1:8000';

const app = createApp(App);
app.use(router); // Use the router
app.mount('#app');