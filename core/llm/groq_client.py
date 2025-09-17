from groq import Groq
from typing import List, Dict, Any
from ..config_loader import config

class GroqLLM:
    def __init__(self):
        self.client = Groq(api_key=config.groq_api_key)
        self.model = config.get('llm.model', 'llama3-8b-8192')
        self.max_tokens = config.get('llm.max_tokens', 1000)
        self.temperature = config.get('llm.temperature', 0.1)
    
    def generate_answer(self, query: str, context_chunks: List[Dict[str, Any]]) -> str:
        if not context_chunks:
            return "I couldn't find relevant information to answer your question."
        
        context_text = "\n\n".join([
            f"Source: {chunk['metadata'].get('source', 'Unknown')}\nContent: {chunk['content']}"
            for chunk in context_chunks
        ])
        
        prompt = f"""Based on the following context from documents, answer the user's question accurately and concisely.

Context:
{context_text}

Question: {query}

Instructions:
- Answer based only on the provided context
- Be precise and factual
- If the context doesn't contain enough information, say so
- Cite the source document when relevant

Answer:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def test_connection(self) -> bool:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return True
        except Exception:
            return False
