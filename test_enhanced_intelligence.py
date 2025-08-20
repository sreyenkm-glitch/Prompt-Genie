"""
Test script for the enhanced intelligence layer
"""

import os
import json
from dotenv import load_dotenv
from agents.gemini_agents import GeminiPromptGeneratorAgents

def test_enhanced_intelligence():
    """Test the enhanced intelligence layer with different input types"""
    print("🧠 Testing Enhanced Intelligence Layer")
    print("=" * 60)
    
    test_cases = [
        {
            "input": "What's the best way to create a marketing campaign?",
            "expected_type": "question",
            "description": "Question input"
        },
        {
            "input": "I need ideas for a data engineering portfolio project",
            "expected_type": "suggestion_request",
            "description": "Suggestion request input"
        },
        {
            "input": "I want to create a social media campaign for our new product",
            "expected_type": "direct_request",
            "description": "Direct request input"
        },
        {
            "input": "How do I build a machine learning model?",
            "expected_type": "question",
            "description": "Technical question input"
        },
        {
            "input": "Give me suggestions for content marketing strategies",
            "expected_type": "suggestion_request",
            "description": "Content suggestion request"
        }
    ]
    
    agents = GeminiPromptGeneratorAgents()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['description']}")
        print(f"   Input: '{test_case['input']}'")
        print(f"   Expected: {test_case['expected_type']}")
        
        try:
            # Test intent analysis
            intent_analysis = agents.analyze_input_intent(test_case['input'])
            print(f"   Detected: {intent_analysis['intent_type']}")
            print(f"   Confidence: {intent_analysis['confidence']}")
            
            # Test smart response generation
            smart_response = agents.generate_smart_response(test_case['input'], intent_analysis)
            print(f"   Response Type: {smart_response['type']}")
            print(f"   Next Action: {smart_response['next_action']}")
            
            # Test full workflow
            workflow_result = agents.process_interactive_workflow(test_case['input'])
            print(f"   Workflow State: {workflow_result['workflow_state']}")
            
            if workflow_result['workflow_state'] == 'smart_response':
                print(f"   ✅ Smart response generated successfully")
            elif workflow_result['workflow_state'] == 'awaiting_answers':
                print(f"   ✅ Direct to prompt generation")
            else:
                print(f"   ⚠️ Unexpected workflow state")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_smart_response_flow():
    """Test the complete smart response flow"""
    print("\n\n🔄 Testing Complete Smart Response Flow")
    print("=" * 50)
    
    test_input = "I need ideas for a data engineering portfolio project"
    
    print(f"Test Input: '{test_input}'")
    
    try:
        agents = GeminiPromptGeneratorAgents()
        
        # Step 1: Process workflow
        print("\n1. Processing workflow...")
        workflow_result = agents.process_interactive_workflow(test_input)
        
        if workflow_result['workflow_state'] == 'smart_response':
            print("   ✅ Smart response detected")
            
            # Step 2: Simulate user choice
            print("\n2. Simulating user choice...")
            user_choice = "I want to work on option 1 - ETL Pipeline for E-commerce Data"
            
            continue_result = agents.continue_from_smart_response(
                workflow_result['original_request'],
                user_choice
            )
            
            print(f"   Workflow State: {continue_result['workflow_state']}")
            print(f"   Department: {continue_result['department_detected']['department']}")
            print(f"   Questions: {len(continue_result['questions']['questions'])}")
            
            # Step 3: Test with sample answers
            print("\n3. Testing with sample answers...")
            sample_answers = {}
            for q in continue_result['questions']['questions']:
                if q.get('type') == 'multiple_choice' and q.get('options'):
                    sample_answers[q['id']] = q['options'][0]
                else:
                    sample_answers[q['id']] = "Sample answer for testing"
            
            final_result = agents.continue_workflow(
                continue_result['original_request'],
                continue_result['department_detected']['department'],
                sample_answers
            )
            
            if final_result['workflow_state'] == 'complete':
                print("   ✅ Complete flow successful!")
                print(f"   Final prompt length: {len(final_result['final_prompt'])} characters")
            else:
                print(f"   ⏳ More questions needed")
        
        else:
            print("   ❌ Expected smart response but got different workflow state")
    
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    """Main test function"""
    print("🚀 Enhanced Intelligence Layer Test")
    print("=" * 60)
    
    # Check API key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    try:
        # Test individual components
        test_enhanced_intelligence()
        
        # Test complete flow
        test_smart_response_flow()
        
        print("\n\n🎉 All enhanced intelligence tests completed!")
        print("💡 You can now run: streamlit run app.py")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
