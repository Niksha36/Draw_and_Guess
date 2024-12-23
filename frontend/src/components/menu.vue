<script setup>
import { useRouter } from 'vue-router';
import '@fortawesome/fontawesome-free/css/all.css';
const router = useRouter();

function goToGame() {
  router.push('/game');
}
</script>

<template>
  <div class="background">

    <div class="menu-wrapper">

    </div>
    <div class="wrapper">
      <div class="avatar">
        <img src="../assets/avatar.svg" alt="Avatar" class="avatar-img">
      </div>
      <button class="logout">
        <i class="fas fa-sign-out-alt"></i> Выйти
      </button>
      <div class="button-play button" @click="goToGame">
        Играть
      </div>
      <div class="button-create-room button">
        Комнаты
      </div>
    </div>

  </div>
</template>

<style scoped>
.background {
  position: relative;
  background-image: url("../assets/bg.svg");
  background-color: #7361f7;
  height: 100vh;
  width: 100vw;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.menu-wrapper {
  content: url("../assets/bg_content.svg");
  height: 100%;
}
.logout{
  height:50px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top:20px
}
.avatar {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100px;
  height: 100px;
  border: 2px solid #000000;
  border-radius: 50%;
}

.avatar-img {
  height: 115px;
  border-radius: 50%;
  object-fit: cover;
}

.wrapper {
  position: absolute;
  z-index: 1;
  display:flex;
  flex-direction:column;
  justify-content:center;
  align-items: center;
}
.button{
  background-image: url("../assets/button.svg");
  width:281px;
  height:66px ;
  color: #ffd506;
  text-shadow: rgb(23,21,86)4px 0px 0px,rgb(23,21,86)3.87565px .989616px 0px,rgb(23,21,86)3.51033px 1.9177px 0px,rgb(23,21,86)2.92676px 2.72656px 0px,rgb(23,21,86)2.16121px 3.36588px 0px,rgb(23,21,86)1.26129px 3.79594px 0px,rgb(23,21,86).282949px 3.98998px 0px,rgb(23,21,86)-.712984px 3.93594px 0px,rgb(23,21,86)-1.66459px 3.63719px 0px,rgb(23,21,86)-2.51269px 3.11229px 0px,rgb(23,21,86)-3.20457px 2.39389px 0px,rgb(23,21,86)-3.69721px 1.52664px 0px,rgb(23,21,86)-3.95997px .56448px 0px,rgb(23,21,86)-3.97652px -.432781px 0px,rgb(23,21,86)-3.74583px -1.40313px 0px,rgb(23,21,86)-3.28224px -2.28625px 0px,rgb(23,21,86)-2.61457px -3.02721px 0px,rgb(23,21,86)-1.78435px -3.57996px 0px,rgb(23,21,86)-.843183px -3.91012px 0px,rgb(23,21,86).150409px -3.99717px 0px,rgb(23,21,86)1.13465px -3.8357px 0px,rgb(23,21,86)2.04834px -3.43574px 0px,rgb(23,21,86)2.83468px -2.82216px 0px,rgb(23,21,86)3.44477px -2.03312px 0px,rgb(23,21,86)3.84068px -1.11766px 0px,rgb(23,21,86)3.9978px -.132717px 0px;
  font-size: 24px;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top:20px;
  cursor: pointer;
}
.button:hover{
  background-image: url("../assets/hover_button.svg");
}
</style>