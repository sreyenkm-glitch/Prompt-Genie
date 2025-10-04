
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
        