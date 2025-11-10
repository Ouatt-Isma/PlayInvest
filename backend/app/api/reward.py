from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.db.models.user import User
from app.db.models.portfolio import Portfolio
from app.auth.auth import get_current_user
from app.core.config import settings
from app.utils.currency import convert

router = APIRouter()


@router.get("/reward")
def reward_user(
    field_name: str = Query(..., description="The boolean field name to check (e.g., 'quiz1_completed')"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify the field exists on the user model
    if not hasattr(current_user, field_name):
        raise HTTPException(status_code=400, detail=f"Invalid field name: {field_name}")

    # Get the value of that field
    field_value = getattr(current_user, field_name)

    # If the field is already True, don't reward again
    if field_value:
        return {"message": "Prime déjà créditée!."}

    # Otherwise, set the field to True and increase cash
    setattr(current_user, field_name, True)

    # Get user's portfolio and update cash
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == current_user.id).first()
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    portfolio.cash += convert(settings.currency, portfolio.currency, settings.amount_tutorial)

    # Commit the transaction
    db.commit()
    db.refresh(current_user)
    db.refresh(portfolio)

    return {"message": f"Vous venez d'être crédité d'une prime de {settings.amount_tutorial}€."}


# 👇 NEW ENDPOINT — Save Quiz Results
@router.post("/profile_quiz_result")
def save_quiz_result(
    profile: str = Query(..., description="Nom du profil obtenu (ex: 'Prudent', 'Modéré')"),
    score: int = Query(..., description="Score total obtenu sur 150"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Save the user's quiz result (profil investisseur) in the database.
    """
    # Optional: you can validate the score range
    if score < 0 or score > 150:
        raise HTTPException(status_code=400, detail="Score invalide (doit être entre 0 et 150)")

    # Create a new QuizResult row
    setattr(current_user, "investor_score", score)
    setattr(current_user, "profile_level", profile)
    
    db.commit()
    db.refresh(current_user)


    return {
        "message": f"Résultat du test enregistré avec succès pour {profile}.",
        "data": {
            "user_id": current_user.id,
            "profile": profile,
            "score": score,
        }
    }
