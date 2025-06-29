from sqlalchemy import Column, Integer, String, DateTime, Boolean, Date
from sqlalchemy.orm import Session
from app.core.database import Base
from datetime import datetime
from app.core.config import settings
import uuid


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    referrer_id = Column(String, nullable=True)
    validated = Column(Boolean, default=False)
    confirmation_token = Column(String, nullable=False)
    avatar_url = Column(String, default=settings.DEFAULT_AVATAR)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    birthdate = Column(Date, nullable=True)
    phone_number = Column(String, nullable=True)
    uid = Column(String, unique=True, index=True, default=lambda: str(uuid.uuid4()))
    
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
