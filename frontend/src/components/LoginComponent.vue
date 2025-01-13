<script setup>
import axios from 'axios';
import showPasswordIcon from '../assets/show-password.svg';
import hidePasswordIcon from '../assets/hide-password.svg';
import RegistrationComponent from './RegistrationComponent.vue';
import {ref, defineEmits, defineProps} from "vue";
import router from "@/router.js";
import {store} from "@/js/store.js";
import {playClickSound, playHoverSound} from "@/js/soundEffects.js";

const props = defineProps(['revertMenu']);
const showPassword = ref(false);
const username = ref(""); 
const password = ref(""); 
const showRegistration = ref(false);
const emit = defineEmits(['login-success']);

function togglePassword() {
  showPassword.value = !showPassword.value;
}
function showRegistrationForm() {
  showRegistration.value = !showRegistration.value;
}
async function loginUser() {
  try { 
    const response = await axios.post('/api/login/', {   
      username: username.value,
      password: password.value,
    });

    store.userId = response.data.id;
    store.username = username.value;
    emit('login-success');
  } catch (error) {
    if (error.response && error.response.status === 400) {
      const errors = error.response.data;
      const errorMessages = Object.values(errors).flat(); 
      alert(errorMessages);
    } else {
      alert("Ошибка при авторизации: Неизвестная ошибка");
    }
  }
}

</script>

<template>
<div v-if="!showRegistration" class="login-form">
  <h3>Вход</h3>
  <input
      name="nikname"
      v-model="username"
      placeholder="Никнейм"
      aria-label="Login"
      autocomplete="username"
  />
  <div class="password-wrapper">
    <input style="margin:0"
        :type="showPassword ? 'text' : 'password'"
        name="password"
        v-model="password"
        placeholder="Пароль"
        aria-label="Password"
        autocomplete="current-password"
    />
    <img :src="showPassword ? showPasswordIcon : hidePasswordIcon" alt="" class="toggle-eye" @click="togglePassword">
  </div>

  <button @click="loginUser" style="margin-top: 17px" @mouseover="playHoverSound" @mousedown="playClickSound" >Войти</button>
  <p style="text-align: center; margin:0; margin-top: 10px; font-size: 18px">Еще нет аккаунта? <a href="" @click.prevent = showRegistrationForm>Зарегистрироваться</a></p>
</div>
  <RegistrationComponent v-else :revert-menu="props.revertMenu"/>
</template>

<style scoped>
.password-wrapper{
  position: relative;
  width: 100%
}
.login-form{
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
a:hover{
  color: #261C5CFF!important;
  text-decoration-color: #261C5CFF !important;
}
.toggle-eye{
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  cursor: pointer;
}
@media (max-height: 467px) {
  .login-form{
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