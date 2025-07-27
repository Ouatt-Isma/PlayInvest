from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.models.articles import Articles  # adjust path to your model
from app.auth.auth import get_current_user
from app.db.models.user import User

router = APIRouter()


@router.get("/articles")
def get_articles(
    db: Session = Depends(get_db),
):
    articles = db.query(Articles).order_by(Articles.id.desc()).all()
    
    return [
        a.to_dict() for a in articles
    ]
