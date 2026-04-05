# Ingest Endpoint - Document Upload Response

## Endpoint: POST /ingest

### Description
Upload a multimodal PDF document and process it for RAG ingestion. The system automatically:
1. Parses PDF content (text, tables, images)
2. Generates vision descriptions for images
3. Creates embeddings for all chunks
4. Indexes everything in the vector store

### Request

```bash
curl -X POST http://localhost:8002/ingest \
  -F "file=@sample_ev_guide.pdf"
```

### Response

```json
{
  "message": "Document ingested successfully",
  "chunks": 1,
  "chunk_types": {
    "text": 1
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `message` | string | Confirmation of successful ingestion |
| `chunks` | integer | Total processed and indexed chunks |
| `chunk_types` | object | Breakdown: `text`, `table`, `image` |

### Example with Multiple Content Types

For a more complex document with tables and images:

```json
{
  "message": "Document ingested successfully",
  "chunks": 25,
  "chunk_types": {
    "text": 15,
    "table": 7,
    "image": 3
  }
}
```

### Supported Document Features

✓ **Text Processing**
- Automatic segmentation into logical chunks
- Maintains semantic coherence
- Embedded with sentence-transformers

✓ **Table Recognition & Markdown Conversion**
- Structure preservation
- Optimized for semantic search

✓ **Image Analysis**
- Automatic description generation (GPT-4o-mini)
- Searchable via text embeddings
- No need for separate image search

### Processing Parameters

The system automatically handles:
- **Chunk Size**: Optimized for semantic relevance
- **Overlap**: Maintains context at chunk boundaries
- **Vector Encoding**: 384-dimensional embeddings (sentence-transformers)

### Error Handling

If no content is extracted:
```json
{"error": "No content extracted from document"}
```
