from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import Session, relationship
from app.core.database import Base
from datetime import datetime 
from app.db.models.performance import Performance
from app.db.models.user import User
from sqlalchemy.sql import func

class Portfolio(Base):
    __tablename__ = "portfolios"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    performance = Column(Float)
    performance_pct = Column(Float)
    cash = Column(Float)
    currency = Column(String)
    rank = Column(Integer)
    updated_at = Column(
        DateTime, 
        default=func.now(),       # set on INSERT
        onupdate=func.now(),      # refresh on UPDATE
        nullable=False
    )
    
    transactions = relationship("Transaction", back_populates="portfolio", cascade="all, delete-orphan")
    performances = relationship(Performance, back_populates="portfolio", cascade="all, delete")
    
    performances = relationship(Performance, back_populates="portfolio", cascade="all, delete")
    
    user = relationship(User, back_populates='portfolios')
    
    def to_dict(self):
        return {"cash": round(self.cash,2), "currency": self.currency}



