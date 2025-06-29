from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.models.user import User
from app.db.schemas.user import UserCreate, UserOut
from app.auth.auth import get_current_user
from app.db.schemas.user import UserUpdate 
from fastapi import Request,  HTTPException, status
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from app.core.config import settings
from app.utils.token import confirm_reset_token, generate_reset_token
from app.utils.email import send_password_reset_email
from app.db.models.user import get_user_by_email

SECRET_KEY =  settings.SECRET_KEY
SECURITY_PASSWORD_SALT = settings.SECURITY_PASSWORD_SALT

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str
    
router = APIRouter()

@router.post("/users", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/update-password")
def update_password(data: PasswordUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
 
    if not current_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    if not pwd_context.verify(data.current_password, current_user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Mot de passe actuel incorrect.")
    
    hashed_password = pwd_context.hash(data.new_password)
    current_user.password_hash = hashed_password
    db.commit()
    return {"message": "Mot de passe mis à jour avec succès"}

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

@router.post("/forgot-password")
async def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    print(data.email)
    user = get_user_by_email(db, data.email)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    token = generate_reset_token(user.email)
    await send_password_reset_email(user.email, user.username, token)

    return {"message": "Un lien de réinitialisation a été envoyé à votre adresse email."}


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str

@router.post("/reset-password")
async def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    email = confirm_reset_token(data.token)
    
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    hashed_pw = pwd_context.hash(data.new_password)  # à adapter avec ta logique de hash
    user.password_hash = hashed_pw
    db.commit()
    return {"message": "Mot de passe mis à jour avec succès"}