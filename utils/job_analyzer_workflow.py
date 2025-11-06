from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated
from pydantic import BaseModel, Field
from dotenv import load_dotenv 
import os
import streamlit as st

load_dotenv()

def get_clients():
    tavily_api_key = st.session_state.get("tavily_api_key")
    gemini_api_key = st.session_state.get("gemini_api_key")

    if not tavily_api_key or not gemini_api_key:
        raise ValueError("API keys are not set in session_state")

    tavily_client = TavilyClient(api_key=tavily_api_key)
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=gemini_api_key)

    return tavily_client, model


from tavily import TavilyClient
#tavily_client = TavilyClient(api_key=st.session_state["tavily_api_key"])

from langchain_google_genai import ChatGoogleGenerativeAI
# model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=st.session_state["gemini_api_key"])

class JobAnalyzer(TypedDict):
    job_desc : list[str]
    skills : list[str]
    job_title: str
    yoe: int
    website: str
    high_priority: list[str] 
    medium_priority : list[str] 
    low_priority : list[str]


class SkillResponse(BaseModel):
    skills : list[str] = Field(description='list of all skills')
    desc : str = Field(description="Summarized description of all skills")

class PriorityResponsse(BaseModel):
    high_priority : list[str] = Field(description="This contains high_priority skills")
    medium_priority : list[str] = Field(description="This contains medium_priority skills")
    low_priority : list[str] = Field(description="This contains low_priority")

def extract_jd(state: JobAnalyzer) -> JobAnalyzer:
    tavily_client, _ = get_clients()

    job_title = state["job_title"]
    years_of_exp = state["yoe"]
    query = f'{job_title} {years_of_exp} jobs site:{state["website"]}'
    links_response = tavily_client.search(query, search_depth="advanced", max_results=1)
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

def extract_skills(state: JobAnalyzer) -> JobAnalyzer:
    _, model = get_clients()
    structured_op = model.with_structured_output(SkillResponse)
    prompt = f"read the job description and give me key skills {state['job_desc']}"

    msg = structured_op.invoke(prompt)
    return {'skills': msg.skills }


def set_priority(state: JobAnalyzer) -> JobAnalyzer:
    _, model = get_clients()
    structured_op = model.with_structured_output(PriorityResponsse)
    prompt = f"Read all the skills {state['skills']} provided and Job Descriptions {state['job_desc']}, based on that provide the priority level. "

    msg = structured_op.invoke(prompt)
    return {'high_priority': msg.high_priority, 'medium_priority':msg.medium_priority, 'low_priority':msg.low_priority}


graph = StateGraph(JobAnalyzer)

graph.add_node("extract_jd",extract_jd)
graph.add_node("extract_skills",extract_skills)
graph.add_node("set_priority",set_priority)

graph.add_edge(START, "extract_jd")
graph.add_edge("extract_jd","extract_skills")
graph.add_edge("extract_skills","set_priority")
graph.add_edge("set_priority",END)

job_analyzer = graph.compile()

# init_state = {
#     'job_title' : "Data Scientist",
#     'yoe':2
# }

# print(workflow.invoke(init_state))