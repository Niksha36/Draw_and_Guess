import { io } from "socket.io-client";


const socket = io("http://localhost:3000", {
    transports: ['websocket'],
    cors: {
        origin: "http://localhost:5173", 
        methods: ["GET", "POST"]
    }
});


function startGame(roomId) {
    socket.emit('startGame', { roomId });
}

export { socket, startGame };