const express = require('express');
const http = require('http');
const { Server } = require('socket.io');
const path = require('path');
const { spawn } = require('child_process');

// Initialize App and Server
const app = express();
const server = http.createServer(app);
const io = new Server(server);

// Set the views directory and view engine (EJS)
app.set('views', path.join(__dirname, 'views')); 
app.set('view engine', 'ejs');

// Serve static files (like CSS, JS)
app.use(express.static(path.join(__dirname, 'public')));

// Serve the Chat UI
app.get('/', (req, res) => {
  res.render('index');  // Render index.ejs
});

// Socket.IO - Handle messages from the front end
io.on('connection', (socket) => {
  console.log('A user connected.');

  socket.on('userMessage', (message) => {
    // Spawn a Python process to handle the database query
    const pythonProcess = spawn('python3', ['backend/find_remedy.py', message]);

    pythonProcess.stdout.on('data', (data) => {
      const result = data.toString();
      socket.emit('botMessage', result);  // Send the response back to the user
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`Error: ${data}`);
      socket.emit('botMessage', 'Sorry, something went wrong. Please try again.');
    });
  });

  socket.on('disconnect', () => {
    console.log('A user disconnected.');
  });
});

// starting server ~~
server.listen(3000, () => {
  console.log('Symptom Sage is running at http://localhost:3000');
});
