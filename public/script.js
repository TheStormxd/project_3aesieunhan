async function sendMessage() {
  const userInput = document.querySelector('.chat-input textarea');
  const userMessage = userInput.value.trim();
  if (!userMessage) return;

  appendMessage(userMessage, 'user');
  userInput.value = '';

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: userMessage })
    });

    const data = await response.json();
    if (data.response) {
      appendMessage(data.response, 'bot');
    } else {
      appendMessage('Error: No response from AI', 'bot');
    }
  } catch (error) {
    console.error('Error:', error);
    appendMessage('Error: Failed to communicate with the backend', 'bot');
  }
}

function appendMessage(message, sender) {
  const chatMessages = document.querySelector('.chat-messages');
  const messageElement = document.createElement('div');
  messageElement.className = `message ${sender}`;

  // Convert hyphens to line breaks
  const formattedMessage = message.replace(/- /g, "<br>");

  messageElement.innerHTML = `
    <div class="${sender}">${sender === 'user' ? 'You' : 'Niko'}:</div>
    <div class="message">${formattedMessage}</div>
  `;

  chatMessages.appendChild(messageElement);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}
