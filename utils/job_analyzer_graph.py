from langgraph.graph import StateGraph, START, END
from functools import partial
from helpers.models import JobAnalyzer
from .job_analyzer_workflow import extract_jd, extract_skills, set_priority
from helpers.clients import get_tavily_client, get_gemini_model

def build_graph(tavily_api_key, gemini_api_key):
    tavily_client = get_tavily_client(tavily_api_key)
    model = get_gemini_model(gemini_api_key)

    graph = StateGraph(JobAnalyzer)

    graph.add_node("extract_jd", partial(extract_jd, tavily_client=tavily_client))
    graph.add_node("extract_skills", partial(extract_skills, model=model))
    graph.add_node("set_priority", partial(set_priority, model=model))

    graph.add_edge(START, "extract_jd")
    graph.add_edge("extract_jd", "extract_skills")
    graph.add_edge("extract_skills", "set_priority")
    graph.add_edge("set_priority", END)

    return graph.compile()
