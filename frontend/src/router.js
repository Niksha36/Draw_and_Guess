import { createRouter, createWebHistory } from 'vue-router';
import Menu from './components/menu.vue';
import Game from './components/game.vue';
import Room from './components/room.vue';
import score from './components/score.vue';
import listOfRooms from "@/components/listOfRooms.vue";

const routes = [
    { path: '/', component: Menu },
    { path:'/listOfRooms', component: listOfRooms },
    { path: '/room/:id/game', component: Game },
    { path: '/score', component: score },
    {
      path: '/room/:roomId',
      component: Room,
      props: true,
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;