from pydantic import BaseModel
from datetime import datetime

class CreateUser(BaseModel):
    username: str
    email: str
    password: str
    is_active: bool
    

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime