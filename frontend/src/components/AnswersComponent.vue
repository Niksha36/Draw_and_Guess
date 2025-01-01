<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { io } from 'socket.io-client';
import {store} from "@/js/store.js";

const socket = io('http://localhost:3000');
const messages = ref([]);
const newMessage = ref('');
const user = store.username;
const correctAnswer = ref('');
const isPainter = ref(store.isPainter);
const blockChat = ref(false);

const scrollToBottom = () => {
  const chatMessages = document.querySelector('.chat-messages-answer');
  if (chatMessages) {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
};

onMounted(() => {
  socket.emit('joinRoom', store.roomId);
  socket.on('answerMessage', (message) => {
    messages.value.push(message);
    scrollToBottom();
  });

  socket.on('correctAnswer', (answer) => {
    correctAnswer.value = answer.correctAnswer;
  });

  socket.on('startNextRound', () => {
    isPainter.value = store.isPainter;
    blockChat.value = false;
  });
});

const sendMessage = () => {
  if (isPainter.value) {
    alert("Художник не может писать в чат!"); 
    return;
  }

  if (newMessage.value.trim() === '') return;
  const message = { userName: user, answer: newMessage.value };
  message.isCorrect = isCorrectAnswer(message);
  
  if (message.isCorrect) {
    let points = 10; // Кол-во баллов за отгаданный рисунок
    socket.emit('updateScore', { userName: user, increment: points });
    axios.patch(`/api/user/${store.userId}/update`, {
      points: points,
    })
    .catch(error => {
      console.error('Ошибка:', error);
    });

    blockChat.value = true;
    message.value = message.value;
    messages.value.push(message);
    messages.value.push({ userName: "Крокодил", answer: "Вы получили " + points + " баллов.", isCorrect: true});
  } else {
    socket.emit('answerMessage', message);
  }
  
  newMessage.value = '';
  scrollToBottom();
};

const isCorrectAnswer = (message) => {
  return message.answer.toLowerCase() === correctAnswer.value;
};
</script>

<template>
  <div class="chat-wrapper">
    <div class="chat-messages-answer" style="overflow-y:auto; height: 100%">
      <div v-for="message in messages" :key="message.id" :class="{'chat-message': true, 'correct-answer': message.isCorrect}">
        <strong class="chat-message-author">{{ message.userName }}</strong>
        <span class="chat-message-text">{{ message.answer }}</span>
      </div>
    </div>

    <div class="chat-input">
      <input
          type="text"
          style="margin:0; user-select: none; height: 50px; margin-bottom: 2%;"
          class="chat-input-field"
          placeholder="Отвечать тут..."
          v-model="newMessage"
          @keyup.enter="sendMessage"
          :disabled="isPainter || blockChat"
      />
    </div>
  </div>
</template>

<style scoped>
.correct-answer{
  color: #0ee30e;
}
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
.chat-message-answer{
  font-size: 18px;
  margin: 3px 0 3px 5px;
}
</style>