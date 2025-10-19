# RAG Application

A Retrieval Augmented Generation (RAG) chatbot that enables ingestion of documents (PDF, DOCX, TXT, MD) and ask questions about their content. Answers are generated using a Large Language Model (Groq API) and include source citations from your documents.

## Features

- Ingests PDF, DOCX, TXT, and Markdown files
- Uses Unstructured API for document parsing
- Stores document chunks in ChromaDB with semantic embeddings
- Fast, accurate answers powered by Groq LLM
- Web interface Chatbot
- Source attribution for every answer

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API keys:**
   - Create a `.env` file in the project root:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     UNSTRUCTURED_API_KEY=your_unstructured_key_optional
     ```

3. **Add documents:**
   - Place your files in the `docs/` folder (PDF, DOCX, TXT, MD supported).

4. **Process documents:**
   ```bash
   python utils/ingest.py
   ```

5. **Run the application:**
   ```bash
   python run.py
   ```
   - Select option 1 for the web interface.
   - Open `http://localhost:8000` in your browser.

## Usage

- Ask questions about any documents via the web interface.
- Answers include relevant document sources.
- For command-line testing, run:
  ```bash
  python test_system.py
  ```

## Configuration

Edit `config.json` to customize:
- Document and data paths
- Processing parameters (chunk size, overlap, file size)
- LLM model, temperature, and max tokens
- UI options (number of search results, source display)

## File Structure

```
core/
  rag_system.py         # Main RAG orchestrator
  config_loader.py      # Loads config and environment variables
  llm/groq_client.py    # Groq API integration
  storage/database.py   # ChromaDB vector storage
ui/
  web_server.py         # Web server and WebSocket handler
utils/
  ingest.py             # Document processor
docs/                   # Place your documents here
data/                   # ChromaDB persistent database
index.html              # Web UI
run.py                  # Main launcher
test_system.py          # System test script
config.json             # Configuration file
requirements.txt        # Python dependencies
.env.example            # API key template
LICENSE                 # MIT License
README.md               # Project documentation
```

## Requirements

- Python 3.8+
- Groq API key (get one at https://console.groq.com/)
- Optional: Unstructured API key for improved PDF parsing

