# Documents Directory

This directory contains the documents that will be processed by the RAG system.

## Supported File Types
- PDF (.pdf)
- Word Documents (.docx) 
- Text Files (.txt)
- Markdown Files (.md)

## How to Add Documents

1. Copy your documents to this directory
2. Run the ingestion script: `python utils/ingest.py`
3. Your documents will be processed and added to the vector database

## Example Usage

```bash
# Add your documents
cp my-document.pdf docs/
cp my-notes.txt docs/

# Process them
python utils/ingest.py

# Start asking questions
python run.py
```

## Note

The actual document files are ignored by git (see .gitignore) to protect potentially sensitive information. Only this README file is tracked.