from sentence_transformers import SentenceTransformer
from typing import List, Union
import numpy as np

# Initialize the sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts: Union[str, List[str]]) -> np.ndarray:
    """
    Embed text content using sentence-transformers.

    Args:
        texts: Single text string or list of text strings

    Returns:
        Numpy array of embeddings
    """
    if isinstance(texts, str):
        texts = [texts]

    # Filter out empty strings
    texts = [text for text in texts if text and text.strip()]

    if not texts:
        return np.array([])

    return model.encode(texts)


def embed_chunks(chunks: List[str], chunk_types: List[str]) -> List[List[float]]:
    """
    Embed chunks of different types. Currently uses the same model for all text-based content.

    Args:
        chunks: List of chunk content
        chunk_types: List of chunk types (text, table, image)

    Returns:
        List of embedding vectors
    """
    # For now, all chunk types are treated as text
    # Future enhancement: use different models for different content types
    embeddings = embed_texts(chunks)

    # Convert to list of lists for easier handling
    if len(embeddings.shape) == 1:
        return [embeddings.tolist()]
    else:
        return embeddings.tolist()
