"""
Configuration file for AI Prompt Generator
Centralized configuration management
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """
    Application configuration class
    """
    
    # Ollama Configuration
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama2")
    
    # CrewAI Configuration
    CREWAI_VERBOSE = os.getenv("CREWAI_VERBOSE", "True").lower() == "true"
    CREWAI_MAX_ITER = int(os.getenv("CREWAI_MAX_ITER", "3"))
    
    # Application Settings
    APP_TITLE = os.getenv("APP_TITLE", "AI Intelligent Prompt Generator")
    APP_DESCRIPTION = os.getenv("APP_DESCRIPTION", "Generate structured prompts for various departments using AI agents")
    
    # Department Configuration
    DEFAULT_DEPARTMENT = os.getenv("DEFAULT_DEPARTMENT", "General")
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # UI Configuration
    THEME_COLOR = "#1f77b4"
    BACKGROUND_COLOR = "#f0f2f6"
    SUCCESS_COLOR = "#28a745"
    WARNING_COLOR = "#ffc107"
    ERROR_COLOR = "#dc3545"
    
    # Supported Departments
    DEPARTMENTS = [
        {
            "value": "content",
            "label": "Content",
            "description": "Content creation, strategy, and optimization",
            "icon": "📝"
        },
        {
            "value": "solutions",
            "label": "Solutions",
            "description": "Solution design and implementation",
            "icon": "🔧"
        },
        {
            "value": "digital_marketing",
            "label": "Digital Marketing",
            "description": "Marketing campaigns and strategies",
            "icon": "📈"
        },
        {
            "value": "digital_analytics",
            "label": "Digital Analytics",
            "description": "Data analysis and insights",
            "icon": "📊"
        },
        {
            "value": "digital_operations",
            "label": "Digital Operations",
            "description": "Process optimization and automation",
            "icon": "⚙️"
        },
        {
            "value": "martech",
            "label": "Martech",
            "description": "Marketing technology and platforms",
            "icon": "🛠️"
        },
        {
            "value": "ai_engineering",
            "label": "AI Engineering",
            "description": "AI/ML development and optimization",
            "icon": "🤖"
        }
    ]
    
    # Prompt Generation Settings
    MAX_INPUT_LENGTH = 1000
    MAX_OUTPUT_LENGTH = 2000
    GENERATION_TIMEOUT = 300  # seconds
    
    # File Paths
    HISTORY_DIR = "history"
    TEMPLATES_DIR = "templates"
    
    @classmethod
    def get_department_by_value(cls, value: str) -> dict:
        """
        Get department configuration by value
        """
        for dept in cls.DEPARTMENTS:
            if dept["value"] == value:
                return dept
        return None
    
    @classmethod
    def validate_config(cls) -> dict:
        """
        Validate application configuration
        """
        validation_result = {
            "status": "valid",
            "issues": [],
            "warnings": []
        }
        
        # Check required environment variables
        if not cls.OLLAMA_BASE_URL:
            validation_result["issues"].append("OLLAMA_BASE_URL not set")
            validation_result["status"] = "invalid"
        
        if not cls.OLLAMA_MODEL:
            validation_result["warnings"].append("OLLAMA_MODEL not set, using default: llama2")
        
        # Check directories
        if not os.path.exists(cls.HISTORY_DIR):
            validation_result["warnings"].append(f"History directory '{cls.HISTORY_DIR}' does not exist")
        
        if not os.path.exists(cls.TEMPLATES_DIR):
            validation_result["warnings"].append(f"Templates directory '{cls.TEMPLATES_DIR}' does not exist")
        
        return validation_result
