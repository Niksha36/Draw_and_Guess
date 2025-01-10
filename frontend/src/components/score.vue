<script>
import axios from "axios";
import {useRouter} from 'vue-router';

export default {
    setup() {
        const router = useRouter();
        return {router};
    },
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
                this.users.sort((a, b) => b.winGames - a.winGames).forEach((user, index));
            } catch (error) {
                console.error("Error fetching users:", error);
            }
        },
        goToMenu() {
            this.router.push('/');
        },
    },
};
</script>
<template>
    <div class="background">
        <div class="scoreboard">
            <div class="go-to-menu-icon" @click="goToMenu" style="cursor: pointer; ">
                <img src="../assets/ic_home.svg" alt="home-icon" width="33px" class="home-icon">
            </div>
            <div class="wrapper" style="position: relative">
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
    </div>
</template>

<style scoped>
.go-to-menu-icon {
    border-radius: 10%;
    border: 3px RGB(23, 21, 86) solid;
    align-self: flex-start;
    margin: 5px;
}

.background {
    background: url("../assets/textura.png") no-repeat center center / cover, linear-gradient(215deg, rgba(116, 84, 249) 0%, rgb(115, 17, 176) 85%);
    height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: start;
}

.scoreboard {
    margin: 20px;
    height: 80%;
    width: 80%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    padding: 20px;
    animation: gradient-animation 10s ease-in-out infinite;
    transform: translateZ(0);
    will-change: background-image;
}

@keyframes gradient-animation {
    0% {
        background-image: url("../assets/textura.png"),
        linear-gradient(215deg, rgb(116, 84, 249), rgb(115, 17, 176));
    }
    12.5% {
        background-image: url("../assets/textura.png"),
        linear-gradient(230deg, rgb(130, 70, 220), rgb(100, 25, 190));
    }
    25% {
        background-image: url("../assets/textura.png"),
        linear-gradient(245deg, rgb(150, 60, 190), rgb(85, 35, 205));
    }
    37.5% {
        background-image: url("../assets/textura.png"),
        linear-gradient(260deg, rgb(170, 50, 160), rgb(70, 45, 220));
    }
    50% {
        background-image: url("../assets/textura.png"),
        linear-gradient(305deg, rgb(200, 50, 100), rgb(50, 100, 200));
    }
    62.5% {
        background-image: url("../assets/textura.png"),
        linear-gradient(280deg, rgb(185, 60, 130), rgb(60, 120, 210));

    }
    75% {
        background-image: url("../assets/textura.png"),
        linear-gradient(265deg, rgb(160, 70, 160), rgb(75, 140, 195));
    }
    87.5% {
        background-image: url("../assets/textura.png"),
        linear-gradient(250deg, rgb(140, 80, 190), rgb(90, 155, 180));
    }
    100% {
        background-image: url("../assets/textura.png"),
        linear-gradient(215deg, rgb(116, 84, 249), rgb(115, 17, 176));
    }
}


.wrapper {
    border: 4px rgba(29, 29, 27, .15) solid;
    -webkit-box-shadow: inset 0px 2px 0px 0px rgba(255, 255, 255, .15), 0px 3px 0px 0px rgba(255, 255, 255, .15);
    -moz-box-shadow: inset 0px 2px 0px 0px rgba(255, 255, 255, .15), 0px 3px 0px 0px rgba(255, 255, 255, .15);
    box-shadow: inset 0px 2px 0px 0px rgba(255, 255, 255, .15), 0px 3px 0px 0px rgba(255, 255, 255, .15);
    -webkit-border-radius: 12px;
    background-color: rgba(255, 255, 255, 0);
    width: 100%;
    height: 95%;
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
    vertical-align: top;
    padding-top: 10px;
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

