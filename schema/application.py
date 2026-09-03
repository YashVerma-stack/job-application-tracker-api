from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional

class ApplicationStatus(str, Enum):
    applied = "applied"
    interview = "interview"
    rejected = "rejected"
    offer = "offer"
    accepted = "accepted"
    

class CreateApplication(BaseModel):
    company: str = Field(min_length=3)
    job_title: str = Field(min_length = 3)
    location: str = Field(min_length = 3)
    salary: int = Field(ge = 0)
    status: ApplicationStatus
    applied_date: datetime
    notes: Optional[str] = None
    
    
    
class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    company: str
    job_title: str
    location: str
    salary: int
    status: ApplicationStatus
    applied_date: datetime
    notes: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}