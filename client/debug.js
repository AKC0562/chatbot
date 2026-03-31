// Debug Console for Advanced Chatbot
document.addEventListener('DOMContentLoaded', () => {
    const debugBtn = document.getElementById('debug-btn');
    const debugPanel = document.getElementById('debug-panel');
    const closeDebugBtn = document.getElementById('close-debug');
    const resetBtn = document.getElementById('reset-btn');
    const debugLogs = document.getElementById('debug-logs');
    
    // Debug buttons
    const showHistoryBtn = document.getElementById('show-history');
    const showSummaryBtn = document.getElementById('show-summary');
    const showIntentsBtn = document.getElementById('show-intents');
    const clearLogsBtn = document.getElementById('clear-logs');

    // Toggle debug panel
    debugBtn.addEventListener('click', () => {
        debugPanel.classList.toggle('hidden');
    });

    closeDebugBtn.addEventListener('click', () => {
        debugPanel.classList.add('hidden');
    });

    // Reset session
    resetBtn.addEventListener('click', async () => {
        if (confirm('Are you sure you want to reset the conversation?')) {
            await ChatbotDebug.resetSession();
            addLog('✅ Session reset successfully');
        }
    });

    // Show history
    showHistoryBtn.addEventListener('click', async () => {
        clearLogs();
        addLog('📝 Loading conversation history...');
        try {
            const history = await ChatbotDebug.getHistory();
            if (history.messages && history.messages.length > 0) {
                addLog(`Found ${history.messages.length} messages:`);
                history.messages.forEach((msg, idx) => {
                    addLog(`  ${idx + 1}. User: "${msg.user}"`);
                    addLog(`     Bot: "${msg.bot}"`);
                    addLog(`     Intent: ${msg.intent} (${Math.round(msg.confidence * 100)}%)`);
                });
            } else {
                addLog('No messages in history yet.');
            }
        } catch (e) {
            addLog('❌ Error loading history: ' + e.message);
        }
    });

    // Show summary
    showSummaryBtn.addEventListener('click', async () => {
        clearLogs();
        addLog('📊 Loading session summary...');
        try {
            const summary = await ChatbotDebug.getSummary();
            addLog('SESSION SUMMARY:');
            addLog(`  Session ID: ${summary.session_id}`);
            addLog(`  Messages: ${summary.message_count}`);
            addLog(`  Summary: ${summary.summary}`);
            if (summary.context) {
                addLog(`  Context: ${JSON.stringify(summary.context, null, 2)}`);
            }
            if (summary.created_at) {
                addLog(`  Created: ${new Date(summary.created_at).toLocaleString()}`);
            }
        } catch (e) {
            addLog('❌ Error loading summary: ' + e.message);
        }
    });

    // Show intents
    showIntentsBtn.addEventListener('click', async () => {
        clearLogs();
        addLog('💡 Loading available intents...');
        try {
            const intents = await ChatbotDebug.getIntents();
            if (intents.intents && intents.intents.length > 0) {
                addLog(`Found ${intents.total_intents} intents:`);
                intents.intents.forEach(intent => {
                    addLog(`  • ${intent.name}`);
                    addLog(`    Patterns: ${intent.patterns.join(', ')}`);
                    addLog(`    Responses: ${intent.response_count}`);
                });
            } else {
                addLog('No intents available.');
            }
        } catch (e) {
            addLog('❌ Error loading intents: ' + e.message);
        }
    });

    // Clear logs
    clearLogsBtn.addEventListener('click', clearLogs);

    function addLog(message) {
        const logEntry = document.createElement('div');
        logEntry.className = 'log-entry';
        logEntry.textContent = message;
        debugLogs.appendChild(logEntry);
        debugLogs.scrollTop = debugLogs.scrollHeight;
    }

    function clearLogs() {
        debugLogs.innerHTML = '';
    }

    // Initial message
    addLog('🔧 Debug Console Ready');
    addLog('Select an option above to inspect chatbot state');
});
