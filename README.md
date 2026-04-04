# Multimodal RAG System

A retrieval-augmented generation (RAG) system for processing PDF documents containing text, tables, and images.

## Features

- **Multimodal Document Processing**: Extracts and processes text, tables, and images from PDFs
- **Vision Language Model Integration**: Uses GPT-4o-mini to generate descriptions of images
- **Advanced Chunking**: Separates content by type (text, table, image) for better retrieval
- **Vector Storage**: Uses FAISS for efficient similarity search
- **Custom RAG Pipeline**: Enhanced prompt templates for grounded, accurate answers
- **RESTful API**: FastAPI-based endpoints for ingestion and querying

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in `.env`:
```bash
OPENAI_API_KEY=your_api_key_here
PROCESS_IMAGES=true  # Set to false to skip image processing
```

3. Start the server:
```bash
python -m uvicorn main:app --reload
```

## API Endpoints

### Document Ingestion
```bash
POST /ingest
# Upload PDF files for processing
curl -X POST "http://localhost:8000/ingest" -F "file=@document.pdf"
```

### Querying
```bash
POST /query
# Ask questions with RAG
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"q": "What are the fuel efficiency standards?"}'
```

### Advanced Querying
```bash
POST /query_by_type
# Query specific content types
curl -X POST "http://localhost:8000/query_by_type" \
  -H "Content-Type: application/json" \
  -d '{"q": "What tables show emission data?", "chunk_type": "table"}'

POST /retrieve
# Get raw retrieval results
curl -X POST "http://localhost:8000/retrieve" \
  -H "Content-Type: application/json" \
  -d '{"q": "fuel efficiency", "k": 3}'
```

### Management
```bash
GET /health      # System status
GET /stats       # Vector store statistics
DELETE /clear    # Clear all data
```

## Architecture

```
PDF Document
├── Parser (PyMuPDF/Docling)
│   ├── Text Chunks
│   ├── Table Chunks
│   └── Image Chunks → Vision Model → Descriptions
│
├── Embedder (Sentence Transformers)
│   └── Vector Embeddings
│
├── Vector Store (FAISS)
│   └── Similarity Search
│
└── LLM (GPT-4o-mini)
    └── RAG Generation
```

## Chunk Types

- **Text**: Regular document text, chunked by sentences
- **Table**: Tabular data extracted as structured content
- **Image**: Visual content processed through VLM for descriptions

## Configuration

- `PROCESS_IMAGES`: Enable/disable image processing (default: true)
- `OPENAI_API_KEY`: Required for LLM and vision processing

## RAG Prompt Template

The system uses a custom prompt template that:
- Provides clear instructions for grounded answers
- Handles different content types appropriately
- Includes source attribution
- Maintains technical accuracy for engineering content</content>
<parameter name="filePath">/workspaces/Assign-RAG/README.md