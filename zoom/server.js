require('dotenv').config();
const jwt = require('jsonwebtoken');
const Redis = require('ioredis');

const redis = new Redis({
  host: process.env.REDIS_HOST,
  port: process.env.REDIS_PORT,
  db: process.env.REDIS_DB,
  password: process.env.REDIS_PASSWORD || undefined
});

const express = require("express");
const app = express();
const server = require("http").Server(app);
const { v4: uuidv4 } = require("uuid");
app.set("view engine", "ejs");
const io = require("socket.io")(server, {
  cors: {
    origin: '*'
  }
});
const { ExpressPeerServer } = require("peer");
const opinions = {
  debug: true,
}

app.use("/peerjs", ExpressPeerServer(server, opinions));
app.use(express.static("public"));

app.get("/", (req, res) => {
  res.redirect(`/${uuidv4()}`);
});

app.get("/:room", async (req, res) => {
  const { token } = req.query;
  const { room } = req.params;

  if (!token) {
    return res.status(403).send("No token");
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    const data = await redis.get(`room:${room}`);
    if (!data) return res.status(403).send("Room not found");
    const parsed = JSON.parse(data);
    console.log(parsed)

    if (parsed.token !== token) {
      return res.status(403).send("Invalid token");

    }

    res.render("room", { roomId: room, token });

  } catch (err) {
    // console.error(err);
    return res.status(403).render("error", {
      message: "Звонок уже окончен"
    });
  }
});

app.get("/check/:room", async (req, res) => {
  const { token } = req.query;
  const { room } = req.params;

  if (!token) {
    return res.status(403).json({ error: "NO_TOKEN" });
  }

  try {
    jwt.verify(token, process.env.JWT_SECRET);
    const data = await redis.get(`room:${room}`);

    if (!data) {
      return res.status(404).json({ error: "ROOM_NOT_FOUND" });
    }

    const parsed = JSON.parse(data);
    if (parsed.token !== token) {
      return res.status(403).json({ error: "INVALID_TOKEN" });
    }
    const roomData = io.sockets.adapter.rooms[room];
    const clientsCount = roomData ? roomData.length : 0;

    if (clientsCount >= 2) {
      return res.status(403).json({ error: "ROOM_FULL" });
    }
    return res.status(200).json({ status: "OK" });

  } catch (err) {
    if (err.name === "TokenExpiredError") {
      return res.status(403).json({ error: "TOKEN_EXPIRED" });
    }

    return res.status(403).json({ error: "INVALID_TOKEN" });
  }
});

io.on("connection", (socket) => {
  socket.on("join-room", (roomId, userId, userName) => {
    const room = io.sockets.adapter.rooms[roomId];
    const clientsCount = room ? room.length : 0;

    if (clientsCount >= 2) {
      socket.emit("room-full");
      return;
    }

    socket.join(roomId);

    setTimeout(() => {
      socket.to(roomId).broadcast.emit("user-connected", userId);
    }, 1000);

    socket.on("message", (message) => {
      io.to(roomId).emit("createMessage", message, userName);
    });
  });
});
server.listen(3030, '0.0.0.0', () => {
  console.log('Сервер запущен на порту 3030 на всех интерфейсах');
});

