<script setup>
import usersTableComponent from './usersInGameTableComponent.vue';
import chatComponent from './chatComponent.vue'
import { onMounted, ref } from 'vue';
import {useRouter} from 'vue-router';
const selectedColor = ref(null);
const currentColor = ref('black');
const brushThickness = ref(5);
const isEraserActive = ref(false);
const isEraserBlackedOut = ref(false);
const router = useRouter();
function goToMenu() {
  router.push('/');
}
const toggleEraserBlackout = () => {
  isEraserBlackedOut.value = !isEraserBlackedOut.value;
};
const changeColor = (color, event) => {
  if (selectedColor.value) {
    selectedColor.value.style.border = 'none';
  }
  selectedColor.value = event.target;
  selectedColor.value.style.border = '2px solid black';
  currentColor.value = color;
  isEraserActive.value = false;
};

const changeThickness = (thickness) => {
  brushThickness.value = thickness;
};

const activateEraser = () => {
  isEraserActive.value = true;
  toggleEraserBlackout()
};

onMounted(() => {
  const canvas = document.getElementById('paintCanvas');
  const ctx = canvas.getContext('2d');
  let painting = false;

  canvas.width = canvas.parentElement.clientWidth;
  canvas.height = canvas.parentElement.clientHeight;

  const startPosition = (e) => {
    painting = true;
    draw(e);
  };

  const endPosition = () => {
    painting = false;
    ctx.beginPath();
  };

  const draw = (e) => {
    if (!painting) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    if (x < 60 || x > canvas.width - 60 || y < 60 || y > canvas.height - 60) {
      endPosition()
      startPosition()
    }

  if (isEraserActive.value) {
    ctx.save();
    ctx.globalCompositeOperation = 'destination-out';
    ctx.lineWidth = brushThickness.value;
    ctx.lineCap = 'round';
    ctx.strokeStyle = 'rgba(0,0,0,1)';

    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);
    ctx.restore();
  } else {
    ctx.lineWidth = brushThickness.value;
    ctx.lineCap = 'round';
    ctx.strokeStyle = currentColor.value;

    ctx.lineTo(x, y);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(x, y);
  }
};

  canvas.addEventListener('mousedown', startPosition);
  canvas.addEventListener('mouseup', endPosition);
  canvas.addEventListener('mousemove', draw);
});
</script>

<template>
  <div class="background" draggable="false">
    <div class="main-wrapper">
      <div class="left-wrapper">
        <div class="user-list-wrapper" style="position: relative;">
            <img src="../assets/bg_rank.svg" alt="" class="user-list-img">
            <usersTableComponent />
        </div>

        <div class="answers" draggable="false">

        </div>

        <div class="chat" draggable="false">
          <chatComponent/>
        </div>
      </div>

      <div class="paint-board-wrapper" draggable="false">
        <img src="../assets/bg_content.svg" alt="Background" class="background-image" draggable="false">
        <canvas draggable="false" id="paintCanvas"></canvas>
        <div class="go-to-menu-icon-wrapper" @click="goToMenu" style="cursor: pointer">
          <div class="go-to-menu-icon">
            <img src="../assets/small_button_border.svg" alt="border" class="home-border">
            <img src="../assets/ic_home.svg" alt="home-icon" width="33px" class="home-icon">
          </div>
        </div>
      </div>

      <div class="tools-panel">
        <div class="colors" style="display: flex; justify-content: center">
          <div class="one-color" @click="changeColor('red', $event)" style="background-color: red; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('orange', $event)" style="background-color: orange; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('yellow', $event)" style="background-color: yellow; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('green', $event)" style="background-color: #00ff00; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('Cyan', $event)" style="background-color: #00fffa; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('blue', $event)" style="background-color: blue; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('violet', $event)" style="background-color: violet; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('purple', $event)" style="background-color: purple; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('magenta', $event)" style="background-color: magenta; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('pink', $event)" style="background-color: pink; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('brown', $event)" style="background-color: brown; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('gray', $event)" style="background-color: gray; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
        </div>

        <div class="brush-thickness" style="margin-top: 20px; user-select: none;" draggable="false">
          <label draggable="false" for="thicknessRange" style="text-align: center">Толщина</label>
          <input draggable="false" id="thicknessRange" type="range" min="1" max="50" v-model="brushThickness" @input="changeThickness(brushThickness)" />
        </div>
        <div class="eraser" @click="activateEraser" style="user-select: none; cursor: pointer" draggable="false">
          <img src="../assets/eraser.svg" alt="Eraser" class="eraser-icon" draggable="false" :style="{ filter: isEraserBlackedOut ? 'brightness(0.75)' : 'none' }" >
        </div>
      </div>
    </div>
  </div>

</template>

<style scoped>
.chat{
  padding: 10px;
}
.home-icon {
  position: absolute;
  right:0;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
.user-list-img{
  height: 100%!important;
  width: 100%!important;
}
.left-wrapper{
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-size: 100% 100%;
}
.user-list-wrapper{
  min-height: 1px;
  /*
  background-image: url("../assets/bg_rank.svg");
  background-size: cover;
  background-repeat: no-repeat;
   */
  height: 200px;
  width: 100%;
}
.background {
  background-image: url("../assets/bg.svg") ;
  background-color: #7361f7;
  height: 100vh;
  width: 100vw;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.left-wrapper{
  width: 376px;
}
.answers {
  background: white;
  border-radius: 20px;
  height: 212px;
}
.user-list-wrapper,
.answers,
.chat {
  width: 100%;
  flex-grow: 1;
  margin-bottom: 2rem;
}
.chat {
  background: white;
  border-radius: 20px;
  height: 212px;
  margin-bottom: 0px;
}

.paint-board-wrapper {
  position: relative;
  height: 100%;
  width: 65%;
  margin-left: 20px;
  user-select: none;
}

.background-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  pointer-events: none;
}

canvas {
  position: relative;
  z-index: 2;
}
.main-wrapper{
  display: flex;
  justify-content: space-between;
  width: 100%;
  height: 90%;
  padding: 0 10px;
}
.tools-panel{
  display:flex;
  flex-direction: column;

  align-items: center;
  background: white;
  border-radius: 20px;
  width: 150px;
  height: 100%;
  padding:10px 10px 10px 10px;
}
.go-to-menu-icon{
  position:absolute;
  display: block;
  z-index:10;
  top: 5.2%;
  left:3.5%;
}
canvas {
  position:absolute;
  display: block;
  z-index:10;
}
.colors{
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  min-width: 10px;
  min-height: 10px;
}
.colors div {
  border-radius: 50%;
}
@media (max-height: 460px) or (max-width: 770px) {
  .go-to-menu-icon {
    width: 20px;
    height: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .tools-panel{
    padding: 5px;
  }
  .one-color{
    width: 27px !important;
    height: 27px !important;
  }
}
@media (max-height: 352px) or (max-width: 770px) {
  .one-color{
    width: 20px !important;
    height: 20px !important;
  }
}
@media (max-width: 1134px){
  .left-wrapper{
    max-width: 200px
  }
}
@media (max-width: 700px){
  .left-wrapper{
    max-width: 150px
  }
}

</style>