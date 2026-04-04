import faiss
import numpy as np
from typing import List, Dict, Any, Optional


class VectorStore:
    """
    Enhanced vector store supporting multiple chunk types with FAISS.
    Handles text, table, and image chunks with appropriate embeddings.
    """

    def __init__(self, dim: int = 384):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.chunks: List[str] = []
        self.metadata: List[Dict[str, Any]] = []
        self.chunk_types: List[str] = []

    def add(self, embeddings: List[List[float]], chunks: List[str], metadata: List[Dict[str, Any]]):
        """
        Add embeddings and their corresponding chunks to the vector store.

        Args:
            embeddings: List of embedding vectors
            chunks: List of chunk content (text, table markdown, or image descriptions)
            metadata: List of metadata dictionaries for each chunk
        """
        if len(embeddings) != len(chunks) or len(chunks) != len(metadata):
            raise ValueError("embeddings, chunks, and metadata must have the same length")

        # Convert to numpy array
        embeddings_array = np.array(embeddings, dtype="float32")

        # Add to FAISS index
        self.index.add(embeddings_array)

        # Store chunks and metadata
        self.chunks.extend(chunks)
        self.metadata.extend(metadata)
        self.chunk_types.extend([meta.get("type", "unknown") for meta in metadata])

    def search(self, query_embedding: List[float], k: int = 5, filter_types: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Search for similar chunks in the vector store.

        Args:
            query_embedding: Query embedding vector
            k: Number of results to return
            filter_types: Optional list of chunk types to filter by (e.g., ["text", "table"])

        Returns:
            List of results with chunk content, metadata, and similarity scores
        """
        query = np.array([query_embedding], dtype="float32")
        distances, indices = self.index.search(query, k)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue

            # Apply type filtering if specified
            if filter_types and self.chunk_types[idx] not in filter_types:
                continue

            results.append({
                "content": self.chunks[idx],
                "metadata": self.metadata[idx],
                "score": float(dist),
                "chunk_type": self.chunk_types[idx]
            })

        return results

    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector store contents.

        Returns:
            Dictionary with statistics about chunk types and counts
        """
        total_chunks = len(self.chunks)
        type_counts = {}

        for chunk_type in self.chunk_types:
            type_counts[chunk_type] = type_counts.get(chunk_type, 0) + 1

        return {
            "total_chunks": total_chunks,
            "chunk_types": type_counts,
            "vector_dimension": self.dim
        }

    def clear(self):
        """
        Clear all data from the vector store.
        """
        self.index = faiss.IndexFlatL2(self.dim)
        self.chunks = []
        self.metadata = []
        self.chunk_types = []
