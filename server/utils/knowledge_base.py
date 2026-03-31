import json
from datetime import datetime

class KnowledgeBase:
    """Knowledge Base system for storing and retrieving information"""
    
    def __init__(self):
        self.kb = {}
        self.facts = []
        self.q_and_a = []
        self._load_default_knowledge()
    
    def _load_default_knowledge(self):
        """Load default knowledge base"""
        self.kb = {
            'python': {
                'description': 'Python is a high-level, interpreted programming language known for its simplicity.',
                'keywords': ['programming', 'coding', 'language'],
                'related': ['java', 'javascript', 'c++']
            },
            'machine learning': {
                'description': 'Machine Learning is a subset of artificial intelligence that enables computers to learn from data.',
                'keywords': ['ai', 'data', 'learning', 'algorithms'],
                'related': ['deep learning', 'neural networks', 'nlp']
            },
            'web development': {
                'description': 'Web development involves creating and maintaining websites using HTML, CSS, JavaScript, and backend languages.',
                'keywords': ['html', 'css', 'javascript', 'frontend', 'backend'],
                'related': ['django', 'flask', 'react']
            },
            'database': {
                'description': 'A database is an organized collection of structured data stored electronically in a computer system.',
                'keywords': ['data', 'storage', 'sql', 'nosql'],
                'related': ['sql', 'mongodb', 'postgresql']
            },
            'api': {
                'description': 'API (Application Programming Interface) allows different software applications to communicate with each other.',
                'keywords': ['interface', 'communication', 'rest', 'integration'],
                'related': ['rest', 'graphql', 'http']
            },
            'flask': {
                'description': 'Flask is a lightweight Python web framework for building web applications.',
                'keywords': ['python', 'web', 'framework', 'backend'],
                'related': ['django', 'bottle']
            },
            'git': {
                'description': 'Git is a version control system that helps track changes in source code during software development.',
                'keywords': ['version control', 'code', 'repository', 'github'],
                'related': ['github', 'gitlab', 'version control']
            },
            'ai': {
                'description': 'Artificial Intelligence (AI) is the simulation of human intelligence by computers.',
                'keywords': ['intelligence', 'automation', 'learning', 'algorithms'],
                'related': ['machine learning', 'deep learning', 'nlp']
            }
        }
        
        # Add Q&A pairs
        self.q_and_a = [
            {
                'question': 'What is Python?',
                'answer': 'Python is a high-level, interpreted programming language known for its simplicity and readability.'
            },
            {
                'question': 'How do I learn Python?',
                'answer': 'You can learn Python through online courses, books, practice coding, and building projects.'
            },
            {
                'question': 'What is the difference between frontend and backend?',
                'answer': 'Frontend is the user-facing part of a web application, while backend handles server-side logic and data.'
            },
            {
                'question': 'What is a REST API?',
                'answer': 'REST API is an architectural style for building web APIs using HTTP methods (GET, POST, PUT, DELETE).'
            }
        ]
    
    def search(self, query):
        """Search knowledge base for relevant information"""
        query_lower = query.lower()
        results = []
        
        # Search in KB
        for topic, info in self.kb.items():
            if query_lower in topic.lower():
                results.append({
                    'source': 'knowledge_base',
                    'topic': topic,
                    'content': info['description'],
                    'relevance': 'high'
                })
            else:
                # Check keywords
                for keyword in info.get('keywords', []):
                    if query_lower in keyword.lower() or keyword.lower() in query_lower:
                        results.append({
                            'source': 'knowledge_base',
                            'topic': topic,
                            'content': info['description'],
                            'relevance': 'medium'
                        })
                        break
        
        # Search Q&A
        for qa in self.q_and_a:
            if query_lower in qa['question'].lower():
                results.append({
                    'source': 'q_and_a',
                    'question': qa['question'],
                    'answer': qa['answer'],
                    'relevance': 'high'
                })
            elif query_lower in qa['answer'].lower():
                results.append({
                    'source': 'q_and_a',
                    'question': qa['question'],
                    'answer': qa['answer'],
                    'relevance': 'medium'
                })
        
        return results
    
    def add_fact(self, fact, category='general'):
        """Add a fact to the knowledge base"""
        self.facts.append({
            'fact': fact,
            'category': category,
            'timestamp': datetime.now().isoformat()
        })
    
    def add_qa(self, question, answer):
        """Add Q&A pair to knowledge base"""
        self.q_and_a.append({
            'question': question,
            'answer': answer
        })
    
    def add_topic(self, topic, description, keywords=None, related=None):
        """Add a new topic to knowledge base"""
        self.kb[topic.lower()] = {
            'description': description,
            'keywords': keywords or [],
            'related': related or []
        }
    
    def get_related_topics(self, topic):
        """Get topics related to a given topic"""
        topic_lower = topic.lower()
        if topic_lower in self.kb:
            return self.kb[topic_lower].get('related', [])
        return []
    
    def get_fact_by_category(self, category):
        """Get facts by category"""
        return [f for f in self.facts if f['category'] == category]
    
    def export_kb(self):
        """Export knowledge base as JSON"""
        return {
            'kb': self.kb,
            'facts': self.facts,
            'q_and_a': self.q_and_a,
            'export_date': datetime.now().isoformat()
        }
    
    def import_kb(self, data):
        """Import knowledge base from JSON"""
        if 'kb' in data:
            self.kb.update(data['kb'])
        if 'facts' in data:
            self.facts.extend(data['facts'])
        if 'q_and_a' in data:
            self.q_and_a.extend(data['q_and_a'])
