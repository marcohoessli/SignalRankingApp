from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, default="user")  # "user" or "admin"
    email_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Stats
    total_predictions = Column(Integer, default=0)
    resolved_predictions = Column(Integer, default=0)
    avg_brier_score = Column(Float, nullable=True)
    rank_global = Column(Integer, nullable=True)
    last_30d_brier = Column(Float, nullable=True)
    best_category = Column(String, nullable=True)
    streak = Column(Integer, default=0)
    
    # Relationships
    predictions = relationship("Prediction", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    created_questions = relationship("Question", back_populates="creator", foreign_keys="Question.created_by")
    challenges_created = relationship("Challenge", back_populates="creator", cascade="all, delete-orphan")
    challenge_entries = relationship("ChallengeEntry", back_populates="user", cascade="all, delete-orphan")
    admin_logs = relationship("AdminLog", back_populates="admin", cascade="all, delete-orphan")
