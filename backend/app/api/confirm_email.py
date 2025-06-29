from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.models.user import User
from app.db.models.portfolio import Portfolio

router = APIRouter()

@router.get("/confirm")
def confirm_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.confirmation_token == token).first()
    if not user:
        raise HTTPException(status_code=404, detail="Token invalide")

    user.validated = True
    portfolio = Portfolio(user_id=user.id, cash=0.0, currency='EUR')
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)

    return {"message": "Email confirmé avec succès"}
