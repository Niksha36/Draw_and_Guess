<script setup>
import usersTableComponent from './usersInGameTableComponent.vue';
import chatComponent from './chatComponent.vue';
import answersComponent from './AnswersComponent.vue';
import axios from 'axios';
import { store } from "@/js/store.js";
import {onMounted, ref, onBeforeUnmount } from 'vue';
import {useRouter} from 'vue-router';
import {io} from 'socket.io-client';

const selectedColor = ref(null);
const currentColor = ref('black');
const brushThickness = ref(5);
const isEraserActive = ref(false);
const isEraserBlackedOut = ref(false);
const router = useRouter();
const socket = io('http://localhost:3000');
const words = ref([]);
const allWords = ref([]);
const canvasStates = ref([]);
const isDialogOpen = ref(false); 
const isPainter = ref(false);
const progressValue = ref(0);
let timer = null;


async function getTopicWords() {
  try {
    const response = await axios.get(`/api/room/${store.roomId}/`);
    const data = await fetch('/words.json').then(response => response.json());
    allWords.value = data[response.data.topic];
  } catch (error) {
    console.error('Ошибка при загрузке данных:', error);
  }
}

async function goToMenu() {
  try {
    await axios.patch(`/api/room/${store.roomId}/exit/`, {
      user_id: store.userId
    });

    router.push('/');
  } catch (error) {
    console.error(error);
    alert("Ошибка при выходе из комнаты. Повторите позже.");
  }
}

function clearCanvas() {
  const canvas = document.getElementById('paintCanvas');
  const ctx = canvas.getContext('2d');
  ctx.clearRect(0, 0, canvas.width, canvas.height);
}

async function changePainter() {
  const response = await axios.get(`/api/room/${store.roomId}/`);
  isPainter.value = response.data.painter == store.userId;
  store.isPainter = isPainter.value;

  if (isPainter.value && !store.beforeunmount) {
    isDialogOpen.value = true;
  }
}

async function startNextRound(word) {
  clearCanvas();
  startTimer();

  const [word1, word2] = getRandomWords(allWords.value);
  words.value = [word1, word2];
  
  socket.emit('correctAnswer', {correctAnswer: word})
  if (isPainter.value && !store.beforeunmount) {
    await axios.post(`/api/room/${store.roomId}/round`);
    socket.emit('startNextRound');
  }
}

function startTimer() {
  progressValue.value = 0;
  isDialogOpen.value = false;
  
  if (timer) clearInterval(timer);
  timer = setInterval(() => {
    if (progressValue.value < 100) {
      progressValue.value += 3.33;
    } else {
      clearInterval(timer);
      store.beforeunmount = false;
      changePainter();
    }
  }, 1000);
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
  toggleEraserBlackout();
};

const saveCanvasState = (canvas, ctx) => {
  const dataUrl = canvas.toDataURL();
  canvasStates.value.push(dataUrl);
};

function getRandomWords(allWords) {
  const randomIndex1 = Math.floor(Math.random() * allWords.length);
  let randomIndex2 = Math.floor(Math.random() * allWords.length);

  while (randomIndex2 === randomIndex1) {
    randomIndex2 = Math.floor(Math.random() * allWords.length);
  }

  return [allWords[randomIndex1], allWords[randomIndex2]];
}

window.addEventListener('beforeunload', () => {
  store.beforeunmount = true;
});

