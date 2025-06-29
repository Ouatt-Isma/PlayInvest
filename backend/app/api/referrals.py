from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.models.user import User
from app.auth.auth import get_current_user
from fastapi import Request, HTTPException

router = APIRouter()

@router.get("/referrals")
def get_referrals(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    referrals = db.query(User).filter(User.referrer_id == current_user.uid).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "created_at": u.created_at,
            "avatar_url": u.avatar_url,
        }
        for u in referrals
    ]