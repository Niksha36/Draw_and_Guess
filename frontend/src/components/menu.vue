<script setup>
import { useRouter } from 'vue-router';
import { computed, ref } from "vue";
import axios from 'axios';
import '@fortawesome/fontawesome-free/css/all.css';
import LoginComponent from './LoginComponent.vue';
import { store } from '@/js/store.js';
import {playClickSound, playHoverSound} from "@/js/soundEffects.js";

const router = useRouter();
const showLogin = ref(false);
const showDialog = ref(false);
const showDialogOpen = ref(false);
const username = computed(() => store.username);
const buttonText = computed(() => (username.value ? 'Выйти' : 'Войти'));

async function goToRoom() {
  try {
    if (store.username == '' || store.userId == '') {
      showDialog.value = true;
      return;
    }

    const response = await axios.post('/api/create/', {
      roomname: store.username,
      painter: store.userId,
      owner: store.userId,
    });

    store.roomId = response.data.id;
    store.token = response.data.token;
    store.linkToken = response.data.link_token;
    router.push(`/room/${response.data.id}?token=${response.data.link_token}`);
  } catch (error) {
    alert("Ошибка при создании комнаты. Повторите позже");
  }
}
function goToGame() {
    if (store.username == '' || store.userId == '') {
      showDialog.value = true;
      return;
    }
  router.push('/listOfRooms');
}
function logout() {
  if (store.username != '') {
    store.username = '';
    return;
  }
  showLogin.value = true;
}
function revertMenu() {
  showLogin.value = false;
}
function goToScore() {
  router.push('/score');
}

</script>

<template>
  <div class="background">
    <dialog v-if="showDialog" open>
      <article class="dialog">
        <p>
          <strong>🔒 Вам нужно авторизоваться!</strong><br>
          Для начала игры, пожалуйста, авторизуйтесь.
        </p>
        <button class="button" @mouseover="playHoverSound" @mousedown="playClickSound" style="margin: 0; background-color: transparent; border: none"
          @click="showDialog = false">Закрыть
        </button>
      </article>
    </dialog>
    <dialog v-if="showDialogOpen" open>
      <article class="dialog">
        <p>
          <strong>⏰️ Нет доступных комнат!</strong><br>
          Создайте свою комнату или подождите пока появятся новые.
        </p>
        <button class="button" @mouseover="playHoverSound" @mousedown="playClickSound" style="margin: 0; background-color: transparent; border: none"
          @click="showDialogOpen = false">Закрыть
        </button>
      </article>
    </dialog>
    <div class="menu-wrapper">
      <img src="../assets/bg_content.svg" class="border-background-img" alt="">
      <div v-if="showLogin" class="go-to-menu-icon-wrapper" @click="revertMenu"  @mouseenter="playHoverSound" @mousedown="playClickSound">
        <div class="go-to-menu-icon">
          <img src="../assets/small_button_border.svg" alt="border" class="home-border">
          <img src="../assets/ic_home.svg" alt="home-icon" width="33px" class="home-icon">
        </div>
      </div>

      <div class="wrapper">
        <div v-if="!showLogin" class="content">
          <div class="avatar">
            <img src="../assets/avatar.svg" alt="Avatar" class="avatar-img">
          </div>
          <div v-if="store.username != ''" class="username" style ="user-select: none; -moz-user-select: none; margin:2%" >
            <p>Привет, {{ store.username }}!</p>
          </div>
          <button class="logout" style="border: none; margin-top:0" @click="logout" @mouseenter="playHoverSound" @mousedown="playClickSound">
            <i class="fas fa-sign-out-alt"></i> {{ buttonText }}
          </button>
          <div class="button-play button" @click="goToGame" @mouseover="playHoverSound" @mousedown="playClickSound">
            Играть
          </div>
          <div class="button-play button" @click="goToRoom" @mouseover="playHoverSound" @mousedown="playClickSound">
            Создать игру
          </div>
          <div class="button-play button" @click="goToScore" @mouseover="playHoverSound" @mousedown="playClickSound">
            Рейтинг
          </div>
        </div>


        <LoginComponent v-else @login-success="revertMenu" :revert-menu="revertMenu" />
      </div>

    </div>


  </div>
</template>

<style scoped>
.border-background-img {
  width: 100%;
  height: 100%;
}

.go-to-menu-icon-wrapper {
  cursor: pointer;
}

.menu-wrapper {
  position: relative;
}

.go-to-menu-icon-wrapper {
  position: absolute;
  top: 4.5%;
  left: 2.8%;
}

.home-icon {
  position: absolute;
  right: 0;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  will-change: auto;
}

.background {
  background-image: url("../assets/bg.svg");
  background-color: #7361f7;
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px 15%;
  z-index: 2;
}

