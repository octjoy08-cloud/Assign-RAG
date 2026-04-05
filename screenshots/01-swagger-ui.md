# Swagger UI - OpenAPI Documentation

The Multimodal RAG System provides complete OpenAPI (Swagger) documentation available at `/docs`

## Available Endpoints

### Health & Status
- **GET `/health`** - System health check and statistics
  - Returns indexed document count, vector dimension, and configuration

### Document Ingestion  
- **POST `/ingest`** - Upload and process multimodal PDF documents
  - Accepts PDF files with text, tables, and images
  - Performs chunking optimization and embedding
  - Returns chunk counts by type

### Query Operations
- **POST `/query`** - Query with RAG (embed query, retrieve sources, generate answer)
  - Parameters: `q` (query string), `chunk_types` (optional filter), `include_sources` (boolean)
  - Returns: answer, sources with context, and metadata

- **POST `/retrieve`** - Get relevant chunks without LLM generation
  - Retrieves top-k similar chunks based on embedding similarity
  - Useful for reviewing source material

- **POST `/query_by_type`** - Query specific content types
  - Filter by: `text`, `table`, `image`
  - Perform targeted searches on particular chunk types

- **POST `/stats`** - Get vector store statistics
  - Total chunks indexed
  - Breakdown by content type
  - Vector dimensions and metadata

### Management
- **DELETE `/clear`** - Clear all indexed vectors
  - Resets system for new documents

## Interactive API Testing

Access the full interactive Swagger UI at:
```
http://localhost:8002/docs
```

This provides:
- Request/response schemas
- Try-it-out functionality
- Auto-generated request examples
- Complete parameter documentation
