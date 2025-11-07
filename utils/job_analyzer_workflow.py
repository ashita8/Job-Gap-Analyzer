from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv 
import os
import streamlit as st
from helpers.models import JobAnalyzer, SkillResponse, PriorityResponsse

load_dotenv()

def extract_jd(state: JobAnalyzer,tavily_client) -> JobAnalyzer:

    job_title = state["job_title"]
    years_of_exp = state["yoe"]
    query = f'{job_title} {years_of_exp} jobs site:{state["website"]}'
    links_response = tavily_client.search(query, search_depth="advanced", max_results=5)
    job_urls = [r["url"] for r in links_response["results"]]

    extract_response = tavily_client.extract(urls=job_urls, format="text", extract_depth="advanced")
    #print(extract_response)
    final_jds = []
    for result in extract_response.get("results", []):
        title = result.get("title", "")
        jd = result.get("description") or result.get("content") or result.get("raw_content")
        if job_title.lower() in title.lower():
            final_jds.append(jd)
    return {'job_desc': final_jds }

def extract_skills(state: JobAnalyzer,model) -> JobAnalyzer:
    structured_op = model.with_structured_output(SkillResponse)
    prompt = f"read the job description and give me key skills {state['job_desc']}"

    msg = structured_op.invoke(prompt)
    return {'skills': msg.skills }


def set_priority(state: JobAnalyzer,model) -> JobAnalyzer:
    structured_op = model.with_structured_output(PriorityResponsse)
    prompt = f"Read all the skills {state['skills']} provided and Job Descriptions {state['job_desc']}, based on that provide the priority level. "

    msg = structured_op.invoke(prompt)
    return {'high_priority': msg.high_priority, 'medium_priority':msg.medium_priority, 'low_priority':msg.low_priority}


# init_state = {
#     'job_title' : "Data Scientist",
#     'yoe':2
# }

# print(workflow.invoke(init_state))