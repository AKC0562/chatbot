# Quick Reference Guide - Nexus AI Chatbot

## 🚀 Startup Commands

### Windows
```batch
# Navigate to project
cd c:\Users\ankit\Documents\python\chatbot

# First time setup
setup.bat

# Start backend
venv\Scripts\activate
python server/app.py

# Start frontend
python -m http.server 8000 --directory client
```

### Mac/Linux
```bash
# Navigate to project
cd c:\Users\ankit\Documents\python\chatbot

# First time setup
chmod +x setup.sh
./setup.sh

# Start backend
source venv/bin/activate
python server/app.py

# Start frontend
python -m http.server 8000 --directory client
```

## 💻 API Quick Reference

### Send Message
```bash
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "session_123"}'
```

### Search Knowledge Base
```bash
curl -X POST http://127.0.0.1:5000/knowledge-base/search \
  -H "Content-Type: application/json" \
  -d '{"query": "python"}'
```

### List All Intents
```bash
curl http://127.0.0.1:5000/intents
```

### Add Custom Intent
```bash
curl -X POST http://127.0.0.1:5000/intents/add \
  -H "Content-Type: application/json" \
  -d '{
    "intent_name": "weather",
    "patterns": ["whats the weather", "will it rain"],
    "responses": ["I cant check weather"]
  }'
```

### Get Session Summary
```bash
curl http://127.0.0.1:5000/session/session_123/summary
```

### Reset Session
```bash
curl -X POST http://127.0.0.1:5000/session/session_123/reset
```

### Health Check
```bash
curl http://127.0.0.1:5000/health
```

### Get Statistics
```bash
curl http://127.0.0.1:5000/stats
```

## 🧪 JavaScript Debug Commands

Open browser console (F12) and run:

```javascript
// View current session ID
ChatbotDebug.sessionId

// Get conversation history
ChatbotDebug.getHistory()

// Get session summary
ChatbotDebug.getSummary()

// List available intents
ChatbotDebug.getIntents()

// Get message count
ChatbotDebug.messageCount()

// Reset conversation
ChatbotDebug.resetSession()
```

## 🐍 Python API Usage

```python
import requests

BASE_URL = 'http://127.0.0.1:5000'
SESSION_ID = 'my_session'

# Send message
response = requests.post(f'{BASE_URL}/chat', json={
    'message': 'Hello',
    'session_id': SESSION_ID
})
print(response.json()['reply'])

# Get history
history = requests.get(f'{BASE_URL}/session/{SESSION_ID}/history').json()
print(f"Messages: {history['message_count']}")

# Search KB
results = requests.post(f'{BASE_URL}/knowledge-base/search',
    json={'query': 'Python'}).json()
for result in results['results']:
    print(result['content'])

# Add intent
requests.post(f'{BASE_URL}/intents/add', json={
    'intent_name': 'custom',
    'patterns': ['test'],
    'responses': ['response']
})
```

## 🛠️ Common Tasks

### Add New Intent (Python)
Edit `server/utils/nlp_engine.py`:
```python
self.intents['my_intent'] = {
    'patterns': ['pattern1', 'pattern2'],
    'responses': ['response1', 'response2']
}
```

### Add Knowledge Base Topic (Python)
Edit `server/utils/knowledge_base.py`:
```python
kb.add_topic('Topic Name', 'Description here', 
             keywords=['key1', 'key2'],
             related=['related1'])
```

### Add Q&A (Python)
```python
kb.add_qa('Question?', 'Answer here.')
```

### Customize UI Style
Edit `client/style.css`, modify `:root` variables:
```css
:root {
    --primary-color: #your-color;
    --bg-gradient: linear-gradient(...);
}
```

### Change Backend Port
Edit `server/app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)
```

### Change Frontend Port
Edit Flask CORS or serve differently:
```bash
python -m http.server 3000 --directory client
```

## 🔄 File Structure Quick Reference

