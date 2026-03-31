# Nexus AI - Advanced Chatbot System

A powerful, production-ready chatbot built entirely in Python without any external API dependencies. Features advanced NLP capabilities, session management, knowledge base integration, and intent recognition.

##  Features

### Core Features
- **Advanced NLP Engine** - Intent recognition, entity extraction, and context awareness
- **Knowledge Base System** - Customizable database for facts, Q&A pairs, and topics
- **Session Management** - Multi-session support with conversation history tracking
- **Response Generation** - Intelligent response generation with multiple templates
- **No API Dependencies** - Runs entirely locally without requiring external APIs
- **RESTful API** - Complete REST API for easy integration

### Advanced Capabilities
- **Intent Recognition** - Automatically identifies user intent with confidence scoring
- **Entity Extraction** - Extracts entities like names, numbers, emails, URLs
- **Context Awareness** - Maintains conversation context across multiple turns
- **Search Functionality** - Search knowledge base for relevant information
- **Custom Intents** - Add custom intents and patterns for specific domains
- **Conversation Analytics** - Track conversation metrics and generate summaries

##  Tech Stack

- **Backend**: Python 3.8+
- **Framework**: Flask 2.3.3
- **CORS**: Flask-CORS for cross-origin requests
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **NLP**: Custom Python NLP engine (no heavy dependencies)

##  Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Navigate to the project directory**
```bash
cd c:\Users\ankit\Documents\python\chatbot
```

2. **Create a virtual environment (optional but recommended)**
```bash
python -m venv venv
.\venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the backend server**
```bash
python server/app.py
```

The server will start on `http://127.0.0.1:5000`

5. **Open the frontend**
Open `client/index.html` in your web browser or serve it with a local server:
```bash
# Using Python 3
python -m http.server 8000 --directory client
```

Access the chatbot at `http://localhost:8000`

##  Project Structure

```
chatbot/
├── client/
│   ├── index.html          # Main HTML interface
│   ├── index.js            # Enhanced frontend with session management
│   ├── debug.js            # Debug console functionality
│   └── style.css           # Advanced styling with glassmorphism
├── server/
│   ├── app.py              # Flask application (main entry point)
│   └── utils/
│       ├── __init__.py
│       ├── nlp_engine.py   # Advanced NLP engine
│       ├── knowledge_base.py # Knowledge base system
│       └── response_generator.py # Response generation engine
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

##  Core Components

### 1. NLP Engine (`utils/nlp_engine.py`)
Handles natural language processing with:
- Text preprocessing and tokenization
- Intent recognition with confidence scoring
- Entity extraction (person, number, email, URL)
- Synonym matching
- Conversation history tracking
- Context management

```python
from utils.nlp_engine import NLPEngine

engine = NLPEngine()
result = engine.recognize_intent("Hello, how are you?")
# Returns: {'intent': 'greeting', 'confidence': 0.95, 'entities': {...}}
```

### 2. Knowledge Base (`utils/knowledge_base.py`)
Manages information storage and retrieval:
- Topic management
- Q&A storage and retrieval
- Fact tracking with categories
- Keyword-based search
- Related topics linking

```python
from utils.knowledge_base import KnowledgeBase

kb = KnowledgeBase()
kb.add_topic('Python', 'Python is a programming language...', 
             keywords=['programming', 'language'])
results = kb.search('Python programming')
```

### 3. Response Generator (`utils/response_generator.py`)
Generates contextual responses:
- Intent-based response templates
- Context-aware personalization
- Error handling with graceful messages
- Follow-up question generation
- Multi-turn conversation support

```python
from utils.response_generator import ResponseGenerator

