<script>
import axios from "axios";
import {useRouter} from 'vue-router';
import {playClickSound, playHoverSound} from "@/js/soundEffects.js";

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
      playClickSound,
      playHoverSound,
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
        <div class="bg">
        </div>
        <div class="scoreboard">
            <div class="go-to-menu-icon" @click="goToMenu" @mouseenter="playHoverSound" @mousedown="playClickSound" style="cursor: pointer; ">
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
                                player.winGames.toLocaleString('en-US', {
                                    minimumIntegerDigits: 5,
                                    useGrouping: false
                                })
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

.bg {
    position: absolute;
    background: url("../assets/textura.png");
    background-size: cover;
    height: 100vh;
    width: 100vw;
}

.background {
    height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: start;
    background: linear-gradient(215deg, rgb(246, 103, 0), rgb(139, 110, 255), rgb(84, 0, 133));
    background-size: 400% 400%;
    animation: gradient-animation 30s ease-in-out infinite;
    transform: translateZ(0);
    will-change: background-position;
}

@keyframes gradient-animation {
    0% {
        background-position: 0% 50%;
    }
    25% {
        background-position: 50% 50%;
    }
    50% {
        background-position: 100% 50%;
    }
    75% {
        background-position: 50% 0%;
    }
    100% {
        background-position: 0% 50%;
    }
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
    z-index: 2;
}

.wrapper {
    border: 4px rgba(29, 29, 27, .15) solid;
    -webkit-box-shadow: inset 0px 2px 0px 0px rgba(255, 255, 255, .15), 0px 3px 0px 0px rgba(255, 255, 255, .15);
    -moz-box-shadow: inset 0px 2px 0px 0px rgba(255, 255, 255, .15), 0px 3px 0px 0px rgba(255, 255, 255, .15);
    box-shadow: inset 0px 2px 0px 0px rgba(255, 255, 255, .15), 0px 3px 0px 0px rgba(255, 255, 255, .15);
    -webkit-border-radius: 12px;
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
    background-color: rgba(74, 62, 145, 0.5);
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

