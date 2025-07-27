from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean
from app.core.database import Base  # adjust if your base is defined elsewhere
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
from app.db.models.transactions import Transaction
from sqlalchemy.sql import func

class Articles(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    topic = Column(String)
    article_id = Column(String)
    category = Column(String)
    resume = Column(String)
    famous = Column(Boolean)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "topic": self.topic,
            "article_id": self.article_id,
            "category": self.category,
            "resume": self.resume,
            "famous": self.famous,
            "created_at": self.created_at.isoformat() if hasattr(self, "created_at") else None
        }