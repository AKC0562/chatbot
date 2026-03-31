# Quick Start Guide for Nexus AI Chatbot

This guide will help you get the advanced chatbot running in just 5 minutes!

## ✅ Prerequisites

- Python 3.8 or later
- Windows, macOS, or Linux
- Any modern web browser
- ~50 MB disk space for dependencies

## 🚀 5-Minute Setup

### Step 1: Navigate to Project
```bash
cd c:\Users\ankit\Documents\python\chatbot
```

### Step 2: Run Setup Script
**Windows:**
```batch
setup.bat
```

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Start the Backend
Activate virtual environment first:

**Windows:**
```batch
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

Then start the server:
```bash
python server/app.py
```

You should see:
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 4: Open the Frontend
Open `client/index.html` in your web browser

**Alternative - Serve with Python:**
```bash
python -m http.server 8000 --directory client
```
Then visit: http://localhost:8000

### Step 5: Start Chatting!
Type any message and press Enter or click the Send button

---

## 🎯 What to Try First

1. **Test Greetings**: Try saying "Hello" or "Hi"
2. **Ask a Question**: Try "Tell me about Python"
3. **Learning Request**: Try asking "How do I learn?"
4. **Help Request**: Try "Can you help me?"

## 🧪 Test the Advanced Features

Open the browser's developer console (F12) and try these:

```javascript
// View all messages in current session
ChatbotDebug.getHistory()

// Get conversation summary
ChatbotDebug.getSummary()

// List all available intents
ChatbotDebug.getIntents()

// Print session ID
console.log(ChatbotDebug.sessionId)
```

Or use the Debug Console button (🔧) in the chat UI!

## 📱 Debug Console Features

Click the 🔧 button in the top-right to access:
- 📝 **Show History** - View all messages
- 📊 **Show Summary** - Session statistics
- 💡 **List Intents** - Available intents
- 🗑️ **Clear Logs** - Clear debug output

## 🔄 Reset the Conversation

Click the 🔄 button to start a fresh conversation anytime.

## 🛑 Troubleshooting

### "Connection refused" error
- Make sure the backend server is running on port 5000
- Check: `python server/app.py` was executed

### "Module not found" error
- Ensure virtual environment is activated
- Run: `pip install -r requirements.txt`

### Port already in use
- Change Flask port in `server/app.py`:
  ```python
  app.run(debug=True, host='127.0.0.1', port=5001)
  ```

## 📚 Next Steps

Once you're comfortable with the basics:

1. **Add Custom Intents**: Edit `server/utils/nlp_engine.py`
2. **Expand Knowledge Base**: Modify `server/utils/knowledge_base.py`
3. **Train the Chatbot**: Use the API endpoints to add topics
4. **Customize UI**: Edit `client/style.css`

## 🚀 Advanced Usage

### Add a Custom Intent via API

```javascript
fetch('http://127.0.0.1:5000/intents/add', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    intent_name: 'weather_check',
    patterns: ['whats the weather', 'will it rain', 'temperature'],
    responses: [
      'I dont have weather data, check weather.com',
      'Weather info requires external service'
    ]
  })
})
```

### Search Knowledge Base via API

```javascript
fetch('http://127.0.0.1:5000/knowledge-base/search', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ query: 'Python' })
})
.then(r => r.json())
.then(data => console.log(data.results))
```

## 💡 Tips

- The chatbot learns from patterns, not external data
- All conversations are local - no data sent anywhere
- Session history is kept in memory during the session
- Add custom topics to improve responses
- Check the debug console to understand how intent recognition works

## 📞 Need Help?

1. Check the **README.md** for detailed documentation
2. Review API endpoints in `server/app.py`
3. Look at component code in `server/utils/`
4. Use the **Debug Console** to inspect conversations

---

**Congratulations!** You now have a fully functional advanced chatbot with NLP capabilities! 🎉

For more information, see `README.md`.
