from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base  # adjust as needed
from sqlalchemy.sql import func

class QuizResult(Base):
    __tablename__ = "quiz_results"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    module = Column(String)
    topic = Column(String)

    score = Column(Integer)
    total = Column(Integer)
    percent = Column(Float)
    passed = Column(Boolean)
    time_seconds = Column(Integer)

    completed_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "module": self.module,
            "topic": self.topic,
            "score": self.score,
            "total": self.total,
            "percent": self.percent,
            "passed": self.passed,
            "time_seconds": self.time_seconds,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }