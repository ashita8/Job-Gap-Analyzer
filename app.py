import streamlit as st
from utils.job_analyzer_workflow import job_analyzer

st.title("Job Analyzer")
st.set_page_config(layout="wide")

job_title = st.text_input("Job Title")
experience = st.number_input("Years of Experience")

if st.button("Start Research"):
    init_state = {
    'job_title' : job_title,
    'yoe':experience
    }
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

