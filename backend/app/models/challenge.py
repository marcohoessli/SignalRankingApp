from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Challenge(Base):
    __tablename__ = "challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    creator_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    invite_code = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    question = relationship("Question", back_populates="challenges")
    creator = relationship("User", back_populates="challenges_created")
    entries = relationship("ChallengeEntry", back_populates="challenge", cascade="all, delete-orphan")

class ChallengeEntry(Base):
    __tablename__ = "challenge_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    probability = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    challenge = relationship("Challenge", back_populates="entries")
    user = relationship("User", back_populates="challenge_entries")
