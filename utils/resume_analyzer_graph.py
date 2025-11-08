from langgraph.graph import StateGraph, START, END
from functools import partial
from helpers.models import ResumeAnalyzer
from helpers.clients import get_tavily_client, get_gemini_model
from utils.resume_analyzer_workflow import extract_skills_from_resume,comapare_jd_with_skills

def build_graph(gemini_api_key):
    # tavily_client = get_tavily_client(tavily_api_key)
    model = get_gemini_model(gemini_api_key)

    # graph = StateGraph(JobAnalyzer)

    # graph.add_node("extract_jd", partial(extract_jd, tavily_client=tavily_client))
    # graph.add_node("extract_skills", partial(extract_skills, model=model))
    # graph.add_node("set_priority", partial(set_priority, model=model))

    # graph.add_edge(START, "extract_jd")
    # graph.add_edge("extract_jd", "extract_skills")
    # graph.add_edge("extract_skills", "set_priority")
    # graph.add_edge("set_priority", END)

    graph = StateGraph(ResumeAnalyzer)

    graph.add_node("extract_skills_from_resume",partial(extract_skills_from_resume,model=model))
    graph.add_node("comapare_jd_with_skills", partial(comapare_jd_with_skills, model=model))

    graph.add_edge(START,"extract_skills_from_resume")
    graph.add_edge("extract_skills_from_resume","comapare_jd_with_skills")
    graph.add_edge("comapare_jd_with_skills",END)

    return graph.compile()
