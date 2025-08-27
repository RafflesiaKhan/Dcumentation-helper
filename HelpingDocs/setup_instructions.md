# 🚀 Quick Setup Instructions for Documentation Helper Agent

## Prerequisites Checklist

Before starting the hands-on session, ensure you have:

- [ ] **Python 3.8+** installed
- [ ] **Git** for version control
- [ ] **Internet connection** for downloading models and dependencies
- [ ] **Terminal/Command Prompt** access
- [ ] **Text editor** or IDE (VS Code recommended)

## Step-by-Step Setup

### 1. Install Ollama

#### macOS/Linux:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### Windows:
1. Download Ollama from [ollama.ai](https://ollama.ai)
2. Run the installer
3. Open Command Prompt as Administrator

#### Verify Installation:
```bash
ollama --version
```

### 2. Pull Language Model

```bash
# Pull the recommended model (this will take 5-10 minutes)
ollama pull llama2:7b-chat

# Verify the model is available
ollama list
```

### 3. Clone/Download Project

```bash
# Option 1: If you have the repository
git clone <repository-url>
cd documentation_helper

# Option 2: If you're creating from scratch
mkdir documentation_helper
cd documentation_helper
```

### 4. Create Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 5. Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# If requirements.txt doesn't exist, install manually:
pip install streamlit==1.29.0 chromadb==0.4.22 sentence-transformers==2.2.2 pypdf2==3.0.1 python-docx==0.8.11 requests==2.31.0 beautifulsoup4==4.12.2 ollama==0.1.7
```

### 6. Test Installation

```bash
# Test Ollama connection
ollama run llama2:7b-chat "Hello, can you help me test the installation?"

# Test Python imports
python -c "import streamlit, chromadb, sentence_transformers; print('All imports successful!')"
```

### 7. Launch Application

```bash
# Start the Streamlit application
streamlit run app.py
```

The application should open in your browser at `http://localhost:8501`

## Troubleshooting Common Issues

### Issue: Ollama command not found
**Solution:**
```bash
# Add Ollama to PATH (on macOS/Linux)
export PATH=$PATH:/usr/local/bin

# Restart terminal and try again
```

### Issue: Python module not found
**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Issue: Port 8501 already in use
**Solution:**
```bash
# Use different port
streamlit run app.py --server.port 8502
```

### Issue: Model download fails
**Solution:**
```bash
# Try smaller model first
ollama pull llama2:7b-chat

# Check internet connection and try again
```

### Issue: ChromaDB permission errors
**Solution:**
```bash
# Clear existing embeddings
rm -rf embeddings/

# Restart application
streamlit run app.py
```

## Testing Your Setup

### Quick Functionality Test

1. **Open Application**: Should see the Documentation Helper Agent interface
2. **Check Ollama Models**: Sidebar should show available models
3. **Upload Test File**: Create a simple .txt file and upload it
4. **Process Documents**: Should see success message and document count
5. **Ask Question**: Test chat functionality

### Sample Test File

Create `test_doc.txt`:
```
# Test Documentation

This is a test document for the Documentation Helper Agent.

## Features
- Document processing
- Vector embeddings
- Chat interface

## Getting Started
1. Upload documents
2. Ask questions
3. Get intelligent responses
```

## Project Structure Verification

After setup, your project should look like:

```
documentation_helper/
├── app.py                    # Main application
├── requirements.txt          # Dependencies
├── src/                     # Source code
│   ├── __init__.py
│   ├── document_processor.py
│   ├── vector_db.py
│   └── llm_client.py
├── data/                    # Sample documents
├── embeddings/             # Vector database (created automatically)
└── README.md               # Documentation
```

## Ready to Start!

Once setup is complete, you're ready to begin the hands-on session. Follow the `HANDS_ON_GUIDE.md` for the complete learning experience.

### Next Steps:
1. Read through the SDLC planning phase
2. Understand the system architecture
3. Start with Phase 1 implementation
4. Test each component as you build
5. Customize for your assigned project

## Getting Help

If you encounter issues during setup:

1. **Check Prerequisites**: Ensure all requirements are met
2. **Read Error Messages**: Often contain helpful information
3. **Check Documentation**: Refer to official docs for each tool
4. **Ask for Help**: Don't hesitate to reach out to instructors

Good luck with your Documentation Helper Agent journey! 🎉


