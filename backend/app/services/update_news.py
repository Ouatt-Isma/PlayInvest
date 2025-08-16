# saver.py
from contextlib import contextmanager
from app.core.database import SessionLocal
from app.db.models.news import News
from app.scrapper.sika import get_all

@contextmanager
def get_session():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def save_article(db, row: dict):
    """
    row = {
      "url": ..., "title": ..., "published_at": ..., "author": ...,
      "body": ..., "image_url": ..., "image_path": ...
    }
    """
    # try to find existing by unique url
    obj = db.query(News).filter(News.url == row["url"]).one_or_none()
    if obj:
        # update only when present in row, keep old otherwise
        for k, v in row.items():
            if v is not None and k != "url":
                setattr(obj, k, v)
        return obj

    obj = News(**row)
    db.add(obj)
    return obj

def add_news(db):
    items = get_all()
    try:
        for row in items:
            save_article(db, row)
            print("Saved:", row["title"])
        db.commit()
    except Exception as e:
        print(f"Error: {e}")
        
        