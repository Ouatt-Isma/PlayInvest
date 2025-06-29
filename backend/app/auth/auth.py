from fastapi import Depends, HTTPException, Request
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.models.user import User
from app.core.config import settings
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid: str = payload.get("uid")
        if uid is None:
            raise JWTError()
        return uid
    except JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token manquant")
    token = auth_header.split(" ")[1]
    print(token)
    uid = decode_token(token)
    print(uid)
    user = db.query(User).filter(User.uid == uid).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    return user