```
chatbot/
├── server/app.py              ← Main backend (edit to change API)
├── server/utils/
│   ├── nlp_engine.py         ← Add intents here
│   ├── knowledge_base.py      ← Add KB entries here
│   └── response_generator.py  ← Response templates
├── client/
│   ├── index.html            ← UI layout
│   ├── index.js              ← Chat logic
│   ├── debug.js              ← Debug console
│   └── style.css             ← Styling
├── requirements.txt           ← Dependencies
├── example_usage.py           ← API examples
├── README.md                 ← Full docs
├── QUICKSTART.md             ← Quick setup
└── PROJECT_SUMMARY.md        ← Overview
```

## 🎯 Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| "Connection refused" | Start backend: `python server/app.py` |
| "Module not found" | Activate venv and reinstall: `pip install -r requirements.txt` |
| Port 5000 in use | Change port in `app.py` line `app.run(port=5001)` |
| CORS error | Already handled, check console for details |
| No response | Check Flask logs, verify JSON format |
| Intent not recognized | Add patterns to `nlp_engine.py` |
| KB not returning results | Check topic is added, search terms match keywords |

## 📊 Performance Tips

1. **Faster Responses**
   - Limit conversation history size
   - Cache frequently searched KB items
   - Use simpler patterns for common intents

2. **Better Accuracy**
   - Add more patterns for each intent
   - Expand knowledge base with domains
   - Fine-tune similarity thresholds

3. **Scalability**
   - Use Gunicorn with multiple workers
   - Implement database for sessions
   - Add caching layer

## 🔐 Security Checklist

- [ ] No API keys in code
- [ ] Input validation enabled
- [ ] CORS properly configured
- [ ] Sessions isolated
- [ ] No sensitive data logged
- [ ] Update dependencies regularly

## 📚 Documentation Map

| Document | Purpose | When to use |
|----------|---------|------------|
| QUICKSTART.md | 5-min setup | Getting started |
| README.md | Full reference | Learning features |
| PROJECT_SUMMARY.md | Overview | Understanding project |
| example_usage.py | Code examples | Integration help |
| VERIFICATION.md | Testing checklist | Verifying setup |
| REFERENCE.md | This file | Quick lookup |

## 💾 Backup Commands

```bash
# Backup entire project
cp -r chatbot chatbot_backup

# Just backup code
cp -r server client requirements.txt backup/

# Just backup configs
cp requirements.txt server/app.py backup/
```

## 🚀 Deployment Command

```bash
# Install production server
pip install gunicorn

# Run with 4 workers
gunicorn --workers 4 --bind 0.0.0.0:5000 server.app:app

# With logging
gunicorn --workers 4 --bind 0.0.0.0:5000 \
  --access-logfile access.log \
  --error-logfile error.log \
  server.app:app
```

## 🎓 Learning Path

1. **Day 1**: Setup and basic usage
2. **Day 2**: Explore debug console
3. **Day 3**: Add custom intents
4. **Day 4**: Extend knowledge base
5. **Day 5**: Customize UI
6. **Day 6**: Deploy locally
7. **Day 7**: Production setup

## 📞 Support Resources

- 📖 **README.md** - Feature documentation
- 🚀 **QUICKSTART.md** - Setup guide
- 📊 **PROJECT_SUMMARY.md** - Project overview
- 🧪 **example_usage.py** - API examples
- ✅ **VERIFICATION.md** - Testing guide
- 💬 **inline code comments** - Implementation details

## 🎁 Bonus Features

### Enable Pretty JSON Output (for testing)
```bash
# Use jq with curl for pretty JSON
curl http://127.0.0.1:5000/stats | jq
```

### Monitor Server in Real-time
```bash
# Watch Flask logs
tail -f /tmp/flask.log
```

### Batch Test Multiple Messages
```bash
# Create test_messages.txt with messages
# Run example_usage.py for batch processing
python example_usage.py
```

---

**Need more help?** Check the full documentation files or review the code comments!

**Happy developing!** 🚀
