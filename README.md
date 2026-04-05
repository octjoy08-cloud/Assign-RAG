# Multimodal RAG System

A comprehensive retrieval-augmented generation (RAG) system for processing PDF documents containing text, tables, and images. Features both a REST API and an interactive web interface for easy querying.

## ✨ Features

- **Multimodal Document Processing**: Extracts and processes text, tables, and images from PDFs
- **Vision Language Model Integration**: Uses GPT-4o-mini to generate descriptions of images
- **Advanced Chunking**: Separates content by type (text, table, image) for better retrieval
- **Vector Storage**: Uses FAISS for efficient similarity search
- **Custom RAG Pipeline**: Enhanced prompt templates for grounded, accurate answers
- **Interactive Web Interface**: User-friendly browser interface for querying
- **RESTful API**: Complete FastAPI-based endpoints for ingestion and querying
- **Content Type Filtering**: Query specific content types (text, tables, images)
- **Real-time Statistics**: Monitor vector store and processing status

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

### 3. Start the Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8002
```

### 4. Access the Web Interface
**Open your browser and go to**: http://localhost:8002/

## 📖 Usage

### Web Interface (Recommended)
1. **Upload Documents**: Click "Choose File" and select a PDF
2. **Process**: Click "Upload & Process" to extract chunks
3. **Query**: Type questions in the query box
4. **Choose Mode**:
   - **RAG Query**: Get AI-generated answers with sources
   - **Retrieve Chunks**: Get raw relevant document chunks

### API Usage

#### Document Ingestion
```bash
# Upload and process a PDF
curl -X POST "http://localhost:8002/ingest" -F "file=@document.pdf"
```

#### Query with RAG
```bash
# Ask questions with AI-generated answers
curl -X POST "http://localhost:8002/query?q=What are the benefits of electric vehicles?"
```

#### Advanced Querying
```bash
# Query specific content types
curl -X POST "http://localhost:8002/query_by_type" \
  -H "Content-Type: application/json" \
  -d '{"q": "What tables show cost data?", "chunk_type": "table"}'

# Retrieve raw chunks without generation
curl -X POST "http://localhost:8002/retrieve?q=charging stations&k=5"
```

#### System Management
```bash
# Get system health and status
curl http://localhost:8002/health

# Get vector store statistics
curl http://localhost:8002/stats

# Clear all data
curl -X DELETE http://localhost:8002/clear
```

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web interface (HTML) |
| `GET` | `/health` | System status and configuration |
| `POST` | `/ingest` | Upload and process PDF documents |
| `POST` | `/query` | Ask questions with RAG generation |
| `POST` | `/retrieve` | Get relevant chunks without generation |
| `POST` | `/query_by_type` | Query specific content types |
| `GET` | `/stats` | Vector store statistics |
| `DELETE` | `/clear` | Clear all data from vector store |

### Query Parameters

#### `/query` Endpoint
- `q` (required): Question to ask
- `chunk_types` (optional): Filter by content type (`text`, `table`, `image`)
- `include_sources` (optional): Include source attribution (`true`/`false`, default: `true`)

#### `/retrieve` Endpoint
- `q` (required): Search query
- `chunk_types` (optional): Filter by content type
- `k` (optional): Number of results to return (default: 5)

#### `/query_by_type` Endpoint
- `q` (required): Question to ask
- `chunk_type` (required): Content type to filter by (`text`, `table`, `image`)

## 🏗️ Architecture

```
PDF Document
├── Parser (PyMuPDF/Docling)
│   ├── Text Chunks → Sentence-based chunking
│   ├── Table Chunks → Structured table extraction
│   └── Image Chunks → Vision Model (GPT-4o-mini) → Descriptions
│
├── Embedder (Sentence Transformers - all-MiniLM-L6-v2)
│   └── Vector Embeddings (384 dimensions)
│
├── Vector Store (FAISS)
│   └── Similarity Search with metadata filtering
│
├── Query Processor
│   ├── Content Type Filtering
│   ├── Similarity Retrieval
│   └── RAG Generation with custom prompts
│
└── Web Interface (HTML/CSS/JavaScript)
    └── Interactive querying and document management
