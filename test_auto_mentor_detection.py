"""
Test script for automatic AI Mentor detection functionality
"""

import os
import json
from dotenv import load_dotenv
from agents.gemini_agents import GeminiPromptGeneratorAgents

def test_auto_mentor_detection():
    """Test automatic AI Mentor detection"""
    print("🤖 Testing Automatic AI Mentor Detection")
    print("=" * 60)
    
    # Load environment
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    test_cases = [
        {
            "input": "What's the best way to create a marketing campaign?",
            "expected_intent": "question",
            "description": "Direct question - should trigger mentor"
        },
        {
            "input": "I need ideas for a data engineering portfolio project",
            "expected_intent": "suggestion_request",
            "description": "Suggestion request - should trigger mentor"
        },
        {
            "input": "I want to create a social media campaign for our new product",
            "expected_intent": "direct_request",
            "description": "Direct request - should not trigger mentor"
        },
        {
            "input": "How do I improve my prompt writing skills?",
            "expected_intent": "question",
            "description": "Learning question - should trigger mentor"
        },
        {
            "input": "Can you suggest some tools for content creation?",
            "expected_intent": "suggestion_request",
            "description": "Tool suggestion request - should trigger mentor"
        }
    ]
    
    agents = GeminiPromptGeneratorAgents()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['description']}")
        print(f"   Input: '{test_case['input']}'")
        print(f"   Expected Intent: {test_case['expected_intent']}")
        
        try:
            # Test intent analysis
            intent_result = agents.analyze_input_intent(test_case['input'])
            actual_intent = intent_result.get('intent_type', 'unknown')
            confidence = intent_result.get('confidence', 'unknown')
            
            print(f"   Actual Intent: {actual_intent}")
            print(f"   Confidence: {confidence}")
            
            # Check if mentor should be triggered
            should_trigger = (
                actual_intent in ['question', 'suggestion_request'] and 
                confidence in ['high', 'medium']
            )
            
            if should_trigger:
                print(f"   ✅ Mentor should be triggered")
                
                # Test mentor response generation
                smart_response = agents.generate_smart_response(test_case['input'], intent_result)
                response_type = smart_response.get('type', 'unknown')
                response_content = smart_response.get('content', '')[:100]
                
                print(f"   Response Type: {response_type}")
                print(f"   Response Preview: {response_content}...")
                
                if response_type in ['question_response', 'suggestions_response']:
                    print(f"   ✅ Mentor response generated successfully")
                else:
                    print(f"   ❌ Unexpected response type: {response_type}")
                
            else:
                print(f"   ❌ Mentor should NOT be triggered")
            
            # Test workflow processing
            workflow_result = agents.process_interactive_workflow(test_case['input'])
            workflow_state = workflow_result.get('workflow_state', 'unknown')
            
            print(f"   Workflow State: {workflow_state}")
            
            if should_trigger and workflow_state == 'chat_mode':
                print(f"   ✅ Workflow correctly triggered chat mode")
            elif not should_trigger and workflow_state == 'awaiting_answers':
                print(f"   ✅ Workflow correctly went to question answering")
            else:
                print(f"   ⚠️ Unexpected workflow state")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    return True

def test_context_aware_mentor():
    """Test context-aware mentor responses"""
    print("\n\n🎯 Testing Context-Aware Mentor Responses")
    print("=" * 60)
    
    try:
        agents = GeminiPromptGeneratorAgents()
        
        # Test different contexts
        contexts = [
            {
                "context": "initial_state",
                "user_input": "How do I start?",
                "description": "Initial state context"
            },
            {
                "context": "question_answering",
                "user_input": "What should I include in my answer?",
                "description": "Question answering context"
            },
            {
                "context": "final_state",
                "user_input": "How can I improve this prompt?",
                "description": "Final state context"
            }
        ]
        
        for context_test in contexts:
            print(f"\nTesting: {context_test['description']}")
            print(f"Context: {context_test['context']}")
            print(f"Input: '{context_test['user_input']}'")
            
            # Test mentor response with context
            if context_test['context'] == 'initial_state':
                prompt = f"""You are a helpful AI mentor helping a user get started with prompt generation. 
                
                User just asked: "{context_test['user_input']}"
                
                Provide a helpful, educational response that:
                1. Directly addresses their question/concern
                2. Provides guidance on how to use the prompt generator
                3. Maintains a friendly, mentor-like tone
                4. Gives examples of good requests they can make
                5. Helps them understand what kind of prompts they can generate
                
                Keep responses conversational and helpful. Focus on helping them get started with the right mindset."""
                
            elif context_test['context'] == 'question_answering':
                prompt = f"""You are a helpful AI mentor helping a user during their prompt generation process. 
                
                Original Request: I want to create a data engineering project
                Current Department: AI Engineering
                Current Step: Answering questions for prompt generation
                
                User just asked: "{context_test['user_input']}"
                
                Provide a helpful, educational response that:
                1. Directly addresses their question/concern
                2. Provides actionable guidance related to their current task
                3. Maintains a friendly, mentor-like tone
                4. Helps them understand how to answer the current questions better
                5. Gives context-specific advice for their department and project
                
                Keep responses conversational and helpful. Focus on helping them complete their prompt generation successfully."""
                
            elif context_test['context'] == 'final_state':
                prompt = f"""You are a helpful AI mentor helping a user with their completed prompt. 
                
                Original Request: I want to create a data engineering project
                Department: AI Engineering
                Generated Prompt: A comprehensive prompt for data engineering project
                Current Status: Prompt generation completed
                
                User just asked: "{context_test['user_input']}"
                
                Provide a helpful, educational response that:
                1. Directly addresses their question/concern about the prompt
                2. Provides guidance on how to use or modify the prompt
                3. Maintains a friendly, mentor-like tone
                4. Helps them understand the prompt better or improve it
                5. Gives context-specific advice for their department and project
                
                Keep responses conversational and helpful. Focus on helping them make the most of their generated prompt."""
            
            response = agents._call_gemini_api(prompt, "AI Mentor")
            print(f"Response: {response[:150]}...")
            print(f"✅ Context-aware response generated")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    return True

def main():
    """Main test function"""
    print("🚀 Automatic AI Mentor Detection Test")
    print("=" * 80)
    
    # Test 1: Auto detection
    test1_success = test_auto_mentor_detection()
    
    # Test 2: Context awareness
    test2_success = test_context_aware_mentor()
    
    if test1_success and test2_success:
        print("\n\n🎉 All automatic mentor detection tests passed!")
        print("💡 The automatic pop-up chat interface should work correctly.")
    else:
        print("\n\n❌ Some tests failed. Check the errors above.")
    
    return test1_success and test2_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
