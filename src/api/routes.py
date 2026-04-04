from fastapi import APIRouter, UploadFile, File
import shutil

from src.ingestion.parser import parse_pdf
from src.ingestion.chunker import chunk_text
from src.models.vision import describe_image
from src.ingestion.embedder import embed_texts
from src.retrieval.vector_store import VectorStore
from src.retrieval.retriever import retrieve
from src.models.llm import generate_answer

router = APIRouter()
vector_store = VectorStore()


@router.get("/health")
def health():
    return {
        "status": "running",
        "documents_indexed": len(vector_store.texts)
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

    for chunk in chunks:
        content = chunk["content"]

        # For image chunks, generate description using vision model
        if chunk["type"] == "image" and "image_path" in chunk:
            try:
                content = describe_image(chunk["image_path"])
            except Exception as e:
                content = f"[Image description failed: {str(e)}]"

        # For table chunks, the content is already in markdown format from Docling
        # For text chunks, content is the raw text

        # Skip empty chunks
        if not content.strip():
            continue

        all_chunks.append(content)
        metadata.append({
            "type": chunk["type"],
            "page": chunk["page"],
            **chunk["metadata"]
        })

    if not all_chunks:
        return {"error": "No content extracted from document"}

    embeddings = embed_texts(all_chunks)
    vector_store.add(embeddings, all_chunks, metadata)

    return {
        "message": "Document ingested successfully",
        "chunks": len(all_chunks),
        "chunk_types": {
            "text": len([m for m in metadata if m["type"] == "text"]),
            "table": len([m for m in metadata if m["type"] == "table"]),
            "image": len([m for m in metadata if m["type"] == "image"])
        }
    }


@router.post("/query")
def query(q: str):
    results = retrieve(q, vector_store)
    answer = generate_answer(q, results)

    return {
        "answer": answer,
        "sources": results
    }
