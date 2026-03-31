import re
import string
from collections import defaultdict
from difflib import SequenceMatcher
import json

class NLPEngine:
    """Advanced NLP Engine for chatbot with intent recognition and entity extraction"""
    
    def __init__(self):
        self.intents = defaultdict(list)
        self.entities = defaultdict(list)
        self.synonyms = defaultdict(list)
        self.conversation_history = []
        self.context = {}
        self._initialize_patterns()
    
    def _initialize_patterns(self):
        """Initialize default intents, entities, and patterns"""
        
        # Define intents with patterns
        self.intents = {
            'greeting': {
                'patterns': ['hello', 'hi', 'hey', 'greetings', 'what\'s up', 'howdy'],
                'responses': [
                    'Hello! How can I assist you today?',
                    'Hi there! What can I help you with?',
                    'Greetings! How may I be of service?',
                    'Hey! What brings you here?'
                ]
            },
            'goodbye': {
                'patterns': ['bye', 'goodbye', 'see you', 'farewell', 'exit', 'quit', 'bye bye'],
                'responses': [
                    'Goodbye! Have a great day!',
                    'See you soon!',
                    'Farewell! Feel free to come back anytime.',
                    'Take care! Bye!'
                ]
            },
            'help': {
                'patterns': ['help', 'assist', 'support', 'can you help', 'i need help', 'what can you do'],
                'responses': [
                    'I can help with general questions, information, provide insights, and engage in conversations.',
                    'I\'m here to assist with answering questions, discussing topics, and providing helpful information.',
                    'I can help with various topics including general knowledge, explanations, and conversations.'
                ]
            },
            'name': {
                'patterns': ['what is your name', 'who are you', 'your name', 'what do you call yourself'],
                'responses': [
                    'I\'m Nexus, an advanced AI assistant designed to help you.',
                    'My name is Nexus. I\'m here to assist you!',
                    'I\'m Nexus, your intelligent chatbot assistant.'
                ]
            },
            'mood': {
                'patterns': ['how are you', 'how\'s it going', 'how do you feel', 'what\'s up', 'you doing'],
                'responses': [
                    'I\'m doing great, thanks for asking! How about you?',
                    'I\'m functioning optimally and ready to help. How are you?',
                    'I\'m excellent! Thanks for checking in. How can I assist you today?'
                ]
            },
            'time': {
                'patterns': ['what time is it', 'current time', 'tell me the time', 'what\'s the time'],
                'responses': [
                    'I don\'t have access to real-time information, but you can check your system clock.',
                    'Sorry, I don\'t track time directly. Please check your device\'s clock.'
                ]
            },
            'date': {
                'patterns': ['what date is it', 'what\'s today', 'current date', 'tell me the date'],
                'responses': [
                    'I can\'t access current date information. Please check your calendar.',
                    'Sorry, I don\'t have date information. Check your device\'s date settings.'
                ]
            },
            'info_request': {
                'patterns': ['tell me about', 'what is', 'explain', 'i want to know', 'information about', 'how does'],
                'responses': [
                    'I\'d be happy to provide information about that. Could you be more specific?',
                    'That\'s an interesting topic. Tell me more about what you\'d like to know.',
                    'I can help explain that. Please provide more details.'
                ]
            },
            'default': {
                'patterns': [],
                'responses': [
                    'That\'s interesting! Can you tell me more about that?',
                    'I see. Could you elaborate on that?',
                    'Interesting point. How does this relate to what we\'re discussing?',
                    'I understand. Tell me more about your thoughts on this.'
                ]
            }
        }
        
        # Entity patterns
        self.entities = {
            'person': r'\b(?:i|me|my|myself|you|he|she|it|we|they|john|mary|james|robert|michael)\b',
            'number': r'\b\d+(?:\.\d+)?\b',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'url': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            'command': r'!?\w+(?:\s+\w+)*'
        }
        
        # Synonyms for better matching
        self.synonyms = {
            'hello': ['hi', 'hey', 'greetings', 'sup', 'howdy'],
            'help': ['assist', 'support', 'aid'],
            'name': ['called', 'namesake'],
            'understand': ['comprehend', 'get', 'follow'],
            'goodbye': ['bye', 'farewell', 'see you']
        }
    
    def preprocess(self, text):
        """Clean and preprocess text"""
        # Convert to lowercase
        text = text.lower()
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
    
    def tokenize(self, text):
        """Split text into tokens"""
        return text.split()
    
    def extract_entities(self, text):
        """Extract named entities from text"""
        entities = {}
        for entity_type, pattern in self.entities.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                entities[entity_type] = matches
        return entities
    
    def calculate_similarity(self, text1, text2):
        """Calculate similarity between two texts (0-1)"""
        return SequenceMatcher(None, text1, text2).ratio()
    
    def recognize_intent(self, user_input):
        """Recognize intent from user input"""
        processed_input = self.preprocess(user_input)
        tokens = self.tokenize(processed_input)
        
        best_intent = 'default'
        best_score = 0
        best_response = None
        
        for intent_name, intent_data in self.intents.items():
            patterns = intent_data.get('patterns', [])
            
            for pattern in patterns:
                # Calculate similarity
                similarity = self.calculate_similarity(processed_input, pattern)
                
                # Check for token matches
                pattern_tokens = self.tokenize(pattern)
                token_matches = sum(1 for token in pattern_tokens if token in tokens)
                token_score = token_matches / max(len(pattern_tokens), 1)
                
                # Combined score
                combined_score = (similarity * 0.4) + (token_score * 0.6)
                
                if combined_score > best_score:
                    best_score = combined_score
                    best_intent = intent_name
        
        # If confidence is high enough, use intent response
        if best_score >= 0.3:
            responses = self.intents[best_intent].get('responses', [])
            if responses:
                import random
                best_response = random.choice(responses)
        
        return {
            'intent': best_intent,
            'confidence': best_score,
            'response': best_response,
            'entities': self.extract_entities(user_input)
        }
    
    def add_to_history(self, user_message, bot_response):
        """Add message pair to conversation history"""
        self.conversation_history.append({
            'user': user_message,
            'bot': bot_response,
            'timestamp': len(self.conversation_history)
        })
    
    def get_context(self):
        """Get current conversation context"""
        return {
            'history_length': len(self.conversation_history),
            'current_topic': self.context.get('topic', 'general'),
            'user_name': self.context.get('user_name', 'User'),
            'messages_count': len(self.conversation_history)
        }
    
    def update_context(self, key, value):
        """Update context information"""
        self.context[key] = value
    
    def add_custom_intent(self, intent_name, patterns, responses):
        """Add custom intent for training"""
        self.intents[intent_name] = {
            'patterns': patterns if isinstance(patterns, list) else [patterns],
            'responses': responses if isinstance(responses, list) else [responses]
        }
    
    def get_conversation_summary(self):
        """Generate summary of conversation"""
        if not self.conversation_history:
            return "No conversation history yet."
        
        total_messages = len(self.conversation_history)
        return f"Conversation has {total_messages} message exchanges."
    
    def reset_conversation(self):
        """Reset conversation history and context"""
        self.conversation_history = []
        self.context = {}
