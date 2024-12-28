import express from 'express';
import http from 'http';
import { Server } from 'socket.io';
import cors from 'cors';

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
    cors: {
        origin: 'http://localhost:5173',
        methods: ['GET', 'POST']
    }
});

app.use(cors({
    origin: 'http://localhost:5173'
}));

io.on('connection', (socket) => {
    console.log('a user connected');

    socket.on('draw', (data) => {
        socket.broadcast.emit('draw', data);
    });
    socket.on('startGame', (data) => {
        io.emit('startGame', data);
    });
    socket.on('chatMessage', ({ userName, message }) => {
        io.emit('chatMessage', { userName,  text:message });
    });

    socket.on('answerMessage', ({ userName, answer}) => {
        io.emit('answerMessage', {userName, answer});
    });

    socket.on('undo', (lastState) => {
        socket.broadcast.emit('undo', lastState);
    });

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
    socket.on('startTimer', (answer) => {
        io.emit('correctAnswer', answer);
    });

    socket.on('getOwnerName', (ownerName) => {
        io.emit('getOwnerName', ownerName)
    });

    socket.on('startNextRound', () => {
        io.emit('startNextRound')
    });
});

server.listen(3000, () => {
    console.log('listening on *:3000');
});