"""
Debug script for the specific input that caused the error
"""

import os
import json
from dotenv import load_dotenv
from agents.gemini_agents import GeminiPromptGeneratorAgents

def debug_specific_input():
    """Debug the specific input that caused the error"""
    print("🔍 Debugging Specific Input")
    print("=" * 50)
    
    # The exact input that caused the error
    user_input = "I want to create a app that tracks website traffic and suggests optimizations i am doing this to build my portfolio and I am a fresher"
    
    print(f"User Input: '{user_input}'")
    print("\n" + "="*50)
    
    try:
        agents = GeminiPromptGeneratorAgents()
        
        # Step 1: Test workflow processing
        print("1. Testing workflow processing...")
        workflow_result = agents.process_interactive_workflow(user_input)
        
        print(f"   Workflow State: {workflow_result['workflow_state']}")
        print(f"   Keys in result: {list(workflow_result.keys())}")
        
        # Step 2: Check if department_detected exists
        if 'department_detected' in workflow_result:
            print(f"   ✅ department_detected exists")
            print(f"   Department: {workflow_result['department_detected']}")
        else:
            print(f"   ❌ department_detected missing")
            print(f"   Available keys: {list(workflow_result.keys())}")
        
        # Step 3: Check if questions exists
        if 'questions' in workflow_result:
            print(f"   ✅ questions exists")
            print(f"   Questions count: {len(workflow_result['questions'].get('questions', []))}")
        else:
            print(f"   ❌ questions missing")
        
        # Step 4: Check if original_request exists
        if 'original_request' in workflow_result:
            print(f"   ✅ original_request exists")
            print(f"   Request: {workflow_result['original_request']}")
        else:
            print(f"   ❌ original_request missing")
        
        return workflow_result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main debug function"""
    print("🚀 Debug Specific Input")
    print("=" * 60)
    
    # Check API key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Run the debug
    result = debug_specific_input()
    
    if result:
        print("\n\n🎉 Debug completed!")
        print("💡 Check the output above for the issue")
    else:
        print("\n\n❌ Debug failed!")
    
    return result is not None

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
