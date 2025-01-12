<script setup>
import {useRouter} from 'vue-router';
import {ref} from "vue";
const router = useRouter();
const selectedRoom = ref(null);
const rooms = ref([
  { id: 1, name: 'Комната 1', users: 2 },
  { id: 2, name: 'Комната 2', users: 3 },
  { id: 3, name: 'Комната 3', users: 4 },
  { id: 4, name: 'Комната 4', users: 5 },
  { id: 5, name: 'Комната 5', users: 6 },
  { id: 6, name: 'Комната 5', users: 7 },
  { id: 7, name: 'Комната 5', users: 8 },
  { id: 8, name: 'Комната 5', users: 9 },
  { id: 9, name: 'Комната 5', users: 10 },
]);
function onPlayButton(){

}
function goToMenu() {
  router.push('/');
}
function choseRoom(roomId) {
  selectedRoom.value = roomId;
}
</script>

<template>
  <div class="background">
    <div class="list-of-rooms" style="position:relative" >
      <div class="go-to-menu-icon-wrapper" @click="goToMenu" style="cursor: pointer">
        <div class="go-to-menu-icon">
          <img src="../assets/small_button_border.svg" alt="border" class="home-border" >
          <img src="../assets/ic_home.svg" alt="home-icon" width="33px" class="home-icon">
        </div>
      </div>
      <h1>Комнаты</h1>
      <div class="rooms">
        <div v-for="room in rooms" :key="room.id"
             :class="['room-template', { 'selected': selectedRoom === room.id }]"
             @click="choseRoom(room.id)">
          <img src="../assets/room-avatar.svg" alt="room-avatar" class="room-avatar">
          <strong class="room-name" style="font-size:90%">{{ room.name }}</strong>
          <div class="room-players" style="display:flex; justify-content:center; align-items:center">
            <img src="../assets/count_of_users.png" alt="player-count-img" style="width:35%" >
            <span class="text-number-of-users" style="margin-left:5%">{{ room.users }}/14</span>
          </div>
        </div>
      </div>
      <button class="play-button" @click="onPlayButton">
        <img src="" alt="" class="play-button-img">
        <span>играть</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.go-to-menu-icon-wrapper {
  position: absolute;
  top: 10px; /* Adjust as needed */
  left: 10px; /* Adjust as needed */
}

.go-to-menu-icon {
  position: relative;
  width: 33px; /* Adjust as needed */
  height: 33px; /* Adjust as needed */
}

.home-border {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.home-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
h1{
  text-align:center;
  text-shadow: var(--text-shadow);
  text-transform: uppercase;
  color: #5cffb6;
}
.rooms{
  overflow-y: scroll;
  background-color: rgba(38, 28, 92, .5);
  display:flex;
  border-radius: 10px;
  height:75%;
  padding:10px;
  gap:1.5%;
  flex-wrap: wrap;
}
.room-avatar{
  width: 30%; border-radius: 50%; box-shadow: 0 0 0 4px white, 0 0 0 6px black;
}
.play-button{
  /*
  position:absolute;
  right:50%;
  transform:translateX(50%);
   */
  margin-top: 1%;
  padding: 10px 20%;
  background: hotpink;
  box-shadow: 0px 6px 0px 0px #301a6b;
  border:none;
  color:rgba(38, 28, 92);
  text-transform: uppercase;
  font-weight:bold;
}
.play-button:hover{
  background: #5cffb6;
}
.room-template{
  display:flex;
  flex-direction: column;
  justify-content:center;
  align-items:center;
  background: white;
  width:23.85%;
  height: calc(50% - 5px);
  border-radius:15px;
}
.room-template:hover{
  border: 5px solid #5cffb6;
}
.background {
  background: url("../assets/textura.png") no-repeat center center / cover, linear-gradient(215deg, rgba(116, 84, 249) 0%, rgb(115, 17, 176) 85%);
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: space-around;
  padding: 20px;
  z-index: 2;
}
/*
.go-to-menu-icon-wrapper {
  position: absolute;
  top: 4.5%;
  left: 2.8%;
  cursor:pointer;
}

 */


.list-of-rooms {
  display: flex;
  flex-direction: column;
  align-items: center;
  border: 4px rgba(29, 29, 27, .15) solid;
  -webkit-box-shadow: inset 0px 2px 0px 0px rgba(255, 255, 255, .15), 0px 3px 0px 0px rgba(255, 255, 255, .15);
  -moz-box-shadow: inset 0px 2px 0px 0px rgba(255, 255, 255, .15), 0px 3px 0px 0px rgba(255, 255, 255, .15);
  box-shadow: inset 0px 2px 0px 0px rgba(255, 255, 255, .15), 0px 3px 0px 0px rgba(255, 255, 255, .15);
  -webkit-border-radius: 12px;
  background-color: rgba(255, 255, 255, 0);
  width: 70%;
  height: 90%;
  border-radius: 15px;
  padding:20px;
  /*
  display: flex;
  justify-content: center;

  flex-direction: column;
   */
}
.room-template.selected {
  border: 5px solid deeppink;
}

.rooms::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

.rooms::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.rooms::-webkit-scrollbar-thumb {
  background: #ff53a4;
  border-radius: 10px;
}

.rooms::-webkit-scrollbar-thumb:hover {
  background: rgb(38, 28, 92);
}
.text-number-of-users{
  font-size: 90%
}
@media (max-height:441px) {
  .room-avatar{
    width: 20%; border-radius: 50%; box-shadow: 0 0 0 2px white, 0 0 0 4px black;
  }

  .room-players img{
    width: 30%!important;
  }
  .room-name{
    font-size:70%!important;
  }
  .text-number-of-users{
    font-size: 70%!important;
  }
}


@media (max-height:600px) {
  .play-button {
    padding: 5px 20%;
  }
  h1{
    font-size: 25px;
    margin-bottom: 10px;
  }
  .list-of-rooms{
    padding:10px 5px
  }
}
</style>