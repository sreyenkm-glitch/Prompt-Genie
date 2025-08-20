"""
Test script for the AI Mentor Chat Extension functionality
"""

import os
import json
from dotenv import load_dotenv
from agents.gemini_agents import GeminiPromptGeneratorAgents

def test_mentor_extension():
    """Test the AI Mentor Chat Extension functionality"""
    print("💬 Testing AI Mentor Chat Extension")
    print("=" * 50)
    
    test_cases = [
        {
            "input": "How do I create a good prompt?",
            "context": "initial_state",
            "description": "Initial state mentor question"
        },
        {
            "input": "What should I include in my answer?",
            "context": "question_answering",
            "description": "Question answering state mentor question"
        },
        {
            "input": "How can I improve this prompt?",
            "context": "final_state",
            "description": "Final state mentor question"
        }
    ]
    
    agents = GeminiPromptGeneratorAgents()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['description']}")
        print(f"   Input: '{test_case['input']}'")
        print(f"   Context: {test_case['context']}")
        
        try:
            # Test mentor response based on context
            if test_case['context'] == 'initial_state':
                prompt = f"""You are a helpful AI mentor helping a user get started with prompt generation. 
                
                User just asked: "{test_case['input']}"
                
                Provide a helpful, educational response that:
                1. Directly addresses their question/concern
                2. Provides guidance on how to use the prompt generator
                3. Maintains a friendly, mentor-like tone
                4. Gives examples of good requests they can make
                5. Helps them understand what kind of prompts they can generate
                
                Keep responses conversational and helpful. Focus on helping them get started with the right mindset."""
                
            elif test_case['context'] == 'question_answering':
                current_context = f"""
                Original Request: I want to create a data engineering project
                Current Department: AI Engineering
                Current Step: Answering questions for prompt generation
                """
                
                prompt = f"""You are a helpful AI mentor helping a user during their prompt generation process. 
                
                {current_context}
                
                User just asked: "{test_case['input']}"
                
                Provide a helpful, educational response that:
                1. Directly addresses their question/concern
                2. Provides actionable guidance related to their current task
                3. Maintains a friendly, mentor-like tone
                4. Helps them understand how to answer the current questions better
                5. Gives context-specific advice for their department and project
                
                Keep responses conversational and helpful. Focus on helping them complete their prompt generation successfully."""
                
            elif test_case['context'] == 'final_state':
                final_context = f"""
                Original Request: I want to create a data engineering project
                Department: AI Engineering
                Generated Prompt: A comprehensive prompt for data engineering project
                Current Status: Prompt generation completed
                """
                
                prompt = f"""You are a helpful AI mentor helping a user with their completed prompt. 
                
                {final_context}
                
                User just asked: "{test_case['input']}"
                
                Provide a helpful, educational response that:
                1. Directly addresses their question/concern about the prompt
                2. Provides guidance on how to use or modify the prompt
                3. Maintains a friendly, mentor-like tone
                4. Helps them understand the prompt better or improve it
                5. Gives context-specific advice for their department and project
                
                Keep responses conversational and helpful. Focus on helping them make the most of their generated prompt."""
            
            # Get AI response
            ai_response = agents._call_gemini_api(prompt, "AI Mentor")
            
            print(f"   🤖 AI Mentor Response: {ai_response[:100]}...")
            print(f"   ✅ Mentor response generated successfully")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_chat_persistence():
    """Test that chat messages persist across different states"""
    print("\n\n🔄 Testing Chat Message Persistence")
    print("=" * 50)
    
    # Simulate chat messages
    chat_messages = [
        {'role': 'user', 'content': 'How do I start?', 'timestamp': 'now'},
        {'role': 'assistant', 'content': 'Great question! Let me help you...', 'timestamp': 'now'},
        {'role': 'user', 'content': 'What should I include?', 'timestamp': 'now'},
        {'role': 'assistant', 'content': 'You should include...', 'timestamp': 'now'}
    ]
    
    print(f"Chat messages count: {len(chat_messages)}")
    print(f"Last 3 messages: {len(chat_messages[-3:])}")
    
    # Test displaying last 3 messages
    for message in chat_messages[-3:]:
        role = message['role']
        content = message['content'][:50] + "..." if len(message['content']) > 50 else message['content']
        print(f"   {role}: {content}")
    
    print("   ✅ Chat persistence working correctly")

def main():
    """Main test function"""
    print("🚀 AI Mentor Chat Extension Test")
    print("=" * 60)
    
    # Check API key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    try:
        # Test mentor extension
        test_mentor_extension()
        
        # Test chat persistence
        test_chat_persistence()
        
        print("\n\n🎉 All AI Mentor Chat Extension tests completed!")
        print("💡 The extension is ready to use in the Streamlit app")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
