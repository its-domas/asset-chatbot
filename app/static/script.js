
const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function appendMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    if (sender === 'user') {
        messageElement.classList.add('user-message');
    } else {
        messageElement.classList.add('bot-message');
    }
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
    const message = userInput.value.trim();
    if (message === '') {
        return;
    }
    appendMessage(`You: ${message}`, 'user');
    userInput.value = '';

    fetch('/chat', { // Changed to relative URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.response) { // Changed from 'answer' to 'response'
            appendMessage(`Bot: ${data.response}`, 'bot');
        } else if (data.error) {
            appendMessage(`Error: ${data.error}`, 'bot');
        } else {
            appendMessage('Error: Unexpected response from server.', 'bot');
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        appendMessage('Error: Could not connect to the server.', 'bot');
    });
}


