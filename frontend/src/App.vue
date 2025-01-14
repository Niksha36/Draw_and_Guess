
<script setup>
import { RouterView } from 'vue-router';
import {onMounted, ref} from "vue";
const isLandscape = ref(window.innerWidth > window.innerHeight);

const checkOrientation = () => {
  isLandscape.value = window.innerWidth > window.innerHeight;
};
onMounted(() => {
  window.addEventListener('resize', checkOrientation);
  checkOrientation();
});
</script>

<template>
  <div>
    <RouterView />
    <dialog v-show="!isLandscape" open style="background-color:white">
      <p class="vertical-warning">Пожалуйста, поверните свой дивайс в горизонталбное положение 📱🔄</p>
    </dialog>
  </div>
</template>

<style scoped>
html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  transform: rotate(90deg);
  transform-origin: center;
}
.vertical-warning{
  text-align:center;
  font-weight: bold;
  font-size: 18px;
  color: #5cffb6;
  text-shadow: var(--text-shadow);
  text-transform: uppercase;
}
</style>