onMounted(async () => {
  await getTopicWords(); 
  const [word1, word2] = getRandomWords(allWords.value);
  words.value = [word1, word2];

  socket.emit('joinRoom', store.roomId);
  socket.on('startNextRound', () => {
    startTimer();
    clearCanvas();
  });
  socket.on('updateScore', (data) => {
    if (isPainter.value && data.userName != store.username) {
      let points = 5; // Кол-во баллов за то, что рисунок аватора 
      socket.emit('updateScore', { userName: store.username, increment: points });
      axios.patch(`/api/user/${store.userId}/update`, {
        points: points,
      })
      .catch(error => {
        console.error('Ошибка:', error);
      });
    }
  });
  
  if (!store.beforeunmount) {
    changePainter();
  } else {
    progressValue.value = 80;
    timer = setInterval(() => {
    if (progressValue.value < 100) {
      progressValue.value += 3.33;
    } else {
      clearInterval(timer);
      store.beforeunmount = false;
      changePainter();
    }
  }, 1000);
  }

  const canvas = document.getElementById('paintCanvas');
  const ctx = canvas.getContext('2d');
  let painting = false;
  let lastX = 0;
  let lastY = 0;

  const resizeCanvas = () => {
    const tempCanvas = document.createElement('canvas');
    const tempCtx = tempCanvas.getContext('2d');
    tempCanvas.width = canvas.width;
    tempCanvas.height = canvas.height;
    tempCtx.drawImage(canvas, 0, 0);

    canvas.width = canvas.parentElement.clientWidth;
    canvas.height = canvas.parentElement.clientHeight;
    ctx.drawImage(tempCanvas, 0, 0);
  };

  window.addEventListener('resize', resizeCanvas);

  const startPosition = (e) => {
    painting = true;
    const rect = canvas.getBoundingClientRect();
    lastX = e.clientX - rect.left;
    lastY = e.clientY - rect.top;
    draw(e);
  };

  const endPosition = () => {
    painting = false;
    ctx.beginPath();
  };

  const draw = (e) => {
    if (!painting || !isPainter.value) return;

    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const boundaryPercentageY = 9;
    const boundaryPercentageX = 3;
    if (x < (canvas.width * boundaryPercentageX / 100) ||
        x > (canvas.width * (100 - boundaryPercentageX) / 100) ||
        y < (canvas.height * boundaryPercentageY / 100) ||
        y > (canvas.height * (100 - boundaryPercentageY) / 100)) {
      endPosition();
      startPosition();
    }
    const drawData = {
      x,
      y,
      lastX,
      lastY,
      color: currentColor.value,
      thickness: brushThickness.value,
      isEraser: isEraserActive.value,
    };

    socket.emit('draw', drawData);

    drawOnCanvas(drawData);

    lastX = x;
    lastY = y;
  };

  const drawOnCanvas = (data) => {
    ctx.beginPath();
    ctx.moveTo(data.lastX, data.lastY);

    if (data.isEraser) {
      ctx.save();
      ctx.globalCompositeOperation = 'destination-out';
      ctx.lineWidth = data.thickness;
      ctx.lineCap = 'round';
      ctx.strokeStyle = 'rgba(0,0,0,1)';

      ctx.lineTo(data.x, data.y);
      ctx.stroke();
      ctx.restore();
    } else {
      ctx.lineWidth = data.thickness;
      ctx.lineCap = 'round';
      ctx.strokeStyle = data.color;

      ctx.lineTo(data.x, data.y);
      ctx.stroke();
    }
  };

  const undoLastAction = (canvas, ctx) => {
    if (canvasStates.value.length > 0) {
      const lastState = canvasStates.value.pop();
      const img = new Image();
      img.src = lastState;
      img.onload = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0);
      };
      socket.emit('undo', lastState); // Emit undo event to the server
    }
  };

  window.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'z') {
      undoLastAction(canvas, ctx);
    }
  });

  socket.on('undo', (lastState) => {
    const img = new Image();
    img.src = lastState;
    img.onload = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.drawImage(img, 0, 0);
    };
  });
  socket.on('draw', (data) => {
    drawOnCanvas(data);
  });

  canvas.addEventListener('mousedown', (e) => {
    saveCanvasState(canvas, ctx);
    startPosition(e);
  });
  canvas.addEventListener('mouseup', endPosition);
  canvas.addEventListener('mousemove', draw);
  canvas.addEventListener('mouseleave', endPosition);
  canvas.addEventListener('mouseout', endPosition);

  resizeCanvas();
});
</script>

