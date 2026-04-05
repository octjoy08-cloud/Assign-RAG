# Query Endpoint - Table-Based Retrieval

## Endpoint: POST /query with chunk_types filter

### Description
Query specifically for table-based content. This is useful when looking for structured data like specifications, comparisons, and formatted information.

### Request

```bash
curl -X POST "http://localhost:8002/query?q=charging%20specifications&chunk_types=table"
```

### Response - Table Query Result

```json
{
  "answer": "Table-based information retrieved successfully",
  "sources": [
    {
      "content": "Red Battery Icon: Critical low battery condition - vehicle needs immediate charging\nYellow Battery Icon: Battery low - charging recommended soon\nTemperature Warning: Battery operating outside optimal temperature range\nEnergy Cost Display: Real-time efficiency metrics and power consumption",
      "type": "table",
      "page": 1,
      "score": 1.2910566329956055
    },
    {
      "content": "Key Functions of BMS:\n- Monitors voltage, current, and temperature of battery cells\n- Prevents overcharging and over-discharging\n- Balances charge distribution across cells\n- Predicts remaining battery capacity and range\n- Initiates emergency shutdown if unsafe conditions occur",
      "type": "table",
      "page": 1,
      "score": 1.4414787292480469
    }
  ],
  "total_sources": 2,
  "query": "charging specifications",
  "filter_types": ["table"]
}
```

### Key Features

#### Type-Specific Filtering

The `chunk_types` parameter enables targeted searches:

```bash
# Query only tables
chunk_types=table

# Query multiple types
chunk_types=text,table

# Query only images
chunk_types=image
```

#### Table Decomposition

Tables are automatically converted to optimized formats:
- Markdown tables are preserved
- Structured data is extracted from PDFs
- Column headers and relationships are maintained
- Makes table data searchable alongside text

### Use Cases

**Specification Lookups**
```
"What are the charging time specifications?"
"Compare Level 1 and Level 2 charging"
"Show me the battery management features"
```

**Structured Data Queries**
```
"What are the warning indicator codes?"
"List charging costs by method"
"Give me the voltage specifications"
```

### Response Notes

Response includes:
- **content**: The actual table or structured data
- **type**: Always "table" for table-filtered queries
- **page**: Source page number in document
- **score**: Semantic relevance (higher = more relevant)

Tables with higher scores are more relevant to your query based on semantic similarity.
