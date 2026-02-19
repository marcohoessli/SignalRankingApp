from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserStats(BaseModel):
    total_predictions: int
    resolved_predictions: int
    avg_brier_score: Optional[float]
    rank_global: Optional[int]
    last_30d_brier: Optional[float]
    best_category: Optional[str]
    streak: int

class UserResponse(UserBase):
    id: int
    role: str
    email_verified: bool
    created_at: datetime
    total_predictions: int
    resolved_predictions: int
    avg_brier_score: Optional[float]
    rank_global: Optional[int]
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str
