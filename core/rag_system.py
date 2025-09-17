from .storage.database import DocumentStorage
from .llm.groq_client import GroqLLM
from .config_loader import config
from typing import Dict, Any, List

class RAGSystem:
    def __init__(self):
        self.storage = DocumentStorage()
        self.llm = GroqLLM()
        self.max_results = config.get('ui.max_search_results', 5)
    
    def query(self, question: str) -> Dict[str, Any]:
        search_results = self.storage.search(question, n_results=self.max_results)
        
        if not search_results:
            return {
                'answer': "I couldn't find any relevant information in the documents to answer your question.",
                'sources': [],
                'query': question
            }
        
        answer = self.llm.generate_answer(question, search_results)
        
        sources = []
        for result in search_results:
            sources.append({
                'source': result['metadata'].get('source', 'Unknown'),
                'content_preview': result['content'][:200] + "...",
                'similarity': result['similarity'],
                'page': result['metadata'].get('page_number')
            })
        
        return {
            'answer': answer,
            'sources': sources,
            'query': question,
            'found_results': len(search_results)
        }
    
    def get_stats(self) -> Dict[str, Any]:
        return {
            'total_documents': self.storage.get_count(),
            'llm_model': self.llm.model,
            'embedding_model': config.get('database.embedding_model'),
            'llm_connected': self.llm.test_connection()
        }
