"""
Utility functions for AI Prompt Generator
Helper functions for data processing, validation, and formatting
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

class PromptGeneratorUtils:
    """
    Utility class for prompt generation helpers
    """
    
    @staticmethod
    def validate_ollama_connection() -> Dict[str, Any]:
        """
        Validate Ollama connection and model availability
        """
        try:
            import requests
            base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            model = os.getenv("OLLAMA_MODEL", "llama2")
            
            # Check if Ollama is running
            response = requests.get(f"{base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m.get("name", "") for m in models]
                
                if model in model_names:
                    return {
                        "status": "connected",
                        "model": model,
                        "available_models": model_names,
                        "message": f"Successfully connected to Ollama with model: {model}"
                    }
                else:
                    return {
                        "status": "model_not_found",
                        "model": model,
                        "available_models": model_names,
                        "message": f"Model {model} not found. Available models: {', '.join(model_names)}"
                    }
            else:
                return {
                    "status": "connection_failed",
                    "message": f"Failed to connect to Ollama at {base_url}"
                }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error validating Ollama connection: {str(e)}"
            }
    
    @staticmethod
    def format_prompt_output(prompt_data: Dict[str, Any]) -> str:
        """
        Format the generated prompt into a clean, modern output
        """
        try:
            # Extract the main prompt content
            prompt_content = prompt_data.get("generated_prompt", "")
            
            # Clean up the prompt content
            cleaned_prompt = PromptGeneratorUtils._clean_prompt_text(prompt_content)
            
            # Add metadata
            metadata = {
                "generated_at": datetime.now().isoformat(),
                "department": prompt_data.get("department", "General"),
                "user_input": prompt_data.get("user_input", ""),
                "status": prompt_data.get("status", "completed")
            }
            
            # Format as a structured output
            formatted_output = f"""
# AI-Generated Prompt

## Department: {metadata['department']}

## Original Request:
{metadata['user_input']}

## Generated Prompt:
{cleaned_prompt}

---
*Generated on: {metadata['generated_at']}*
            """.strip()
            
            return formatted_output
            
        except Exception as e:
            return f"Error formatting prompt: {str(e)}"
    
    @staticmethod
    def _clean_prompt_text(text: str) -> str:
        """
        Clean and format prompt text for better readability
        """
        if not text:
            return ""
        
        # Remove extra whitespace and normalize line breaks
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r' +', ' ', text)
        
        # Remove markdown code blocks if they're not needed
        text = re.sub(r'```\w*\n', '', text)
        text = re.sub(r'```\n', '', text)
        
        return text.strip()
    
    @staticmethod
    def get_department_suggestions() -> List[Dict[str, str]]:
        """
        Get suggested departments with descriptions
        """
        return [
            {"value": "content", "label": "Content", "description": "Content creation, strategy, and optimization"},
            {"value": "solutions", "label": "Solutions", "description": "Solution design and implementation"},
            {"value": "digital_marketing", "label": "Digital Marketing", "description": "Marketing campaigns and strategies"},
            {"value": "digital_analytics", "label": "Digital Analytics", "description": "Data analysis and insights"},
            {"value": "digital_operations", "label": "Digital Operations", "description": "Process optimization and automation"},
            {"value": "martech", "label": "Martech", "description": "Marketing technology and platforms"},
            {"value": "ai_engineering", "label": "AI Engineering", "description": "AI/ML development and optimization"}
        ]
    
    @staticmethod
    def save_prompt_history(prompt_data: Dict[str, Any], filename: str = None) -> str:
        """
        Save generated prompt to history
        """
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"prompt_history_{timestamp}.json"
            
            # Create history directory if it doesn't exist
            history_dir = "history"
            if not os.path.exists(history_dir):
                os.makedirs(history_dir)
            
            filepath = os.path.join(history_dir, filename)
            
            # Add timestamp to prompt data
            prompt_data["saved_at"] = datetime.now().isoformat()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(prompt_data, f, indent=2, ensure_ascii=False)
            
            return filepath
            
        except Exception as e:
            return f"Error saving prompt history: {str(e)}"
    
    @staticmethod
    def load_prompt_history(filename: str) -> Optional[Dict[str, Any]]:
        """
        Load prompt from history
        """
        try:
            filepath = os.path.join("history", filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return None
        except Exception as e:
            return None
    
    @staticmethod
    def get_prompt_templates() -> Dict[str, str]:
        """
        Get basic prompt templates for different use cases
        """
        return {
            "content_creation": "Create engaging content for {platform} about {topic}",
            "data_analysis": "Analyze {data_type} data to provide insights about {objective}",
            "strategy_development": "Develop a strategic plan for {department} to achieve {goal}",
            "process_optimization": "Optimize the {process_name} process to improve {metric}",
            "technical_solution": "Design a technical solution for {problem} using {technology}",
            "campaign_planning": "Plan a {campaign_type} campaign targeting {audience}",
            "report_generation": "Generate a comprehensive report on {subject} for {stakeholders}"
        }
