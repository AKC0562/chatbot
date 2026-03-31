"""
Example usage of the Nexus AI Chatbot API

This script demonstrates:
- Sending messages to the chatbot
- Managing sessions
- Searching the knowledge base
- Adding custom intents
- Working with conversation history
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = 'http://127.0.0.1:5000'
SESSION_ID = 'example_session_001'

# Color codes for terminal output
class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

def print_header(text):
    """Print formatted header"""
    print(f"\n{Colors.BLUE}{'='*50}")
    print(f"{text}")
    print(f"{'='*50}{Colors.END}\n")

def send_message(message):
    """Send a message to the chatbot"""
    print(f"{Colors.YELLOW}You: {message}{Colors.END}")
    
    response = requests.post(f'{BASE_URL}/chat', json={
        'message': message,
        'session_id': SESSION_ID
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"{Colors.GREEN}Bot: {data['reply']}{Colors.END}")
        print(f"  Intent: {data['intent']} ({data['confidence']*100:.1f}%)")
        if data.get('entities'):
            print(f"  Entities: {data['entities']}")
        return data
    else:
        print(f"{Colors.RED}Error: {response.text}{Colors.END}")
        return None

def search_knowledge_base(query):
    """Search the knowledge base"""
    print(f"{Colors.YELLOW}Searching KB for: '{query}'{Colors.END}")
    
    response = requests.post(f'{BASE_URL}/knowledge-base/search', json={
        'query': query
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"{Colors.GREEN}Found {data['result_count']} results:{Colors.END}")
        for i, result in enumerate(data['results'], 1):
            if result['source'] == 'knowledge_base':
                print(f"  {i}. {result['topic']}: {result['content']}")
            else:
                print(f"  {i}. Q&A: {result.get('question', 'N/A')}")
        return data
    else:
        print(f"{Colors.RED}Error: {response.text}{Colors.END}")
        return None

def get_session_history():
    """Get conversation history for current session"""
    response = requests.get(f'{BASE_URL}/session/{SESSION_ID}/history')
    
    if response.status_code == 200:
        data = response.json()
        print(f"{Colors.GREEN}Conversation History ({data['message_count']} messages):{Colors.END}")
        for i, msg in enumerate(data['messages'], 1):
            print(f"\n  [{i}] User: {msg['user']}")
            print(f"      Bot: {msg['bot']}")
            print(f"      Intent: {msg['intent']} ({msg['confidence']*100:.1f}%)")
        return data
    else:
        print(f"{Colors.RED}Error: {response.text}{Colors.END}")
        return None

def get_session_summary():
    """Get session summary"""
    response = requests.get(f'{BASE_URL}/session/{SESSION_ID}/summary')
    
    if response.status_code == 200:
        data = response.json()
        print(f"{Colors.GREEN}Session Summary:{Colors.END}")
        print(f"  Session ID: {data['session_id']}")
        print(f"  Messages: {data['message_count']}")
        print(f"  Summary: {data['summary']}")
        print(f"  Context: {json.dumps(data['context'], indent=4)}")
        return data
    else:
        print(f"{Colors.RED}Error: {response.text}{Colors.END}")
        return None

def list_intents():
    """List all available intents"""
    response = requests.get(f'{BASE_URL}/intents')
    
    if response.status_code == 200:
        data = response.json()
        print(f"{Colors.GREEN}Available Intents ({data['total_intents']}):{Colors.END}")
        for intent in data['intents']:
            print(f"  • {intent['name']}")
            print(f"    Patterns: {', '.join(intent['patterns'] if intent['patterns'] else ['None'])}")
            print(f"    Responses: {intent['response_count']}")
        return data
    else:
        print(f"{Colors.RED}Error: {response.text}{Colors.END}")
        return None

def add_custom_intent(intent_name, patterns, responses):
    """Add a custom intent"""
    print(f"{Colors.YELLOW}Adding custom intent: {intent_name}{Colors.END}")
    
    response = requests.post(f'{BASE_URL}/intents/add', json={
        'intent_name': intent_name,
        'patterns': patterns,
        'responses': responses
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"{Colors.GREEN}✓ Intent added successfully{Colors.END}")
        return data
    else:
        print(f"{Colors.RED}Error: {response.text}{Colors.END}")
        return None

def add_knowledge_base_topic(topic, description, keywords=None, related=None):
    """Add a topic to knowledge base"""
    print(f"{Colors.YELLOW}Adding KB topic: {topic}{Colors.END}")
    
    response = requests.post(f'{BASE_URL}/knowledge-base/add-topic', json={
        'topic': topic,
        'description': description,
        'keywords': keywords or [],
        'related': related or []
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"{Colors.GREEN}✓ Topic added successfully{Colors.END}")
        return data
    else:
        print(f"{Colors.RED}Error: {response.text}{Colors.END}")
        return None

def add_qa_pair(question, answer):
    """Add Q&A pair to knowledge base"""
    print(f"{Colors.YELLOW}Adding Q&A: {question}{Colors.END}")
    
    response = requests.post(f'{BASE_URL}/knowledge-base/add-qa', json={
        'question': question,
        'answer': answer
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"{Colors.GREEN}✓ Q&A added successfully{Colors.END}")
        return data
    else:
        print(f"{Colors.RED}Error: {response.text}{Colors.END}")
        return None

def get_health():
    """Check server health"""
    response = requests.get(f'{BASE_URL}/health')
    
    if response.status_code == 200:
        data = response.json()
        print(f"{Colors.GREEN}✓ Server is {data['status']}")
        print(f"  Active sessions: {data['active_sessions']}{Colors.END}")
        return data
    else:
        print(f"{Colors.RED}✗ Server is not responding{Colors.END}")
        return None

def main():
    """Main example execution"""
    
    print_header("Nexus AI - Chatbot API Examples")
    
    # Check server health
    print_header("1. Health Check")
    health = get_health()
    if not health:
        print(f"{Colors.RED}ERROR: Server not running!{Colors.END}")
        print("Please start the server with: python server/app.py")
        return
    
    # Basic conversation
    print_header("2. Basic Conversation")
    send_message("Hello, how are you?")
    send_message("Tell me about Python")
    send_message("What can you do?")
    
    # List available intents
    print_header("3. List Available Intents")
    list_intents()
    
    # Add custom intent
    print_header("4. Add Custom Intent")
    add_custom_intent(
        'mood_check',
        ['how are you', 'how do you feel', 'are you okay'],
        ['I am functioning optimally!', 'Everything is great!']
    )
    
    # Search knowledge base
    print_header("5. Search Knowledge Base")
    search_knowledge_base("Python")
    
    # Add knowledge base entries
    print_header("6. Add Knowledge Base Entries")
    add_knowledge_base_topic(
        'Web Development',
        'Web development involves creating websites using HTML, CSS, and JavaScript.',
        keywords=['html', 'css', 'javascript'],
        related=['frontend', 'backend']
    )
    
    add_qa_pair(
        'What is Flask?',
        'Flask is a lightweight Python web framework for building web applications.'
    )
    
    # Continue conversation
    print_header("7. Continue Conversation with New Intent")
    send_message("How are you?")
    send_message("Tell me about Web Development")
    
    # Get session summary
    print_header("8. Get Session Summary")
    get_session_summary()
    
    # Get session history
    print_header("9. Get Full Conversation History")
    get_session_history()
    
    print_header("Examples Complete!")
    print(f"{Colors.GREEN}All API endpoints demonstrated successfully!{Colors.END}\n")

if __name__ == '__main__':
    main()
