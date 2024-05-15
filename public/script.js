async function sendMessage() {
  const userInput = document.getElementById('user-input');
  const userMessage = userInput.value.trim();
  if (!userMessage) return;

  appendMessage(userMessage, 'user-message');
  userInput.value = '';

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: userMessage })
    });

    const data = await response.json();
    if (data.response) {
      appendMessage(data.response, 'bot-message');
    } else {
      appendMessage('Error: No response from AI', 'bot-message');
    }
  } catch (error) {
    console.error('Error:', error);
    appendMessage('Error: Failed to communicate with the backend', 'bot-message');
  }
}

function appendMessage(message, className) {
  const chatBox = document.getElementById('chat-box');
  const messageElement = document.createElement('div');
  messageElement.className = `message ${className}`;
  messageElement.textContent = message;
  chatBox.appendChild(messageElement);
  chatBox.scrollTop = chatBox.scrollHeight;
}
