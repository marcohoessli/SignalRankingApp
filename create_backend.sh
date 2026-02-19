#!/bin/bash

# Create schemas
cat > /tmp/marcohoessli/SignalRankingApp/backend/app/schemas/question.py << 'EOF'
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
EOF

cat > /tmp/marcohoessli/SignalRankingApp/backend/app/schemas/prediction.py << 'EOF'
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
EOF

cat > /tmp/marcohoessli/SignalRankingApp/backend/app/schemas/__init__.py << 'EOF'
from .user import UserCreate, UserLogin, UserResponse, Token, PasswordResetRequest, PasswordReset
from .question import QuestionCreate, QuestionUpdate, QuestionResponse, QuestionResolve
from .prediction import PredictionCreate, PredictionUpdate, PredictionResponse

__all__ = [
    "UserCreate", "UserLogin", "UserResponse", "Token", "PasswordResetRequest", "PasswordReset",
    "QuestionCreate", "QuestionUpdate", "QuestionResponse", "QuestionResolve",
    "PredictionCreate", "PredictionUpdate", "PredictionResponse"
]
EOF

# Create core __init__.py files
touch /tmp/marcohoessli/SignalRankingApp/backend/app/__init__.py
touch /tmp/marcohoessli/SignalRankingApp/backend/app/core/__init__.py
touch /tmp/marcohoessli/SignalRankingApp/backend/app/api/__init__.py
touch /tmp/marcohoessli/SignalRankingApp/backend/app/services/__init__.py
touch /tmp/marcohoessli/SignalRankingApp/backend/app/utils/__init__.py

echo "Backend schemas created successfully"
