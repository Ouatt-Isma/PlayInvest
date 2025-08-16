from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.models.quizzes import Quizzes
from app.db.models.quiz_results import QuizResult  # make sure this is imported
from app.db.models.user import User
from app.auth.auth import get_current_user

from pydantic import BaseModel
from datetime import datetime
from app.db.models.portfolio import Portfolio
from app.core.config import settings
from app.utils.currency import convert 


# Pydantic input model
class QuizResultIn(BaseModel):
    topic: str
    module: str
    score: int
    total: int
    percent: float
    passed: bool
    time_seconds: int
    completed_at: datetime
    
    
router = APIRouter()

@router.get("/quizzes")
def list_quizzes(topic: str = Query(None), db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if topic:
        quizzes = db.query(Quizzes).filter(Quizzes.topic == topic).all()
    else:
        quizzes = db.query(Quizzes).all()
    
    print(f"Fetched {len(quizzes)} quizzes" + (f" for topic: {topic}" if topic else ""))
    return [q.to_dict() for q in quizzes]


# ✅ NEW ENDPOINT
@router.get("/quiz-results/status")
def quiz_status(
    topic: str = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = (
        db.query(QuizResult)
        .filter(QuizResult.topic == topic, QuizResult.user_id == current_user.id)
        .order_by(QuizResult.completed_at.desc())
        .first()
    )

    if not result:
        return {"passed": False}

    print({
        "passed": result.passed,
        "score": result.score,
        "percent": result.percent,
        "completed_at": result.completed_at.isoformat()
    })
    return {
        "passed": result.passed,
        "score": result.score,
        "percent": result.percent,
        "completed_at": result.completed_at.isoformat()
    }
    
@router.post("/quiz-results")
def save_quiz_result(
    payload: QuizResultIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_id = current_user.id

    # Do nothing if not passed
    if not payload.passed:
        return {"message": "Le quiz n'a pas été réussi, aucun résultat enregistré."}

    # Check if user already passed this topic before
    existing_pass = (
        db.query(QuizResult)
        .filter(
            QuizResult.topic == payload.topic,
            QuizResult.user_id == user_id,
            QuizResult.passed == True
        )
        .first()
    )

    # If already passed, don't add cash or duplicate result
    if existing_pass:
        return {"message": "Quiz déjà réussi précédemment. Aucun ajout de cash ni enregistrement."}

    # Save the result since it's passed and hasn't been passed before
    new_result = QuizResult(
        user_id=user_id,
        topic=payload.topic,
        module=payload.module,
        score=payload.score,
        total=payload.total,
        percent=payload.percent,
        passed=True,
        time_seconds=payload.time_seconds,
        completed_at=payload.completed_at
    )
    db.add(new_result)

    # Add cash to portfolio
    portfolio = db.query(Portfolio).filter_by(user_id=user_id).first()
    portfolio.cash += convert(settings.currency, portfolio.currency, settings.amount_qcm)
    db.add(portfolio)

    db.commit()
    db.refresh(new_result)

    return {"message": "Résultat enregistré et récompense ajoutée.", "id": new_result.id}