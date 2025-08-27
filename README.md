# 🤖 Documentation Helper Agent

A learning project for building AI agents that can intelligently answer questions about documentation using local LLMs and vector embeddings.

## 🎯 Project Overview

This agent helps users interact with documentation by:
- Loading documents from various sources (files, directories, URLs)
- Creating vector embeddings for semantic search
- Using local LLMs (via Ollama) for intelligent responses
- Providing a user-friendly Streamlit interface

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **LLM**: Ollama (local models)
- **Vector Database**: ChromaDB
- **Embeddings**: Sentence Transformers
- **Document Processing**: PyPDF2, python-docx, BeautifulSoup4

## 📋 Prerequisites

1. **Python 3.8+**
2. **Ollama**: Install from [ollama.ai](https://ollama.ai)
3. **Git**: For cloning repositories

## 🚀 Quick Start

### 1. Install Ollama

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model (this will take a few minutes)
ollama pull llama2:7b-chat
```

### 2. Setup Python Environment

```bash
# Clone or navigate to project directory
cd documentation_helper

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 How to Use

### 1. Configure Your Project
- Set the project name (e.g., "FastAPI", "Django", "React")
- Add a brief project description
- Select your preferred Ollama model

### 2. Load Documentation
Choose one of these methods:

**Upload Files:**
- Click "Browse files" and select .txt, .md, .pdf, or .docx files
- Click "Process Uploaded Files"

**Load from Directory:**
- Enter the path to a directory containing documentation
- Click "Load from Directory"

**Load from URL:**
- Enter a documentation URL
- Click "Load from URL" (basic web scraping)

### 3. Ask Questions
- Use the chat input to ask questions about the documentation
- Try the sample question buttons for inspiration
- View sources used for each response

## 🔧 Features

### Document Processing
- ✅ Multiple file formats (.txt, .md, .pdf, .docx)
- ✅ Directory scanning
- ✅ URL content extraction
- ✅ Intelligent text chunking

### Vector Search
- ✅ Semantic similarity search
- ✅ Relevance scoring
- ✅ Context retrieval

### LLM Integration
- ✅ Local Ollama models
- ✅ Context-aware responses
- ✅ Project-specific prompting
- ✅ Fallback when no context available

### User Interface
- ✅ Real-time chat interface
- ✅ Document loading progress
- ✅ Source attribution
- ✅ Sample question suggestions

## 📁 Project Structure

```
documentation_helper/
├── app.py                    # Main Streamlit application
├── src/
│   ├── __init__.py
│   ├── document_processor.py # Document loading and processing
│   ├── vector_db.py         # Vector database operations
│   └── llm_client.py        # Ollama LLM client
├── data/                    # Local document storage
├── embeddings/             # Vector database files
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── HANDS_ON_GUIDE.md     # Detailed learning guide
```

## 🧪 Testing the Agent

### Test Scenarios

1. **Empty State**: Ask questions before loading any documents
2. **Single Document**: Load one file and test specific queries
3. **Multiple Documents**: Load various file types and test complex queries
4. **Edge Cases**: Test with large files, corrupted files, etc.

### Sample Questions
- "How do I get started with this project?"
- "What are the main components?"
- "How do I configure the settings?"
- "What are the API endpoints?"

## 🔍 Troubleshooting

### Common Issues

**Ollama Connection Error:**
```bash
# Check if Ollama is running
ollama list

# Start Ollama service if needed
ollama serve
```

**Model Not Found:**
```bash
# Pull the required model
ollama pull llama2:7b-chat

# List available models
ollama list
```

**ChromaDB Issues:**
- Delete the `embeddings/` directory and restart
- Check disk space and permissions

**Import Errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## 🚀 Customization

### For Different Projects

1. **Update Project Settings**: Change project name and description
2. **Custom System Prompt**: Modify `llm_client.py` system prompt
3. **Document Sources**: Add project-specific documentation
4. **Model Selection**: Choose different Ollama models

### Advanced Features

- Add support for more file formats
- Implement document versioning
- Add conversation memory
- Create project templates

## 🤝 Contributing

This is a learning project! Feel free to:
- Experiment with different models
- Add new document processors
- Improve the UI/UX
- Add testing scenarios

## 📚 Learning Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [ChromaDB Guide](https://docs.trychroma.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Sentence Transformers](https://www.sbert.net/)

## 📄 License

This project is for educational purposes. Feel free to use and modify as needed.

---

**Happy Learning! 🎉**

