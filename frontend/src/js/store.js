// frontend/src/js/store.js
import { reactive, watch } from 'vue';

export const store = reactive({
    username: localStorage.getItem('username') || '',
    userId: localStorage.getItem('userId') || '',
    roomId: localStorage.getItem('roomId') || '',
});

// Watch for changes to the username and save to localStorage
watch(() => store.username, (newUsername) => {
    localStorage.setItem('username', newUsername);
});
watch(() => store.userId, (newUserId) => {
    localStorage.setItem('userId', newUserId);
});
watch(() => store.roomId, (newRoomId) => {
    localStorage.setItem('roomId', newRoomId);
});