<template>
  <div class="background" draggable="false">
    <dialog open v-if="isDialogOpen">
      <article  class="dialog">
        <p>
          <strong class="text">Выберите тему</strong>
        </p>
        <button
            v-for="word in words"
            :key="word"
            class="button"
            style="margin: 5px; background-color: transparent; border: none"
            @click="startNextRound(word)"
        >
          {{ word }}
        </button>
      </article>
    </dialog>
    <div class="main-wrapper">
      <div class="left-wrapper">
        <div class="user-list-wrapper" style="position: relative;">
          <img src="../assets/bg_rank.svg" alt="" class="user-list-img">
          <usersTableComponent/>
        </div>

        <div class="answers" draggable="false" style="position: relative;">
          <answers-component/>
          <div class="chat-banner">
            <span>Ответы</span>
          </div>
        </div>

        <div class="chat" draggable="false" style="position: relative;">
          <chatComponent/>
          <div class="chat-banner">
            <span>Чат</span>
          </div>
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
        <div class="draw-time-wrapper" style="position: absolute; padding-left:3%; padding-right: 10%; display:flex; justify-content: space-between; align-items: center; bottom: 5%; z-index: 100;  width: 100%">
          <img src="../assets/ic_time.svg" alt="time" width="10%">
          <progress class="custom-progress" style="color: deeppink!important;margin: 0; width: 100%" :value="progressValue" max="100"></progress>
        </div>

      </div>

      <div class="tools-panel">
        <div class="colors" style="display: flex; justify-content: center">
          <div class="one-color" @click="changeColor('black', $event)"
               style="background-color: black; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('white', $event)"
               style="background-color: white; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('red', $event)"
               style="background-color: red; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('orange', $event)"
               style="background-color: orange; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('yellow', $event)"
               style="background-color: yellow; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('green', $event)"
               style="background-color: #00ff00; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('Cyan', $event)"
               style="background-color: #00fffa; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('blue', $event)"
               style="background-color: blue; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('violet', $event)"
               style="background-color: violet; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('purple', $event)"
               style="background-color: purple; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('magenta', $event)"
               style="background-color: magenta; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('pink', $event)"
               style="background-color: pink; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('brown', $event)"
               style="background-color: brown; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
          <div class="one-color" @click="changeColor('gray', $event)"
               style="background-color: gray; width: 30px; height: 30px; border-radius: 50%;cursor: pointer"></div>
        </div>

        <div class="brush-thickness" style="margin-top: 20px; user-select: none;" draggable="false">
          <label draggable="false" for="thicknessRange" class="brush-thickness-text"
                 style="text-align: center">Толщина</label>
          <input style="color: #858585" draggable="false" id="thicknessRange" type="range" min="1" max="50"
                 v-model="brushThickness"
                 @input="changeThickness(brushThickness)"/>
        </div>
        <div class="eraser" @click="activateEraser" style="user-select: none; cursor: pointer" draggable="false">
          <img src="../assets/eraser.svg" alt="Eraser" class="eraser-icon" draggable="false"
               :style="{ filter: isEraserBlackedOut ? 'brightness(0.75)' : 'none' }">
        </div>
      </div>
    </div>
  </div>

</template>
<style>
:root {
  --text-shadow: rgb(23, 5, 87) 3px 0px 0px, rgb(23, 5, 87) 2.83487px .981584px 0px, rgb(23, 5, 87) 2.35766px 1.85511px 0px, rgb(23, 5, 87) 1.62091px 2.52441px 0px, rgb(23, 5, 87) .705713px 2.91581px 0px, rgb(23, 5, 87) -.287171px 2.98622px 0px, rgb(23, 5, 87) -1.24844px 2.72789px 0px, rgb(23, 5, 87) -2.07227px 2.16926px 0px, rgb(23, 5, 87) -2.66798px 1.37182px 0px, rgb(23, 5, 87) -2.96998px .42336px 0px, rgb(23, 5, 87) -2.94502px -.571704px 0px, rgb(23, 5, 87) -2.59586px -1.50383px 0px, rgb(23, 5, 87) -1.96093px -2.27041px 0px, rgb(23, 5, 87) -1.11013px -2.78704px 0px, rgb(23, 5, 87) -.137119px -2.99686px 0px, rgb(23, 5, 87) .850987px -2.87677px 0px, rgb(23, 5, 87) 1.74541px -2.43999px 0px, rgb(23, 5, 87) 2.44769px -1.73459px 0px, rgb(23, 5, 87) 2.88051px -.838247px 0px;
}
</style>

<style scoped>
.chat-banner{
  position: absolute;
  padding:1.5% 0;
  width: 40%;
  top: -12%;
  text-transform: uppercase;
  text-align: center;
  box-shadow: 0px 6px 0px 0px #301a6b;
  background: deeppink;
  border-radius: 7px;
  color: #5cffb6;
  font-weight: bold;
  right:0;
  text-shadow: var(--text-shadow);
}
.custom-progress::-webkit-progress-value {
  background-color: deeppink;
}

