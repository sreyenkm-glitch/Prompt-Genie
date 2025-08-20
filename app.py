"""
AI Intelligent Prompt Generator - Streamlit Application
Modern, sleek interface for generating structured prompts using AI agents
"""

import streamlit as st
import json
import os
from datetime import datetime
from agents.gemini_agents import GeminiPromptGeneratorAgents
from utils.helpers import PromptGeneratorUtils
from config import Config

# Page configuration
st.set_page_config(
    page_title="AI Intelligent Prompt Generator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'workflow_state' not in st.session_state:
    st.session_state.workflow_state = 'initial'
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'department_detected' not in st.session_state:
    st.session_state.department_detected = None
if 'current_questions' not in st.session_state:
    st.session_state.current_questions = None
if 'original_request' not in st.session_state:
    st.session_state.original_request = ""
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'chat_active' not in st.session_state:
    st.session_state.chat_active = False
if 'chat_context' not in st.session_state:
    st.session_state.chat_context = {}

def validate_gemini_connection():
    """Validate Gemini API connection"""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return False, "API key not found"
        
        # Test API connection
        agents = GeminiPromptGeneratorAgents()
        test_response = agents._call_gemini_api("Say hello", "Test")
        if "Error" in test_response:
            return False, f"API Error: {test_response}"
        
        return True, "Connected"
    except Exception as e:
        return False, f"Connection Error: {str(e)}"

def save_prompt_history(prompt_data):
    """Save generated prompt to history"""
    try:
        utils = PromptGeneratorUtils()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"history/prompt_{timestamp}.json"
        
        history_data = {
            "timestamp": timestamp,
            "department": prompt_data.get("department", "Unknown"),
            "original_request": prompt_data.get("original_request", ""),
            "final_prompt": prompt_data.get("final_prompt", ""),
            "total_questions": prompt_data.get("total_questions_answered", 0)
        }
        
        utils.save_prompt_history(filename, history_data)
        return True
    except Exception as e:
        st.error(f"Error saving history: {str(e)}")
        return False

# Sidebar
with st.sidebar:
    st.title("🤖 AI Prompt Generator")
    st.markdown("---")
    
    # Connection status
    is_connected, status_msg = validate_gemini_connection()
    if is_connected:
        st.success(f"✅ {status_msg}")
    else:
        st.error(f"❌ {status_msg}")
        st.info("Please check your GEMINI_API_KEY in .env file")
    
    st.markdown("---")
    
    # Department info - simplified
    if st.session_state.department_detected:
        st.subheader("🎯 Department")
        dept_info = st.session_state.department_detected
        st.info(f"**{dept_info['department']}**")
    
    # Chat status
    if st.session_state.chat_active:
        st.subheader("💬 Chat Status")
        st.success("**Active** - AI Mentor is helping you")
        st.caption(f"Messages: {len(st.session_state.chat_messages)}")
    
    st.markdown("---")
    
    # Progress indicator
    if st.session_state.workflow_state != 'initial':
        if 'progress' in st.session_state:
            st.subheader("📊 Progress")
            st.progress(st.session_state.progress / 100)
            st.caption(f"{st.session_state.progress}% Complete")
    
    st.markdown("---")
    
    # Reset button
    if st.button("🔄 Reset Session", type="secondary"):
        st.session_state.workflow_state = 'initial'
        st.session_state.user_answers = {}
        st.session_state.department_detected = None
        st.session_state.current_questions = None
        st.session_state.original_request = ""
        st.session_state.chat_messages = []
        st.session_state.chat_active = False
        st.session_state.chat_context = {}
        st.rerun()

# Main content
st.title("🤖 AI Intelligent Prompt Generator")
st.markdown("""
**✨ Magical Prompt Creation** - Generate professional prompts in minutes through intelligent AI questioning. 
The system automatically understands your needs and creates ready-to-use prompts while teaching you the art of prompt engineering.
""")

# Initial state - User input
if st.session_state.workflow_state == 'initial':
    st.markdown("---")
    st.subheader("🚀 Start Your Prompt Generation")
    
    st.info("⚡ **Fast & Easy:** Complete in just a few minutes")
    
    # Main input form with automatic mentor detection
    with st.form("initial_request_form"):
        user_request = st.text_area(
            "Describe what you need help with:",
            placeholder="e.g., I want to create a social media campaign for our new product launch...",
            height=120,
            help="Tell us what you need - we'll figure out the rest"
        )
        
        submitted = st.form_submit_button("🚀 Start", type="primary")
        
        # Automatic AI Mentor Chat Detection
        # AI Mentor Chat Extension (Always available)
        with st.expander("💬 Need Help? Ask Your AI Mentor", expanded=False):
            st.info("🤖 Your AI mentor is here to help with your request!")
            
            # Display existing chat messages if any
            if hasattr(st.session_state, 'chat_messages') and st.session_state.chat_messages:
                st.markdown("**Previous Chat:**")
                for message in st.session_state.chat_messages[-3:]:  # Show last 3 messages
                    if message['role'] == 'user':
                        st.markdown(f"**You:** {message['content']}")
                    else:
                        st.markdown(f"**AI Mentor:** {message['content']}")
                st.markdown("---")
            
            # Chat input for questions
            with st.form("initial_mentor_chat_form"):
                initial_mentor_input = st.text_area(
                    "Ask your AI mentor:",
                    placeholder="Need help understanding? Want suggestions? Ask anything!",
                    height=80,
                    key="initial_mentor_chat_input"
                )
                
                initial_mentor_submitted = st.form_submit_button("💬 Ask Mentor", type="primary")
                
                if initial_mentor_submitted and initial_mentor_input.strip():
                    # Add user message
                    if not hasattr(st.session_state, 'chat_messages'):
                        st.session_state.chat_messages = []
                    
                    st.session_state.chat_messages.append({
                        'role': 'user',
                        'content': initial_mentor_input,
                        'timestamp': 'now'
                    })
                    
                    # Get AI response
                    with st.spinner("🤖 AI mentor is thinking..."):
                        try:
                            # Get enhanced context for better responses
                            context = f"""
                            Original Request: {user_request}
                            Current Input: {initial_mentor_input}
                            Conversation Stage: Initial guidance
                            User Profile: Learning prompt engineering
                            """
                            
                            ai_response = agents._call_gemini_api(
                                f"""You are an intelligent AI mentor with deep expertise in project development and prompt engineering.
                                
                                CONVERSATION CONTEXT:
                                {context}
                                
                                USER'S QUESTION: "{initial_mentor_input}"
                                
                                RESPONSE GUIDELINES:
                                1. **Direct Answer**: Provide a specific, actionable answer to their question
                                2. **Context Awareness**: Reference their original request and current situation
                                3. **Personalized Guidance**: Give advice tailored to their specific project and goals
                                4. **Next Steps**: Provide clear, specific next steps they can take immediately
                                5. **Follow-up Questions**: Ask 1-2 relevant follow-up questions to understand their needs better
                                
                                IMPORTANT: Be specific, avoid generic advice, and provide concrete examples relevant to their situation.
                                
                                Format your response as:
                                - Direct answer to their question
                                - Specific guidance for their situation
                                - Clear next steps
                                - 1-2 follow-up questions to better understand their needs""",
                                "AI Mentor"
                            )
                            
                            st.session_state.chat_messages.append({
                                'role': 'assistant',
                                'content': ai_response,
                                'timestamp': 'now'
                            })
                            
                            # Clear the input field
                            st.session_state.initial_mentor_chat_input = ""
                            st.rerun()
                            
                        except Exception as e:
                            st.error(f"Error getting AI response: {str(e)}")
                            st.error(f"Full error: {e}")
                            import traceback
                            st.error(f"Traceback: {traceback.format_exc()}")
        
        if submitted and user_request.strip():
            with st.spinner("🤖 Analyzing your request..."):
                try:
                    agents = GeminiPromptGeneratorAgents()
                    workflow_result = agents.process_interactive_workflow(user_request)
                    
                    if workflow_result['workflow_state'] == 'help_needed':
                        st.info(workflow_result['message'])
                    elif workflow_result['workflow_state'] == 'need_more_info':
                        st.warning(workflow_result['message'])
                    elif workflow_result['workflow_state'] == 'chat_mode':
                        # Start chat interface
                        st.session_state.workflow_state = 'chat_mode'
                        st.session_state.chat_active = True
                        st.session_state.original_request = workflow_result['original_request']
                        st.session_state.chat_context = {
                            'intent_analysis': workflow_result['intent_analysis'],
                            'smart_response': workflow_result['smart_response']
                        }
                        # Add initial AI message
                        if workflow_result['smart_response']['type'] == 'question_response':
                            st.session_state.chat_messages.append({
                                'role': 'assistant',
                                'content': workflow_result['smart_response']['content'],
                                'timestamp': 'now'
                            })
                        elif workflow_result['smart_response']['type'] == 'suggestions_response':
                            st.session_state.chat_messages.append({
                                'role': 'assistant',
                                'content': workflow_result['smart_response']['content'],
                                'timestamp': 'now'
                            })
                        st.rerun()
                    else:
                        # Normal prompt generation flow
                        st.session_state.workflow_state = 'awaiting_answers'
                        st.session_state.department_detected = workflow_result['department_detected']
                        st.session_state.current_questions = workflow_result['questions']
                        st.session_state.original_request = workflow_result['original_request']
                        st.rerun()
                    
                except Exception as e:
                    st.error(f"Error processing request: {str(e)}")
                    st.error(f"Workflow result: {workflow_result}")
                    st.error("Please try again or contact support if the issue persists.")

# Chat mode - Dynamic chat interface
elif st.session_state.workflow_state == 'chat_mode':
    st.markdown("---")
    
    # Show chat interface
    st.subheader("💬 AI Mentor Chat")
    st.info("🤖 Your AI mentor is here to help! Ask questions and get guidance.")
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_messages:
            if message['role'] == 'user':
                with st.chat_message("user"):
                    st.write(message['content'])
            else:
                with st.chat_message("assistant"):
                    st.markdown(message['content'])
    
    # Chat input
    with st.form("chat_form"):
        chat_input = st.text_area(
            "Ask your AI mentor:",
            placeholder="Ask questions, seek clarification, or tell me what you'd like to work on...",
            height=80,
            key="chat_input"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            chat_submitted = st.form_submit_button("💬 Send", type="primary")
        with col2:
            end_chat = st.form_submit_button("✅ End Chat & Continue", type="secondary")
        
        if chat_submitted and chat_input.strip():
            # Add user message
            st.session_state.chat_messages.append({
                'role': 'user',
                'content': chat_input,
                'timestamp': 'now'
            })
            
            # Get AI response
            with st.spinner("🤖 AI mentor is thinking..."):
                try:
                    agents = GeminiPromptGeneratorAgents()
                    ai_response = agents._call_gemini_api(
                        f"""You are a helpful AI mentor helping a user with their project. 
                        
                        Original user request: "{st.session_state.original_request}"
                        Chat context: {st.session_state.chat_context}
                        
                        User just said: "{chat_input}"
                        
                        Provide a helpful, educational response that:
                        1. Directly addresses their question/concern
                        2. Provides actionable guidance
                        3. Maintains a friendly, mentor-like tone
                        4. Helps them move toward creating their prompt
                        5. Asks follow-up questions if needed
                        
                        Keep responses conversational and helpful.""",
                        "AI Mentor"
                    )
                    
                    st.session_state.chat_messages.append({
                        'role': 'assistant',
                        'content': ai_response,
                        'timestamp': 'now'
                    })
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error getting AI response: {str(e)}")
        
        elif end_chat:
            # Transition to prompt generation with chat context
            with st.spinner("🤖 Preparing your personalized prompt generation..."):
                try:
                    agents = GeminiPromptGeneratorAgents()
                    
                    # Create enhanced context from chat
                    chat_summary = "\n".join([
                        f"{msg['role']}: {msg['content']}" 
                        for msg in st.session_state.chat_messages
                    ])
                    
                    enhanced_request = f"{st.session_state.original_request}\n\nChat Context:\n{chat_summary}"
                    
                    # Detect department with enhanced context
                    department_info = agents.detect_department(enhanced_request)
                    
                    # Generate questions with chat context
                    questions_info = agents.generate_interactive_questions(enhanced_request, department_info["department"])
                    
                    st.session_state.workflow_state = 'awaiting_answers'
                    st.session_state.department_detected = department_info
                    st.session_state.current_questions = questions_info
                    st.session_state.original_request = enhanced_request
                    st.session_state.chat_active = False
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error transitioning from chat: {str(e)}")

# Question answering state
elif st.session_state.workflow_state == 'awaiting_answers':
    st.markdown("---")
    
    # Show department detection result
    if st.session_state.department_detected:
        dept_info = st.session_state.department_detected
        st.success(f"🎯 **Department Detected:** {dept_info['department']}")
    
    # Show current questions
    if st.session_state.current_questions:
        questions_data = st.session_state.current_questions
        
        st.subheader("📝 Questions")
        st.caption(f"Step: {questions_data.get('next_step', 'Gathering information')}")
        
        # Simple progress bar
        progress = questions_data.get('progress_percentage', 0)
        st.progress(progress / 100)
        st.caption(f"Progress: {progress}%")
        
        # Question form - separate from mentor chat to avoid nested forms
        with st.form("questions_form_initial"):
            answers = {}
            
            for question in questions_data.get('questions', []):
                st.markdown(f"**{question['question']}**")
                
                if question.get('type') == 'multiple_choice' and question.get('options'):
                    answer = st.selectbox(
                        "Choose an option:",
                        options=question['options'],
                        key=f"q_{question['id']}"
                    )
                else:
                    answer = st.text_area(
                        "Your answer:",
                        key=f"q_{question['id']}",
                        height=80
                    )
                
                answers[question['id']] = answer
            
            # Simple time estimate
            num_questions = len(questions_data.get('questions', []))
            if num_questions <= 2:
                st.info("⏱️ Almost done!")
            elif num_questions <= 3:
                st.info("⏱️ Just a few more questions")
            else:
                st.info("⏱️ Quick process")
            
            submitted = st.form_submit_button("➡️ Continue", type="primary")
            
            if submitted:
                # Update user answers
                st.session_state.user_answers.update(answers)
                
                with st.spinner("🤖 Generating your prompt..."):
                    try:
                        agents = GeminiPromptGeneratorAgents()
                        workflow_result = agents.continue_workflow(
                            st.session_state.original_request,
                            st.session_state.department_detected['department'],
                            st.session_state.user_answers
                        )
                        
                        if workflow_result['workflow_state'] == 'complete':
                            st.session_state.workflow_state = 'complete'
                            st.session_state.final_prompt = workflow_result['final_prompt']
                            st.session_state.summary = workflow_result['summary']
                        elif workflow_result['workflow_state'] == 'error':
                            st.error(workflow_result['error'])
                        else:
                            st.session_state.current_questions = workflow_result['questions']
                            st.session_state.progress = workflow_result['progress']
                        
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error processing answers: {str(e)}")
    
    # Legacy AI Mentor Chat Extension Button (fallback)
    with st.expander("💬 Need Help? Ask Your AI Mentor", expanded=False):
        st.info("🤖 Your AI mentor is here to help anytime during the process!")
        
        # Display existing chat messages if any
        if hasattr(st.session_state, 'chat_messages') and st.session_state.chat_messages:
            st.markdown("**Previous Chat:**")
            for message in st.session_state.chat_messages[-3:]:  # Show last 3 messages
                if message['role'] == 'user':
                    st.markdown(f"**You:** {message['content']}")
                else:
                    st.markdown(f"**AI Mentor:** {message['content']}")
            st.markdown("---")
        
        # Chat input for questions
        with st.form("mentor_chat_form"):
            mentor_input = st.text_area(
                "Ask your AI mentor:",
                placeholder="Need clarification? Want suggestions? Ask anything!",
                height=80,
                key="mentor_chat_input"
            )
            
            mentor_submitted = st.form_submit_button("💬 Ask Mentor", type="primary")
            
            if mentor_submitted and mentor_input.strip():
                # Add user message
                if not hasattr(st.session_state, 'chat_messages'):
                    st.session_state.chat_messages = []
                
                st.session_state.chat_messages.append({
                    'role': 'user',
                    'content': mentor_input,
                    'timestamp': 'now'
                })
                
                # Get AI response
                with st.spinner("🤖 AI mentor is thinking..."):
                    try:
                        agents = GeminiPromptGeneratorAgents()
                        
                        # Create context for mentor
                        current_context = f"""
                        Original Request: {st.session_state.original_request}
                        Current Department: {st.session_state.department_detected['department']}
                        Current Step: Answering questions for prompt generation
                        """
                        
                        ai_response = agents._call_gemini_api(
                            f"""You are a helpful AI mentor helping a user during their prompt generation process. 
                            
                            {current_context}
                            
                            User just asked: "{mentor_input}"
                            
                            Provide a helpful, educational response that:
                            1. Directly addresses their question/concern
                            2. Provides actionable guidance related to their current task
                            3. Maintains a friendly, mentor-like tone
                            4. Helps them understand how to answer the current questions better
                            5. Gives context-specific advice for their department and project
                            
                            Keep responses conversational and helpful. Focus on helping them complete their prompt generation successfully.""",
                            "AI Mentor"
                        )
                        
                        st.session_state.chat_messages.append({
                            'role': 'assistant',
                            'content': ai_response,
                            'timestamp': 'now'
                        })
                        
                        # Clear the input field
                        st.session_state.mentor_chat_input = ""
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error getting AI response: {str(e)}")
                        st.error(f"Full error: {e}")
                        import traceback
                        st.error(f"Traceback: {traceback.format_exc()}")
    
    # Show current questions
    if st.session_state.current_questions:
        questions_data = st.session_state.current_questions
        
        st.subheader("📝 Questions")
        st.caption(f"Step: {questions_data.get('next_step', 'Gathering information')}")
        
        # Simple progress bar
        progress = questions_data.get('progress_percentage', 0)
        st.progress(progress / 100)
        st.caption(f"Progress: {progress}%")
        
        # Question form
        with st.form("questions_form_continue"):
            answers = {}
            
            for question in questions_data.get('questions', []):
                st.markdown(f"**{question['question']}**")
                
                if question.get('type') == 'multiple_choice' and question.get('options'):
                    answer = st.selectbox(
                        "Choose an option:",
                        options=question['options'],
                        key=f"q_{question['id']}"
                    )
                else:
                    answer = st.text_area(
                        "Your answer:",
                        key=f"q_{question['id']}",
                        height=80
                    )
                
                answers[question['id']] = answer
            
            # Simple time estimate
            num_questions = len(questions_data.get('questions', []))
            if num_questions <= 2:
                st.info("⏱️ Almost done!")
            elif num_questions <= 3:
                st.info("⏱️ Just a few more questions")
            else:
                st.info("⏱️ Quick process")
            
            submitted = st.form_submit_button("➡️ Continue", type="primary")
            
            if submitted:
                # Update user answers
                st.session_state.user_answers.update(answers)
                
                with st.spinner("🤖 Generating your prompt..."):
                    try:
                        agents = GeminiPromptGeneratorAgents()
                        workflow_result = agents.continue_workflow(
                            st.session_state.original_request,
                            st.session_state.department_detected['department'],
                            st.session_state.user_answers
                        )
                        
                        if workflow_result['workflow_state'] == 'complete':
                            st.session_state.workflow_state = 'complete'
                            st.session_state.final_prompt = workflow_result['final_prompt']
                            st.session_state.summary = workflow_result['summary']
                        elif workflow_result['workflow_state'] == 'error':
                            st.error(workflow_result['error'])
                        else:
                            st.session_state.current_questions = workflow_result['questions']
                            st.session_state.progress = workflow_result['progress']
                        
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error processing answers: {str(e)}")

# Final prompt state
elif st.session_state.workflow_state == 'complete':
    st.markdown("---")
    st.success("🎉 **Your Prompt is Ready!**")
    
    # AI Mentor Chat Extension Button (Final State)
    with st.expander("💬 Need Help? Ask Your AI Mentor", expanded=False):
        st.info("🤖 Your AI mentor is here to help with your generated prompt!")
        
        # Display existing chat messages if any
        if hasattr(st.session_state, 'chat_messages') and st.session_state.chat_messages:
            st.markdown("**Previous Chat:**")
            for message in st.session_state.chat_messages[-3:]:  # Show last 3 messages
                if message['role'] == 'user':
                    st.markdown(f"**You:** {message['content']}")
                else:
                    st.markdown(f"**AI Mentor:** {message['content']}")
            st.markdown("---")
        
        # Chat input for questions
        with st.form("final_mentor_chat_form"):
            final_mentor_input = st.text_area(
                "Ask your AI mentor:",
                placeholder="Need help understanding the prompt? Want to modify it? Ask anything!",
                height=80,
                key="final_mentor_chat_input"
            )
            
            final_mentor_submitted = st.form_submit_button("💬 Ask Mentor", type="primary")
            
            if final_mentor_submitted and final_mentor_input.strip():
                # Add user message
                if not hasattr(st.session_state, 'chat_messages'):
                    st.session_state.chat_messages = []
                
                st.session_state.chat_messages.append({
                    'role': 'user',
                    'content': final_mentor_input,
                    'timestamp': 'now'
                })
                
                # Get AI response
                with st.spinner("🤖 AI mentor is thinking..."):
                    try:
                        agents = GeminiPromptGeneratorAgents()
                        
                        # Create context for mentor
                        final_context = f"""
                        Original Request: {st.session_state.original_request}
                        Department: {st.session_state.department_detected['department']}
                        Generated Prompt: {st.session_state.final_prompt}
                        Current Status: Prompt generation completed
                        """
                        
                        ai_response = agents._call_gemini_api(
                            f"""You are a helpful AI mentor helping a user with their completed prompt. 
                            
                            {final_context}
                            
                            User just asked: "{final_mentor_input}"
                            
                            Provide a helpful, educational response that:
                            1. Directly addresses their question/concern about the prompt
                            2. Provides guidance on how to use or modify the prompt
                            3. Maintains a friendly, mentor-like tone
                            4. Helps them understand the prompt better or improve it
                            5. Gives context-specific advice for their department and project
                            
                            Keep responses conversational and helpful. Focus on helping them make the most of their generated prompt.""",
                            "AI Mentor"
                        )
                        
                        st.session_state.chat_messages.append({
                            'role': 'assistant',
                            'content': ai_response,
                            'timestamp': 'now'
                        })
                        
                        # Clear the input field
                        st.session_state.final_mentor_chat_input = ""
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error getting AI response: {str(e)}")
                        st.error(f"Full error: {e}")
                        import traceback
                        st.error(f"Traceback: {traceback.format_exc()}")
    
    # Summary - simplified
    if hasattr(st.session_state, 'summary'):
        summary = st.session_state.summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Department", summary['department'])
        with col2:
            st.metric("Questions", summary['total_questions_answered'])
        with col3:
            st.metric("Request", summary['original_request'][:30] + "..." if len(summary['original_request']) > 30 else summary['original_request'])
    
    # Final prompt
    st.subheader("📝 Your Ready-to-Use Prompt")
    
    if hasattr(st.session_state, 'final_prompt'):
        st.text_area(
            "Generated Prompt:",
            value=st.session_state.final_prompt,
            height=400,
            disabled=True
        )
        
        # Copy button
        if st.button("📋 Copy to Clipboard", type="primary"):
            st.write("✅ Prompt copied to clipboard!")
        
        # Save to history
        if st.button("💾 Save to History", type="secondary"):
            prompt_data = {
                "department": st.session_state.department_detected['department'],
                "original_request": st.session_state.original_request,
                "final_prompt": st.session_state.final_prompt,
                "total_questions_answered": st.session_state.summary['total_questions_answered']
            }
            if save_prompt_history(prompt_data):
                st.success("✅ Prompt saved to history!")
    
    # Start new session
    if st.button("🔄 Generate Another Prompt", type="primary"):
        st.session_state.workflow_state = 'initial'
        st.session_state.user_answers = {}
        st.session_state.department_detected = None
        st.session_state.current_questions = None
        st.session_state.original_request = ""
        st.rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>Powered by Google Gemini AI 🤖 | Built with Streamlit 🎈</p>
        <p>Experience the magic of intelligent prompt creation</p>
    </div>
    """,
    unsafe_allow_html=True
)
