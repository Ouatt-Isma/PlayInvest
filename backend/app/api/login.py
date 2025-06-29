from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from app.core.database import get_db
from app.db.models.user import User
from app.db.models.portfolio import Portfolio
import uuid
from typing import Optional
from app.core.jwt_handler import create_access_token

router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    token: str
    validated: bool
    user_id: str
    avatar_url: Optional[str] = None 
    first_name: Optional[str] = None  
    currency: Optional[str] = None  

@router.post("/login", response_model=LoginResponse)
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user or not bcrypt.verify(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect")

    if not user.validated:
        return {
            "token": "",
            "validated": False,
            "user_id": user.uid,  # Use uid here
            "avatar_url": user.avatar_url,
            "first_name": user.first_name
        }
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == user.id).first()
    currency = portfolio.currency if portfolio else None
    token = create_access_token({"uid": user.uid})
    print(currency)
    return {
        "token": token,
        "validated": True,
        "user_id": user.uid,
        "avatar_url": user.avatar_url,
        "first_name": user.first_name, 
        "currency": currency, 
    }