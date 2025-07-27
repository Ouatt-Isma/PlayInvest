from sqlalchemy import Column, Integer, String, JSON, DateTime
from app.core.database import Base  # adjust if your base is defined elsewhere
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
from app.db.models.transactions import Transaction
from sqlalchemy.sql import func

class Quizzes(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    topic = Column(String)
    module = Column(String)
    question = Column(String)
    options = Column(JSON)
    correct_answer = Column(JSON)

    def to_dict(self):
        return {
            "id": self.id,
            "topic": self.topic,
            "module": self.module,
            "options": self.options,
            "question": self.question,
            "correct_answer": self.correct_answer
        }
