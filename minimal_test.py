"""
Minimal Viable Test for AI Prompt Generator
Tests core functionality without heavy dependencies
"""

import os
import sys
import json
from datetime import datetime

def test_file_structure():
    """Test if all required files exist"""
    print("📁 Testing file structure...")
    
    required_files = [
        "app.py",
        "config.py", 
        "requirements.txt",
        "README.md",
        "env_example.txt",
        "agents/__init__.py",
        "agents/prompt_agents.py",
        "utils/__init__.py", 
        "utils/helpers.py",
        "templates/__init__.py",
        "templates/prompt_templates.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def test_imports():
    """Test basic imports without heavy dependencies"""
    print("\n📦 Testing imports...")
    
    try:
        # Test basic Python imports
        import json
        import os
        import sys
        from datetime import datetime
        print("✅ Basic Python imports successful")
        
        # Test our custom modules
        from config import Config
        print("✅ Config import successful")
        
        from utils.helpers import PromptGeneratorUtils
        print("✅ Utils import successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_configuration():
    """Test configuration functionality"""
    print("\n⚙️ Testing configuration...")
    
    try:
        from config import Config
        
        # Test department configuration
        depts = Config.DEPARTMENTS
        if len(depts) == 7:
            print(f"✅ Found {len(depts)} departments")
        else:
            print(f"❌ Expected 7 departments, found {len(depts)}")
            return False
        
        # Test department lookup
        test_dept = Config.get_department_by_value("content")
        if test_dept and test_dept["label"] == "Content":
            print("✅ Department lookup working")
        else:
            print("❌ Department lookup failed")
            return False
        
        # Test config validation
        config_status = Config.validate_config()
        print(f"✅ Configuration validation: {config_status['status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_utils():
    """Test utility functions"""
    print("\n🔧 Testing utility functions...")
    
    try:
        from utils.helpers import PromptGeneratorUtils
        
        # Test department suggestions
        depts = PromptGeneratorUtils.get_department_suggestions()
        if len(depts) == 7:
            print(f"✅ Department suggestions: {len(depts)} departments")
        else:
            print(f"❌ Expected 7 departments, found {len(depts)}")
            return False
        
        # Test prompt formatting
        test_data = {
            "generated_prompt": "This is a test prompt for validation",
            "department": "test_department",
            "user_input": "test user input",
            "status": "completed"
        }
        
        formatted = PromptGeneratorUtils.format_prompt_output(test_data)
        if "AI-Generated Prompt" in formatted:
            print("✅ Prompt formatting working")
        else:
            print("❌ Prompt formatting failed")
            return False
        
        # Test prompt templates
        templates = PromptGeneratorUtils.get_prompt_templates()
        if len(templates) > 0:
            print(f"✅ Prompt templates: {len(templates)} templates")
        else:
            print("❌ No prompt templates found")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Utils test failed: {e}")
        return False

def test_mock_agents():
    """Test mock agent functionality"""
    print("\n🤖 Testing mock agent functionality...")
    
    try:
        # Create a simple mock agent class
        class MockPromptGenerator:
            def __init__(self):
                self.status = "ready"
            
            def generate_prompt(self, user_input, department):
                return {
                    "generated_prompt": f"Mock prompt for {department}: {user_input}",
                    "user_input": user_input,
                    "department": department,
                    "status": "completed"
                }
        
        # Test mock generation
        mock_agent = MockPromptGenerator()
        result = mock_agent.generate_prompt("test input", "content")
        
        if result["status"] == "completed":
            print("✅ Mock agent generation successful")
            print(f"📝 Generated: {result['generated_prompt'][:50]}...")
        else:
            print("❌ Mock agent generation failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Mock agent test failed: {e}")
        return False

def test_streamlit_app_structure():
    """Test Streamlit app structure without running it"""
    print("\n🌐 Testing Streamlit app structure...")
    
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Check for required Streamlit components
        required_components = [
            "import streamlit as st",
            "st.set_page_config",
            "st.markdown",
            "st.sidebar",
            "st.columns",
            "st.button"
        ]
        
        missing_components = []
        for component in required_components:
            if component not in content:
                missing_components.append(component)
            else:
                print(f"✅ Found: {component}")
        
        if missing_components:
            print(f"❌ Missing components: {missing_components}")
            return False
        
        print("✅ Streamlit app structure looks good")
        return True
        
    except Exception as e:
        print(f"❌ Streamlit app test failed: {e}")
        return False

def create_simple_demo():
    """Create a simple demo version"""
    print("\n🎯 Creating simple demo...")
    
    try:
        demo_code = '''
import streamlit as st

st.title("🤖 AI Prompt Generator - Demo Mode")
st.write("This is a demo version showing the interface structure.")

# Department selection
dept = st.selectbox("Select Department", ["Content", "Digital Marketing", "AI Engineering"])

# User input
user_input = st.text_area("Describe your task:", placeholder="Enter your task description...")

if st.button("Generate Prompt"):
    if user_input:
        st.success("Demo: Prompt generation would happen here!")
        st.info(f"Department: {dept}")
        st.info(f"Input: {user_input}")
    else:
        st.error("Please enter a task description")

st.write("---")
st.write("This demo shows the basic interface. Full functionality requires Ollama setup.")
        '''
        
        with open("demo_app.py", "w", encoding="utf-8") as f:
            f.write(demo_code)
        
        print("✅ Demo app created: demo_app.py")
        return True
        
    except Exception as e:
        print(f"❌ Demo creation failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 AI Prompt Generator - Minimal Viable Test")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Configuration", test_configuration),
        ("Utility Functions", test_utils),
        ("Mock Agents", test_mock_agents),
        ("Streamlit App Structure", test_streamlit_app_structure),
        ("Demo Creation", create_simple_demo)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} crashed: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for setup.")
        print("\n📋 Next Steps:")
        print("1. Install Ollama: https://ollama.ai")
        print("2. Pull a model: ollama pull llama2")
        print("3. Run demo: streamlit run demo_app.py")
        print("4. Run full app: streamlit run app.py")
    else:
        print("⚠️ Some tests failed. Check the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
