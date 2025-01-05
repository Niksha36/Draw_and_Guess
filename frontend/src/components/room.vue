<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import { store } from "@/js/store.js";
import { io } from 'socket.io-client';

const socket = io('http://localhost:3000');
const isOpen = ref(false);
const isEmpty = ref(false);
const selectedTopic = ref();
const intervalId = ref(null);
const players = ref([]);
const isOwner = ref(false);
const router = useRouter();
let isActive = false;

async function fetchRoomData() {
  try {
    const response = await axios.get(`/api/room/${store.roomId}/`);
    players.value = response.data.players;
    selectedTopic.value = response.data.topic;
    isOpen.value = !response.data.is_private;

    if (Number(store.userId) == response.data.owner) {
      isOwner.value = true;
    }
  } catch (error) {
    console.error('Ошибка при получении данных комнаты:', error);
  }
}

function updateRoom(theme) {
  selectedTopic.value = theme;

  axios.patch(`/api/room/${store.roomId}/update/`, {
    is_private: !isOpen.value,
    is_active: isActive,
    topic: selectedTopic.value,
    user_id: store.userId,
  })
  .catch(error => {
    console.error('Ошибка:', error);
  });
}

async function goToMenu() {
  try {
    if (store.username == '' || store.userId == '') {
      showLogin.value = true;
      return;
    }

    await axios.patch(`/api/room/${store.roomId}/exit/`, {
      user_id: store.userId
    });
    

    router.push('/');
  } catch (error) {
    if (error.response && error.response.status === 404) {
      router.push('/');
    } else {
      alert("Ошибка при выходе из комнаты. Повторите позже.");
    }
  }
}

async function startGame() {
  try {
    if (players.value.length == 1) {
      isEmpty.value = true;
      return;
    }
    
    isActive = true;
    updateRoom();

    socket.emit('startGame', store.roomId);
  } catch (error) {
    console.error('Ошибка при начале игры:', error);
    alert("Ошибка при начале игры. Повторите позже.");
  }
}

onMounted(() => {
  fetchRoomData();
  socket.emit('joinRoom', store.roomId)

  socket.on('startGame', () => {
    store.isEnd = false;
    store.isDialogOpen = false;
    store.beforeunmount = false;
    store.correctAnswer = '';
    router.push(`/room/${store.roomId}/game`);
  });

  intervalId.value = setInterval(fetchRoomData, 500);
  
  axios.patch(`/api/user/${store.userId}/update`, {
    zeroing: true,
  })
  .catch(error => {
    console.error('Ошибка:', error);
  });
});

onBeforeUnmount(() => {
  clearInterval(intervalId.value);
  if (socket) {
    socket.close();
  }
});
</script>

<template>
  <div class="background">
    <dialog v-if="isEmpty" open>
      <article class="dialog">
        <p>
          <strong>🤼 Недостаточно игроков!</strong><br>
          Для начала игры необходимо хотя бы два игрока.
        </p>
        <button class="button" style="margin: 0; background-color: transparent; border: none"
          @click="isEmpty = false">Закрыть
        </button>
      </article>
    </dialog>
    <div class="wrapper">
      <div class="top-wrapper">
        <div class="return-to-menu-btn" @click="goToMenu"></div>
        <div class="privacy-switcher-wrapper" style="background: rgba(38, 28, 92, .5); border-radius: 15px; padding: 10px; margin-right: 20px">
          <label style="color: #5cffb6; text-shadow: var(--text-shadow);">
            <input name="terms" type="checkbox" role="switch" v-model="isOpen" @change="updateRoom(selectedTopic)" :checked="isOpen" :disabled="!isOwner" />
            Открытая комната
          </label>
        </div>
      </div>
      <div class="bottom-wrapper">
        <div class="left-wrapper">
          <div class="text">ЧЕЛ. {{ players.length }}/14</div>
          <div class="player-container">
            <div class="player-card" v-for="player in players" :key="player.id">
              <div class="player-avatar"></div>
              <div class="theme-text">{{ player.username }}</div>
            </div>
          </div>
        </div>
        <div class="right-wrapper">
          <div class="text">Тема</div>
          <div class="theme-wrapper">
            <div class="theme-container"
                 v-for="theme in ['Человек Паук', 'Животные', 'Наука', 'Мультфильмы', 'Кино', 'Игры']"
                 :key="theme"
                 :class="{ 'selected': selectedTopic === theme, 'disabled': !isOwner }"
                 @click="isOwner ? updateRoom(theme) : null">
              <div class="theme-text">{{ theme }}</div>
            </div>
          </div>
          <div class="buttons-wrapper">
            <div class="button" :class="{ 'disabled': !isOwner }" @click="isOwner ? startGame() : null">Играть</div>
            <div class="button" :class="{ 'disabled': !isOwner }">Пригласить</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style>
