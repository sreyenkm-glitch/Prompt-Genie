#!/usr/bin/env python3
"""
Deployment Test Script
Tests all imports and basic functionality before Streamlit Cloud deployment
"""

import sys
import os

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing imports...")
    
    try:
        import streamlit as st
        print("✅ streamlit imported successfully")
    except ImportError as e:
        print(f"❌ streamlit import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ numpy imported successfully")
    except ImportError as e:
        print(f"❌ numpy import failed: {e}")
        return False
    
    try:
        import yaml
        print("✅ pyyaml imported successfully")
    except ImportError as e:
        print(f"❌ pyyaml import failed: {e}")
        return False
    
    try:
        import google.generativeai
        print("✅ google-generativeai imported successfully")
    except ImportError as e:
        print(f"❌ google-generativeai import failed: {e}")
        return False
    
    try:
        from agents.gemini_agents import GeminiPromptGeneratorAgents
        print("✅ GeminiPromptGeneratorAgents imported successfully")
    except ImportError as e:
        print(f"❌ GeminiPromptGeneratorAgents import failed: {e}")
        return False
    
    try:
        from utils.helpers import PromptGeneratorUtils
        print("✅ PromptGeneratorUtils imported successfully")
    except ImportError as e:
        print(f"❌ PromptGeneratorUtils import failed: {e}")
        return False
    
    try:
        from config import Config
        print("✅ Config imported successfully")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    # Test CrewAI imports (optional)
    try:
        from agents.prompt_agents import PromptGeneratorAgents
        print("✅ PromptGeneratorAgents (CrewAI) imported successfully")
    except ImportError as e:
        print(f"⚠️  PromptGeneratorAgents (CrewAI) import failed: {e}")
        print("   This is optional and won't affect main app functionality")
    
    return True

def test_environment():
    """Test environment setup"""
    print("\n🔍 Testing environment...")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
    else:
        print("⚠️  .env file not found (will use environment variables)")
    
    # Check for required directories
    required_dirs = ['agents', 'utils', 'templates', 'history']
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ directory found")
        else:
            print(f"❌ {dir_name}/ directory missing")
            return False
    
    # Check for required files
    required_files = ['app.py', 'config.py', 'requirements.txt']
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ {file_name} found")
        else:
            print(f"❌ {file_name} missing")
            return False
    
    return True

def test_config():
    """Test configuration loading"""
    print("\n🔍 Testing configuration...")
    
    try:
        from config import Config
        config = Config()
        print("✅ Config loaded successfully")
        print(f"   App Title: {config.APP_TITLE}")
        print(f"   Default Department: {config.DEFAULT_DEPARTMENT}")
        print(f"   Departments Count: {len(config.DEPARTMENTS)}")
        return True
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def test_streamlit_config():
    """Test Streamlit configuration"""
    print("\n🔍 Testing Streamlit configuration...")
    
    if os.path.exists('.streamlit/config.toml'):
        print("✅ .streamlit/config.toml found")
        return True
    else:
        print("❌ .streamlit/config.toml missing")
        return False

def main():
    """Run all deployment tests"""
    print("🚀 Starting Deployment Tests...\n")
    
    tests = [
        ("Import Tests", test_imports),
        ("Environment Tests", test_environment),
        ("Configuration Tests", test_config),
        ("Streamlit Config Tests", test_streamlit_config)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        print(f"📋 Running {test_name}...")
        if not test_func():
            all_passed = False
        print()
    
    if all_passed:
        print("🎉 All tests passed! Your app is ready for deployment.")
        print("\n📋 Next steps:")
        print("1. Push your code to GitHub")
        print("2. Deploy on Streamlit Cloud")
        print("3. Configure environment variables")
        print("4. Test the deployed app")
    else:
        print("❌ Some tests failed. Please fix the issues before deploying.")
        sys.exit(1)

if __name__ == "__main__":
    main()
