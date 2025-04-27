import faiss
import numpy as np
import os
import pickle

class RAGRetrieval:
    def __init__(self, dimension=128):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.vectors = []
        self.documents = []

    def add_document(self, vector, document):
        self.vectors.append(vector)
        self.documents.append(document)
        self.index.add(np.array([vector]).astype('float32'))

    def search(self, query_vector, top_k=5):
        D, I = self.index.search(np.array([query_vector]).astype('float32'), top_k)
        results = []
        for i in I[0]:
            if i < len(self.documents):
                results.append(self.documents[i])
        return results

    def save(self, path):
        """Save the RAG retrieval system state."""
        os.makedirs(path, exist_ok=True)
        
        # Save index
        faiss.write_index(self.index, os.path.join(path, "faiss_index"))
        
        # Save vectors and documents
        with open(os.path.join(path, "metadata.pkl"), "wb") as f:
            pickle.dump({
                "dimension": self.dimension,
                "vectors": self.vectors,
                "documents": self.documents
            }, f)

    @classmethod
    def load(cls, path):
        """Load a saved RAG retrieval system."""
        # Load metadata
        with open(os.path.join(path, "metadata.pkl"), "rb") as f:
            metadata = pickle.load(f)
        
        # Create instance
        instance = cls(dimension=metadata["dimension"])
        instance.vectors = metadata["vectors"]
        instance.documents = metadata["documents"]
        
        # Load index
        instance.index = faiss.read_index(os.path.join(path, "faiss_index"))
        
        return instance

if __name__ == "__main__":
    rag = RAGRetrieval()
    # Example usage
    vec = np.random.rand(128).astype('float32')
    rag.add_document(vec, "Example document")
    results = rag.search(vec)
    print("Search results:", results)
