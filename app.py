import streamlit as st
#********************Utility************************


#********************Session State******************
if "tavily_api_key" not in st.session_state:
    st.session_state["tavily_api_key"] = None

if "gemini_api_key" not in st.session_state:
    st.session_state["gemini_api_key"] = None

if "job_anlayzer_skills" not in st.session_state:
    st.session_state["job_anlayzer_skills"] = {}


#*****************Main UI***************************

def show_welcome():
    st.title("Welcome to the Job Analyzer App!")
    st.write("""
        👋 Hello and welcome!  
        This app helps you identify key skills and learning gaps by analyzing job requirements and your experience.  
        Use the sidebar to enter your API keys and start your research journey.  
        Let's get started! 🚀
    """)

if __name__ == "__main__":
    show_welcome()
