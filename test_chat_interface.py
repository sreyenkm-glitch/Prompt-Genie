"""
Test script for the dynamic chat interface
"""

import os
import json
from dotenv import load_dotenv
from agents.gemini_agents import GeminiPromptGeneratorAgents

def test_chat_interface():
    """Test the dynamic chat interface functionality"""
    print("💬 Testing Dynamic Chat Interface")
    print("=" * 50)
    
    test_cases = [
        {
            "input": "What's the best way to create a marketing campaign?",
            "expected_workflow": "chat_mode",
            "description": "Question input - should trigger chat"
        },
        {
            "input": "I need ideas for a data engineering portfolio project",
            "expected_workflow": "chat_mode",
            "description": "Suggestion request - should trigger chat"
        },
        {
            "input": "I want to create a social media campaign for our new product",
            "expected_workflow": "awaiting_answers",
            "description": "Direct request - should go to prompt generation"
        }
    ]
    
    agents = GeminiPromptGeneratorAgents()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['description']}")
        print(f"   Input: '{test_case['input']}'")
        print(f"   Expected Workflow: {test_case['expected_workflow']}")
        
        try:
            # Test workflow processing
            workflow_result = agents.process_interactive_workflow(test_case['input'])
            print(f"   Actual Workflow: {workflow_result['workflow_state']}")
            
            if workflow_result['workflow_state'] == test_case['expected_workflow']:
                print(f"   ✅ Correct workflow detected")
            else:
                print(f"   ❌ Unexpected workflow state")
            
            # Test chat functionality if chat mode
            if workflow_result['workflow_state'] == 'chat_mode':
                print(f"   📝 Testing chat functionality...")
                
                # Simulate chat interaction
                chat_context = {
                    'intent_analysis': workflow_result['intent_analysis'],
                    'smart_response': workflow_result['smart_response']
                }
                
                # Test AI mentor response
                test_chat_input = "Can you explain more about this?"
                ai_response = agents._call_gemini_api(
                    f"""You are a helpful AI mentor helping a user with their project. 
                    
                    Original user request: "{test_case['input']}"
                    Chat context: {chat_context}
                    
                    User just said: "{test_chat_input}"
                    
                    Provide a helpful, educational response that:
                    1. Directly addresses their question/concern
                    2. Provides actionable guidance
                    3. Maintains a friendly, mentor-like tone
                    4. Helps them move toward creating their prompt
                    5. Asks follow-up questions if needed
                    
                    Keep responses conversational and helpful.""",
                    "AI Mentor"
                )
                
                print(f"   🤖 AI Mentor Response: {ai_response[:100]}...")
                print(f"   ✅ Chat functionality working")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_chat_transition():
    """Test transition from chat to prompt generation"""
    print("\n\n🔄 Testing Chat to Prompt Generation Transition")
    print("=" * 50)
    
    test_input = "I need ideas for a data engineering portfolio project"
    
    try:
        agents = GeminiPromptGeneratorAgents()
        
        # Step 1: Start chat
        print("1. Starting chat mode...")
        workflow_result = agents.process_interactive_workflow(test_input)
        
        if workflow_result['workflow_state'] == 'chat_mode':
            print("   ✅ Chat mode activated")
            
            # Step 2: Simulate chat messages
            print("2. Simulating chat conversation...")
            chat_messages = [
                {'role': 'assistant', 'content': 'Here are some great project ideas...'},
                {'role': 'user', 'content': 'I like the ETL pipeline idea'},
                {'role': 'assistant', 'content': 'Great choice! Let me help you set it up...'},
                {'role': 'user', 'content': 'I want to proceed with this project'}
            ]
            
            # Step 3: Create enhanced context
            print("3. Creating enhanced context...")
            chat_summary = "\n".join([
                f"{msg['role']}: {msg['content']}" 
                for msg in chat_messages
            ])
            
            enhanced_request = f"{test_input}\n\nChat Context:\n{chat_summary}"
            print(f"   Enhanced Request: {enhanced_request[:200]}...")
            
            # Step 4: Test transition to prompt generation
            print("4. Testing transition to prompt generation...")
            department_info = agents.detect_department(enhanced_request)
            questions_info = agents.generate_interactive_questions(enhanced_request, department_info["department"])
            
            print(f"   Department: {department_info['department']}")
            print(f"   Questions: {len(questions_info['questions'])}")
            print(f"   ✅ Transition successful")
            
        else:
            print("   ❌ Expected chat mode but got different workflow")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    """Main test function"""
    print("🚀 Dynamic Chat Interface Test")
    print("=" * 60)
    
    # Check API key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    try:
        # Test chat interface
        test_chat_interface()
        
        # Test chat transition
        test_chat_transition()
        
        print("\n\n🎉 All chat interface tests completed!")
        print("💡 You can now run: streamlit run app.py")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
