from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.models.user import User
from app.db.schemas.user import UserCreate, UserOut
from app.auth.auth import get_current_user
from app.db.schemas.user import UserUpdate 
from app.db.models.portfolio import Portfolio 
from fastapi import Request, HTTPException
from app.auth.auth import get_current_user

router = APIRouter()


@router.get("/me")
def get_current_user_route(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me")
def update_current_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    portfolio = db.query(Portfolio).filter_by(user_id=current_user.id).first()
    portfolio.currency= user_update.currency
    db.commit()
    db.refresh(current_user)

    return {
        "id": current_user.id,
        "username": current_user.username,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "birthdate": current_user.birthdate,
        "phone_number": current_user.phone_number,
        "avatar_url": current_user.avatar_url,
        "currency": current_user.currency,
    }
