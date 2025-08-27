"""
Documentation Helper Agent
Main Streamlit Application
"""

import streamlit as st
import os
import sys
from pathlib import Path
import logging

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.document_processor import DocumentProcessor
from src.vector_db import VectorDatabase
from src.llm_client import OllamaClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Documentation Helper Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'vector_db' not in st.session_state:
    st.session_state.vector_db = VectorDatabase()
if 'llm_client' not in st.session_state:
    st.session_state.llm_client = OllamaClient()
if 'doc_processor' not in st.session_state:
    st.session_state.doc_processor = DocumentProcessor()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'project_name' not in st.session_state:
    st.session_state.project_name = "OpenSource Project"
if 'project_description' not in st.session_state:
    st.session_state.project_description = "A comprehensive open-source project with detailed documentation."


def main():
    """Main application function"""
    
    # Title and description
    st.title("🤖 Documentation Helper Agent")
    st.markdown("Ask questions about your documentation, and get intelligent answers!")
    
    # Sidebar for configuration and document loading
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Project settings
        st.subheader("Project Settings")
        project_name = st.text_input(
            "Project Name", 
            value=st.session_state.project_name,
            help="Name of the open-source project"
        )
        project_description = st.text_area(
            "Project Description",
            value=st.session_state.project_description,
            help="Brief description of what this project does"
        )
        
        if project_name != st.session_state.project_name:
            st.session_state.project_name = project_name
        if project_description != st.session_state.project_description:
            st.session_state.project_description = project_description
        
        st.divider()
        
        # Model selection
        st.subheader("🧠 LLM Model")
        available_models = st.session_state.llm_client.get_available_models()
        if available_models:
            selected_model = st.selectbox(
                "Select Ollama Model",
                available_models,
                index=0 if available_models else None
            )
            if st.button("Switch Model"):
                if st.session_state.llm_client.set_model(selected_model):
                    st.success(f"Switched to {selected_model}")
                else:
                    st.error(f"Failed to switch to {selected_model}")
        else:
            st.error("No Ollama models found. Please install Ollama and pull a model.")
            st.code("ollama pull llama2:7b-chat")
        
        st.divider()
        
        # Document loading section
        st.subheader("📚 Load Documentation")
        
        # Display current status
        db_info = st.session_state.vector_db.get_collection_info()
        st.metric("Documents Loaded", db_info['document_count'])
        
        # File upload
        uploaded_files = st.file_uploader(
            "Upload Documents",
            type=['txt', 'md', 'pdf', 'docx'],
            accept_multiple_files=True,
            help="Upload .txt, .md, .pdf, or .docx files"
        )
        
        if uploaded_files and st.button("Process Uploaded Files"):
            process_uploaded_files(uploaded_files)
        
        # Directory path input
        st.subheader("📁 Load from Directory")
        directory_path = st.text_input(
            "Directory Path",
            placeholder="e.g., ./data or /path/to/docs",
            help="Path to directory containing documentation files"
        )
        
        if directory_path and st.button("Load from Directory"):
            process_directory(directory_path)
        
        # URL input
        st.subheader("🌐 Load from URL")
        url = st.text_input(
            "Documentation URL",
            placeholder="https://github.com/user/repo/tree/main/docs",
            help="URL to documentation (basic web scraping)"
        )
        
        if url and st.button("Load from URL"):
            process_url(url)
        
        st.divider()
        
        # Sample questions
        st.subheader("💡 Sample Questions")
        st.markdown("Click on any topic to ask a relevant question:")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📖 Process Definitions", use_container_width=True):
                st.session_state.current_query = "What are the main processes defined in this documentation?"
        with col2:
            if st.button("⚙️ Process Tasks", use_container_width=True):
                st.session_state.current_query = "What are the key tasks and workflows described?"
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("🚀 Getting Started", use_container_width=True):
                st.session_state.current_query = "How do I get started with this project?"
        with col4:
            if st.button("🔧 Configuration", use_container_width=True):
                st.session_state.current_query = "How do I configure this project?"
        
        # Clear database
        if st.button("🗑️ Clear All Documents", type="secondary"):
            if st.session_state.vector_db.clear_collection():
                st.success("All documents cleared!")
                st.rerun()
    
    # Main chat interface
    st.header("💬 Chat with Documentation")
    
    # Display chat history
    for i, (question, answer) in enumerate(st.session_state.chat_history):
        with st.container():
            st.markdown(f"**You:** {question}")
            st.markdown(f"**Assistant:** {answer}")
            st.divider()
    
    # Chat input
    if 'current_query' in st.session_state:
        query = st.session_state.current_query
        del st.session_state.current_query
    else:
        query = st.chat_input("Ask a question about the documentation...")
    
    if query:
        handle_query(query)


