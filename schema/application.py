from pydantic import BaseModel
from datetime import datetime

class CreateApplication(BaseModel):
    company: str
    job_title: str
    location: str
    salary: int
    status: str
    applied_date: datetime
    notes: str
    
    
class ApplicationResponse(BaseModel):
    id: int
    user_id: int
    company: str
    job_title: str
    location: str
    salary: int
    status: str
    applied_date: datetime
    notes: str
    created_at: datetime
    updated_at: datetime