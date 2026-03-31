from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

# Import our advanced components
from utils.nlp_engine import NLPEngine
from utils.knowledge_base import KnowledgeBase
from utils.response_generator import ResponseGenerator

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize our advanced chatbot components
nlp_engine = NLPEngine()
knowledge_base = KnowledgeBase()
response_generator = ResponseGenerator(knowledge_base)

# Store active sessions
sessions = {}

@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint for processing user messages"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        session_id = data.get('session_id', 'default')
        
        if not user_message:
            return jsonify({"error": "Message is required"}), 400
        
        # Initialize session if needed
        if session_id not in sessions:
            sessions[session_id] = {
                'messages': [],
                'created_at': datetime.now().isoformat(),
                'nlp_engine': NLPEngine(),
                'context': {}
            }
        
        session = sessions[session_id]
        engine = session['nlp_engine']
        
        # Process message through NLP engine
        intent_data = engine.recognize_intent(user_message)
        
        # Extract entities
        entities = intent_data.get('entities', {})
        
        # Get context
        context = engine.get_context()
        
        # Generate response
        bot_response = response_generator.generate_response(
            intent_data,
            user_message,
            context
        )
        
        # For info requests, try to get knowledge base info
        if intent_data['intent'] == 'info_request' or intent_data['confidence'] < 0.5:
            kb_results = knowledge_base.search(user_message)
            if kb_results:
                kb_response = response_generator._format_kb_response(kb_results[0])
                if kb_response:
                    bot_response = kb_response
        
        # Store in message history
        engine.add_to_history(user_message, bot_response)
        session['messages'].append({
            'user': user_message,
            'bot': bot_response,
            'intent': intent_data['intent'],
            'confidence': round(intent_data['confidence'], 2),
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify({
            'reply': bot_response,
            'intent': intent_data['intent'],
            'confidence': round(intent_data['confidence'], 2),
            'entities': entities,
            'session_id': session_id
        })
    
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({
            'error': 'An error occurred while processing your message',
            'details': str(e)
        }), 500

@app.route('/session/<session_id>/history', methods=['GET'])
def get_chat_history(session_id):
    """Get conversation history for a session"""
    try:
        if session_id not in sessions:
            return jsonify({"error": "Session not found"}), 404
        
        session = sessions[session_id]
        return jsonify({
            'session_id': session_id,
            'messages': session['messages'],
            'created_at': session['created_at'],
            'message_count': len(session['messages'])
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/session/<session_id>/summary', methods=['GET'])
def get_session_summary(session_id):
    """Get session summary"""
    try:
        if session_id not in sessions:
            return jsonify({"error": "Session not found"}), 404
        
        session = sessions[session_id]
        engine = session['nlp_engine']
        
        return jsonify({
            'session_id': session_id,
            'summary': engine.get_conversation_summary(),
            'message_count': len(session['messages']),
            'context': engine.get_context(),
            'created_at': session['created_at']
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/session/<session_id>/reset', methods=['POST'])
def reset_session(session_id):
    """Reset a conversation session"""
    try:
        if session_id in sessions:
            del sessions[session_id]
        
        return jsonify({
            'message': 'Session reset successfully',
            'session_id': session_id
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/knowledge-base/search', methods=['POST'])
def search_kb():
    """Search knowledge base"""
    try:
        data = request.json
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({"error": "Query is required"}), 400
        
        results = knowledge_base.search(query)
        
        return jsonify({
            'query': query,
            'results': results,
            'result_count': len(results)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/knowledge-base/add-topic', methods=['POST'])
def add_kb_topic():
    """Add a new topic to knowledge base"""
    try:
        data = request.json
        topic = data.get('topic', '').strip()
        description = data.get('description', '').strip()
        keywords = data.get('keywords', [])
        related = data.get('related', [])
        
        if not topic or not description:
            return jsonify({"error": "Topic and description are required"}), 400
        
        knowledge_base.add_topic(topic, description, keywords, related)
        
        return jsonify({
            'message': 'Topic added successfully',
            'topic': topic
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/knowledge-base/add-qa', methods=['POST'])
def add_kb_qa():
    """Add Q&A pair to knowledge base"""
    try:
        data = request.json
        question = data.get('question', '').strip()
        answer = data.get('answer', '').strip()
        
        if not question or not answer:
            return jsonify({"error": "Question and answer are required"}), 400
        
        knowledge_base.add_qa(question, answer)
        
        return jsonify({
            'message': 'Q&A added successfully',
            'question': question
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/intents', methods=['GET'])
def get_intents():
    """Get all available intents"""
    try:
        intents_list = []
        for intent_name, intent_data in nlp_engine.intents.items():
            intents_list.append({
                'name': intent_name,
                'patterns': intent_data.get('patterns', []),
                'response_count': len(intent_data.get('responses', []))
            })
        
        return jsonify({
            'intents': intents_list,
            'total_intents': len(intents_list)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/intents/add', methods=['POST'])
def add_intent():
    """Add custom intent"""
    try:
        data = request.json
        intent_name = data.get('intent_name', '').strip()
        patterns = data.get('patterns', [])
        responses = data.get('responses', [])
        
        if not intent_name or not patterns or not responses:
            return jsonify({"error": "intent_name, patterns, and responses are required"}), 400
        
        nlp_engine.add_custom_intent(intent_name, patterns, responses)
        
        return jsonify({
            'message': 'Intent added successfully',
            'intent_name': intent_name
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'app': 'Advanced Chatbot',
        'active_sessions': len(sessions),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get chatbot statistics"""
    try:
        total_messages = sum(len(s['messages']) for s in sessions.values())
        
        return jsonify({
            'total_sessions': len(sessions),
            'total_messages': total_messages,
            'available_intents': len(nlp_engine.intents),
            'kb_topics': len(knowledge_base.kb),
            'kb_qas': len(knowledge_base.q_and_a),
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        'app': 'Advanced Chatbot API',
        'version': '1.0.0',
        'endpoints': {
            'chat': {
                'method': 'POST',
                'path': '/chat',
                'description': 'Send message to chatbot',
                'payload': {'message': 'string', 'session_id': 'string (optional)'}
            },
            'session_history': {
                'method': 'GET',
                'path': '/session/<session_id>/history',
                'description': 'Get conversation history'
            },
            'session_summary': {
                'method': 'GET',
                'path': '/session/<session_id>/summary',
                'description': 'Get session summary'
            },
            'reset_session': {
                'method': 'POST',
                'path': '/session/<session_id>/reset',
                'description': 'Reset a session'
            },
            'kb_search': {
                'method': 'POST',
                'path': '/knowledge-base/search',
                'description': 'Search knowledge base',
                'payload': {'query': 'string'}
            },
            'kb_add_topic': {
                'method': 'POST',
                'path': '/knowledge-base/add-topic',
                'description': 'Add topic to KB'
            },
            'intents': {
                'method': 'GET',
                'path': '/intents',
                'description': 'List all intents'
            },
            'health': {
                'method': 'GET',
                'path': '/health',
                'description': 'Health check'
            },
            'stats': {
                'method': 'GET',
                'path': '/stats',
                'description': 'Get statistics'
            }
        }
    })

if __name__ == '__main__':
    app.run(
        debug=True,
        host='127.0.0.1',
        port=5000
    )
