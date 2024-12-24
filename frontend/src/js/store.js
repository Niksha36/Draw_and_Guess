// frontend/src/js/store.js
import { reactive, watch } from 'vue';

export const store = reactive({
    username: localStorage.getItem('username') || '',
    userId: localStorage.getItem('userId') || '',
});

// Watch for changes to the username and save to localStorage
watch(() => store.username, (newUsername) => {
    localStorage.setItem('username', newUsername);
});