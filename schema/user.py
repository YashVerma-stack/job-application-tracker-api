from pydantic import BaseModel, Field, ConfigDict, EmailStr
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    user = "user"
    admin = "admin"
    
class UpdatePassword(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8, max_length=128)
    
class CreateUser(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    role: UserRole
    created_at: datetime
    
    
    model_config = {"from_attributes": True}   