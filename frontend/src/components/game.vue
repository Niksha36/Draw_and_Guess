<script setup>
import { onMounted, ref } from 'vue';

const selectedColor = ref(null);
const currentColor = ref('black');
const brushThickness = ref(5);
const isEraserActive = ref(false);

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

    if (x < 60 || x > canvas.width - 60 || y < 60 || y > canvas.height - 60) return;

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
  <div class="background">
    <div class="main-wrapper">
      <div class="left-wrapper">
        <div class="user-list-wrapper">
          <div class="user-list">

          </div>
        </div>

        <div class="answers">

        </div>

        <div class="chat">

        </div>
      </div>

      <div class="paint-board-wrapper">
        <img src="../assets/bg_content.svg" alt="Background" class="background-image" >
        <canvas id="paintCanvas"></canvas>
      </div>

      <div class="tools-panel">
        <div class="colors">
          <div @click="changeColor('red', $event)" style="background-color: red; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div @click="changeColor('orange', $event)" style="background-color: orange; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div @click="changeColor('yellow', $event)" style="background-color: yellow; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div @click="changeColor('green', $event)" style="background-color: #00ff00; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div @click="changeColor('Cyan', $event)" style="background-color: #00fffa; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div @click="changeColor('blue', $event)" style="background-color: blue; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div @click="changeColor('violet', $event)" style="background-color: violet; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div @click="changeColor('purple', $event)" style="background-color: purple; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div @click="changeColor('magenta', $event)" style="background-color: magenta; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div @click="changeColor('pink', $event)" style="background-color: pink; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div @click="changeColor('brown', $event)" style="background-color: brown; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div @click="changeColor('gray', $event)" style="background-color: gray; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
        </div>

        <div class="brush-thickness" style="margin-top: 20px; margin-left: -10px; margin-right:10px" >
          <label for="thicknessRange">Толщина</label>
          <input id="thicknessRange" type="range" min="1" max="50" v-model="brushThickness" @input="changeThickness(brushThickness)" />
        </div>
        <div class="eraser" @click="activateEraser">
          <img src="../assets/eraser.svg" alt="Eraser" class="eraser-icon">
        </div>
      </div>
    </div>
  </div>

</template>

<style scoped>
.left-wrapper{
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-size: 100% 100%;
}
.user-list-wrapper{
  background-image: url("../assets/bg_rank.svg");
  background-size: cover;
  background-repeat: no-repeat;
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
  background: white;
  border-radius: 20px;
  width: 150px;
  height: 100%;
  padding:10px 0 10px 20px;
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
}
.colors div {
  border-radius: 50%;
}

</style>