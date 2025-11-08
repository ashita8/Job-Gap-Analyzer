from typing import TypedDict, Annotated
from pydantic import BaseModel, Field

class JobAnalyzer(TypedDict):
    job_desc : list[str]
    skills : list[str]
    job_title: str
    yoe: int
    website: str
    job_listings : int
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

class ResumeAnalyzer(TypedDict):
    resume_file : list[str]
    resume_skills : list[str]
    resume_skills_summary : str
    feedback : str
    highly_required_skills : list[str]
    good_to_have_skills : list[str]
    already_have : list[str]
    need_to_have_skills: list[str]
    jd_skills: list[str]

class ResumeSkills(BaseModel):
    resume_skills : list[str] = Field(description="List of all the skills present in the resume")
    summary : str = Field(description="Summary of the whole resume in 100 words")


class checkResumeSkills(BaseModel):
    already_have : list[str] = Field(description="skills present in High Priority in the job description and on resume")
    need_to_have_skills : list[str] = Field(description="skills only present in job descriptions high priority")

class ResumeSkillsCompare(BaseModel):
    highly_required_skills : list[str] = Field(description="List of all the skills present High Priority in the resume")
    good_to_have_skills : str = Field(description="Summary of the whole resume in 100 words")

class PriorityResponsse(BaseModel):
    high_priority : list[str] = Field(description="This contains high_priority skills")
    medium_priority : list[str] = Field(description="This contains medium_priority skills")
    low_priority : list[str] = Field(description="This contains low_priority")