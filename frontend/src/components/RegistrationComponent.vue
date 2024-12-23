<script setup>

import LoginComponent from "@/components/LoginComponent.vue";
import {ref} from "vue";
import showPasswordIcon from "@/assets/show-password.svg";
import hidePasswordIcon from "@/assets/hide-password.svg";
const showLogin = ref(false);
function showLoginForm(){
  showLogin.value = !showLogin.value;
}

const showPassword = ref(false);

function togglePassword() {
  showPassword.value = !showPassword.value;
}
</script>

<template>
<div v-if="!showLogin" class="registration-form">
  <h3>Регистрация</h3>
  <input
      name="nikname"
      placeholder="Никнейм"
      aria-label="Login"
      autocomplete="username"
  />

  <div class="password-wrapper" style="width: 100%">
    <input style="margin:0"

           :type="showPassword ? 'text' : 'password'"
           name="password"
           placeholder="Пароль"
           aria-label="Password"
           autocomplete="current-password"
    />
    <img :src="showPassword ? showPasswordIcon : hidePasswordIcon" alt="" class="toggle-eye" @click="togglePassword">
  </div>
  <div class="password-wrapper" style="margin-top: 17px; width: 100%">
    <input style="margin:0"
           type="password"
           name="password"
           placeholder="Повторите пароль"
           aria-label="Password"
           autocomplete="current-password"
    />
  </div>
  <button @click="showRegistrationForm" style="margin-top: 17px; width: 100%">Зарегистрироваться</button>
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
.registration-form{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.35);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0,0,0,0.5);
  width: 40%;
}
</style>