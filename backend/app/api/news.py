from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.models.news import News  # adjust path to your model
from app.auth.auth import get_current_user
from app.db.models.user import User

router = APIRouter()


@router.get("/news")
def get_news(
    db: Session = Depends(get_db),
):
    news = db.query(News).order_by(News.id.desc()).all()
    
    return [
        a.to_dict() for a in news
    ]
