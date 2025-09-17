import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.rag_system import RAGSystem

def test_rag_system():
    try:
        rag = RAGSystem()
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure GROQ_API_KEY is set in .env file")
        return
    
    test_questions = [
        "What is Rinvoq used for?",
        "What are the side effects?",
        "Who should not take this medication?"
    ]
    
    stats = rag.get_stats()
    print("Document Q&A RAG Bot - Test Results")
    print(f"Database contains {stats['total_documents']} document chunks")
    print(f"LLM Model: {stats['llm_model']}")
    print(f"LLM Connected: {stats['llm_connected']}")
    print("=" * 80)
    
    for question in test_questions:
        print(f"\nQuestion: {question}")
        print("-" * 60)
        
        response = rag.query(question)
        
        print(f"Answer: {response['answer']}")
        print(f"\nSources ({response['found_results']} found):")
        
        for i, source in enumerate(response['sources'][:2], 1):
            print(f"{i}. {source['source']} (Similarity: {source['similarity']:.3f})")
            print(f"   {source['content_preview']}")
        
        print("=" * 80)

if __name__ == "__main__":
    test_rag_system()
