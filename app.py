import streamlit as st
from utils.job_analyzer_workflow import job_analyzer

#********************Utility************************


#********************Session State******************
if "tavily_api_key" not in st.session_state:
    st.session_state["tavily_api_key"] = None

if "gemini_api_key" not in st.session_state:
    st.session_state["gemini_api_key"] = None


#****************Sidebar**************************
st.session_state["tavily_api_key"] = st.sidebar.text_input("Tavily API key")
st.session_state["gemini_api_key"] = st.sidebar.text_input("Gemini API key")

#*****************Main UI***************************
st.title("Job Analyzer")
st.set_page_config(layout="wide")

job_title = st.text_input("Job Title")
experience = st.number_input("Years of Experience")
site = st.radio(
    "Select the Website you want to research",
    ["Indeed", "LinkedIn", "Naukri"],
    index=None,
)

if st.button("Start Research"):
    website = site.lower() + ".com"
    init_state = {
    'job_title' : job_title,
    'yoe':experience,
    'website': website
    }
    with st.spinner("Analyzing job data, please wait..."):
        response = job_analyzer.invoke(init_state)

    cols = st.columns(3)
    with cols[0]:
        st.subheader("High Priority Skills")
        for skill in response["high_priority"]:
            st.markdown(f"- {skill}")

    with cols[1]:
        st.subheader("Medium Priority Skills")
        for skill in response["medium_priority"]:
            st.markdown(f"- {skill}")

    with cols[2]:
        st.subheader("Low Priority Skills")
        for skill in response["low_priority"]:
            st.markdown(f"- {skill}")

