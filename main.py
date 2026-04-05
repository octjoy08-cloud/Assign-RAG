from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.api.routes import router
import os

app = FastAPI(
    title="Multimodal RAG System",
    description="A retrieval-augmented generation system for processing PDFs with text, tables, and images",
    version="1.0.0"
)

app.include_router(router)

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=FileResponse)
def root():
    """Serve the web UI for the RAG system."""
    if os.path.exists("static/index.html"):
        return "static/index.html"
    else:
        # Fallback API response
        return {
            "message": "Multimodal RAG API",
            "endpoints": {
                "health": "GET /health - System status and statistics",
                "ingest": "POST /ingest - Upload and process PDF documents",
                "query": "POST /query - Ask questions with RAG",
                "retrieve": "POST /retrieve - Get relevant chunks without generation",
                "query_by_type": "POST /query_by_type - Query specific chunk types",
                "clear": "DELETE /clear - Clear vector store",
                "stats": "GET /stats - Vector store statistics",
                "ui": "Open http://localhost:8001/ in your browser for the web interface"
            }
        }
