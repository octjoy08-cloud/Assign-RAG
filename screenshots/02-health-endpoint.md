# Health Endpoint Response

## Endpoint: GET /health

### Description
System health check and statistics showing indexed document count and configuration status.

### Response

```json
{
  "status": "running",
  "configuration": {
    "process_images": true,
    "openai_available": false
  },
  "total_chunks": 6,
  "chunk_types": {
    "text": 4,
    "table": 2
  },
  "vector_dimension": 384
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | System operational status |
| `configuration.process_images` | boolean | Whether vision model is enabled |
| `configuration.openai_available` | boolean | OpenAI API key availability |
| `total_chunks` | integer | Total indexed chunks in vector store |
| `chunk_types` | object | Count of chunks by type (text, table, image) |
| `vector_dimension` | integer | Embedding vector dimension (sentence-transformers) |

### Key Information

- **Document Status**: Shows if documents have been successfully ingested
- **Indexed Chunks**: Current count of processed and embedded content pieces
- **Content Types**: Breakdown of text, table, and vision-based chunks
- **Vector Configuration**: Embedding model dimensions (384 for sentence-transformers)

### Use Case

Monitor system health and confirm successful document ingestion before querying.

```bash
curl -X GET http://localhost:8002/health | jq
```
