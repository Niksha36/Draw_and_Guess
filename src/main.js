
import { createApp } from 'vue'
import App from './App.vue'
import router from './router.js';
import '@picocss/pico'

const app = createApp(App);
app.use(router); // Use the router
app.mount('#app');