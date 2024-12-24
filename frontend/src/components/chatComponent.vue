<script setup>
import { onMounted } from 'vue';
import { messages, newMessage, fetchMessages, sendMessage } from '../js/chat.js';

onMounted(fetchMessages);
</script>

<template>
  <div class="chat-wrapper">
    <div class="chat-messages">
      <div v-for="message in messages" :key="message.id" class="chat-message">
        <strong class="chat-message-author">{{ message.author }}</strong>
        <span class="chat-message-text">{{ message.text }}</span>
      </div>
    </div>

    <div class="chat-input">
      <input
          type="text"
          style="margin:0; user-select: none; height: 50px; margin-bottom: 2%;"
          class="chat-input-field"
          placeholder="Чат здесь..."
          v-model="newMessage"
          @keyup.enter="sendMessage"
      />
    </div>
  </div>
</template>

<style scoped>
.chat-message-text{
  margin-left: 10px;
  user-select: none;
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