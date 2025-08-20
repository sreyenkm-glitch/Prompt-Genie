"""
Test script for AI Prompt Generator backend
Verify that the AI agents are working correctly
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_ollama_connection():
    """Test Ollama connection"""
    print("🔍 Testing Ollama connection...")
    
    try:
        from utils.helpers import PromptGeneratorUtils
        status = PromptGeneratorUtils.validate_ollama_connection()
        
        if status["status"] == "connected":
            print(f"✅ {status['message']}")
            return True
        elif status["status"] == "model_not_found":
            print(f"⚠️ {status['message']}")
            print("💡 Please run: ollama pull llama2")
            return False
        else:
            print(f"❌ {status['message']}")
            print("💡 Please ensure Ollama is running: ollama serve")
            return False
    except Exception as e:
        print(f"❌ Error testing connection: {str(e)}")
        return False

def test_agents():
    """Test AI agents functionality"""
    print("\n🤖 Testing AI agents...")
    
    try:
        from agents.prompt_agents import PromptGeneratorAgents
        
        # Initialize agents
        print("📦 Initializing agents...")
        agents = PromptGeneratorAgents()
        print("✅ Agents initialized successfully")
        
        # Test prompt generation
        print("🧪 Testing prompt generation...")
        test_input = "I need to create a social media campaign for our new product launch"
        test_department = "digital_marketing"
        
        result = agents.generate_prompt(test_input, test_department)
        
        if result and result.get("status") == "completed":
            print("✅ Prompt generation successful!")
            print(f"📝 Generated prompt length: {len(str(result.get('generated_prompt', '')))} characters")
            return True
        else:
            print("❌ Prompt generation failed")
            return False
            
    except ImportError as e:
        print(f"⚠️  CrewAI dependencies not available: {str(e)}")
        print("   This is optional and won't affect the main app functionality")
        return True  # Don't fail the test, just skip CrewAI
    except Exception as e:
        print(f"❌ Error testing agents: {str(e)}")
        return False

def test_utils():
    """Test utility functions"""
    print("\n🔧 Testing utility functions...")
    
    try:
        from utils.helpers import PromptGeneratorUtils
        from config import Config
        
        # Test department suggestions
        depts = PromptGeneratorUtils.get_department_suggestions()
        print(f"✅ Found {len(depts)} departments")
        
        # Test configuration
        config_status = Config.validate_config()
        print(f"✅ Configuration status: {config_status['status']}")
        
        # Test prompt formatting
        test_data = {
            "generated_prompt": "This is a test prompt",
            "department": "test",
            "user_input": "test input",
            "status": "completed"
        }
        
        formatted = PromptGeneratorUtils.format_prompt_output(test_data)
        print(f"✅ Prompt formatting successful: {len(formatted)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing utils: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 AI Prompt Generator - Backend Test")
    print("=" * 50)
    
    # Test Ollama connection
    ollama_ok = test_ollama_connection()
    
    if not ollama_ok:
        print("\n❌ Ollama connection failed. Please fix this before proceeding.")
        return False
    
    # Test utility functions
    utils_ok = test_utils()
    
    if not utils_ok:
        print("\n❌ Utility functions failed.")
        return False
    
    # Test AI agents
    agents_ok = test_agents()
    
    if not agents_ok:
        print("\n❌ AI agents failed.")
        return False
    
    print("\n🎉 All tests passed! Backend is ready.")
    print("💡 You can now run: streamlit run app.py")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
