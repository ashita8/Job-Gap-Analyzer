from typing import TypedDict, Annotated
from pydantic import BaseModel, Field

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

