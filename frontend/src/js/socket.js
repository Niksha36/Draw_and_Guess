import { io } from "socket.io-client";

// Укажите URL вашего сервера сокетов
const socket = io("http://localhost:3000", {
    transports: ['websocket'], // Используйте веб-сокеты
    cors: {
        origin: "http://localhost:5173", // Замените на ваш URL фронтенда
        methods: ["GET", "POST"]
    }
});


function startGame(roomId) {
    socket.emit('startGame', { roomId });
}

export { socket, startGame };