def process_uploaded_files(uploaded_files):
    """Process uploaded files and add to vector database"""
    with st.spinner("Processing uploaded files..."):
        try:
            documents = st.session_state.doc_processor.load_uploaded_files(uploaded_files)
            
            if documents:
                # Chunk documents
                all_chunks = []
                for doc in documents:
                    chunks = st.session_state.doc_processor.chunk_document(doc)
                    all_chunks.extend(chunks)
                
                # Add to vector database
                if st.session_state.vector_db.add_documents(all_chunks):
                    st.success(f"Successfully processed {len(uploaded_files)} files into {len(all_chunks)} chunks!")
                else:
                    st.error("Failed to add documents to vector database")
            else:
                st.warning("No valid documents found in uploaded files")
                
        except Exception as e:
            st.error(f"Error processing uploaded files: {str(e)}")


def process_directory(directory_path):
    """Process documents from directory"""
    with st.spinner(f"Loading documents from {directory_path}..."):
        try:
            documents = st.session_state.doc_processor.load_from_directory(directory_path)
            
            if documents:
                # Chunk documents
                all_chunks = []
                for doc in documents:
                    chunks = st.session_state.doc_processor.chunk_document(doc)
                    all_chunks.extend(chunks)
                
                # Add to vector database
                if st.session_state.vector_db.add_documents(all_chunks):
                    st.success(f"Successfully loaded {len(documents)} documents into {len(all_chunks)} chunks!")
                else:
                    st.error("Failed to add documents to vector database")
            else:
                st.warning(f"No valid documents found in {directory_path}")
                
        except Exception as e:
            st.error(f"Error loading from directory: {str(e)}")


def process_url(url):
    """Process documentation from URL"""
    with st.spinner(f"Loading documentation from {url}..."):
        try:
            documents = st.session_state.doc_processor.load_from_url(url)
            
            if documents:
                # Chunk documents
                all_chunks = []
                for doc in documents:
                    chunks = st.session_state.doc_processor.chunk_document(doc)
                    all_chunks.extend(chunks)
                
                # Add to vector database
                if st.session_state.vector_db.add_documents(all_chunks):
                    st.success(f"Successfully loaded documentation from URL into {len(all_chunks)} chunks!")
                else:
                    st.error("Failed to add documents to vector database")
            else:
                st.warning("No content could be extracted from the URL")
                
        except Exception as e:
            st.error(f"Error loading from URL: {str(e)}")


def handle_query(query):
    """Handle user query and generate response"""
    with st.spinner("Generating response..."):
        try:
            # Search for relevant context
            context = []
            if not st.session_state.vector_db.is_empty():
                context = st.session_state.vector_db.search(query, n_results=5)
            
            # Generate response
            response = st.session_state.llm_client.generate_response(
                question=query,
                context=context,
                project_name=st.session_state.project_name,
                project_description=st.session_state.project_description
            )
            
            # Add to chat history
            st.session_state.chat_history.append((query, response))
            
            # Show the latest interaction
            st.markdown(f"**You:** {query}")
            st.markdown(f"**Assistant:** {response}")
            
            # Show context information if available
            if context:
                with st.expander("📄 Sources Used", expanded=False):
                    for i, doc in enumerate(context[:3]):
                        st.markdown(f"**Source {i+1}:** {doc['metadata']['source']}")
                        st.markdown(f"**Relevance:** {doc['relevance_score']:.2f}")
                        st.markdown(f"**Content:** {doc['content'][:200]}...")
                        st.divider()
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")


if __name__ == "__main__":
    main()

