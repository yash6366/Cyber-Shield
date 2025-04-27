import faiss
import numpy as np

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

if __name__ == "__main__":
    rag = RAGRetrieval()
    # Example usage
    vec = np.random.rand(128).astype('float32')
    rag.add_document(vec, "Example document")
    results = rag.search(vec)
    print("Search results:", results)
