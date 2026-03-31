// Advanced Chatbot Frontend with Session Management and Intent Recognition
document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatBox = document.getElementById('chat-box');
    const sendBtn = document.getElementById('send-btn');

    // Configuration
    const BACKEND_URL = 'http://127.0.0.1:5000';
    const SESSION_ID = generateSessionId();
    const API = {
        chat: `${BACKEND_URL}/chat`,
        history: `${BACKEND_URL}/session/${SESSION_ID}/history`,
        summary: `${BACKEND_URL}/session/${SESSION_ID}/summary`,
        reset: `${BACKEND_URL}/session/${SESSION_ID}/reset`,
        intents: `${BACKEND_URL}/intents`,
        health: `${BACKEND_URL}/health`,
        kbSearch: `${BACKEND_URL}/knowledge-base/search`
    };

    let messageCount = 0;
    let isProcessing = false;

    // Initialize
    userInput.focus();
    checkServerHealth();

    // Event Listeners
    userInput.addEventListener('input', () => {
        sendBtn.disabled = userInput.value.trim().length === 0;
    });

    sendBtn.disabled = true;

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = userInput.value.trim();
        if (!message || isProcessing) return;

        isProcessing = true;
        addMessage(message, 'user');
        
        userInput.value = '';
        sendBtn.disabled = true;

        const typingIndicator = addTypingIndicator();

        try {
            const response = await fetch(API.chat, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    message,
                    session_id: SESSION_ID
                })
            });

            const data = await response.json();

            typingIndicator.style.opacity = '0';
            setTimeout(() => {
                typingIndicator.remove();
                
                if (response.ok && data.reply) {
                    addMessage(data.reply, 'bot', {
                        intent: data.intent,
                        confidence: data.confidence,
                        entities: data.entities
                    });
                } else {
                    const errorMsg = data.error || 'An error occurred';
                    addMessage(errorMsg, 'bot', { isError: true });
                }
                isProcessing = false;
                userInput.focus();
            }, 300);

        } catch (error) {
            console.error('Connection error:', error);
            
            typingIndicator.style.opacity = '0';
            setTimeout(() => {
                typingIndicator.remove();
                addMessage('Server connection failed. Make sure the backend is running.', 'bot', { isError: true });
                isProcessing = false;
                userInput.focus();
            }, 300);
        }
    });

    function addMessage(text, sender, metadata = {}) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.style.animation = 'fadeIn 0.3s ease-in';
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = text;
        
        if (metadata.isError) {
            contentDiv.style.color = '#ef4444';
            contentDiv.style.borderColor = 'rgba(239, 68, 68, 0.4)';
            contentDiv.style.background = 'rgba(127, 29, 29, 0.2)';
        }

        messageDiv.appendChild(contentDiv);

        // Add metadata info for bot messages
        if (sender === 'bot' && metadata.intent) {
            const metaDiv = document.createElement('div');
            metaDiv.className = 'message-meta';
            metaDiv.style.fontSize = '11px';
            metaDiv.style.opacity = '0.6';
            metaDiv.style.marginTop = '4px';
            metaDiv.textContent = `💡 Intent: ${metadata.intent} (${(metadata.confidence * 100).toFixed(0)}%)`;
            
            if (metadata.entities && Object.keys(metadata.entities).length > 0) {
                metaDiv.textContent += ` | Entities: ${Object.keys(metadata.entities).join(', ')}`;
            }
            
            messageDiv.appendChild(metaDiv);
        }

        messageCount++;
        chatBox.appendChild(messageDiv);
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
        requestAnimationFrame(() => {
            chatBox.scrollTo({
                top: chatBox.scrollHeight,
                behavior: 'smooth'
            });
        });
    }

    function generateSessionId() {
        // Create unique session ID based on timestamp and random value
        return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    async function checkServerHealth() {
        try {
            const response = await fetch(API.health);
            const data = await response.json();
            console.log('Server status:', data.status);
            return data.status === 'healthy';
        } catch (error) {
            console.warn('Server health check failed:', error);
            return false;
        }
    }

    // Advanced Features (exposed for debugging)
    window.ChatbotDebug = {
        sessionId: SESSION_ID,
        messageCount: () => messageCount,
        getHistory: async () => {
            try {
                const resp = await fetch(API.history);
                return resp.json();
            } catch (e) {
                console.error('Failed to get history:', e);
            }
        },
        getSummary: async () => {
            try {
                const resp = await fetch(API.summary);
                return resp.json();
            } catch (e) {
                console.error('Failed to get summary:', e);
            }
        },
        resetSession: async () => {
            try {
                const resp = await fetch(API.reset, { method: 'POST' });
                chatBox.innerHTML = '<div class="message bot-message"><div class="message-content">Session reset. Starting fresh conversation...</div></div>';
                messageCount = 0;
                return resp.json();
            } catch (e) {
                console.error('Failed to reset:', e);
            }
        },
        getIntents: async () => {
            try {
                const resp = await fetch(API.intents);
                return resp.json();
            } catch (e) {
                console.error('Failed to get intents:', e);
            }
        }
    };

    // Add CSS animation for message fade-in
    if (!document.getElementById('chatbot-animations')) {
        const style = document.createElement('style');
        style.id = 'chatbot-animations';
        style.textContent = `
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .message { animation: fadeIn 0.3s ease-in; }
        `;
        document.head.appendChild(style);
    }
});