.menu-wrapper {
  /*
  background-image: url("../assets/bg_content.svg");
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
   */
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.content {
  position: absolute;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.wrapper {
  position: absolute;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 78%;
  width: 60%
}

.logout {
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  background-color: #7361f7;
  box-shadow: 0px 6px 0px 0px #320067;
}

.logout:hover {
  background-color: #5a4db8 !important;
}

.avatar {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 120px;
  height: 120px;
  border: 2px solid #000000;
  border-radius: 50%;
  will-change: auto;
}

.avatar-img {
  height: 135px;
  border-radius: 50%;
  object-fit: cover;
  will-change: auto;
}

.button {
  background-image: url("../assets/button.svg");
  width: 281px;
  height: 66px;
  color: #ffd506;
  text-shadow: rgb(23, 21, 86) 4px 0px 0px, rgb(23, 21, 86) 3.87565px .989616px 0px, rgb(23, 21, 86) 3.51033px 1.9177px 0px, rgb(23, 21, 86) 2.92676px 2.72656px 0px, rgb(23, 21, 86) 2.16121px 3.36588px 0px, rgb(23, 21, 86) 1.26129px 3.79594px 0px, rgb(23, 21, 86) .282949px 3.98998px 0px, rgb(23, 21, 86) -.712984px 3.93594px 0px, rgb(23, 21, 86) -1.66459px 3.63719px 0px, rgb(23, 21, 86) -2.51269px 3.11229px 0px, rgb(23, 21, 86) -3.20457px 2.39389px 0px, rgb(23, 21, 86) -3.69721px 1.52664px 0px, rgb(23, 21, 86) -3.95997px .56448px 0px, rgb(23, 21, 86) -3.97652px -.432781px 0px, rgb(23, 21, 86) -3.74583px -1.40313px 0px, rgb(23, 21, 86) -3.28224px -2.28625px 0px, rgb(23, 21, 86) -2.61457px -3.02721px 0px, rgb(23, 21, 86) -1.78435px -3.57996px 0px, rgb(23, 21, 86) -.843183px -3.91012px 0px, rgb(23, 21, 86) .150409px -3.99717px 0px, rgb(23, 21, 86) 1.13465px -3.8357px 0px, rgb(23, 21, 86) 2.04834px -3.43574px 0px, rgb(23, 21, 86) 2.83468px -2.82216px 0px, rgb(23, 21, 86) 3.44477px -2.03312px 0px, rgb(23, 21, 86) 3.84068px -1.11766px 0px, rgb(23, 21, 86) 3.9978px -.132717px 0px;
  font-size: 24px;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  cursor: pointer;
  background-position: center;
  box-shadow: none;
  will-change: auto;
}
.button:hover {
  background-image: url("../assets/hover_button.svg");
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
.username {
  margin-top: 20px;
  font-size: 24px;
  font-weight: bold;
  text-align: center;
}
.username p {
  margin: 10px;
  font-weight: bold;
  font-size: 30px;
  color: #ffbe5c;
  text-shadow: rgb(23, 5, 87) 3px 0px 0px, rgb(23, 5, 87) 2.83487px .981584px 0px, rgb(23, 5, 87) 2.35766px 1.85511px 0px, rgb(23, 5, 87) 1.62091px 2.52441px 0px, rgb(23, 5, 87) .705713px 2.91581px 0px, rgb(23, 5, 87) -.287171px 2.98622px 0px, rgb(23, 5, 87) -1.24844px 2.72789px 0px, rgb(23, 5, 87) -2.07227px 2.16926px 0px, rgb(23, 5, 87) -2.66798px 1.37182px 0px, rgb(23, 5, 87) -2.96998px .42336px 0px, rgb(23, 5, 87) -2.94502px -.571704px 0px, rgb(23, 5, 87) -2.59586px -1.50383px 0px, rgb(23, 5, 87) -1.96093px -2.27041px 0px, rgb(23, 5, 87) -1.11013px -2.78704px 0px, rgb(23, 5, 87) -.137119px -2.99686px 0px, rgb(23, 5, 87) .850987px -2.87677px 0px, rgb(23, 5, 87) 1.74541px -2.43999px 0px, rgb(23, 5, 87) 2.44769px -1.73459px 0px, rgb(23, 5, 87) 2.88051px -.838247px 0px;
  text-transform: uppercase;
  text-align: center;
}

@media (max-height: 515px) {
  .button {

    background-size: contain;
  }
}

@media (max-height: 543px) {
  .button {
    margin-top: 10px;
    background-size: contain;
    font-size: 18px;
    width: 271px;
    height: 40px;
  }
}
@media (max-height: 460px) {
  .button {
    margin-top: 10px;
    background-size: contain;
    font-size: 18px;
    width: 271px;
    height: 40px;
  }

  .logout {
    height: 10%;
    font-size: 16px;
    margin-top: 10px;
    padding-top: 10px;
    padding-bottom: 10px;
  }

  .avatar {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 70px;
    height: 70px;
    border: 2px solid #000000;
    border-radius: 50%;
  }

  .avatar-img {
    height: 77px;
    border-radius: 50%;
    object-fit: cover;
  }

}

@media (max-height: 350px) {
  .wrapper>* {
    font-size: 12px;
  }

  .button {
    margin-top: 20px;
    background-size: contain;
  }
}
@media (max-height: 628px) {
  .username p {
    font-size: 15px; padding: 0; margin: 1%; width: 100%;
  }
}

</style>