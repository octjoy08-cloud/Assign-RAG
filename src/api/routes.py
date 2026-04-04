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

    parsed = parse_pdf(file_path)

    all_chunks = []
    metadata = []

    for page in parsed:
        # TEXT
        text_chunks = chunk_text(page["text"])
        for chunk in text_chunks:
            all_chunks.append(chunk)
            metadata.append({"type": "text", "page": page["page"]})

        # IMAGES
        for img in page["images"]:
            desc = describe_image(img)
            all_chunks.append(desc)
            metadata.append({"type": "image", "page": page["page"]})

    embeddings = embed_texts(all_chunks)
    vector_store.add(embeddings, all_chunks, metadata)

    return {
        "message": "Document ingested successfully",
        "chunks": len(all_chunks)
    }


@router.post("/query")
def query(q: str):
    results = retrieve(q, vector_store)
    answer = generate_answer(q, results)

    return {
        "answer": answer,
        "sources": results
    }