:root {
  --text-shadow: rgb(23, 5, 87) 3px 0px 0px, rgb(23, 5, 87) 2.83487px .981584px 0px, rgb(23, 5, 87) 2.35766px 1.85511px 0px, rgb(23, 5, 87) 1.62091px 2.52441px 0px, rgb(23, 5, 87) .705713px 2.91581px 0px, rgb(23, 5, 87) -.287171px 2.98622px 0px, rgb(23, 5, 87) -1.24844px 2.72789px 0px, rgb(23, 5, 87) -2.07227px 2.16926px 0px, rgb(23, 5, 87) -2.66798px 1.37182px 0px, rgb(23, 5, 87) -2.96998px .42336px 0px, rgb(23, 5, 87) -2.94502px -.571704px 0px, rgb(23, 5, 87) -2.59586px -1.50383px 0px, rgb(23, 5, 87) -1.96093px -2.27041px 0px, rgb(23, 5, 87) -1.11013px -2.78704px 0px, rgb(23, 5, 87) -.137119px -2.99686px 0px, rgb(23, 5, 87) .850987px -2.87677px 0px, rgb(23, 5, 87) 1.74541px -2.43999px 0px, rgb(23, 5, 87) 2.44769px -1.73459px 0px, rgb(23, 5, 87) 2.88051px -.838247px 0px;
}
</style>

<style scoped>
.background {
  user-select: none;
}
.background * {
  user-select: none;
}
.disabled {
  opacity: 0.5;
  pointer-events: none;
}
input[type="checkbox"]:checked {
  background: #5cffb6;
  border:none!important;
}
input[type="checkbox"]:focus {
  outline: none;
  box-shadow: none;
}
.background {
  background: url("../assets/textura.png") no-repeat center center / cover, linear-gradient(215deg, rgba(116, 84, 249) 0%, rgb(115, 17, 176) 85%);
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: 20px;
  z-index: 2;
}

