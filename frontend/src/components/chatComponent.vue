<script setup>
import {ref, onMounted, nextTick} from 'vue';
import { io } from 'socket.io-client';
import {store} from "@/js/store.js";
import {playWarningSound} from "@/js/soundEffects.js";

const socket = io('http://localhost:3000');
const messages = ref([]);
const newMessage = ref('');
const user = store.username
const correctAnswer = ref('');

const scrollToBottom = async () => {
  await nextTick();
  const chatMessages = document.querySelector('.chat-messages');
  if (chatMessages) {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
};

onMounted(() => {
  socket.emit('joinRoom', Number(store.roomId));

  socket.on('chatHistory', (chatMessages) => {
    messages.value = chatMessages;
    scrollToBottom();
  });

  socket.on('chatMessage', (message) => {
    messages.value.push(message);
    scrollToBottom();
  });

  socket.on('correctAnswer', (answer) => {
    correctAnswer.value = answer.correctAnswer;
    store.correctAnswer = correctAnswer.value;
  });
  socket.on('endRound', () => {
    store.isPainter = false;
  })

  if (store.correctAnswer != '') {
    correctAnswer.value = store.correctAnswer;
  }
})

const sendMessage = () => {
  if (store.isPainter) {
    alert("Художник не может писать в чат!"); 
    return;
  }

  if (isCorrectAnswer(newMessage)) {
    messages.value.push({ userName: "Крокодил", text: "Нельзя делиться ответом в чате!", exception: true});
    playWarningSound()
    scrollToBottom();
    return;
  }
  
  if (newMessage.value.trim() === '') return;
  socket.emit('chatMessage', { userName: user, message: newMessage.value});
  newMessage.value = '';
  scrollToBottom();
};

const isCorrectAnswer = (message) => {
  return message.value.toLowerCase() === correctAnswer.value;
};
</script>

<template>
  <div class="chat-wrapper">
    <div class="chat-messages" style="overflow-y:auto; height: 100%">
      <div v-for="message in messages" :key="message.id" :class="{'chat-message': true, 'exception-message': message.exception}">
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
          :disabled="store.isPainter"
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

.exception-message {
  color: #e30e0e;
}
</style>