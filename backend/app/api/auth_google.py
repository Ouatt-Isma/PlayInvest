from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.models.user import User
from app.db.models.portfolio import Portfolio
from app.utils.currency import convert
from app.core.config import settings
import requests
from app.core.jwt_handler import create_access_token, verify_token
import uuid
import urllib.parse
import datetime

from pydantic import BaseModel

class GoogleExchangeRequest(BaseModel):
    token: str


router = APIRouter()

@router.get("/auth/google")
def google_login():
    print(settings.GOOGLE_REDIRECT_URI)
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid email profile",
        "access_type": "offline",
        "prompt": "select_account",
    }

    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)
    return RedirectResponse(url)


@router.get("/auth/google/callback")
def google_callback(code: str, db: Session = Depends(get_db)):

    token_res = requests.post(
        "https://oauth2.googleapis.com/token",
        data={
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        },
    )

    if token_res.status_code != 200:
        return RedirectResponse(f"{settings.FRONTEND_URL}/login?error=google_auth")

    access_token = token_res.json()["access_token"]

    userinfo = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()

    email = userinfo["email"].lower()
    avatar_url = userinfo.get("picture")

    user = db.query(User).filter(User.email == email).first()

    if user and user.provider == "local":
        return RedirectResponse(
            f"{settings.FRONTEND_URL}/login?error=account_exists_password"
        )

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
            cash=convert(settings.currency, user.currency, settings.amount_begin),
        )
        db.add(portfolio)
        db.commit()

    jwt_token = create_access_token({"uid": str(user.id)})

    redirect_url = getattr(
    settings,
    "MOBILE_REDIRECT_URL",
    f"{settings.FRONTEND_URL}/auth/google/callback"
)

    return RedirectResponse(
        f"{redirect_url}?token={jwt_token}"
    )

    # return RedirectResponse(
    #     f"{settings.FRONTEND_URL}/auth/google/callback?token={jwt_token}"
    # )



@router.post("/auth/google/exchange")
def google_exchange(
    request: Request,
    payload: GoogleExchangeRequest,
    db: Session = Depends(get_db)
):
    print("RAW BODY:", request.headers.get("content-type"))
    token = payload.token
    uid = verify_token(token)
    if not uid:
        raise HTTPException(status_code=401)

    user = db.query(User).filter(User.id == uid).first()
    if not user:
        raise HTTPException(status_code=404)
    portfolio = db.query(Portfolio).filter(Portfolio.user_id == user.id).first()
    currency = portfolio.currency if portfolio else None
    token = create_access_token({"uid": user.uid})
    return {
        "token": token,
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "validated": user.validated,
        "avatar_url": user.avatar_url,
        "currency": currency, 
    }
