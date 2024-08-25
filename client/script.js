const socket = new WebSocket('ws://localhost:8000');

socket.onopen = () => {
    console.log('WebSocket connection opened');
};

socket.onmessage = (event) => {
    const message = JSON.parse(event.data);
    const messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML += `<p>${message.text}</p>`;
};

socket.onerror = (error) => {
    console.error('WebSocket error:', error);
};

const sendButton = document.getElementById('sendButton');
sendButton.addEventListener('click', () => {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value;
    socket.send(JSON.stringify({ text: message }));
    messageInput.value = '';
});