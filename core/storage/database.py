import hashlib
from typing import List, Dict, Any
import chromadb
from chromadb.utils import embedding_functions
from ..config_loader import config

class Document:
    def __init__(self, page_content: str, metadata: dict):
        self.page_content = page_content
        self.metadata = metadata

class DocumentStorage:
    def __init__(self, db_path: str = None):
        db_path = db_path or str(config.db_path)
        config.data_dir.mkdir(exist_ok=True)
        
        self.embedder = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=config.get('database.embedding_model', 'BAAI/bge-base-en-v1.5')
        )
        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(
            name=config.get('database.collection_name', 'documents'), 
            embedding_function=self.embedder
        )
    
    def _hash_text(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]
    
    def store_documents(self, documents: List[Document]) -> None:
        if not documents:
            return
        
        ids = []
        texts = []
        metadatas = []
        
        for i, doc in enumerate(documents):
            doc_id = f"doc_{i}_{self._hash_text(doc.page_content)}"
            ids.append(doc_id)
            texts.append(doc.page_content)
            metadatas.append(doc.metadata)
        
        self.collection.upsert(
            ids=ids,
            documents=texts,
            metadatas=metadatas
        )
        
        print(f"Stored {len(documents)} documents")
    
    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                include=["documents", "metadatas", "distances"]
            )
            
            documents = results.get("documents", [[]])[0]
            metadatas = results.get("metadatas", [[]])[0]
            distances = results.get("distances", [[]])[0]
            
            search_results = []
            for doc, meta, dist in zip(documents, metadatas, distances):
                search_results.append({
                    "content": doc,
                    "metadata": meta,
                    "similarity": 1 - dist if dist else 0
                })
            
            return search_results
            
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def get_count(self) -> int:
        try:
            return self.collection.count()
        except:
            return 0
