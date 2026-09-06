from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    user = "user"
    admin = "admin"
    
class UpdatePassword(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)
    
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
    
    
    model_config = {"from_attributes": True}
    
    
    
    