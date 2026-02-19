from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.prediction import Prediction
from app.models.question import Question
from app.models.user import User
from app.schemas.prediction import PredictionCreate, PredictionUpdate, PredictionResponse
from app.utils.auth import get_current_user
from typing import List
from datetime import datetime

router = APIRouter(prefix="/api/predictions", tags=["predictions"])

@router.get("", response_model=List[PredictionResponse])
def get_my_predictions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    predictions = db.query(Prediction).filter(Prediction.user_id == current_user.id).all()
    return predictions

@router.post("", response_model=PredictionResponse, status_code=status.HTTP_201_CREATED)
def create_prediction(
    prediction_data: PredictionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if question exists and is open
    question = db.query(Question).filter(Question.id == prediction_data.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    if question.status != "OPEN":
        raise HTTPException(status_code=400, detail="Question is not open for predictions")
    
    if question.close_time < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Question deadline has passed")
    
    # Check if prediction already exists
    existing = db.query(Prediction).filter(
        Prediction.user_id == current_user.id,
        Prediction.question_id == prediction_data.question_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Prediction already exists. Use PUT to update.")
    
    # Create prediction
    prediction = Prediction(
        user_id=current_user.id,
        question_id=prediction_data.question_id,
        probability=prediction_data.probability
    )
    
    db.add(prediction)
    current_user.total_predictions += 1
    db.commit()
    db.refresh(prediction)
    
    return prediction

@router.put("/{prediction_id}", response_model=PredictionResponse)
def update_prediction(
    prediction_id: int,
    prediction_data: PredictionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prediction = db.query(Prediction).filter(
        Prediction.id == prediction_id,
        Prediction.user_id == current_user.id
    ).first()
    
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    
    # Check if question is still open
    question = prediction.question
    if question.status != "OPEN":
        raise HTTPException(status_code=400, detail="Cannot update prediction after question closes")
    
    if question.close_time < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Question deadline has passed")
    
    prediction.probability = prediction_data.probability
    prediction.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(prediction)
    
    return prediction

@router.get("/question/{question_id}", response_model=PredictionResponse)
def get_prediction_for_question(
    question_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    prediction = db.query(Prediction).filter(
        Prediction.user_id == current_user.id,
        Prediction.question_id == question_id
    ).first()
    
    if not prediction:
        raise HTTPException(status_code=404, detail="No prediction found for this question")
    
    return prediction
