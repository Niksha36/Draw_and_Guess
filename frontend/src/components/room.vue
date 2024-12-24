<script setup>
import {ref, onMounted, onBeforeUnmount} from 'vue';
import {useRouter} from 'vue-router';
import axios from 'axios';
import router from "@/router.js";
import {store} from "@/js/store.js";


const isOpen = ref(false);
const selectedTopic = ref('Человек Паук');
const intervalId = ref(null);
const players = ref([]);

async function fetchRoomData() {
  try {
    const response = await axios.get(`/api/room/${store.roomId}/`);
    players.value = response.data.players;
  } catch (error) {
    console.error('Ошибка при получении данных комнаты:', error);
  }
}
function updateRoom(theme) {
    selectedTopic.value = theme;
    
    axios.patch(`/api/room/${store.roomId}/update/`, { 
      is_private: !isOpen.value,
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
    console.error(error);
    alert("Ошибка при выходе из комнаты. Повторите позже.");
  }
}
onMounted(() => {
  fetchRoomData();
  intervalId.value = setInterval(fetchRoomData, 5000);
});
onBeforeUnmount(() => {
  clearInterval(intervalId.value);
});
</script>

<template>
  <div class="background">
    <div class="wrapper">
      <div class="top-wrapper">
        <div class="return-to-menu-btn" @click="goToMenu"></div>
        <div class="privacy-switcher-wrapper" style="background: rgba(38, 28, 92, .5); border-radius: 15px; padding: 10px; margin-right: 20px">
          <label  style="color: #5cffb6; text-shadow: rgb(23, 5, 87) 3px 0px 0px, rgb(23, 5, 87) 2.83487px .981584px 0px, rgb(23, 5, 87) 2.35766px 1.85511px 0px, rgb(23, 5, 87) 1.62091px 2.52441px 0px, rgb(23, 5, 87) .705713px 2.91581px 0px, rgb(23, 5, 87) -.287171px 2.98622px 0px, rgb(23, 5, 87) -1.24844px 2.72789px 0px, rgb(23, 5, 87) -2.07227px 2.16926px 0px, rgb(23, 5, 87) -2.66798px 1.37182px 0px, rgb(23, 5, 87) -2.96998px .42336px 0px, rgb(23, 5, 87) -2.94502px -.571704px 0px, rgb(23, 5, 87) -2.59586px -1.50383px 0px, rgb(23, 5, 87) -1.96093px -2.27041px 0px, rgb(23, 5, 87) -1.11013px -2.78704px 0px, rgb(23, 5, 87) -.137119px -2.99686px 0px, rgb(23, 5, 87) .850987px -2.87677px 0px, rgb(23, 5, 87) 1.74541px -2.43999px 0px, rgb(23, 5, 87) 2.44769px -1.73459px 0px, rgb(23, 5, 87) 2.88051px -.838247px 0px;
                  text-transform: uppercase; font-weight: bold">
            <input name="terms" type="checkbox" role="switch" v-model="isOpen" @change="updateRoom(selectedTopic)" :checked="isOpen" />
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
                :class="{ 'selected': selectedTopic === theme }" 
                @click="updateRoom(theme)">
                <div class="theme-text">{{ theme }}</div>
            </div>
          </div>
          <div class="buttons-wrapper">
            <div class="button">Пригласить</div>
            <div class="button">Играть</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<style scoped>
.background {
  user-select: none;
}
.background * {
  user-select: none;
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
  text-shadow: rgb(23, 5, 87) 3px 0px 0px, rgb(23, 5, 87) 2.83487px .981584px 0px, rgb(23, 5, 87) 2.35766px 1.85511px 0px, rgb(23, 5, 87) 1.62091px 2.52441px 0px, rgb(23, 5, 87) .705713px 2.91581px 0px, rgb(23, 5, 87) -.287171px 2.98622px 0px, rgb(23, 5, 87) -1.24844px 2.72789px 0px, rgb(23, 5, 87) -2.07227px 2.16926px 0px, rgb(23, 5, 87) -2.66798px 1.37182px 0px, rgb(23, 5, 87) -2.96998px .42336px 0px, rgb(23, 5, 87) -2.94502px -.571704px 0px, rgb(23, 5, 87) -2.59586px -1.50383px 0px, rgb(23, 5, 87) -1.96093px -2.27041px 0px, rgb(23, 5, 87) -1.11013px -2.78704px 0px, rgb(23, 5, 87) -.137119px -2.99686px 0px, rgb(23, 5, 87) .850987px -2.87677px 0px, rgb(23, 5, 87) 1.74541px -2.43999px 0px, rgb(23, 5, 87) 2.44769px -1.73459px 0px, rgb(23, 5, 87) 2.88051px -.838247px 0px;
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

</style>