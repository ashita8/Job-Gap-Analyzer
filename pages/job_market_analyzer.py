import streamlit as st
import time
import numpy as np
from sidebar import render_sidebar
from utils.job_analyzer_graph import build_graph

st.set_page_config(page_title="Plotting Demo", page_icon="📈")

st.title("Job Analyzer")
st.set_page_config(layout="centered")

def show_analyzer():
    job_title = st.text_input("Job Title")
    experience = st.number_input("Years of Experience")
    Job_listings_count = st.slider("How many Job Listings you want to analyze?", 0, 5, 30)
    site = st.radio(
        "Select the Website you want to research",
        ["Indeed", "LinkedIn", "Naukri"],
        index=None,
    )

    tavily_api_key = st.session_state.get("tavily_api_key")
    gemini_api_key = st.session_state.get("gemini_api_key")

    if tavily_api_key and gemini_api_key:
        job_analyzer = build_graph(tavily_api_key, gemini_api_key)
    else:
        st.error("Please input the keys in Sidebar")

    if st.button("Start Research"):
        if tavily_api_key and gemini_api_key:

            website = site.lower() + ".com"
            init_state = {
            'job_title' : job_title,
            'yoe':experience,
            'website': website,
            'job_listings' : Job_listings_count
            }
            
            with st.spinner("Analyzing job data, please wait..."):
                response = job_analyzer.invoke(init_state)
                st.session_state["job_anlayzer_skills"] = response

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
        else:
            st.error("Please Enter Keys")

render_sidebar()
show_analyzer()