import streamlit as st
from utils.resume_analyzer_graph import build_graph
import tempfile
from langchain.document_loaders.pdf import PyPDFLoader
from sidebar import render_sidebar

st.set_page_config(page_title="", page_icon="📈")

st.title("Resume Analyzer")
st.set_page_config(layout="centered")

def render_resume_anlayzer():
    uploaded_file = st.file_uploader("Upload your resume here!! ",["pdf"])
    if uploaded_file  is not None:
    # Save uploaded PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

    gemini_api_key = st.session_state.get("gemini_api_key")

    if gemini_api_key:
        resume_analyzer = build_graph(gemini_api_key)
    #print("Analysis",st.session_state["job_anlayzer_skills"])
    if "job_anlayzer_skills" not in st.session_state:
        st.session_state["job_anlayzer_skills"] = {}

    # if st.session_state["job_anlayzer_skills"] not in st.session_state:
    #     st.warning("Please do Job Market Analysis First")
    #     print("hey")
    
    else:
        if st.session_state.get("job_anlayzer_skills"):   
            if st.button("Analyze"):
                if gemini_api_key:
                    init_state = {
                        'jd_skills': st.session_state["job_anlayzer_skills"],
                        'resume_file' : tmp_path,
                    }

                    response = resume_analyzer.invoke(init_state)
                    with st.container(border=True):
                        st.write("Resume Summary")
                        st.write(response["resume_skills_summary"])

                    with st.container(border=True):
                        st.write("The required skills you already have")
                        for skill in response["already_have"]:
                            st.markdown(f"- {skill}")
                    
                    with st.container(border=True):
                        st.write("The skills you need")
                        for skill in response["need_to_have_skills"]:
                            st.markdown(f"- {skill}")

                    with st.container(border=True):
                        st.write("Good to have skills")
                        for skill in st.session_state["job_anlayzer_skills"]["medium_priority"]:
                            st.markdown(f"- {skill}")                
                        for skill in st.session_state["job_anlayzer_skills"]["low_priority"]:
                            st.markdown(f"- {skill}") 
                else:
                    st.info("Please input the Gemini keys first.")
        else:   
            st.info("Please do a Job Market Analysis First.")
render_sidebar()
render_resume_anlayzer()