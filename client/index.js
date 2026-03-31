document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const sendBtn = document.getElementById('send-btn');

    // Server API endpoint - default Flask port
    const BACKEND_URL = 'http://127.0.0.1:5000/chat';

    // Auto-focus input field on load
    userInput.focus();

    // Prevent submitting empty value just hitting enter
    userInput.addEventListener('input', () => {
        sendBtn.disabled = userInput.value.trim().length === 0;
    });

    // Make sure button is initially synced to input empty state
    sendBtn.disabled = true;

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to UI
        addMessage(message, 'user');
        
        // Clear input and disable button
        userInput.value = '';
        sendBtn.disabled = true;

        // Add typing indicator immediately
        const typingIndicator = addTypingIndicator();

        try {
            // Send request to Flask Backend
            const response = await fetch(BACKEND_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });

            const data = await response.json();

            // Setup smooth removal of typing indicator
            typingIndicator.style.opacity = '0';
            setTimeout(() => {
                typingIndicator.remove();
                
                if (response.ok && data.reply) {
                    addMessage(data.reply, 'bot');
                } else {
                    const errorMsg = data.error || 'The server responded with an error.';
                    addMessage(errorMsg, 'bot', true);
                }
            }, 300); // Wait for fade out animation

        } catch (error) {
            console.error('Error connecting to Server:', error);
            
            typingIndicator.style.opacity = '0';
            setTimeout(() => {
                typingIndicator.remove();
                addMessage('Network error. Unable to reach the server. Is the Python backend running?', 'bot', true);
            }, 300);

        } finally {
            // Re-focus and enable input typing logic
            userInput.focus();
        }
    });

    function addMessage(text, sender, isError = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = text;
        
        if (isError) {
            contentDiv.style.color = '#ef4444'; // Red-ish error text
            contentDiv.style.borderColor = 'rgba(239, 68, 68, 0.4)';
            contentDiv.style.background = 'rgba(127, 29, 29, 0.2)'; 
        }

        messageDiv.appendChild(contentDiv);
        chatBox.appendChild(messageDiv);
        
        // Scroll to the newest message smoothly
        scrollToBottom();
    }

    function addTypingIndicator() {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.id = 'typing-indicator';
        messageDiv.style.transition = 'opacity 0.3s ease';
        
        const wrapperDiv = document.createElement('div');
        wrapperDiv.className = 'typing-wrapper';
        wrapperDiv.innerHTML = `
            <div class="dot"></div>
            <div class="dot"></div>
            <div class="dot"></div>
        `;

        messageDiv.appendChild(wrapperDiv);
        chatBox.appendChild(messageDiv);
        
        scrollToBottom();
        
        return messageDiv;
    }

    function scrollToBottom() {
        // Adding a slight delay to ensure DOM is updated before scrolling
        requestAnimationFrame(() => {
            chatBox.scrollTo({
                top: chatBox.scrollHeight,
                behavior: 'smooth'
            });
        });
    }
});
