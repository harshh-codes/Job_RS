from pydantic import BaseModel, Field
from typing import List, Optional

class JobBase(BaseModel):
    title: str
    company: str
    location: str
    description: str
    required_skills: List[str]
    salary_range: Optional[str] = None
    job_type: str = Field(..., example="Full-time")

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: int
    recommendation_score: Optional[float] = 0.0

    class Config:
        from_attributes = True

class ResumeAnalysis(BaseModel):
    skills: List[str]
    experience_years: float
    education: str
    current_role: Optional[str] = None
