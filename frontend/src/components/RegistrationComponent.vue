<script setup>
import axios from "axios";
import LoginComponent from "@/components/LoginComponent.vue";
import {ref, defineProps} from "vue";
import showPasswordIcon from "@/assets/show-password.svg";
import hidePasswordIcon from "@/assets/hide-password.svg";
import {store} from "@/js/store.js";
import {playClickSound, playHoverSound} from "@/js/soundEffects.js";
import { errorMessages } from "vue/compiler-sfc";

const props = defineProps(['revertMenu']);
const showLogin = ref(false); 
const showPassword = ref(false); 
const errorMessage = ref(false);
const username = ref(""); 
const password = ref(""); 
const confirmPassword = ref(""); 

function showLoginForm(){
  showLogin.value = !showLogin.value;
}

function togglePassword() {
  showPassword.value = !showPassword.value;
}

async function registerUser() { 
  if (password.value !== confirmPassword.value) { 
    errorMessage.value = true;
    return; 
  } 

  try { 
    const response = await axios.post('/api/register/', { 
      username: username.value, 
      password: password.value, 
    });

    store.userToken = response.data.token;
    store.username = username.value;
    store.userId = response.data.id;
    props.revertMenu();
  } catch (error) { 
    if (error.response && error.response.status === 400) {
      const errors = error.response.data;
      const errorMessages = Object.values(errors).flat(); 
      alert(errorMessages);
    } else {
      alert("Ошибка при регистрации: Неизвестная ошибка");
    }
  }
}

</script>

<template>
<dialog v-if="errorMessage" open>
  <article class="dialog">
    <p>
      <strong>🔒 Пароли не совпадают!</strong><br>
      Убедитесь, что вы правильно указали оба пароля.
    </p>
    <button class="button" style="margin: 0; background-color: transparent; border: none" @mouseover="playHoverSound" @mousedown="playClickSound"
      @click="errorMessage = false">Закрыть
    </button>
  </article>
</dialog>
<div v-if="!showLogin" class="registration-form">
  <h3>Регистрация</h3>
  <input
      v-model="username" 
      placeholder="Никнейм"
      aria-label="Login"
      autocomplete="username"
  />

  <div class="password-wrapper" style="width: 100%">
    <input style="margin:0"

           :type="showPassword ? 'text' : 'password'"
           v-model="password"
           placeholder="Пароль"
           aria-label="Password"
           autocomplete="current-password"
    />
    <img :src="showPassword ? showPasswordIcon : hidePasswordIcon" alt="" class="toggle-eye" @click="togglePassword">
  </div>
  <div class="password-wrapper" style="margin-top: 17px; width: 100%">
    <input style="margin:0"
           type="password"
           v-model="confirmPassword"
           placeholder="Повторите пароль"
           aria-label="Password"
           autocomplete="current-password"
    />
  </div>
  <button @click="registerUser" style="margin-top: 17px; width: 100%" @mouseover="playHoverSound" @mousedown="playClickSound">Зарегистрироваться</button>
  <p style="margin:0; margin-top: 10px; font-size: 18px">Уже есть аккаунт? <a href="" @click.prevent = showLoginForm>Войти</a></p>
</div>
  <LoginComponent v-else />
</template>


<style scoped>
.password-wrapper{
  position: relative;
}
.toggle-eye{
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  cursor: pointer;
}

a:hover{
  color: #261C5CFF!important;
  text-decoration-color: #261C5CFF !important;
}

button{
  padding-top: 10px;
  padding-bottom: 10px;
  width: 100%;
  background-color: #7361f7;
  box-shadow: 0px 6px 0px 0px #320067;
  border: none;
  color: #ffffff;
}
button:hover{
  background: #5a4db8
}
.dialog {
  padding-left:5%;
  padding-right:5%;
  border-radius: 10px;
  flex-wrap: wrap;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
}
.button {
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
.button:hover {
  background-image: url("../assets/hover_button.svg");
}
.registration-form{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.35);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0,0,0,0.5);
  width: 100%;
}
@media (max-height: 467px) {
  .registration-form{
    padding: 10px;
  }
  p{
    font-size: 12px !important;
  }
  button{
    padding-top: 7.5px;
    padding-bottom: 7.5px;
    font-size: 14px
  }
  input{
    margin-bottom: 10px;
    padding-top: 0px !important;
    padding-bottom:0px !important;
    font-size: 14px;
    height: 40px !important;
  }
  h3{
    margin-bottom: 10px;
    font-size: 20px;
  }
}
</style>