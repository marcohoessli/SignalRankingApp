from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.question import Question
from app.models.prediction import Prediction
from app.models.user import User
from app.models.admin_log import AdminLog
from app.schemas.question import QuestionCreate, QuestionUpdate, QuestionResponse, QuestionResolve
from app.utils.auth import get_current_user, get_current_admin
from typing import List, Optional
from datetime import datetime

router = APIRouter(prefix="/api/questions", tags=["questions"])

@router.get("", response_model=List[QuestionResponse])
def get_questions(
    status: Optional[str] = None,
    category: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    query = db.query(Question)
    
    if status:
        query = query.filter(Question.status == status)
    if category:
        query = query.filter(Question.category == category)
    if search:
        query = query.filter(Question.title.ilike(f"%{search}%"))
    
    questions = query.order_by(Question.created_at.desc()).offset(skip).limit(limit).all()
    return questions

@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(question_id: int, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

@router.post("", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
def create_question(
    question_data: QuestionCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    question = Question(
        **question_data.dict(),
        created_by=current_user.id
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    
    # Log action
    log = AdminLog(
        admin_id=current_user.id,
        action="create_question",
        target_type="question",
        target_id=question.id
    )
    db.add(log)
    db.commit()
    
    return question

@router.put("/{question_id}", response_model=QuestionResponse)
def update_question(
    question_id: int,
    question_data: QuestionUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    for key, value in question_data.dict(exclude_unset=True).items():
        setattr(question, key, value)
    
    db.commit()
    db.refresh(question)
    
    # Log action
    log = AdminLog(
        admin_id=current_user.id,
        action="update_question",
        target_type="question",
        target_id=question.id
    )
    db.add(log)
    db.commit()
    
    return question

@router.post("/{question_id}/close")
def close_question(
    question_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    question.status = "CLOSED"
    db.commit()
    
    # Log action
    log = AdminLog(
        admin_id=current_user.id,
        action="close_question",
        target_type="question",
        target_id=question.id
    )
    db.add(log)
    db.commit()
    
    return {"message": "Question closed successfully"}

@router.post("/{question_id}/resolve")
def resolve_question(
    question_id: int,
    resolve_data: QuestionResolve,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    question.status = "RESOLVED"
    question.outcome = resolve_data.outcome
    question.resolve_time = datetime.utcnow()
    
    # Calculate Brier scores for all predictions
    predictions = db.query(Prediction).filter(Prediction.question_id == question_id).all()
    outcome_value = 1.0 if resolve_data.outcome else 0.0
    
    for pred in predictions:
        prob_decimal = pred.probability / 100.0
        brier = (prob_decimal - outcome_value) ** 2
        pred.brier_score = brier
        
        # Update user stats
        user = pred.user
        user.resolved_predictions += 1
        
        # Recalculate average Brier score
        avg_brier = db.query(func.avg(Prediction.brier_score)).filter(
            Prediction.user_id == user.id,
            Prediction.brier_score.isnot(None)
        ).scalar()
        user.avg_brier_score = float(avg_brier) if avg_brier else None
    
    db.commit()
    
    # Recalculate rankings
    users_with_scores = db.query(User).filter(
        User.resolved_predictions >= 10,
        User.avg_brier_score.isnot(None)
    ).order_by(User.avg_brier_score).all()
    
    for rank, user in enumerate(users_with_scores, start=1):
        user.rank_global = rank
    
    db.commit()
    
    # Log action
    log = AdminLog(
        admin_id=current_user.id,
        action="resolve_question",
        target_type="question",
        target_id=question.id
    )
    db.add(log)
    db.commit()
    
    return {"message": "Question resolved successfully"}

@router.delete("/{question_id}")
def delete_question(
    question_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    db.delete(question)
    db.commit()
    
    # Log action
    log = AdminLog(
        admin_id=current_user.id,
        action="delete_question",
        target_type="question",
        target_id=question_id
    )
    db.add(log)
    db.commit()
    
    return {"message": "Question deleted successfully"}
