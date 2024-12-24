<script>
import axios from "axios";

export default {
  data() {
    return {
      users: [],
    };
  },
  created() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get('/api/users/');
        this.users = response.data; 
        console.log(this.users);
      } catch (error) {
        console.error("Error fetching users:", error); 
      }
    },
  },
};
</script>
<template>
  <div class="scoreboard background">
    <div class="wrapper">
      <table>
        <thead>
        <tr>
          <th class="header-text">Место</th>
          <th class="header-text">Имя игрока</th>
          <th class="header-text">Рекорд</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(player, index) in users" :key="index">
          <td class="score-text">{{ index + 1 }}</td>
          <td class="score-text">{{ player.username }}</td>
          <td class="score-text">{{
              player.winGames.toLocaleString('en-US', {minimumIntegerDigits: 5, useGrouping: false})
            }}
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.scoreboard {
  background: url("../assets/textura.png") no-repeat center center / cover, linear-gradient(215deg, rgba(116, 84, 249) 0%, rgb(115, 17, 176) 85%);
  height: 100vh;
  width: 100vw;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.wrapper {
  border: 4px rgba(29, 29, 27, .15) solid;
  -webkit-box-shadow: inset 0px 2px 0px 0px rgba(255, 255, 255, .15), 0px 3px 0px 0px rgba(255, 255, 255, .15);
  -moz-box-shadow: inset 0px 2px 0px 0px rgba(255, 255, 255, .15), 0px 3px 0px 0px rgba(255, 255, 255, .15);
  box-shadow: inset 0px 2px 0px 0px rgba(255, 255, 255, .15), 0px 3px 0px 0px rgba(255, 255, 255, .15);
  -webkit-border-radius: 12px;
  background-color: rgba(255, 255, 255, 0);
  width: 70%;
  height: 80%;
  display: flex;
  border-radius: 15px;
  align-items: center;
  justify-content: center;

}

table {
  border-radius: 10px;
  width: 95%;
  height: 90%;
  border-spacing: 15px 0px;
  border-collapse: separate;
  margin: 10px;

}

th, td {
  padding: 10px;
  text-align: center;
}

th {
  background-color: rgba(38, 28, 92, .5);
  border: none;
}


.header-text {
  margin: 10px;
  font-weight: bold;
  font-size: 22px;
  color: #5cffb6;
  text-shadow: rgb(23, 5, 87) 3px 0px 0px, rgb(23, 5, 87) 2.83487px .981584px 0px, rgb(23, 5, 87) 2.35766px 1.85511px 0px, rgb(23, 5, 87) 1.62091px 2.52441px 0px, rgb(23, 5, 87) .705713px 2.91581px 0px, rgb(23, 5, 87) -.287171px 2.98622px 0px, rgb(23, 5, 87) -1.24844px 2.72789px 0px, rgb(23, 5, 87) -2.07227px 2.16926px 0px, rgb(23, 5, 87) -2.66798px 1.37182px 0px, rgb(23, 5, 87) -2.96998px .42336px 0px, rgb(23, 5, 87) -2.94502px -.571704px 0px, rgb(23, 5, 87) -2.59586px -1.50383px 0px, rgb(23, 5, 87) -1.96093px -2.27041px 0px, rgb(23, 5, 87) -1.11013px -2.78704px 0px, rgb(23, 5, 87) -.137119px -2.99686px 0px, rgb(23, 5, 87) .850987px -2.87677px 0px, rgb(23, 5, 87) 1.74541px -2.43999px 0px, rgb(23, 5, 87) 2.44769px -1.73459px 0px, rgb(23, 5, 87) 2.88051px -.838247px 0px;
  text-transform: uppercase;
  text-align: center;
}

.score-text {
  background-color: white;
  font-weight: bold;
  font-size: 18px;
  color: #301a6b;
  text-align: center;
  text-transform: uppercase;
}
</style>

