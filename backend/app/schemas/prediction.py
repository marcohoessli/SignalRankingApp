from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class PredictionCreate(BaseModel):
    question_id: int
    probability: float = Field(ge=0, le=100)

class PredictionUpdate(BaseModel):
    probability: float = Field(ge=0, le=100)

class PredictionResponse(BaseModel):
    id: int
    user_id: int
    question_id: int
    probability: float
    created_at: datetime
    updated_at: datetime
    brier_score: Optional[float]
    
    class Config:
        from_attributes = True