```

## 📊 Chunk Types

- **Text**: Regular document text, intelligently chunked by sentences and paragraphs
- **Table**: Tabular data extracted as structured markdown content
- **Image**: Visual content processed through GPT-4o-mini for detailed descriptions

## ⚙️ Configuration

### Environment Variables (`.env`)
```bash
OPENAI_API_KEY=your_api_key_here          # Required for LLM and vision processing
PROCESS_IMAGES=true                       # Enable/disable image processing (default: true)
```

### Dependencies
- **FastAPI**: Web framework and API
- **PyMuPDF**: PDF parsing and text extraction
- **Docling**: Advanced document layout analysis
- **Sentence Transformers**: Text embedding (384D vectors)
- **FAISS**: Vector similarity search
- **OpenAI GPT-4o-mini**: LLM for generation and vision
- **Pillow**: Image processing

## 🎯 Example Queries

### Basic Questions
- "What are the benefits of electric vehicles?"
- "How do charging stations work?"
- "What are the environmental impacts?"

### Content-Specific Queries
- "What tables show cost comparisons?" (table filter)
- "What images show battery technology?" (image filter)
- "What text discusses government policies?" (text filter)

### Advanced Retrieval
- Get raw chunks: `"charging infrastructure", k=10`
- Filtered search: `"emission standards", chunk_types="table"`

## 🔧 Development

### Project Structure
```
├── main.py                 # FastAPI application with CORS and static files
├── src/
│   ├── api/routes.py       # API endpoints and request handlers
│   ├── ingestion/
│   │   ├── parser.py       # PDF parsing and chunk extraction
│   │   ├── embedder.py     # Text embedding with Sentence Transformers
│   │   └── chunker.py      # Text chunking utilities
│   ├── retrieval/
│   │   ├── vector_store.py # FAISS vector storage and search
│   │   └── retriever.py    # Query processing and retrieval logic
│   └── models/
│       ├── llm.py          # OpenAI integration for RAG generation
│       └── vision.py       # Image description with GPT-4o-mini
├── static/
│   └── index.html          # Web interface
├── requirements.txt        # Python dependencies
├── .env.example           # Environment configuration template
└── README.md              # This file
```

### Running Tests
```bash
# Test API endpoints
curl http://localhost:8002/health

# Test document ingestion
curl -X POST -F "file=@test.pdf" http://localhost:8002/ingest

# Test querying
curl "http://localhost:8002/query?q=What is this document about?"
```

## 🚨 Troubleshooting

### Common Issues

**"Failed to fetch" Error**
- Ensure CORS is enabled (automatically configured)
- Check that server is running on correct port (8002)
- Verify browser is accessing http://localhost:8002/

**Document Processing Fails**
- Check PDF file is not corrupted
- Ensure sufficient disk space for processing
- Verify OpenAI API key is configured

**No Search Results**
- Confirm documents have been ingested
- Check vector store statistics: `GET /stats`
- Try different query terms

**Image Processing Disabled**
- Set `PROCESS_IMAGES=true` in `.env`
- Ensure OpenAI API key has sufficient credits
- Images will fallback to filename-only descriptions if VLM fails

### Logs and Debugging
- Server logs appear in terminal when running with `--reload`
- Check browser developer console for frontend errors
- API responses include detailed error messages

## 📄 License

This project is for educational and research purposes.

---

**Ready to explore your documents?** Start the server and open http://localhost:8002/ in your browser! 🎉

## RAG Prompt Template

The system uses a custom prompt template that:
- Provides clear instructions for grounded answers
- Handles different content types appropriately
- Includes source attribution
- Maintains technical accuracy for engineering content</content>
<parameter name="filePath">/workspaces/Assign-RAG/README.md