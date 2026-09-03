from database import Base
from sqlalchemy import Column,  Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime, timezone

class Application(Base):
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True, index = True)
    user_id = Column(Integer, ForeignKey('users.id'))
    company = Column(String)
    job_title = Column(String)
    location = Column(String)
    salary = Column(Integer)
    status = Column(String)
    applied_date = Column(DateTime)
    notes = Column(String)
    
    
    created_at = Column(
        DateTime(timezone = True),
        default = lambda: datetime.now(timezone.utc)
    )
    updated_at = Column(
        DateTime(timezone=True),
        default = lambda: datetime.now(timezone.utc),
        onupdate = lambda: datetime.now(timezone.utc)
    )