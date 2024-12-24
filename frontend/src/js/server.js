import express from 'express';
import http from 'http';
import { Server } from 'socket.io';
import cors from 'cors';

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
    cors: {
        origin: 'http://localhost:5173', // Replace with your frontend URL
        methods: ['GET', 'POST']
    }
});

app.use(cors({
    origin: 'http://localhost:5173' // Replace with your frontend URL
}));

io.on('connection', (socket) => {
    console.log('a user connected');

    socket.on('draw', (data) => {
        socket.broadcast.emit('draw', data);
    });

    socket.on('chatMessage', (message) => {
        io.emit('chatMessage', message); // Broadcast the message to all clients
    });

    socket.on('answerMessage', (message) => {
        io.emit('answerMessage', message); // Broadcast the answer to all clients
    });

    socket.on('undo', (lastState) => {
        socket.broadcast.emit('undo', lastState);
    });

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
});

server.listen(3000, () => {
    console.log('listening on *:3000');
});