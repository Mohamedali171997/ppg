// static/js/assistant.js

document.addEventListener('DOMContentLoaded', function() {
    const chatToggleButton = document.getElementById('chat-toggle-button');
    const chatContainer = document.getElementById('chat-container');
    const closeChatButton = document.getElementById('close-chat-button');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const chatBox = document.getElementById('chat-box');

    // Toggle chat window visibility
    chatToggleButton.addEventListener('click', function() {
        chatContainer.classList.toggle('hidden');
        chatContainer.classList.toggle('visible');
        if (chatContainer.classList.contains('visible')) {
            userInput.focus(); // Focus on input when chat opens
        }
    });

    closeChatButton.addEventListener('click', function() {
        chatContainer.classList.add('hidden');
        chatContainer.classList.remove('visible');
    });

    function appendMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', sender);
        // Use innerHTML for markdown formatting if Gemini returns it, or textContent for plain text
        messageElement.innerHTML = message.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>'); // Basic markdown for bold
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight; // Auto-scroll to bottom
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage('user', message);
        userInput.value = ''; // Clear input

        // Show a loading indicator
        const loadingMessageElement = document.createElement('div');
        loadingMessageElement.classList.add('message', 'assistant', 'loading');
        loadingMessageElement.innerHTML = '<span class="loading-dots">.</span><span class="loading-dots">.</span><span class="loading-dots">.</span>';
        chatBox.appendChild(loadingMessageElement);
        chatBox.scrollTop = chatBox.scrollHeight;

        try {
            const response = await fetch('/gemini-assistant/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken // Use csrftoken from base.html script
                },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Network response was not ok');
            }

            const data = await response.json();

            // Remove loading indicator and append actual response
            chatBox.removeChild(loadingMessageElement);
            appendMessage('assistant', data.response);

        } catch (error) {
            console.error('Error sending message to Gemini:', error);
            if (chatBox.contains(loadingMessageElement)) {
                chatBox.removeChild(loadingMessageElement);
            }
            appendMessage('assistant', 'Sorry, I\'m having trouble connecting right now. Please try again later.');
        }
    }

    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});