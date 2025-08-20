"""
Simple test for AI Mentor Chat functionality
"""

import os
import json
from dotenv import load_dotenv
from agents.gemini_agents import GeminiPromptGeneratorAgents

def test_simple_mentor_chat():
    """Test simple AI Mentor Chat functionality"""
    print("💬 Testing Simple AI Mentor Chat")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    try:
        agents = GeminiPromptGeneratorAgents()
        
        # Test 1: Simple mentor question
        print("\n1. Testing simple mentor question...")
        test_question = "How do I create a good prompt?"
        
        prompt = f"""You are a helpful AI mentor helping a user get started with prompt generation. 
        
        User just asked: "{test_question}"
        
        Provide a helpful, educational response that:
        1. Directly addresses their question/concern
        2. Provides guidance on how to use the prompt generator
        3. Maintains a friendly, mentor-like tone
        4. Gives examples of good requests they can make
        5. Helps them understand what kind of prompts they can generate
        
        Keep responses conversational and helpful. Focus on helping them get started with the right mindset."""
        
        response = agents._call_gemini_api(prompt, "AI Mentor")
        print(f"   Question: {test_question}")
        print(f"   Response: {response[:100]}...")
        print(f"   ✅ Response generated successfully")
        
        # Test 2: Check if response is meaningful
        if len(response) > 50:
            print(f"   ✅ Response is meaningful (length: {len(response)} chars)")
        else:
            print(f"   ❌ Response seems too short (length: {len(response)} chars)")
        
        # Test 3: Check for error indicators
        if "Error" in response or "error" in response.lower():
            print(f"   ❌ Response contains error indicators")
            return False
        else:
            print(f"   ✅ No error indicators found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mentor_chat_integration():
    """Test mentor chat integration with workflow"""
    print("\n\n🔄 Testing Mentor Chat Integration")
    print("=" * 50)
    
    try:
        agents = GeminiPromptGeneratorAgents()
        
        # Test workflow with a question that should trigger chat
        test_input = "What's the best way to create a marketing campaign?"
        
        print(f"Testing input: '{test_input}'")
        
        # Test intent analysis
        intent_result = agents.analyze_input_intent(test_input)
        print(f"Intent Analysis: {intent_result.get('intent_type', 'unknown')}")
        print(f"Confidence: {intent_result.get('confidence', 'unknown')}")
        
        # Test smart response generation
        smart_response = agents.generate_smart_response(test_input, intent_result)
        print(f"Smart Response Type: {smart_response.get('type', 'unknown')}")
        print(f"Smart Response Content: {smart_response.get('content', '')[:100]}...")
        
        # Test full workflow
        workflow_result = agents.process_interactive_workflow(test_input)
        print(f"Workflow State: {workflow_result.get('workflow_state', 'unknown')}")
        
        if workflow_result.get('workflow_state') == 'chat_mode':
            print("✅ Chat mode triggered correctly")
        else:
            print(f"❌ Expected chat_mode, got {workflow_result.get('workflow_state')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🚀 Simple AI Mentor Chat Test")
    print("=" * 60)
    
    # Test 1: Simple mentor chat
    test1_success = test_simple_mentor_chat()
    
    # Test 2: Integration test
    test2_success = test_mentor_chat_integration()
    
    if test1_success and test2_success:
        print("\n\n🎉 All tests passed! AI Mentor Chat should be working.")
        print("💡 If it's still not working in the app, check the Streamlit session state.")
    else:
        print("\n\n❌ Some tests failed. Check the errors above.")
    
    return test1_success and test2_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
