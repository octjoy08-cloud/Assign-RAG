from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(
    title="Multimodal RAG System",
    description="A retrieval-augmented generation system for processing PDFs with text, tables, and images",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Multimodal RAG API",
        "endpoints": {
            "health": "GET /health - System status and statistics",
            "ingest": "POST /ingest - Upload and process PDF documents",
            "query": "POST /query - Ask questions with RAG",
            "retrieve": "POST /retrieve - Get relevant chunks without generation",
            "query_by_type": "POST /query_by_type - Query specific chunk types",
            "clear": "DELETE /clear - Clear vector store",
            "stats": "GET /stats - Vector store statistics"
        }
    }
