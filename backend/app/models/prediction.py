from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    probability = Column(Float, nullable=False)  # 0-100
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    brier_score = Column(Float, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="predictions")
    question = relationship("Question", back_populates="predictions")
    
    # One active prediction per user per question
    __table_args__ = (UniqueConstraint('user_id', 'question_id', name='_user_question_uc'),)
