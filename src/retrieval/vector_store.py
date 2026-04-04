import faiss
import numpy as np


class VectorStore:
    def __init__(self, dim=384):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []
        self.metadata = []

    def add(self, embeddings, texts, metadata):
        self.index.add(np.array(embeddings, dtype="float32"))
        self.texts.extend(texts)
        self.metadata.extend(metadata)

    def search(self, query_embedding, k=5):
        query = np.array(query_embedding, dtype="float32")
        distances, indices = self.index.search(query, k)

        results = []
        for i in indices[0]:
            if i == -1:
                continue
            results.append({
                "text": self.texts[i],
                "metadata": self.metadata[i]
            })

        return results
