import { createRouter, createWebHistory } from 'vue-router';
import Menu from './components/menu.vue';
import Game from './components/game.vue';

const routes = [
    { path: '/', component: Menu },
    { path: '/game', component: Game },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;