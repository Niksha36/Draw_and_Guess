<template>
  <div class="user-list">
    <div class="user" v-for="user in users" :key="user.name">
      <div class="user-name">{{ user.name }}</div>
      <div class="user-score" style="color: #5dcdff;">{{ user.score }}</div>
      <div class="user-place" style="color: #5cffb6;">{{ user.place }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { store } from "@/js/store.js";
import axios from 'axios';
import {io} from "socket.io-client";


const socket = io('http://localhost:3000');
const users = ref([]);
const endRound = ref(false);
const finallyScore = 160;

async function updateScore(userName, scoreIncrement, isOwner) {
  const user = users.value.find(user => user.name === userName);
  if (user) {
    fetchRoomData();
    updatePlaces();
    
    if (!isOwner) {
      store.answersCount++;
    }

    if (store.isPainter && store.answersCount === users.value.length - 1 && !endRound.value) {
      socket.emit('updateScore', { userName: store.username, increment: 3, isOwnwer: true });  
      axios.patch(`/api/score/${store.userId}/update/`, {
          token: store.token,
          room_id: store.roomId,
          points: 3,
        })
        .catch(error => {
          console.error('Ошибка:', error);
        });
        socket.emit('endRound');
        endRound.value = true;
    }
  }
}
function updatePlaces() {
  users.value.sort((a, b) => b.score - a.score).forEach((user, index) => {
    user.place = index + 1;
  });
}
async function fetchRoomData() {
  try {
    const response = await axios.get(`/api/room/${store.roomId}/`);
    const players = response.data.players;
  
    users.value = players.map((player, index) => ({
      name: player.username,
      score: player.score,
      place: index + 1
    }));

    const winner = users.value.find(user => user.score >= finallyScore);
    if (winner) {
      if (winner.name == store.username && !endRound.value) {
        endRound.value = true;
        axios.patch(`/api/score/${store.userId}/update/`, {
          token: store.token,
          room_id: store.roomId,
          increment: true,
        })
        .catch(error => {
          console.error('Ошибка:', error);
        });
      }
      socket.emit('endGame');
      return;
    }

    if (players.length == 1) {
      socket.emit('endGame');
      return;
    }
    
    if (store.isPainter && store.answersCount === users.value.length - 1) {
        socket.emit('endRound');
    }

    updatePlaces()
  } catch (error) {
    console.error('Ошибка при получении данных комнаты:', error);
  }
}

onMounted(() => {
  fetchRoomData();
  socket.emit('joinRoom', Number(store.roomId));
  socket.on('updateScore', (data) => {
    updateScore(data.userName, data.increment, data.isOwner);
  });
  socket.on('changePainter', () => {
    fetchRoomData();
  });
  socket.on('roomExit', (answer) => {
    store.answersCount -= (answer && store.isPainter) ? 1 : 0;
    fetchRoomData();
  });
  socket.on('endRound', () => {
    endRound.value = false;
    store.answersCount = 0;
  })
});
</script>

<style scoped>
.user-list {
  position: absolute;
  overflow-y: scroll;
  scrollbar-width: none;
  top:5%;
  width: 100%;
  height:100%;
  padding: 16px 10px;
  margin-bottom:40px!important;
  display: flex;
  flex-direction: column;
}

.user {
  display: flex;
  justify-content: center;
  margin: 0px 15px 0;
}

.user-name {
  flex: 1;
  text-align: left;
  font-weight: bolder;
  color:#7361f7
}

.user-score, .user-place {
  margin-left: auto;
  text-align: right;
  font-weight: bold;
  font-size: 20px;
  text-shadow: rgb(23, 5, 87) 3px 0px 0px, rgb(23, 5, 87) 2.83487px .981584px 0px, rgb(23, 5, 87) 2.35766px 1.85511px 0px, rgb(23, 5, 87) 1.62091px 2.52441px 0px, rgb(23, 5, 87) .705713px 2.91581px 0px, rgb(23, 5, 87) -.287171px 2.98622px 0px, rgb(23, 5, 87) -1.24844px 2.72789px 0px, rgb(23, 5, 87) -2.07227px 2.16926px 0px, rgb(23, 5, 87) -2.66798px 1.37182px 0px, rgb(23, 5, 87) -2.96998px .42336px 0px, rgb(23, 5, 87) -2.94502px -.571704px 0px, rgb(23, 5, 87) -2.59586px -1.50383px 0px, rgb(23, 5, 87) -1.96093px -2.27041px 0px, rgb(23, 5, 87) -1.11013px -2.78704px 0px, rgb(23, 5, 87) -.137119px -2.99686px 0px, rgb(23, 5, 87) .850987px -2.87677px 0px, rgb(23, 5, 87) 1.74541px -2.43999px 0px, rgb(23, 5, 87) 2.44769px -1.73459px 0px, rgb(23, 5, 87) 2.88051px -.838247px 0px;
}
.user-place{
  margin-left: 17px;
}

</style>