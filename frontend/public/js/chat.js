const socket = io();  // Initialize socket connection

const messageInput = document.getElementById('message');
const sendButton = document.getElementById('send');
const output = document.getElementById('output');

// Send user input (symptom) to the backend
sendButton.addEventListener('click', () => {
  const message = messageInput.value;  // Get input from the user
  if (message.trim()) {  // Only send if the message is not empty
    output.innerHTML += `<p><strong>You:</strong> ${message}</p>`;  // Show message in chat window
    socket.emit('userMessage', message);  // Send the message to the backend (via socket)
    messageInput.value = '';  // Clear the input field
  }
});

// Listen for the response from the backend and display it
socket.on('botMessage', (data) => {
  output.innerHTML += `<p><strong>Bot:</strong> ${data}</p>`;  // Show bot's response
  output.scrollTop = output.scrollHeight;  // Scroll to the bottom
});
