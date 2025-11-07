import streamlit as st

@st.dialog("Show previous Analysis",width="medium")
def show_analyzer_result():
    
    if "job_anlayzer_skills" not in st.session_state:
        st.session_state["job_anlayzer_skills"] = {}

    if st.session_state["job_anlayzer_skills"] == {}:
        st.info("No preious Analysis Saved")

    else:
        with st.expander("High Priority"):
            for skill in st.session_state["job_anlayzer_skills"]["high_priority"]:
                    st.markdown(f"- {skill}")

        with st.expander("Medium Priority"):
            for skill in st.session_state["job_anlayzer_skills"]["medium_priority"]:
                    st.markdown(f"- {skill}")
        with st.expander("Low Priority"):
            for skill in st.session_state["job_anlayzer_skills"]["low_priority"]:
                    st.markdown(f"- {skill}")


def render_sidebar():
    
    st.session_state["tavily_api_key"] = st.sidebar.text_input("Tavily API key")
    st.session_state["gemini_api_key"] = st.sidebar.text_input("Gemini API key")

    if st.sidebar.button("Show Job Analyzer Result"):
        show_analyzer_result()
         