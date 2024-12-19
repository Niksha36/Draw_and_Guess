<script setup>

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

      <div class="paint-board">

      </div>

      <div class="tools-panel">

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
  background-size: contain;
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

.paint-board {
  content: url("../assets/bg_content.svg");
  height: 100%;
  width: 65%;
  margin-left: 20px;
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
}

</style>