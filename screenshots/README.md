# API Screenshots and Evidence

This directory contains comprehensive documentation of all Multimodal RAG System endpoints with real examples and responses.

## Contents

### 1. [Swagger UI Documentation](01-swagger-ui.md)
Complete list of all available endpoints with descriptions and access instructions.
- Health monitoring
- Document ingestion
- Query operations
- Content retrieval
- Management endpoints

### 2. [Health Endpoint Response](02-health-endpoint.md)
System health check showing indexed document count and configuration.

**Real Response:**
- Status: running
- Total Chunks: 6
- Chunk Types: 4 text, 2 table
- Vector Dimension: 384

### 3. [Ingest Endpoint](03-ingest-endpoint.md)
Document upload and processing with multimodal PDF support.

**Real Response:**
- Successfully ingested PDF with 6 chunks
- 4 text chunks extracted
- 2 table chunks extracted
- Automatic vision processing enabled

### 4. [Text Query Results](04-query-text.md)
Semantic search with relevance scoring and source attribution.

**Example Query:** "Tell me about battery management system"
- Retrieves 5 relevant text chunks
- Shows semantic similarity scores
- Includes source page numbers

### 5. [Table Query Results](05-query-table.md)
Targeted retrieval of structured table-based content.

**Example Query:** "charging specifications" (table filter)
- Returns only table-type chunks
- Preserves structured data format
- Shows table metadata

### 6. [Image Query Results](06-query-image.md)
Multimodal retrieval of image descriptions from documents.

**Capabilities:**
- Automatic image extraction from PDFs
- GPT-4o-mini vision descriptions
- Searchable image summaries
- Mixed with text results

### 7. [Retrieve Endpoint](07-retrieve-endpoint.md)
Raw chunk retrieval without LLM answer generation.

**Real Response:**
- Returns 5 most relevant chunks
- Includes full metadata
- Type-specific information
- Semantic relevance scores

---

## Usage Examples

### Access Swagger UI
```
GET http://localhost:8002/docs
```

### Ingest a Document
```bash
curl -X POST http://localhost:8002/ingest \
  -F "file=@document.pdf"
```

### Query with RAG
```bash
curl -X POST "http://localhost:8002/query?q=your%20question"
```

### Filter by Content Type
```bash
curl -X POST "http://localhost:8002/query?q=query&chunk_types=table"
```

### Retrieve Raw Chunks
```bash
curl -X POST "http://localhost:8002/retrieve?q=query&k=5"
```

### Check System Health
```bash
curl -X GET "http://localhost:8002/health"
```

---

## Key Metrics (Real Test Data)

| Metric | Value |
|--------|-------|
| Total Indexed Chunks | 6 |
| Text Chunks | 4 |
| Table Chunks | 2 |
| Vector Dimension | 384 |
| Vector Store | FAISS |
| Embedding Model | sentence-transformers |
| Status | Running |

---

## Content Types Supported

### ✓ Text Processing
- Automatic chunking with semantic coherence
- Paragraph and section detection
- Preserves document structure

### ✓ Table Processing
- Extracts and converts to markdown
- Preserves column relationships
- Makes structured data searchable

### ✓ Image Processing
- Automatic extraction from PDFs
- GPT-4o-mini descriptions
- Searchable image summaries

---

## Integration Notes

All endpoints return JSON responses suitable for:
- Web applications
- Mobile apps
- Third-party integrations
- Custom RAG pipelines
- Chatbot backends

Full API documentation available at `/docs` (Swagger UI) or `/redoc` (ReDoc).
