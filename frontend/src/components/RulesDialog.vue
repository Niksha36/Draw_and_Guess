<script setup>
import {defineEmits} from 'vue';

const emit = defineEmits(['close']);

function closeDialog() {
  emit('close');
}
</script>

<template>
  <dialog open style="z-index:1000">
    <div class="game-rules" style="
    width:90%!important;
    background:white;
    border-radius:20px;
    overflow-y: scroll;
    height:90%;
    padding:20px;

    ">
      <img src="../assets/img-close-button.png" alt="close-button" class="close-button" @click="closeDialog"
           style="
        position: absolute;
        top: 2%;
        right: 2%;
        cursor: pointer;
      ">

      <header class="game-header">
        <h1>Добро пожаловать в <span class="game-title">Scketch Guess</span> – взрыв эмоций и творчества в онлайн-формате!
          📖🎨</h1>
      </header>

      <main class="game-content">
        <section class="game-section">
          <h2>Цель игры</h2>
          <p>
            Игра идет до <strong>160 очков</strong>, так что будьте быстрыми, меткими и креативными! Каждый игрок получает
            баллы за скорость и
            сообразительность, а художник — за то, как хорошо его понимают.
          </p>
        </section>

        <section class="game-section">
          <h2>Как заработать очки?</h2>
          <ul>
            <li>🏆 <strong>Первый угадавший</strong> слово забирает 10 очков.</li>
            <li>🥈 <strong>Второй</strong> получает 6 очков.</li>
            <li>🥉 <strong>Третий</strong> — 4 очка.</li>
            <li>👫 Все остальные угадавшие получают по 2 очка.</li>
          </ul>
        </section>

        <section class="game-section">
          <h2>Баллы художника:</h2>
          <ul>
            <li>✍️ За каждую успешную догадку его рисунка художник получает 2 очка.</li>
            <li>🌟 Если <strong>ВСЕ игроки</strong> отгадали слово, художник получает дополнительный бонус: +3 очка!</li>
          </ul>
        </section>

        <section class="game-section">
          <h2>Чего нельзя делать:</h2>
          <ul>
            <li>❌ Рисовать буквы, цифры или любые подсказки, которые заменяют сам рисунок.</li>
            <li>❌ Писать или рисовать оскорбления — будьте доброжелательными!</li>
          </ul>
        </section>

        <section class="game-section">
          <h2>Готовы стать чемпионом?</h2>
          <p>
            Каждый ход — это шанс проявить себя. Удивляйте своих друзей необычными идеями, соревнуйтесь в
            сообразительности и наслаждайтесь
            моментами, когда ваш шедевр оказывается понят всеми. <strong>Вперёд!</strong> 🎉
          </p>
        </section>
      </main>
    </div>
  </dialog>


</template>

<style scoped>
strong{
  color:rgba(116, 84, 249);
}
li::marker {
  color: #170557FF; /* Change this to your desired color */
}
h2{
  color: #fbd60a;
  text-shadow: var(--text-shadow);

}
h1{
  color:#5cffb6;
  text-shadow: var(--text-shadow);
}
.game-rules::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

.game-rules::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.game-rules::-webkit-scrollbar-thumb {
  background: rgba(116, 84, 249);
  border-radius: 10px;
}
</style>