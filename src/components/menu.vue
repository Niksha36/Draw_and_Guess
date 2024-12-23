<script setup>
import {useRouter} from 'vue-router';
import {ref} from "vue";
import '@fortawesome/fontawesome-free/css/all.css';
import LoginComponent from './LoginComponent.vue';

const router = useRouter();
const showLogin = ref(false);

function goToGame() {
  router.push('/game');
}
function logout() {
  showLogin.value = true;
}
function revertMenu() {
  showLogin.value = false;
}
</script>

<template>
  <div class="background">

    <div class="menu-wrapper">
      <img src="../assets/bg_content.svg" class="border-background-img" alt="">
      <div  v-if="showLogin" class="go-to-menu-icon-wrapper" @click="revertMenu">
        <div class="go-to-menu-icon">
          <img src="../assets/small_button_border.svg" alt="border" class="home-border">
          <img src="../assets/ic_home.svg" alt="home-icon" width="33px" class="home-icon">
        </div>
      </div>

      <div  class="wrapper">
        <div v-if="!showLogin"  class="content">
          <div class="avatar">
            <img src="../assets/avatar.svg" alt="Avatar" class="avatar-img">
          </div>
          <button class="logout" @click="logout">
            <i class="fas fa-sign-out-alt"></i> Выйти
          </button>
          <div class="button-play button" @click="goToGame">
            Играть
          </div>
          <div class="button-create-room button">
            Комнаты
          </div>
        </div>
        <LoginComponent v-else />

      </div>

    </div>


  </div>
</template>

<style scoped>
.border-background-img{
  width: 100%;
  height: 100%;
}
.go-to-menu-icon-wrapper{
  cursor: pointer;
}
.menu-wrapper{
  position:relative;
}
.go-to-menu-icon-wrapper{
  position:absolute;
  top: 4.5%;
  left:2.8%;
}

.home-icon {
  position: absolute;
  right:0;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);

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

.content{
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
  height: 80%;
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

.avatar {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 120px;
  height: 120px;
  border: 2px solid #000000;
  border-radius: 50%;
}

.avatar-img {
  height: 135px;
  border-radius: 50%;
  object-fit: cover;
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
}

.button:hover {
  background-image: url("../assets/hover_button.svg");
}

@media (max-height: 515px) {
  .button {

    background-size: contain;
  }
}

@media (max-height: 460px) {
  .button {
    margin-top: 15px;
    background-size: contain;
    font-size: 18px;
    width: 271px;
    height: 56px;
  }

  .logout {
    height: 10%;
    font-size: 16px;
    margin-top: 15px;
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
  .wrapper > * {
    font-size: 12px;
  }

  .button {
    margin-top: 20px;
    background-size: contain;
  }
}
</style>