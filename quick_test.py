"""
Quick test to verify system components
"""

import os
from dotenv import load_dotenv

def quick_test():
    print("🚀 Quick System Test")
    print("=" * 30)
    
    # Load environment
    load_dotenv()
    
    # Check API key
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print("✅ API Key: Found")
    else:
        print("❌ API Key: Not found")
        return
    
    # Test imports
    try:
        from agents.gemini_agents import GeminiPromptGeneratorAgents
        print("✅ Gemini Agents: Import successful")
    except Exception as e:
        print(f"❌ Gemini Agents: {e}")
        return
    
    try:
        from utils.helpers import PromptGeneratorUtils
        print("✅ Utils: Import successful")
    except Exception as e:
        print(f"❌ Utils: {e}")
        return
    
    try:
        from config import Config
        print("✅ Config: Import successful")
    except Exception as e:
        print(f"❌ Config: {e}")
        return
    
    # Test basic functionality
    try:
        agents = GeminiPromptGeneratorAgents()
        print("✅ Agents: Initialized successfully")
        
        # Quick API test
        result = agents._call_gemini_api("Say hello", "Test")
        if "Error" not in result:
            print("✅ API: Working correctly")
            print(f"📝 Sample response: {result[:50]}...")
        else:
            print(f"❌ API: {result}")
            
    except Exception as e:
        print(f"❌ Agents: {e}")
    
    print("\n🎯 Next Steps:")
    print("1. Run: streamlit run app.py")
    print("2. Or run: streamlit run demo_app.py")

if __name__ == "__main__":
    quick_test()
