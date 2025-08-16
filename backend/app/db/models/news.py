from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, UniqueConstraint
from sqlalchemy.sql import func
from app.core.database import Base

class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # --- new fields used by the scraper/table ---
    url = Column(Text, nullable=False, index=True)
    title = Column(Text, nullable=False)
    published_at = Column(DateTime(timezone=True), nullable=True)
    author = Column(String(255), nullable=True)
    body = Column(Text, nullable=True)
    source = Column(String(255), nullable=True, server_default="sikafinance")
    image_url = Column(Text, nullable=True)
    image_path = Column(Text, nullable=True)
    category = Column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint("url", name="uq_news_url"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            # new fields
            "url": self.url,
            "title": self.title,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "author": self.author,
            "body": self.body,
            "source": self.source,
            "image_url": self.image_url,
            "image_path": self.image_path,
            "category": self.category,
        }
