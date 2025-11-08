from helpers.models import ResumeAnalyzer,ResumeSkills,checkResumeSkills
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated
from pydantic import BaseModel, Field
from langchain.document_loaders.pdf import PyPDFLoader
import tempfile
import streamlit as st
from dotenv import load_dotenv 
import os


def extract_skills_from_resume(state: ResumeAnalyzer,model) -> ResumeAnalyzer:
    #resume_path = "Ashita_resume.pdf"

    loader = PyPDFLoader(state['resume_file'])
    docs = loader.load()
    doc_lst =[]
    for i, doc in enumerate(docs):
        doc_lst.append(doc.page_content)

    complete_resume = " ".join(doc_lst)
    structured_response = model.with_structured_output(ResumeSkills)

    prompt = f"You have provided the Resume text extract all the skills you can find in it and also generate a summary of this Resume : {complete_resume}"
    response = structured_response.invoke(prompt)

    return {'resume_skills':response.resume_skills, 'resume_skills_summary': response.summary}

def comapare_jd_with_skills(state: ResumeAnalyzer,model) -> ResumeAnalyzer:
    jd_response = state['jd_skills']
    jd_high_priority_skills = jd_response["high_priority"]

    structured_response = model.with_structured_output(checkResumeSkills)

    prompt = f"You have provided the list of High proiority skills  {jd_high_priority_skills} and resume skills: {state['resume_skills']} you need to comapre these skills and provide skills already have and required"
    response = structured_response.invoke(prompt)

    return {'already_have': response.already_have, 'need_to_have_skills':response.need_to_have_skills}

