import { ref } from 'vue';
import axios from 'axios';

export const messages = ref([]);
export const newMessage = ref('');

export async function fetchMessages() {
    try {
        const response = await axios.get('');
        messages.value = response.data;
    } catch (error) {
        console.error('Error fetching messages:', error);
    }
}

export async function sendMessage() {
    if (newMessage.value.trim() === '') return;

    try {
        const response = await axios.post('', { text: newMessage.value });
        messages.value.push(response.data);
        newMessage.value = '';
    } catch (error) {
        console.error('Error sending message:', error);
    }
}