.brush-thickness-text {
  font-weight: bold;
  font-size: 18px;
  color: #5cffb6;
  text-shadow: var(--text-shadow);
  text-transform: uppercase;
}

#thicknessRange::-webkit-slider-runnable-track {
  background: rgba(116, 84, 249);
  height: 8px;
  border-radius: 5px;
}

#thicknessRange::-webkit-slider-thumb {
  background: #5cffb6;
  border: 2.5px solid rgb(23, 5, 87) /* Change this to your desired color */
}

.chat {
  padding: 10px;
}

.home-icon {
  position: absolute;
  right: 0;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.user-list-img {
  height: 100% !important;
  width: 100% !important;
}

.left-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-size: 100% 100%;
}

.user-list-wrapper {
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
  background-image: url("../assets/bg.svg");
  background-color: #7361f7;
  height: 100vh;
  width: 100vw;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.left-wrapper {
  width: 376px;
}

.answers {
  background: white;
  border-radius: 20px;
  height: 212px;
  padding: 10px;
  padding-top:6%;
  box-shadow: 0 4px 8px rgb(93, 205, 255), 0 6px 20px rgb(93, 205, 255);
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
  padding-top:6%;
  box-shadow: 0 4px 8px rgb(93, 205, 255), 0 6px 20px rgb(93, 205, 255);
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

.main-wrapper {
  display: flex;
  justify-content: space-between;
  width: 100%;
  height: 90%;
  padding: 0 10px;
}

.tools-panel {
  display: flex;
  flex-direction: column;

  align-items: center;
  background: rgba(245, 245, 245, 0.92);
  border-radius: 20px;
  width: 150px;
  height: 100%;
  padding: 10px 10px 10px 10px;
}

.go-to-menu-icon {
  position: absolute;
  display: block;
  z-index: 10;
  top: 5.2%;
  left: 3.5%;
}

canvas {
  width: 100%;
  height: 100%;
  position: absolute;
  display: block;
  z-index: 10;
}

.colors {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  min-width: 10px;
  min-height: 10px;
}

.colors div {
  border-radius: 50%;
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

.text {
  margin: 10px;
  font-weight: bold;
  font-size: 22px;
  color: #5cffb6;
  text-shadow: rgb(23, 5, 87) 3px 0px 0px, rgb(23, 5, 87) 2.83487px .981584px 0px, rgb(23, 5, 87) 2.35766px 1.85511px 0px, rgb(23, 5, 87) 1.62091px 2.52441px 0px, rgb(23, 5, 87) .705713px 2.91581px 0px, rgb(23, 5, 87) -.287171px 2.98622px 0px, rgb(23, 5, 87) -1.24844px 2.72789px 0px, rgb(23, 5, 87) -2.07227px 2.16926px 0px, rgb(23, 5, 87) -2.66798px 1.37182px 0px, rgb(23, 5, 87) -2.96998px .42336px 0px, rgb(23, 5, 87) -2.94502px -.571704px 0px, rgb(23, 5, 87) -2.59586px -1.50383px 0px, rgb(23, 5, 87) -1.96093px -2.27041px 0px, rgb(23, 5, 87) -1.11013px -2.78704px 0px, rgb(23, 5, 87) -.137119px -2.99686px 0px, rgb(23, 5, 87) .850987px -2.87677px 0px, rgb(23, 5, 87) 1.74541px -2.43999px 0px, rgb(23, 5, 87) 2.44769px -1.73459px 0px, rgb(23, 5, 87) 2.88051px -.838247px 0px;
  text-transform: uppercase;
  text-align: center;
}

@media (max-height: 460px) or (max-width: 770px) {
  .go-to-menu-icon {
    width: 20px;
    height: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .tools-panel {
    padding: 5px;
  }

  .one-color {
    width: 27px !important;
    height: 27px !important;
  }
}

@media (max-height: 352px) or (max-width: 770px) {
  .one-color {
    width: 20px !important;
    height: 20px !important;
  }
}

@media (max-width: 1134px) {
  .left-wrapper {
    max-width: 200px
  }
}

@media (max-width: 700px) {
  .left-wrapper {
    max-width: 150px
  }
}

</style>