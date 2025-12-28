from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from firebase_admin import auth as firebase_auth

from app.core.database import get_db
from app.db.models.user import User
from app.db.models.portfolio import Portfolio
from app.utils.currency import convert
from app.core.config import settings
from app.core.jwt_handler import create_access_token
import uuid

from pydantic import BaseModel

router = APIRouter()

class GoogleExchangeRequest(BaseModel):
    token: str  # Firebase ID token


@router.post("/auth/google/exchange_app")
def google_exchange(
    payload: GoogleExchangeRequest,
    db: Session = Depends(get_db),
):
    print("token: ", payload.token)
    # 1️⃣ Verify Firebase ID token
    try:
        decoded_token = firebase_auth.verify_id_token(payload.token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")

    firebase_uid = decoded_token["uid"]
    email = decoded_token.get("email")
    name = decoded_token.get("name")
    avatar_url = decoded_token.get("picture")

    if not email:
        raise HTTPException(status_code=400, detail="Email not available")

    email = email.lower()

    # 2️⃣ Find existing user
    user = db.query(User).filter(User.email == email).first()

    # 3️⃣ If user exists but was created with password → block
    if user and user.provider == "local":
        raise HTTPException(
            status_code=409,
            detail="Account exists with email/password",
        )

    # 4️⃣ Create user if not exists
    if not user:
        username = f"{email.split('@')[0]}_{uuid.uuid4().hex[:6]}"

        user = User(
            username=username,
            email=email,
            password_hash=None,
            provider="google",
            validated=True,
            confirmation_token=None,
            avatar_url=avatar_url,
            currency=settings.currency,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        portfolio = Portfolio(
            user_id=user.id,
            currency=user.currency,
            cash=convert(
                settings.currency,
                user.currency,
                settings.amount_begin,
            ),
        )
        db.add(portfolio)
        db.commit()

    # 5️⃣ Issue YOUR backend JWT
    jwt_token = create_access_token({"uid": str(user.id)})

    return {
        "token": jwt_token,
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "validated": user.validated,
        "avatar_url": user.avatar_url,
        "currency": user.currency,
    }
