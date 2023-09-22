// Function to send a message to the chatbot
function sendMessage() {
    const userInput = document.getElementById('userInput').value;
    if (userInput.trim() === '') return;

    // Send the user message to the backend API
    fetch('/api/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        const chatbox = document.getElementById('chatbox');
        chatbox.innerHTML += `<div class="user-message">${userInput}</div>`;
        chatbox.innerHTML += `<div class="bot-message">${data.response}</div>`;
        document.getElementById('userInput').value = '';
    });
}
