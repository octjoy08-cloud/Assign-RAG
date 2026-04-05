# Retrieve Endpoint - Raw Chunk Retrieval

## Endpoint: POST /retrieve

### Description
Retrieve relevant document chunks without generating an LLM answer. Useful for:
- Previewing source materials
- Building custom response logic
- Reviewing raw retrieval quality
- Reducing token usage for external LLMs

### Request

```bash
curl -X POST "http://localhost:8002/retrieve?q=battery%20temperature&k=5"
```

### Response - Retrieve Result

```json
{
  "query": "battery temperature",
  "results": [
    {
      "content": "Red Battery Icon: Critical low battery condition - vehicle needs immediate charging\nYellow Battery Icon: Battery low - charging recommended soon\nTemperature Warning: Battery operating outside optimal temperature range\nEnergy Cost Display: Real-time efficiency metrics and power consumption",
      "metadata": {
        "type": "table",
        "page": 1,
        "table_index": 1,
        "estimated_rows": 4
      },
      "score": 0.98658287525177,
      "chunk_type": "table"
    },
    {
      "content": "of health (SoH) throughout the battery's lifetime. Dashboard Warning Indicators:\nRed Battery Icon: Critical low battery condition - vehicle needs immediate charging\nYellow Battery Icon: Battery low - charging recommended soon\nTemperature Warning: Battery operating outside optimal temperature range...",
      "metadata": {
        "type": "text",
        "page": 1,
        "text_length": 371,
        "chunk_index": 1
      },
      "score": 1.0412418842315674,
      "chunk_type": "text"
    },
    {
      "content": "Key Functions of BMS:\n- Monitors voltage, current, and temperature of battery cells\n- Prevents overcharging and over-discharging\n- Balances charge distribution across cells\n- Predicts remaining battery capacity and range\n- Initiates emergency shutdown if unsafe conditions occur",
      "metadata": {
        "type": "table",
        "page": 1,
        "table_index": 0,
        "estimated_rows": 6
      },
      "score": 1.1244747638702393,
      "chunk_type": "table"
    }
  ],
  "filter_types": null,
  "total_results": 5
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `query` | string | Original search query |
| `results` | array | Retrieved chunks with metadata |
| `results[].content` | string | Actual text from document |
| `results[].chunk_type` | string | `text`, `table`, or `image` |
| `results[].score` | float | Semantic similarity score |
| `results[].metadata` | object | Type-specific metadata |
| `filter_types` | array | Applied chunk type filters |
| `total_results` | integer | Number of chunks returned |

### Query Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `q` | string | Search query | Required |
| `chunk_types` | string | Filter by type (comma-separated) | null |
| `k` | integer | Number of results to return | 5 |

### Metadata by Chunk Type

#### Text Chunks
```json
{
  "type": "text",
  "page": 1,
  "text_length": 371,
  "chunk_index": 0
}
```

#### Table Chunks
```json
{
  "type": "table",
  "page": 1,
  "table_index": 0,
  "estimated_rows": 6
}
```

#### Image Chunks
```json
{
  "type": "image",
  "page": 2,
  "image_path": "temp_images/image_page_2_001.png"
}
```

### Use Cases

#### Custom Response Generation
```bash
# Get raw chunks for building custom responses
curl -X POST "http://localhost:8002/retrieve?q=charging%20safety&k=10"
```

#### Quality Assurance
```bash
# Verify retrieval quality without LLM processing
curl -X POST "http://localhost:8002/retrieve?q=battery%20specifications"
```

#### Downstream Processing
```bash
# Pass chunks to external LLM or API
CHUNKS=$(curl -s -X POST "http://localhost:8002/retrieve?q=query")
# Process with external service
```

#### Type-Specific Retrieval
```bash
# Get only tables
curl -X POST "http://localhost:8002/retrieve?q=costs&chunk_types=table&k=5"

# Get only images
curl -X POST "http://localhost:8002/retrieve?q=diagram&chunk_types=image&k=3"
```

### Advantages Over /query

| Feature | /retrieve | /query |
|---------|-----------|--------|
| LLM Generation | No | Yes |
| Speed | Faster | Slower |
| Token Usage | Lower | Higher |
| Response Format | Raw chunks | Generated answer |
| Metadata | Full | Limited |
| API Key Required | No* | Yes** |

*Not required for retrieval only
**Only required if OpenAI features are used

### Integration Patterns

**Stream Results**
```python
response = requests.post("http://localhost:8002/retrieve?q=query&k=10")
for result in response.json()["results"]:
    process_chunk(result)
```

**Build Custom RAG**
```python
retrieved = get_retrieve_results("user query")
custom_answer = my_llm(retrieved, user_query)
```

**Hybrid Search**
```python
retrieve_results = get_retrieve()
combined_with_bm25 = bm25_search() + retrieve_results
```
