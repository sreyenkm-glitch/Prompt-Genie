"""
Debug script to test the current system with the exact user input
"""

import os
import json
from dotenv import load_dotenv
from agents.gemini_agents import GeminiPromptGeneratorAgents

def test_exact_user_input():
    """Test the exact user input to see what's happening"""
    print("🔍 Testing Exact User Input")
    print("=" * 50)
    
    # Exact user input
    user_input = "I want to create a data engineering project to build my portfolio and I am a fresher."
    
    print(f"User Input: '{user_input}'")
    print("\n" + "="*50)
    
    try:
        agents = GeminiPromptGeneratorAgents()
        
        # Step 1: Test department detection
        print("1. Testing Department Detection...")
        dept_result = agents.detect_department(user_input)
        print(f"   Detected Department: {dept_result['department']}")
        print(f"   Confidence: {dept_result['confidence']}")
        print(f"   Reasoning: {dept_result['reasoning']}")
        print(f"   Keywords: {dept_result['keywords_detected']}")
        
        # Step 2: Test initial questions
        print("\n2. Testing Initial Questions...")
        questions_result = agents.generate_interactive_questions(user_input, dept_result['department'])
        print(f"   Progress: {questions_result['progress_percentage']}%")
        print(f"   Next Step: {questions_result['next_step']}")
        print(f"   Number of Questions: {len(questions_result['questions'])}")
        print(f"   Is Complete: {questions_result.get('is_complete', False)}")
        
        for i, q in enumerate(questions_result['questions'], 1):
            print(f"   Question {i}: {q['question']}")
            if q.get('options'):
                print(f"      Options: {q['options']}")
        
        # Step 3: Test with sample answers
        print("\n3. Testing with Sample Answers...")
        sample_answers = {}
        for q in questions_result['questions']:
            if q.get('type') == 'multiple_choice' and q.get('options'):
                sample_answers[q['id']] = q['options'][0]
            else:
                sample_answers[q['id']] = "Sample answer for testing"
        
        print(f"   Sample Answers: {sample_answers}")
        
        continue_result = agents.continue_workflow(user_input, dept_result['department'], sample_answers)
        print(f"   Workflow State: {continue_result['workflow_state']}")
        
        if continue_result['workflow_state'] == 'complete':
            print("   ✅ Workflow completed!")
            print(f"   Final prompt length: {len(continue_result['final_prompt'])} characters")
            print("\n   Final Prompt Preview:")
            print("-" * 40)
            print(continue_result['final_prompt'][:500] + "...")
        else:
            print(f"   ⏳ More questions needed: {len(continue_result['questions']['questions'])}")
        
        return dept_result, questions_result, continue_result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None, None

def analyze_issues(dept_result, questions_result, continue_result):
    """Analyze what issues exist"""
    print("\n\n🔍 ISSUE ANALYSIS")
    print("=" * 50)
    
    issues = []
    
    # Check department detection
    if dept_result:
        expected_dept = "AI Engineering"
        actual_dept = dept_result['department']
        if actual_dept != expected_dept:
            issues.append(f"❌ Department Detection: Expected '{expected_dept}', got '{actual_dept}'")
        else:
            print(f"✅ Department Detection: Correctly detected '{actual_dept}'")
    
    # Check question quality
    if questions_result:
        num_questions = len(questions_result['questions'])
        if num_questions > 5:
            issues.append(f"❌ Too Many Questions: {num_questions} questions (should be 3-5 max)")
        else:
            print(f"✅ Question Count: {num_questions} questions (good)")
        
        # Check if questions are relevant to data engineering portfolio
        portfolio_keywords = ['portfolio', 'fresher', 'project', 'data engineering', 'skills']
        question_text = ' '.join([q['question'].lower() for q in questions_result['questions']])
        relevant_count = sum(1 for keyword in portfolio_keywords if keyword in question_text)
        if relevant_count < 2:
            issues.append(f"❌ Question Relevance: Only {relevant_count} portfolio-related questions")
        else:
            print(f"✅ Question Relevance: {relevant_count} portfolio-related questions (good)")
    
    # Check final output
    if continue_result and continue_result['workflow_state'] == 'complete':
        final_prompt = continue_result['final_prompt'].lower()
        portfolio_keywords = ['portfolio', 'fresher', 'entry-level', 'career', 'job']
        portfolio_count = sum(1 for keyword in portfolio_keywords if keyword in final_prompt)
        if portfolio_count < 3:
            issues.append(f"❌ Final Prompt: Only {portfolio_count} portfolio-related mentions")
        else:
            print(f"✅ Final Prompt: {portfolio_count} portfolio-related mentions (good)")
    
    if issues:
        print("\n🚨 ISSUES FOUND:")
        for issue in issues:
            print(f"   {issue}")
    else:
        print("\n✅ No major issues found!")
    
    return issues

def main():
    """Main debug function"""
    print("🚀 Debug Test - Data Engineering Portfolio Input")
    print("=" * 60)
    
    # Check API key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY not found in environment variables")
        return False
    
    print(f"✅ API Key found: {api_key[:10]}...")
    
    # Run the test
    dept_result, questions_result, continue_result = test_exact_user_input()
    
    # Analyze issues
    issues = analyze_issues(dept_result, questions_result, continue_result)
    
    return len(issues) == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
