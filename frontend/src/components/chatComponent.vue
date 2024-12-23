<script setup>

</script>

<template>
  <div class="chat-wrapper">
    <div class="chat-messages">
      <div class="chat-message">
        <strong class="chat-message-author">Nikita</strong>
        <span class="chat-message-text">Hello, guys!</span>
      </div>
      <div class="chat-message">
        <strong>Eduard</strong>
        <span class="chat-message-text">Hello, Nikita!</span>
      </div>
      <!--        <div class="chat-message">-->
      <!--          <div class="chat-message-author">Vasya</div>-->
      <!--          <div class="chat-message-text">Hello, guys!</div>-->
      <!--        </div>-->
      <!--        <div class="chat-message">-->
      <!--          <div class="chat-message-author">Vnya</div>-->
      <!--          <div class="chat-message-text">Hello, guys!</div>-->
      <!--        </div>-->
      <!--        <div class="chat-message">-->
      <!--          <div class="chat-message-author">Vnya</div>-->
      <!--          <div class="chat-message-text">Hello, guys!</div>-->
      <!--        </div>-->
      <!--        <div class="chat-message">-->
      <!--          <div class="chat-message-author">Vnya</div>-->
      <!--          <div class="chat-message-text">Hello, guys!</div>-->
      <!--        </div>-->
      <!--        <div class="chat-message">-->
      <!--          <div class="chat-message-author">Vnya</div>-->
      <!--          <div class="chat-message-text">Hello, guys!</div>-->
      <!--        </div>-->
      <!--        <div class="chat-message">-->
      <!--          <div class="chat-message-author">Vnya</div>-->
      <!--          <div class="chat-message-text">Hello, guys!</div>-->
      <!--        </div>-->
      <!--        <div class="chat-message">-->
      <!--          <div class="chat-message-author">Vnya</div>-->
      <!--          <div class="chat-message-text">Hello, guys!</div>-->
      <!--        </div>-->
      <!--        <div class="chat-message">-->
      <!--          <div class="chat-message-author">Vnya</div>-->
      <!--          <div class="chat-message-text">Hello, guys!</div>-->
      <!--        </div>-->
      <!--        <div class="chat-message">-->
      <!--          <div class="chat-message-author">Vnya</div>-->
      <!--          <div class="chat-message-text">Hello, guys!</div>-->
      <!--        </div>-->

    </div>

    <div class="chat-input">
      <input type="text" style="margin:0; height: 50px; margin-bottom: 2%; " class="chat-input-field" placeholder="Чат здесь..."/>
    </div>
  </div>
</template>

<style scoped>
.chat-message-text{
  margin-left: 10px
}
.chat-wrapper{
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
  height: 100%;
  flex:1;
}
.chat-message{
  font-size: 18px;
  margin: 3px 0 3px 5px;
}
</style>