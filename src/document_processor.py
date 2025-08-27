"""
Document Processor Module
Handles loading and processing of various document formats
"""

import os
import logging
from typing import List, Dict, Any
from pathlib import Path
import requests
from bs4 import BeautifulSoup

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    from docx import Document as DocxDocument
except ImportError:
    DocxDocument = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentProcessor:
    """Processes documents from various sources and formats"""
    
    def __init__(self):
        self.supported_extensions = ['.txt', '.md', '.pdf', '.docx']
        
    def load_from_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """Load all supported documents from a directory"""
        documents = []
        directory = Path(directory_path)
        
        if not directory.exists():
            logger.error(f"Directory {directory_path} does not exist")
            return documents
            
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_extensions:
                try:
                    content = self._process_file(file_path)
                    if content:
                        documents.append({
                            'content': content,
                            'source': str(file_path),
                            'type': file_path.suffix.lower()
                        })
                        logger.info(f"Processed {file_path}")
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {str(e)}")
                    
        return documents
    
    def load_from_url(self, url: str) -> List[Dict[str, Any]]:
        """Load documentation from a URL (basic web scraping)"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
                
            # Get text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return [{
                'content': text,
                'source': url,
                'type': 'web'
            }]
            
        except Exception as e:
            logger.error(f"Error loading from URL {url}: {str(e)}")
            return []
    
    def load_uploaded_files(self, uploaded_files) -> List[Dict[str, Any]]:
        """Process uploaded files from Streamlit"""
        documents = []
        
        for uploaded_file in uploaded_files:
            try:
                # Get file extension
                file_extension = Path(uploaded_file.name).suffix.lower()
                
                if file_extension not in self.supported_extensions:
                    logger.warning(f"Unsupported file type: {file_extension}")
                    continue
                
                # Process based on file type
                content = None
                if file_extension == '.txt' or file_extension == '.md':
                    content = str(uploaded_file.read(), "utf-8")
                elif file_extension == '.pdf' and PyPDF2:
                    content = self._extract_pdf_content(uploaded_file)
                elif file_extension == '.docx' and DocxDocument:
                    content = self._extract_docx_content(uploaded_file)
                
                if content:
                    documents.append({
                        'content': content,
                        'source': uploaded_file.name,
                        'type': file_extension
                    })
                    logger.info(f"Processed uploaded file: {uploaded_file.name}")
                    
            except Exception as e:
                logger.error(f"Error processing uploaded file {uploaded_file.name}: {str(e)}")
        
        return documents
    
    def _process_file(self, file_path: Path) -> str:
        """Process a single file based on its extension"""
        extension = file_path.suffix.lower()
        
        try:
            if extension in ['.txt', '.md']:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            elif extension == '.pdf' and PyPDF2:
                with open(file_path, 'rb') as f:
                    return self._extract_pdf_content(f)
            elif extension == '.docx' and DocxDocument:
                return self._extract_docx_content(file_path)
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            
        return ""
    
    def _extract_pdf_content(self, file_obj) -> str:
        """Extract text content from PDF"""
        if not PyPDF2:
            logger.error("PyPDF2 not installed. Cannot process PDF files.")
            return ""
            
        try:
            reader = PyPDF2.PdfReader(file_obj)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting PDF content: {str(e)}")
            return ""
    
    def _extract_docx_content(self, file_obj) -> str:
        """Extract text content from DOCX"""
        if not DocxDocument:
            logger.error("python-docx not installed. Cannot process DOCX files.")
            return ""
            
        try:
            doc = DocxDocument(file_obj)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting DOCX content: {str(e)}")
            return ""
    
    def chunk_document(self, document: Dict[str, Any], chunk_size: int = 1000, overlap: int = 200) -> List[Dict[str, Any]]:
        """Split document into chunks for embedding"""
        content = document['content']
        chunks = []
        
        # Simple text chunking
        start = 0
        chunk_id = 0
        
        while start < len(content):
            end = start + chunk_size
            chunk_text = content[start:end]
            
            # Try to end on a sentence or paragraph
            if end < len(content):
                last_period = chunk_text.rfind('.')
                last_newline = chunk_text.rfind('\n')
                
                if last_period > chunk_size * 0.7:  # If we find a period in the last 30%
                    end = start + last_period + 1
                    chunk_text = content[start:end]
                elif last_newline > chunk_size * 0.7:  # If we find a newline in the last 30%
                    end = start + last_newline + 1
                    chunk_text = content[start:end]
            
            chunks.append({
                'content': chunk_text.strip(),
                'source': document['source'],
                'type': document['type'],
                'chunk_id': chunk_id,
                'start_pos': start,
                'end_pos': end
            })
            
            chunk_id += 1
            start = end - overlap  # Overlap chunks
            
        return chunks

