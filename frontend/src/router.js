import { createRouter, createWebHistory } from 'vue-router';
import Menu from './components/menu.vue';
import Game from './components/game.vue';
import Room from './components/room.vue';
import score from './components/score.vue';

const routes = [
    { path: '/', component: Menu },
    { path: '/game', component: Game },
    { path: '/score', component: score },
    {
    path: '/room/:id',
    component: Room,
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;