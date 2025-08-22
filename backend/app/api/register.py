from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from app.core.database import engine, SessionLocal, Base
from app.db.models.user import User




from fastapi import BackgroundTasks
import uuid
from app.utils.email import send_confirmation_email
Base.metadata.create_all(bind=engine)
router = APIRouter()

class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str
    referrer_id: str 


# @router.post("/register")
# def register(user: RegisterUser):
#     db: Session = SessionLocal()
#     existing = db.query(User).filter(User.email == user.email).first()
#     if existing:
#         raise HTTPException(status_code=400, detail="Email déjà utilisé")

#     hashed_pw = bcrypt.hash(user.password)
#     new_user = User(
#     username=user.username.lower(),
#     email=user.email,
#     password_hash=hashed_pw  
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return {"message": "Compte créé", "user_id": new_user.id}



@router.post("/register")
def register(user: RegisterUser, background_tasks: BackgroundTasks):
    db: Session = SessionLocal()
    existing = db.query(User).filter(User.email == user.email.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    existing = db.query(User).filter(User.username == user.username.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà utilisé")
    hashed_pw = bcrypt.hash(user.password)
    token = str(uuid.uuid4())  # Store this in DB if you want to verify later
    parrain_uid = None 
    if(user.referrer_id):
        parrain = db.query(User).filter(User.username == user.referrer_id.lower()).first()
        if not parrain:
            raise HTTPException(status_code=400, detail="Nom d'utilisateur du parrain inexistant")
        parrain_uid = parrain.uid
    
    new_user = User(
        username=user.username.lower(),
        email=user.email.lower(),
        password_hash=hashed_pw,
        referrer_id = parrain_uid,
        confirmation_token = token
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate confirmation token
    

    # Send email in the background
    background_tasks.add_task(send_confirmation_email, user.email.lower(), user.username.lower(), token)
    return {"message": "Compte créé. Vérifiez votre email pour confirmer.", "user_id": new_user.id}


