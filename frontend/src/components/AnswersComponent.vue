<script setup>
import axios from 'axios';
import { ref, onMounted } from 'vue';
import { io } from 'socket.io-client';
import {store} from "@/js/store.js";
import {playCorrectAnswerSound} from "@/js/soundEffects.js";
import stringSimilarity from 'string-similarity';

const socket = io('http://localhost:3000');
const messages = ref([]);
const newMessage = ref('');
const user = store.username;
const correctAnswer = ref('');

const scrollToBottom = () => {
  const chatMessages = document.querySelector('.chat-messages-answer');
  if (chatMessages) {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
};

onMounted(() => {
  socket.emit('joinRoom', Number(store.roomId));
  socket.on('answerMessage', (message) => {
    messages.value.push(message);
    scrollToBottom();
  });

  socket.on('correctAnswer', (answer) => {
    correctAnswer.value = answer.correctAnswer;
    store.correctAnswer = correctAnswer.value;
  });

  socket.on('startNextRound', () => {
    store.blockChat = false;
  });
  socket.on('endRound', () => {
    store.blockChat = true;
  })

  if (store.correctAnswer != '') {
    correctAnswer.value = store.correctAnswer;
  }
});

function getScoreIncrement(answersCount) {
  switch (answersCount) {
    case 0:
      return 10;
    case 1:
      return 6;
    case 2:
      return 4;
    default:
      return 2;
  }
}

const sendMessage = () => {
  if (store.isPainter || newMessage.value.trim() === '') return;

  const message = { userName: user, answer: newMessage.value };
  message.isCorrect = isCorrectAnswer(message);
  let points = getScoreIncrement(store.answersCount);

  if (message.isCorrect) {
    playCorrectAnswerSound()
    socket.emit('updateScore', { userName: user, increment: points, isOwnwer: false });
    axios.patch(`/api/score/${store.userId}/update`, {
      token: store.token,
      room_id: store.roomId,
      points: points,
    })
    .catch(error => {
      console.error('Ошибка:', error);
    });

    store.blockChat = true;
    message.value = message.value;
    messages.value.push(message);
    messages.value.push({ userName: "Крокодил", answer: "Вы получили " + points + " баллов.", isCorrect: true});
    socket.emit('answerMessage', { userName: "Крокодил", answer: "Игрок `" + user + "` угадал слово!", isCorrectPlayer: true });
  } else {
    const similarityCoef = stringSimilarity.compareTwoStrings(message.answer.toLowerCase(), correctAnswer.value);
    console.log(similarityCoef)
    if (similarityCoef >= 0.8) { 
      messages.value.push({ userName: "Крокодил", answer: "Вы были близки.", isClose: true});
    } else {
      socket.emit('answerMessage', message);
    }
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
      <div v-for="message in messages" :key="message.id" :class="{'chat-message': true, 'correct-answer': message.isCorrect, 'correct-answer-player': message.isCorrectPlayer, 'message-close': message.isClose}">
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
          :disabled="store.isPainter || store.blockChat"
      />
    </div>
  </div>
</template>

<style scoped>
.correct-answer{
  color: #0ee30e;
}
.correct-answer-player {
  color: #ffbf00;
}
.message-close {
  color: #e600ff;
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