from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String, nullable=False)  # Crypto, Politics, Tech, Sports, Other
    status = Column(String, default="OPEN")  # OPEN, CLOSED, RESOLVED
    close_time = Column(DateTime, nullable=False)
    resolve_time = Column(DateTime, nullable=True)
    outcome = Column(Boolean, nullable=True)  # True=YES, False=NO, None=unresolved
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    source_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    creator = relationship("User", back_populates="created_questions", foreign_keys=[created_by])
    predictions = relationship("Prediction", back_populates="question", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="question", cascade="all, delete-orphan")
    challenges = relationship("Challenge", back_populates="question", cascade="all, delete-orphan")
