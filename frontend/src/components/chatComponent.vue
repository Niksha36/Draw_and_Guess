<script setup>
import { ref, onMounted } from 'vue';
import { io } from 'socket.io-client';
import {store} from "@/js/store.js";

const socket = io('http://localhost:3000');
const messages = ref([]);
const newMessage = ref('');
const user = store.username
onMounted(() => {
  socket.emit('joinRoom', store.roomId);
  socket.on('chatMessage', (message) => {
    messages.value.push(message);
  });
});

const sendMessage = () => {
  if (newMessage.value.trim() === '') return;
  socket.emit('chatMessage', { userName: user, message: newMessage.value });
  newMessage.value = '';
};
</script>

<template>
  <div class="chat-wrapper">
    <div class="chat-messages" style="overflow-y:auto; height: 100%">
      <div v-for="message in messages" :key="message.id" class="chat-message">
        <strong class="chat-message-author">{{ message.userName }}</strong>
        <span class="chat-message-text">{{ message.text }}</span>
      </div>
    </div>

    <div class="chat-input">
      <input
          type="text"
          style="margin:0; user-select: none; height: 50px; margin-bottom: 2%;"
          class="chat-input-field"
          placeholder="Чат здесь..."
          v-model="newMessage"
          @keyup.enter="sendMessage"
      />
    </div>
  </div>
</template>

<style scoped>
.chat-message-text{
  margin-left: 10px;
  user-select: none;
}
.chat-wrapper{
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
  height: 100%;
  flex:1;
}
.chat-message{
  font-size: 18px;
  margin: 3px 0 3px 5px;
}
</style>