from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class QuestionBase(BaseModel):
    title: str
    description: str
    category: str
    close_time: datetime
    source_url: Optional[str] = None

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    close_time: Optional[datetime] = None
    source_url: Optional[str] = None

class QuestionResponse(QuestionBase):
    id: int
    status: str
    resolve_time: Optional[datetime]
    outcome: Optional[bool]
    created_by: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class QuestionResolve(BaseModel):
    outcome: bool
