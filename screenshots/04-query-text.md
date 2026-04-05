# Query Endpoint - Text-Based Retrieval

## Endpoint: POST /query

### Description
Query the vector store with semantic search and generate RAG-based answers with source attribution. The system:
1. Embeds the user's natural language query
2. Finds top-k semantically similar chunks
3. Generates contextual answer with the LLM
4. Provides source references with content snippets

### Request

```bash
curl -X POST "http://localhost:8002/query?q=What%20charging%20methods%20are%20available%20for%20electric%20vehicles?"
```

### Response - Text Query Result

```json
{
  "answer": "Multiple charging methods are available for electric vehicles.",
  "sources": [
    {
      "content": "EV Charging Guide\nCharging Methods:\nLevel 1: 120V - 8-12 hours\nLevel 2: 240V - 4-6 hours\nDC Fast: 480V - 20-30 min\nCharging Specifications:\n",
      "type": "text",
      "page": 0,
      "score": 0.7963719367980957
    }
  ],
  "total_sources": 1,
  "query": "What charging methods are available for electric vehicles?",
  "filter_types": null
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `answer` | string | Generated answer based on sources |
| `sources` | array | Retrieved chunks with similarity scores |
| `sources[].content` | string | Actual text from the document |
| `sources[].type` | string | `text`, `table`, or `image` |
| `sources[].page` | integer | Source page number |
| `sources[].score` | float | Similarity score (higher = more relevant, max 1.0) |
| `total_sources` | integer | Number of relevant sources found |
| `query` | string | Original query string |
| `filter_types` | array | Applied content type filters (if any) |

### Key Features

### Semantic Similarity Scoring

The `score` field indicates relevance:
- **> 0.80**: Highly relevant
- **0.70-0.80**: Very relevant  
- **0.60-0.70**: Relevant
- **< 0.60**: Marginally relevant

### Query Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `q` | string | Natural language query | Required |
| `chunk_types` | string | Filter by type (comma-separated) | null |
| `include_sources` | boolean | Include detailed sources | true |

### Example Queries

#### Question about specific concepts:
```
"What does the battery management system do?"
"How long does Level 2 charging take?"
"What are the safety precautions?"
```

#### Multi-concept queries:
```
"Compare Level 1 and Level 2 charging times and costs"
"What equipment is needed for DC fast charging?"
```

### With Content Type Filtering

```bash
# Query only text chunks
curl -X POST "http://localhost:8002/query?q=charging%20definition&chunk_types=text"

# Query only table content
curl -X POST "http://localhost:8002/query?q=charging%20times&chunk_types=table"

# Query only image summaries
curl -X POST "http://localhost:8002/query?q=charging%20setup&chunk_types=image"
```
