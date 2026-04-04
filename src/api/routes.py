from fastapi import APIRouter, UploadFile, File
import shutil
import os

from src.ingestion.parser import parse_pdf
from src.ingestion.chunker import chunk_text
from src.models.vision import describe_image
from src.ingestion.embedder import embed_texts, embed_chunks
from src.retrieval.vector_store import VectorStore
from src.retrieval.retriever import retrieve
from src.models.llm import generate_answer

router = APIRouter()
vector_store = VectorStore()

# Configuration
PROCESS_IMAGES = os.getenv("PROCESS_IMAGES", "true").lower() == "true"


@router.get("/health")
def health():
    stats = vector_store.get_stats()
    return {
        "status": "running",
        "configuration": {
            "process_images": PROCESS_IMAGES,
            "openai_available": bool(os.getenv("OPENAI_API_KEY"))
        },
        **stats
    }


@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    file_path = f"temp_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Parse PDF with Docling - returns structured chunks
    chunks = parse_pdf(file_path)

    all_chunks = []
    metadata = []
    chunk_types = []

    for chunk in chunks:
        content = chunk["content"]

        # For image chunks, generate description using vision model
        if chunk["type"] == "image" and "image_path" in chunk:
            if PROCESS_IMAGES:
                try:
                    print(f"Processing image: {chunk['image_path']}")
                    content = describe_image(chunk["image_path"])
                    print(f"Generated description for image on page {chunk['page']}")
                except Exception as e:
                    # Fallback description when vision model fails
                    content = f"[Image on page {chunk['page']}: {os.path.basename(chunk['image_path'])}. Unable to generate description due to: {str(e)}]"
                    print(f"Failed to describe image {chunk['image_path']}: {e}")
            else:
                # Skip image processing
                content = f"[Image processing disabled. Image: {os.path.basename(chunk['image_path'])} on page {chunk['page']}]"
                print(f"Skipping image processing for {chunk['image_path']} (PROCESS_IMAGES=false)")

        # For table chunks, the content is already in markdown format
        # For text chunks, content is the raw text

        # Skip empty chunks (but allow image chunks with fallback descriptions)
        if not content.strip() and chunk["type"] != "image":
            continue

        all_chunks.append(content)
        metadata.append({
            "type": chunk["type"],
            "page": chunk["page"],
            **chunk["metadata"]
        })
        chunk_types.append(chunk["type"])

    if not all_chunks:
        return {"error": "No content extracted from document"}

    # Embed all chunks using the enhanced embedder
    embeddings = embed_chunks(all_chunks, chunk_types)

    # Add to vector store
    vector_store.add(embeddings, all_chunks, metadata)

    return {
        "message": "Document ingested successfully",
        "chunks": len(all_chunks),
        "chunk_types": {
            chunk_type: chunk_types.count(chunk_type)
            for chunk_type in set(chunk_types)
        }
    }


@router.post("/query")
def query(q: str, chunk_types: str = None):
    """
    Query the vector store for relevant chunks.

    Args:
        q: Query string
        chunk_types: Optional comma-separated list of chunk types to filter by (e.g., "text,table")
    """
    # Parse chunk types filter
    filter_types = None
    if chunk_types:
        filter_types = [t.strip() for t in chunk_types.split(",") if t.strip()]

    # Embed the query
    query_embedding = embed_texts([q])[0]

    # Search the vector store
    results = vector_store.search(query_embedding, k=5, filter_types=filter_types)

    # Generate answer using LLM
    answer = generate_answer(q, results)

    return {
        "answer": answer,
        "sources": results,
        "query": q,
        "filter_types": filter_types
    }


@router.delete("/clear")
def clear_vector_store():
    """
    Clear all data from the vector store.
    """
    vector_store.clear()
    return {"message": "Vector store cleared successfully"}


@router.get("/stats")
def get_stats():
    """
    Get detailed statistics about the vector store.
    """
    return vector_store.get_stats()
