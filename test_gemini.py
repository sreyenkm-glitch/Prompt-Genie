"""
Test script for Gemini API integration
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_api():
    """Test Gemini API connection"""
    print("🔍 Testing Gemini API connection...")
    
    try:
        from agents.gemini_agents import GeminiPromptGeneratorAgents
        
        # Initialize agents
        print("📦 Initializing Gemini agents...")
        agents = GeminiPromptGeneratorAgents()
        print("✅ Gemini agents initialized successfully")
        
        # Test API call
        print("🧪 Testing API call...")
        test_result = agents._call_gemini_api("Hello, this is a test", "Test Agent")
        
        if "Error" in test_result:
            print(f"❌ API call failed: {test_result}")
            return False
        else:
            print("✅ API call successful!")
            print(f"📝 Response: {test_result[:100]}...")
            return True
            
    except Exception as e:
        print(f"❌ Error testing Gemini API: {str(e)}")
        return False

def test_prompt_generation():
    """Test prompt generation"""
    print("\n🤖 Testing prompt generation...")
    
    try:
        from agents.gemini_agents import GeminiPromptGeneratorAgents
        
        # Initialize agents
        agents = GeminiPromptGeneratorAgents()
        
        # Test prompt generation
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
            
    except Exception as e:
        print(f"❌ Error testing prompt generation: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 AI Prompt Generator - Gemini API Test")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("💡 Please add your Gemini API key to .env file")
        return False
    
    print(f"✅ Found API key: {api_key[:10]}...")
    
    # Test API connection
    api_ok = test_gemini_api()
    
    if not api_ok:
        print("\n❌ Gemini API connection failed.")
        return False
    
    # Test prompt generation
    generation_ok = test_prompt_generation()
    
    if not generation_ok:
        print("\n❌ Prompt generation failed.")
        return False
    
    print("\n🎉 All tests passed! Gemini API integration is working.")
    print("💡 You can now run: streamlit run app.py")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
