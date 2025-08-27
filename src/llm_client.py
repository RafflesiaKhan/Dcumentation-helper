"""
LLM Client Module
Handles communication with Ollama local LLM
"""

import logging
from typing import List, Dict, Any, Optional
import ollama
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for interacting with Ollama LLM"""
    
    def __init__(self, model_name: str = "llama2:7b-chat"):
        self.model_name = model_name
        self.system_prompt_template = """You are a helpful documentation assistant for {project_name}. 

{project_description}

Instructions:
- Answer questions clearly and concisely
- Use the provided context when available
- If context is provided, prioritize information from the context
- If no context is available, use your general knowledge about {project_name}
- Always be helpful and informative
- If you don't know something, say so honestly
- Format your responses in a user-friendly way with proper markdown when helpful

Context: {context}

User Question: {question}
"""
        
        # Test connection to Ollama
        self._test_connection()
    
    def _test_connection(self) -> bool:
        """Test connection to Ollama service"""
        try:
            # Try to list available models
            models = ollama.list()
            logger.info(f"Connected to Ollama. Available models: {len(models['models'])}")
            
            # Check if our model is available
            model_names = [model['name'] for model in models['models']]
            if self.model_name not in model_names:
                logger.warning(f"Model {self.model_name} not found. Available: {model_names}")
                # Try to pull the model
                logger.info(f"Attempting to pull model: {self.model_name}")
                try:
                    ollama.pull(self.model_name)
                    logger.info(f"Successfully pulled model: {self.model_name}")
                except Exception as e:
                    logger.error(f"Failed to pull model {self.model_name}: {str(e)}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to Ollama: {str(e)}")
            return False
    
    def generate_response(
        self, 
        question: str, 
        context: List[Dict[str, Any]] = None,
        project_name: str = "this project",
        project_description: str = "An open-source project."
    ) -> str:
        """Generate response using Ollama"""
        try:
            # Prepare context string
            context_str = ""
            if context:
                context_str = "\n\n".join([
                    f"Document: {doc['metadata']['source']}\nContent: {doc['content'][:500]}..."
                    for doc in context[:3]  # Use top 3 most relevant documents
                ])
                if not context_str:
                    context_str = "No specific documentation context available."
            else:
                context_str = "No documentation loaded yet."
            
            # Create the prompt
            prompt = self.system_prompt_template.format(
                project_name=project_name,
                project_description=project_description,
                context=context_str,
                question=question
            )
            
            logger.info(f"Generating response for question: {question[:50]}...")
            
            # Generate response
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                options={
                    'temperature': 0.7,
                    'top_p': 0.9,
                    'max_tokens': 1000
                }
            )
            
            answer = response['response'].strip()
            logger.info("Successfully generated response")
            
            return answer
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return f"I apologize, but I encountered an error while processing your question. Please make sure Ollama is running and the model '{self.model_name}' is available. Error: {str(e)}"
    
    def get_available_models(self) -> List[str]:
        """Get list of available Ollama models"""
        try:
            models = ollama.list()
            return [model['name'] for model in models['models']]
        except Exception as e:
            logger.error(f"Error getting available models: {str(e)}")
            return []
    
    def set_model(self, model_name: str) -> bool:
        """Change the active model"""
        try:
            # Test if model is available
            available_models = self.get_available_models()
            if model_name not in available_models:
                logger.warning(f"Model {model_name} not available. Attempting to pull...")
                ollama.pull(model_name)
            
            self.model_name = model_name
            logger.info(f"Successfully switched to model: {model_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error switching to model {model_name}: {str(e)}")
            return False

