import express from 'express';
import http from 'http';
import { Server } from 'socket.io';
import cors from 'cors';
import { createClient } from 'redis';

const app = express();
const server = http.createServer(app);

//функции для редиса
const saveChatMessage = async (room, message) => {
    await redisClient.rPush(`room:${room}:chatMessages`, JSON.stringify(message));
};

const getChatMessages = async (room) => {
    const messages = await redisClient.lRange(`room:${room}:chatMessages`, 0, -1);
    return messages.map(message => JSON.parse(message));
};
const getDrawingData = async (room) => {
    const drawingData = await redisClient.lRange(`room:${room}:drawings`, 0, -1);
    return drawingData.map(data => JSON.parse(data));
}
//соккет
const io = new Server(server, {
    cors: {
        origin: 'http://localhost:5173',
        methods: ['GET', 'POST']
    }
});
const redisClient = createClient({
    url: 'redis://redis :6379'
});
redisClient.connect();

let dialogTimer = null;
let timer = null;

app.use(cors({
    origin: 'http://localhost:5173'
}));

io.on('connection', (socket) => {
    console.log('a user connected');

    socket.on('joinRoom', async (room) => {
        socket.join(room);
        socket.room = room;
        console.log(`User joined room: ${room}`);
        // Retrieve and send chat messages to the user
        const chatMessages = await getChatMessages(room);
        socket.emit('chatHistory', chatMessages);

        const drawingData = await getDrawingData(room)
        socket.emit('allDrawings', drawingData);
    });

    socket.on('draw', async (data) => {
        const room = socket.room;
        if (room) {
            await redisClient.rPush(`room:${room}:drawings`, JSON.stringify(data));
            socket.broadcast.to(room).emit('draw', data);
        }
    });

    socket.on('startGame', (data) => {
        io.to(socket.room).emit('startGame', data);
    });

    socket.on('token', (linkToken, token) => {
        io.to(socket.room).emit('token', linkToken, token);
    });

    socket.on('chatMessage', async ({userName, message}) => {
        const chatMessage = { userName, text: message };
        await saveChatMessage(socket.room, chatMessage);
        io.to(socket.room).emit('chatMessage', chatMessage);
    });

    socket.on('answerMessage', ({ userName, answer, isCorrectPlayer }) => {
        io.to(socket.room).emit('answerMessage', { userName, answer, isCorrectPlayer });
    });

    socket.on('undo', async (lastState) => {
        const room = socket.room;
        if (room) {
            // Remove the last drawing state from Redis
            await redisClient.rPop(`room:${room}:drawings`);
            socket.broadcast.to(room).emit('undo', lastState);
        }
    });

    socket.on('disconnect', () => {
        console.log('user disconnected');
    });

    socket.on('correctAnswer', (answer) => {
        io.to(socket.room).emit('correctAnswer', answer);
    })

    socket.on('getOwnerName', (ownerName) => {
        io.to(socket.room).emit('getOwnerName', ownerName);
    });

    socket.on('startNextRound', () => {
        io.to(socket.room).emit('startNextRound');
    });
    
    socket.on('changePainter', () => {
        io.to(socket.room).emit('changePainter');
    });

    socket.on('updateScore', (userName, increment, isOwner) => {
        io.in(socket.room).emit('updateScore', userName, increment, isOwner);
    });

    socket.on('time', (time) => {
        io.in(socket.room).emit('time', time);
    });

    socket.on('dialogTime', (time) => {
        io.in(socket.room).emit('dialogTime', time);
    });

    socket.on('roomExit', (answer) => {
        io.in(socket.room).emit('roomExit', answer);
    });

    socket.on('endRound', async () => {
        const room = socket.room;
        if (room) {
            await redisClient.del(`room:${room}:drawings`);
            io.to(socket.room).emit('clearCanvasStates');
        }
        io.in(room).emit('endRound');
    });

    socket.on('endGame', async () => {
        const room = socket.room;
        if (room) {
            await redisClient.del(`room:${room}:drawings`);
            await redisClient.del(`room:${room}:chatMessages`);
            await redisClient.del(`room:${room}`);
        }
        io.in(room).emit('endGame');
    });

    socket.on('startGame', () => {
        if (timer) {
            clearInterval(timer);
        }
        let timerValue = 0;
        timer = setInterval(() => {
            timerValue++;
            io.to(socket.room).emit('time', timerValue);
            if (timerValue > 60) {
                clearInterval(timer);
                timer = null;
                return;
            }
        }, 1000);
    });

    socket.on('startTimer', () => {
        if (dialogTimer) {
            clearInterval(dialogTimer);
        }
        let dialogTimerValue = 0;
        dialogTimer = setInterval(() => {
            dialogTimerValue++;
            io.to(socket.room).emit('dialogTime', dialogTimerValue);
            if (dialogTimerValue > 10) {
                clearInterval(dialogTimer);
                dialogTimer = null;
                return;
            }
        }, 1000);
    });

    socket.on('resetTimer', () => {
        if (timer) {
            clearInterval(timer);
            timer = null;
        }
        if (dialogTimer) {
            clearInterval(dialogTimer);
            dialogTimer = null;
        }
        io.to(socket.room).emit('time', 0); 
        io.to(socket.room).emit('dialogTime', 0);
    });
});

server.listen(3000, () => {
    console.log('listening on *:3000');
});