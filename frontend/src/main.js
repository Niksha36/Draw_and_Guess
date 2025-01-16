import axios from "axios";
import { createApp } from 'vue'
import App from './App.vue'
import router from './router.js';
import '@picocss/pico'

axios.defaults.baseURL = 'http://127.0.0.1:8000';

const app = createApp(App);

app.config.errorHandler = (err, vm, info) => {
  console.error('Error captured:', err, vm, info)
}

if (process.env.NODE_ENV === 'production') {
app.config.errorHandler = () => null
}

app.config.warnHandler = () => {};

app.use(router); // Use the router
app.mount('#app');