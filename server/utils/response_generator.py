import random
from typing import Dict, List

class ResponseGenerator:
    """Generates intelligent responses based on intents and context"""
    
    def __init__(self, knowledge_base=None):
        self.kb = knowledge_base
        self.response_templates = {}
        self._initialize_templates()
    
    def _initialize_templates(self):
        """Initialize response templates for different scenarios"""
        self.response_templates = {
            'question': [
                "Based on what I know, {content}",
                "That's a great question. {content}",
                "Here's what I can tell you: {content}",
                "Interesting! {content}",
                "Good question! {content}"
            ],
            'greeting': [
                "Hello! How can I assist you today?",
                "Hi there! What can I help you with?",
                "Greetings! How may I be of service?",
                "Hey! What brings you here?"
            ],
            'acknowledgment': [
                "I understand your point.",
                "That makes sense.",
                "I hear you.",
                "Got it!",
                "I see what you mean."
            ],
            'clarification': [
                "Could you provide more details?",
                "Can you elaborate on that?",
                "I'd like to understand better. Can you tell me more?",
                "Could you clarify that for me?",
                "Help me understand - could you expand on that?"
            ],
            'uncertain': [
                "I'm not entirely sure about that, but based on general knowledge...",
                "That's a complex topic. Here's what I think...",
                "I don't have specific information, but generally...",
                "That's beyond my expertise, but I can suggest..."
            ]
        }
    
    def generate_response(self, intent_data, user_input, context=None):
        """Generate response based on intent, input, and context"""
        intent = intent_data.get('intent', 'default')
        confidence = intent_data.get('confidence', 0)
        entities = intent_data.get('entities', {})
        
        # If we have a predefined response from intent, use it
        if intent_data.get('response'):
            return self._enhance_response(intent_data['response'], context)
        
        # Otherwise, generate contextual response
        if confidence < 0.3:
            # Low confidence - ask for clarification
            return self._select_random(self.response_templates['clarification'])
        
        # Check if it's information request
        if 'tell' in user_input.lower() or 'what' in user_input.lower() or 'how' in user_input.lower():
            # Try to find answer from KB
            if self.kb:
                results = self.kb.search(user_input)
                if results:
                    return self._format_kb_response(results[0])
            
            # Fallback response
            return self._select_random(self.response_templates['clarification'])
        
        # Default response
        return self._select_random(self.response_templates['acknowledgment'])
    
    def _enhance_response(self, response, context):
        """Enhance response with context information"""
        if context is None:
            return response
        
        # Add personalization
        if 'user_name' in context and context['user_name'] != 'User':
            response = response.replace('{name}', context['user_name'])
        
        return response
    
    def _format_kb_response(self, kb_result):
        """Format knowledge base result into response"""
        if kb_result.get('source') == 'q_and_a':
            return kb_result.get('answer', 'I found some information but need to format it better.')
        
        elif kb_result.get('source') == 'knowledge_base':
            content = kb_result.get('content', '')
            template = self._select_random(self.response_templates['question'])
            return template.format(content=content)
        
        return "I found some information about that, but let me explain it better."
    
    def _select_random(self, items):
        """Select random item from list"""
        if isinstance(items, list) and items:
            return random.choice(items)
        return items
    
    def generate_follow_up_question(self, current_topic, entities=None):
        """Generate follow-up question to continue conversation"""
        follow_ups = [
            f"Would you like to know more about {current_topic}?",
            f"Is there anything else about {current_topic} you'd like to discuss?",
            f"Do you have any other questions regarding {current_topic}?",
            f"What else would you like to know about {current_topic}?",
            "Is there anything else I can help you with?"
        ]
        return self._select_random(follow_ups)
    
    def generate_error_message(self, error_type='generic'):
        """Generate appropriate error message"""
        error_messages = {
            'generic': "I encountered an issue processing your request. Could you rephrase that?",
            'connection': "I'm having technical difficulties. Please try again.",
            'timeout': "The request took too long. Can you try again?",
            'invalid_input': "I couldn't understand that. Can you be more specific?",
            'no_info': "I don't have information about that, but I'd like to learn more!"
        }
        return error_messages.get(error_type, error_messages['generic'])
    
    def generate_multi_turn_response(self, turn_number, conversation_history):
        """Generate response considering conversation history"""
        if turn_number == 1:
            return "Hello! How can I assist you?"
        
        # Get last topic from history
        if conversation_history:
            last_exchange = conversation_history[-1]
            return self._select_random(self.response_templates['acknowledgment'])
        
        return "How else can I help?"
    
    def generate_detailed_explanation(self, topic, depth='medium'):
        """Generate detailed explanation with variable depth"""
        explanations = {
            'shallow': "Here's a brief overview: ",
            'medium': "Let me provide a more detailed explanation: ",
            'deep': "Here's a comprehensive breakdown: "
        }
        
        prefix = explanations.get(depth, explanations['medium'])
        
        if self.kb and hasattr(self.kb, 'search'):
            results = self.kb.search(topic)
            if results:
                content = results[0].get('content', '')
                return prefix + content
        
        return prefix + f"I have information about {topic}, but I need more context to explain it best."
