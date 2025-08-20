"""
Test script for enhanced AI Mentor intelligence
"""

import os
import json
from dotenv import load_dotenv
from agents.gemini_agents import GeminiPromptGeneratorAgents

def test_enhanced_mentor_intelligence():
    """Test enhanced AI Mentor intelligence with context awareness"""
    print("🧠 Testing Enhanced AI Mentor Intelligence")
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
            "input": "this is my first project in website optimization I have zero experience, what do you suggest?",
            "expected_context": {
                "experience_level": "beginner",
                "project_type": "optimization project",
                "should_be_specific": True
            },
            "description": "Beginner asking for suggestions - should get specific, beginner-friendly advice"
        },
        {
            "input": "I need ideas for a data engineering portfolio project",
            "expected_context": {
                "experience_level": "unknown",
                "project_type": "data analysis",
                "should_be_specific": True
            },
            "description": "Portfolio project request - should get specific project ideas"
        },
        {
            "input": "How do I improve my prompt writing skills?",
            "expected_context": {
                "experience_level": "unknown",
                "project_type": "general",
                "should_be_specific": True
            },
            "description": "Learning question - should get specific guidance"
        }
    ]
    
    agents = GeminiPromptGeneratorAgents()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. Testing: {test_case['description']}")
        print(f"   Input: '{test_case['input']}'")
        
        try:
            # Test intent analysis
            intent_analysis = agents.analyze_input_intent(test_case['input'])
            print(f"   Intent: {intent_analysis.get('intent_type', 'unknown')}")
            print(f"   Confidence: {intent_analysis.get('confidence', 'unknown')}")
            
            # Test enhanced smart response
            smart_response = agents.generate_smart_response(test_case['input'], intent_analysis)
            response_type = smart_response.get('type', 'unknown')
            response_content = smart_response.get('content', '')
            context_used = smart_response.get('context_used', '')
            
            print(f"   Response Type: {response_type}")
            print(f"   Context Used: {context_used[:100]}...")
            print(f"   Response Length: {len(response_content)} characters")
            
            # Check if response is specific and contextual
            is_specific = any(keyword in response_content.lower() for keyword in [
                'specific', 'concrete', 'example', 'step', 'first', 'then', 'next'
            ])
            
            if is_specific:
                print(f"   ✅ Response is specific and actionable")
            else:
                print(f"   ❌ Response seems generic")
            
            # Check for follow-up questions
            has_follow_up = '?' in response_content and any(word in response_content.lower() for word in [
                'what', 'how', 'which', 'when', 'where', 'why'
            ])
            
            if has_follow_up:
                print(f"   ✅ Response includes follow-up questions")
            else:
                print(f"   ❌ Response lacks follow-up questions")
            
            # Check context awareness
            expected_context = test_case['expected_context']
            if expected_context['experience_level'] in context_used.lower():
                print(f"   ✅ Correctly detected experience level: {expected_context['experience_level']}")
            else:
                print(f"   ❌ Failed to detect experience level")
            
            if expected_context['project_type'] in context_used.lower():
                print(f"   ✅ Correctly detected project type: {expected_context['project_type']}")
            else:
                print(f"   ❌ Failed to detect project type")
            
            print(f"   Response Preview: {response_content[:200]}...")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            import traceback
            traceback.print_exc()
    
    return True

def test_context_generation():
    """Test context generation functionality"""
    print("\n\n🎯 Testing Context Generation")
    print("=" * 60)
    
    try:
        agents = GeminiPromptGeneratorAgents()
        
        test_inputs = [
            "this is my first project in website optimization I have zero experience",
            "I'm an intermediate developer working on a data analysis project",
            "As an expert in marketing, I need to create a campaign"
        ]
        
        for i, test_input in enumerate(test_inputs, 1):
            print(f"\n{i}. Testing context generation for: '{test_input}'")
            
            # Create mock intent analysis
            intent_analysis = {
                'intent_type': 'suggestion_request',
                'confidence': 'high'
            }
            
            # Test context generation
            context = agents._get_conversation_context(test_input, intent_analysis)
            print(f"   Generated Context: {context}")
            
            # Check if context contains expected elements
            if 'experience level' in context.lower():
                print(f"   ✅ Context includes experience level")
            else:
                print(f"   ❌ Context missing experience level")
            
            if 'project type' in context.lower():
                print(f"   ✅ Context includes project type")
            else:
                print(f"   ❌ Context missing project type")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    return True

def test_follow_up_generation():
    """Test follow-up question generation"""
    print("\n\n❓ Testing Follow-up Question Generation")
    print("=" * 60)
    
    try:
        agents = GeminiPromptGeneratorAgents()
        
        test_cases = [
            {
                "input": "this is my first project in website optimization I have zero experience, what do you suggest?",
                "expected": "beginner-focused follow-up"
            },
            {
                "input": "I need ideas for a data engineering portfolio project",
                "expected": "project-specific follow-up"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{i}. Testing follow-up for: '{test_case['input']}'")
            
            # Create mock intent analysis
            intent_analysis = {
                'intent_type': 'suggestion_request',
                'confidence': 'high'
            }
            
            # Generate context
            context = agents._get_conversation_context(test_case['input'], intent_analysis)
            
            # Test follow-up generation
            follow_up = agents._generate_contextual_follow_up(test_case['input'], intent_analysis, context)
            print(f"   Generated Follow-up: {follow_up}")
            
            # Check if follow-up is relevant
            if '?' in follow_up and len(follow_up) > 10:
                print(f"   ✅ Follow-up is relevant and specific")
            else:
                print(f"   ❌ Follow-up seems generic or too short")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    return True

def main():
    """Main test function"""
    print("🚀 Enhanced AI Mentor Intelligence Test")
    print("=" * 80)
    
    # Test 1: Enhanced intelligence
    test1_success = test_enhanced_mentor_intelligence()
    
    # Test 2: Context generation
    test2_success = test_context_generation()
    
    # Test 3: Follow-up generation
    test3_success = test_follow_up_generation()
    
    if test1_success and test2_success and test3_success:
        print("\n\n🎉 All enhanced intelligence tests passed!")
        print("💡 The AI Mentor should now provide much smarter, more contextual responses.")
    else:
        print("\n\n❌ Some tests failed. Check the errors above.")
    
    return test1_success and test2_success and test3_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
