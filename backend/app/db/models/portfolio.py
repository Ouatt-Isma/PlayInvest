from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import Session, relationship
from app.core.database import Base
from datetime import datetime 
from app.db.models.performance import Performance
from app.db.models.user import User


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
    
    transactions = relationship("Transaction", back_populates="portfolio", cascade="all, delete-orphan")
    performances = relationship(Performance, back_populates="portfolio", cascade="all, delete")
    
    performances = relationship(Performance, back_populates="portfolio", cascade="all, delete")
    
    user = relationship(User, back_populates='portfolios')
    
    def to_dict(self):
        return {"cash": round(self.cash,2), "currency": self.currency}



