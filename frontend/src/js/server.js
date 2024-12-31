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

    socket.on('joinRoom', (room) => {
        socket.join(room);
        socket.room = room; // Store room in socket object
        console.log(`User joined room: ${room}`);
    });

    socket.on('draw', (data) => {
        socket.broadcast.to(socket.room).emit('draw', data);
    });

    socket.on('startGame', (data) => {
        io.to(socket.room).emit('startGame', data);
    });

    socket.on('chatMessage', ({ userName, message }) => {
        io.to(socket.room).emit('chatMessage', { userName, text: message });
    });

    socket.on('answerMessage', ({ userName, answer }) => {
        io.to(socket.room).emit('answerMessage', { userName, answer });
    });

    socket.on('undo', (lastState) => {
        socket.broadcast.to(socket.room).emit('undo', lastState);
    });

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
    socket.on('correctAnswer', (answer) => {
        io.to(socket.room).emit('correctAnswer', answer);
    })
    // socket.on('startTimer', (answer) => {
    //     io.to(socket.room).emit('correctAnswer', answer);
    // });

    socket.on('getOwnerName', (ownerName) => {
        io.to(socket.room).emit('getOwnerName', ownerName);
    });

    socket.on('startNextRound', () => {
        io.to(socket.room).emit('startNextRound');
    });

    socket.on('updateScore', (userName, increment) => {
        io.in(socket.room).emit('updateScore', userName, increment);
    });
});

server.listen(3000, () => {
    console.log('listening on *:3000');
});