.wrapper {
  border: 4px rgba(29, 29, 27, .15) solid;
  -webkit-box-shadow: inset 0px 2px 0px 0px rgba(255, 255, 255, .15), 0px 3px 0px 0px rgba(255, 255, 255, .15);
  -moz-box-shadow: inset 0px 2px 0px 0px rgba(255, 255, 255, .15), 0px 3px 0px 0px rgba(255, 255, 255, .15);
  box-shadow: inset 0px 2px 0px 0px rgba(255, 255, 255, .15), 0px 3px 0px 0px rgba(255, 255, 255, .15);
  -webkit-border-radius: 12px;
  background-color: rgba(255, 255, 255, 0);
  width: 70%;
  height: 80%;
  display: flex;
  border-radius: 15px;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.top-wrapper {
  margin-top: 20px;
  width: 100%;
  height: 10%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.return-to-menu-btn {
  cursor: pointer;
  margin: 20px;
  height: 100%;
  aspect-ratio: 1 / 1;
  background: url("../assets/ic_home.svg") no-repeat center center / cover, url("../assets/small_button_border.svg") no-repeat center center / cover;

}

.bottom-wrapper {
  width: 100%;
  height: 90%;
  display: flex;
  border-radius: 15px;
  justify-content: center;
  align-items: center;
}

.left-wrapper {
  display: flex;
  background-color: rgba(38, 28, 92, .5);
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  border-radius: 10px;
  width: 40%;
  height: 90%;
  margin: 0 20px;
}

.text {
  margin: 10px;
  font-weight: bold;
  font-size: 22px;
  color: #5cffb6;
  text-shadow: var(--text-shadow);
  text-transform: uppercase;
  text-align: center;
}

.player-container {
  overflow: auto;
  margin: 10px;
  display: flex;
  flex-direction: column;
  width: 90%;
  height: 90%;
  gap: 10px
}

.player-container::-webkit-scrollbar {
  width: 12px;
  height: 12px;
}

.player-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.player-container::-webkit-scrollbar-thumb {
  background: #ff53a4;
  border-radius: 10px;
}

.player-container::-webkit-scrollbar-thumb:hover {
  background: rgb(38, 28, 92);
}

.player-card {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  background-color: white;
  border-radius: 45px 10px 10px 45px;
  width: 95%;
  flex: 0 0 18%;
  gap: 10px;
}

.player-avatar {
  margin: 10px;
  background-image: url("../assets/1.svg");
  width: 20%;
  height: 100%;
  background-repeat: no-repeat;
}

.right-wrapper {
  display: flex;
  background-color: rgba(38, 28, 92, .5);
  flex-direction: column;
  justify-content: flex-start;
  border-radius: 10px;
  width: 60%;
  height: 90%;
  margin-right: 20px;
}

.theme-wrapper {
  display: flex;
  flex-wrap: wrap;
  align-content: flex-start;
  border-radius: 10px;
  height: 70%;
  padding: 2%;
  gap: 2%;
}

.theme-container {
  background: rgb(255, 255, 255);
  width: 32%;
  height: 27%;
  border-radius: 10px;
  border: 5px solid rgb(255, 255, 255);
}

.theme-container.selected {
  border: 5px solid #ff53a4;
}

.theme-container:hover {
  border: 5px solid #ff53a4;
}

.theme-text {
  font-weight: bold;
  font-size: 18px;
  color: #301a6b;
  margin: 8px 0 5px;
  text-align: center;
  text-transform: uppercase;
}

.buttons-wrapper {
  display: flex;
  justify-content: center;
  height: 13%;
}

.button {
  margin: 10px;
  border-radius: 5px;
  background-color: white;
  font-weight: bold;
  font-size: 18px;
  color: #301a6b;
  box-shadow: 0px 6px 0px 0px #301a6b;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  text-transform: uppercase;
  width: 40%;
}

.button:hover {
  background-color: #89ffcc;
}

.dialog {
  border-radius: 10px;
  max-width: 400px;
  max-height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}

.dialog .button {
  background-image: url("../assets/button.svg");
  width: 281px;
  height: 66px;
  border: none;
  color: #ffd506;
  text-shadow: rgb(23, 21, 86) 4px 0px 0px, rgb(23, 21, 86) 3.87565px .989616px 0px, rgb(23, 21, 86) 3.51033px 1.9177px 0px, rgb(23, 21, 86) 2.92676px 2.72656px 0px, rgb(23, 21, 86) 2.16121px 3.36588px 0px, rgb(23, 21, 86) 1.26129px 3.79594px 0px, rgb(23, 21, 86) .282949px 3.98998px 0px, rgb(23, 21, 86) -.712984px 3.93594px 0px, rgb(23, 21, 86) -1.66459px 3.63719px 0px, rgb(23, 21, 86) -2.51269px 3.11229px 0px, rgb(23, 21, 86) -3.20457px 2.39389px 0px, rgb(23, 21, 86) -3.69721px 1.52664px 0px, rgb(23, 21, 86) -3.95997px .56448px 0px, rgb(23, 21, 86) -3.97652px -.432781px 0px, rgb(23, 21, 86) -3.74583px -1.40313px 0px, rgb(23, 21, 86) -3.28224px -2.28625px 0px, rgb(23, 21, 86) -2.61457px -3.02721px 0px, rgb(23, 21, 86) -1.78435px -3.57996px 0px, rgb(23, 21, 86) -.843183px -3.91012px 0px, rgb(23, 21, 86) .150409px -3.99717px 0px, rgb(23, 21, 86) 1.13465px -3.8357px 0px, rgb(23, 21, 86) 2.04834px -3.43574px 0px, rgb(23, 21, 86) 2.83468px -2.82216px 0px, rgb(23, 21, 86) 3.44477px -2.03312px 0px, rgb(23, 21, 86) 3.84068px -1.11766px 0px, rgb(23, 21, 86) 3.9978px -.132717px 0px;
  font-size: 24px;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
  cursor: pointer;
  background-position: center;
  box-shadow: none;
}

.dialog .button:hover {
  background-image: url("../assets/hover_button.svg");
}

</style>