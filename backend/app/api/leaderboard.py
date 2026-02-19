from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse
from typing import List, Optional

router = APIRouter(prefix="/api/leaderboard", tags=["leaderboard"])

@router.get("", response_model=List[UserResponse])
def get_leaderboard(
    category: Optional[str] = None,
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(User).filter(
        User.resolved_predictions >= 10,
        User.avg_brier_score.isnot(None)
    )
    
    if category:
        query = query.filter(User.best_category == category)
    
    users = query.order_by(User.avg_brier_score).limit(limit).all()
    return users
