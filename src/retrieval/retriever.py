from src.ingestion.embedder import embed_texts


def retrieve(query, vector_store, k=5):
    query_embedding = embed_texts([query])
    results = vector_store.search(query_embedding, k)
    return results
