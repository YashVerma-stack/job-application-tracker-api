from database import Base
from sqlalchemy import Column,  Integer, String, Boolean, DateTime
from datetime import datetime, timezone
from schema.user import UserRole
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index = True)
    username = Column(String, unique=True)
    email = Column(String, unique = True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc)) 
    role = Column(String, default = UserRole.user.value)   
    
    applications = relationship("Application", back_populates="user", cascade = "all, delete-orphan")