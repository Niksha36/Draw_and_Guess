<script setup>
import showPasswordIcon from '../assets/show-password.svg';
import hidePasswordIcon from '../assets/hide-password.svg';
import RegistrationComponent from './RegistrationComponent.vue';
import {ref} from "vue";
const showPassword = ref(false);

function togglePassword() {
  showPassword.value = !showPassword.value;
}
function showRegistrationForm() {
  showPassword.value = !showPassword.value;
}
</script>

<template>
<div v-if=!showPassword class="login-form">
  <h3>Вход</h3>
  <input
      name="nikname"
      placeholder="Никнейм"
      aria-label="Login"
      autocomplete="username"
  />
  <div class="password-wrapper">
    <input style="margin:0"
        :type="showPassword ? 'text' : 'password'"
        name="password"
        placeholder="Пароль"
        aria-label="Password"
        autocomplete="current-password"
    />
    <img :src="showPassword ? showPasswordIcon : hidePasswordIcon" alt="" class="toggle-eye" @click="togglePassword">
  </div>

  <button style="margin-top: 17px">Войти</button>
  <p style="margin:0; margin-top: 10px; font-size: 18px">Еще нет аккаунта? <a href="" @click.prevent = showRegistrationForm>Зарегистрироваться</a></p>
</div>
  <RegistrationComponent v-else />

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
  width: 30%;
}
button{
  padding-top: 10px;
  padding-bottom: 10px;
  width: 100%;
}
.toggle-eye{
  position: absolute;
  top: 50%;
  right: 10px;
  transform: translateY(-50%);
  cursor: pointer;
}
</style>