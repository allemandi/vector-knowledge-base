# Vector Knowledge Base

A minimalist command-line knowledge system with semantic memory capabilities using vector embeddings for information retrieval.

## Features

- **Semantic Memory**: Store and retrieve information using vector embeddings
- **Fast Similarity Search**: Powered by FAISS for efficient vector similarity matching
- **Persistent Storage**: Knowledge is stored in SQLite for persistence between sessions
- **Efficient Caching**: Embedding caching to improve performance
- **Minimal UI**: Simple command-line interface

## Acknowledgments  
- This project was developed with the help of AI tools (e.g., GitHub Copilot, Cursor) for code suggestions, debugging, and optimizations.  

## Requirements

- Python 3.8 or higher

## Installation

1. Clone the repository:
```bash
git clone https://github.com/allemandi/vector-knowledge-base.git
cd vector-knowledge-base
```

2. Create and activate a virtual environment:
```bash
# Create a virtual environment
python -m venv venv

# Note: On some systems, try python3 instead to explicitly use Python 3.

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the knowledge base:
```bash
python main.py
```

Use Commands.

Remember to run the following to leave the Python virtual environment.
```bash
deactivate
```
### Commands

- **Remember [text]** - Store information in the knowledge base
- **Forget [text]** - Remove specific information
- **Forget** - Remove the previously returned information
- **Threshold [0-1]** - Set similarity threshold (0.0-1.0) to control recall precision
- **Exit** - Quit the program
- **Any other text** - Query the knowledge base (the system will search for relevant information)

## How It Works

1. **Embeddings**: Text is converted to vector embeddings using SentenceTransformers
2. **Vector Search**: When you enter a query, it's converted to an embedding and compared to stored knowledge
3. **Similarity Matching**: The most similar piece of information is returned if it exceeds the similarity threshold
4. **Knowledge Management**: You can add, remove, and manage stored information

## Project Structure

- `main.py` - Command-line interface
- `knowledge_base.py` - Core knowledge base functionality
- `memory.py` - Vector storage and retrieval with SQLite persistence
- `embeddings.py` - Text to vector embedding conversion
- `models.py` - Data models for the application

## Dependencies

- sentence-transformers - Text embedding generation
- FAISS - Vector similarity search
- orjson - Fast JSON serialization
- SQLite - Persistent storage

## License

MIT 