"""
Test script for the new interactive workflow
"""

import os
import json
from dotenv import load_dotenv
from agents.gemini_agents import GeminiPromptGeneratorAgents

def test_department_detection():
    """Test department detection functionality"""
    print("🔍 Testing Department Detection")
    print("=" * 50)
    
    test_cases = [
        "I want to create a social media campaign for our new product",
        "Analyze customer data to understand buying patterns",
        "Build a machine learning model for fraud detection",
        "Create content strategy for our blog",
        "Optimize our digital operations workflow",
        "Implement marketing automation tools",
        "Develop AI solutions for customer service"
    ]
    
    agents = GeminiPromptGeneratorAgents()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: '{test_case}'")
        try:
            result = agents.detect_department(test_case)
            print(f"   Department: {result['department']}")
            print(f"   Confidence: {result['confidence']}")
            print(f"   Reasoning: {result['reasoning']}")
            print(f"   Keywords: {result['keywords_detected']}")
        except Exception as e:
            print(f"   Error: {e}")

def test_interactive_questions():
    """Test interactive question generation"""
    print("\n\n📝 Testing Interactive Questions")
    print("=" * 50)
    
    test_request = "I want to create a social media campaign for our new product"
    test_department = "Digital Marketing"
    
    agents = GeminiPromptGeneratorAgents()
    
    # Test initial questions
    print(f"\n1. Initial questions for: '{test_request}'")
    print(f"   Department: {test_department}")
    
    try:
        questions = agents.generate_interactive_questions(test_request, test_department)
        print(f"   Progress: {questions['progress_percentage']}%")
        print(f"   Next Step: {questions['next_step']}")
        print(f"   Questions: {len(questions['questions'])}")
        
        for q in questions['questions']:
            print(f"   - {q['question']}")
            if q.get('options'):
                print(f"     Options: {q['options']}")
    
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test with some answers
    print(f"\n2. Follow-up questions with answers")
    user_answers = {
        "q1": "Increase brand awareness",
        "q2": "Instagram and Facebook",
        "q3": "5000-10000"
    }
    
    try:
        follow_up = agents.generate_interactive_questions(test_request, test_department, user_answers)
        print(f"   Progress: {follow_up['progress_percentage']}%")
        print(f"   Is Complete: {follow_up['is_complete']}")
        print(f"   Questions: {len(follow_up['questions'])}")
        
        for q in follow_up['questions']:
            print(f"   - {q['question']}")
    
    except Exception as e:
        print(f"   Error: {e}")

def test_complete_workflow():
    """Test the complete interactive workflow"""
    print("\n\n🔄 Testing Complete Workflow")
    print("=" * 50)
    
    test_request = "I want to create a cooking app for my mom"
    
    agents = GeminiPromptGeneratorAgents()
    
    print(f"Original Request: '{test_request}'")
    
    try:
        # Step 1: Start workflow
        print("\n1. Starting workflow...")
        workflow_result = agents.process_interactive_workflow(test_request)
        
        department = workflow_result['department_detected']['department']
        print(f"   Department Detected: {department}")
        print(f"   Confidence: {workflow_result['department_detected']['confidence']}")
        print(f"   Initial Questions: {len(workflow_result['questions']['questions'])}")
        
        # Step 2: Simulate user answers
        print("\n2. Simulating user answers...")
        user_answers = {}
        for q in workflow_result['questions']['questions']:
            if q.get('type') == 'multiple_choice' and q.get('options'):
                user_answers[q['id']] = q['options'][0]  # Choose first option
            else:
                user_answers[q['id']] = "Sample answer for testing"
        
        print(f"   Answers provided: {len(user_answers)}")
        
        # Step 3: Continue workflow
        print("\n3. Continuing workflow...")
        continue_result = agents.continue_workflow(test_request, department, user_answers)
        
        if continue_result['workflow_state'] == 'complete':
            print("   ✅ Workflow completed!")
            print(f"   Final prompt length: {len(continue_result['final_prompt'])} characters")
            print(f"   Summary: {continue_result['summary']}")
        else:
            print(f"   ⏳ Workflow continues... Progress: {continue_result['progress']}%")
            print(f"   More questions: {len(continue_result['questions']['questions'])}")
    
    except Exception as e:
        print(f"   Error: {e}")

def main():
    """Main test function"""
    print("🚀 Interactive Workflow Test")
    print("=" * 60)
    
    # Check API key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        print("💡 Please add your Gemini API key to .env file")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    try:
        # Test individual components
        test_department_detection()
        test_interactive_questions()
        test_complete_workflow()
        
        print("\n\n🎉 All tests completed!")
        print("💡 You can now run: streamlit run app.py")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