generator = ResponseGenerator(knowledge_base)
response = generator.generate_response(intent_data, user_input, context)
```

##  API Endpoints

### Chat Endpoint
**POST** `/chat`
- Send user message and get response
- Parameters: `message` (required), `session_id` (optional)
- Response includes: `reply`, `intent`, `confidence`, `entities`, `session_id`

```bash
curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "session_123"}'
```

### Session Management
- **GET** `/session/<session_id>/history` - Get conversation history
- **GET** `/session/<session_id>/summary` - Get session summary
- **POST** `/session/<session_id>/reset` - Reset session

### Knowledge Base
- **POST** `/knowledge-base/search` - Search knowledge base
- **POST** `/knowledge-base/add-topic` - Add new topic
- **POST** `/knowledge-base/add-qa` - Add Q&A pair

### Intent Management
- **GET** `/intents` - List all available intents
- **POST** `/intents/add` - Add custom intent

### System
- **GET** `/health` - Health check
- **GET** `/stats` - Get chatbot statistics
- **GET** `/` - API documentation

##  Usage Examples

### Basic Chat
```javascript
// Send message to chatbot
const response = await fetch('http://127.0.0.1:5000/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ 
    message: 'What is Python?',
    session_id: 'user_123'
  })
});
const data = await response.json();
console.log(data.reply);
```

### Add Custom Intent (Python)
```python
nlp_engine.add_custom_intent(
    'weather_query',
    patterns=['what is the weather', 'will it rain', 'how cold is it'],
    responses=['I don\'t have weather data', 'Check a weather service']
)
```

### Search Knowledge Base (Python)
```python
results = knowledge_base.search('machine learning')
for result in results:
    print(f"Topic: {result['topic']}")
    print(f"Content: {result['content']}")
```

##  Debug Console

The frontend includes a debug console accessible via the 🔧 button:

**Available Features:**
-  **Show History** - View all messages in current session
-  **Show Summary** - Get session statistics
-  **List Intents** - View all available intents
-  **Clear Logs** - Clear debug log messages
-  **Reset Chat** - Reset conversation

**Debug API (JavaScript Console):**
```javascript
// Check available methods
console.log(ChatbotDebug);

// Get session history
ChatbotDebug.getHistory();

// Get session summary
ChatbotDebug.getSummary();

// List intents
ChatbotDebug.getIntents();

// Reset session
ChatbotDebug.resetSession();
```

##  Customization

### Adding New Intents
Edit `server/utils/nlp_engine.py` in the `_initialize_patterns()` method:

```python
self.intents['custom_name'] = {
    'patterns': ['pattern1', 'pattern2', 'pattern3'],
    'responses': ['response1', 'response2', 'response3']
}
```

### Extending Knowledge Base
Add topics and Q&A pairs in `server/utils/knowledge_base.py` or via API:

```python
kb.add_topic('Your Topic', 'Description', keyword_list, related_topics)
kb.add_qa('Question?', 'Answer')
```

### Styling
Modify `client/style.css` to customize the UI:
- Color palette in `:root` CSS variables
- Animations for message transitions
- Responsive design for mobile devices

##  Deployment

### Local Development
```bash
python server/app.py
```

### Production Setup (Example with Gunicorn)
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn --workers 4 --bind 0.0.0.0:5000 server.app:app
```

##  Performance Considerations

- **Message Caching**: Conversation history is cached in memory
- **NLP Optimization**: Similarity calculations use efficient algorithms
- **No External Calls**: Everything runs locally for fast responses
- **Scalability**: Session management allows multiple concurrent users

##  Security Notes

- The chatbot runs locally with no external API calls
- Session IDs are generated client-side (use UUIDs in production)
- Input is validated before processing
- No sensitive data is logged by default

##  Contributing

To extend the chatbot:

1. Add new intents in `nlp_engine.py`
2. Create knowledge base entries
3. Customize response templates in `response_generator.py`
4. Enhance frontend UI in `index.html` and `style.css`

##  License

This project is open source and available for educational and commercial use.

##  Troubleshooting

### Server Connection Failed
- Ensure the Flask server is running on port 5000
- Check firewall settings
- Verify no other application is using port 5000

### Intent Not Recognized
- Check pattern definitions in `nlp_engine.py`
- Increase confidence threshold or add more patterns
- Use debug console to inspect intent recognition

### Missing Responses
- Ensure knowledge base is properly populated
- Check response generator templates
- Verify session is properly initialized

##  Support

For issues or questions:
1. Check the debug console for error messages
2. Review API responses for detailed error information
3. Consult the code comments in utility files
4. Review the examples in this README

---

**Version**: 1.0.0  
**Last Updated**: 2026-03-31  
**Status**: Production Ready
