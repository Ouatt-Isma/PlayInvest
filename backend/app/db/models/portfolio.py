from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import Session, relationship
from app.core.database import Base
from datetime import datetime 
from app.db.models.performance import Performance


class Portfolio(Base):
    __tablename__ = "portfolios"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    performance = Column(Float)
    performance_pct = Column(Float)
    cash = Column(Float)
    currency = Column(String)
    
    transactions = relationship("Transaction", back_populates="portfolio", cascade="all, delete-orphan")
    performances = relationship(Performance, back_populates="portfolio", cascade="all, delete")
    
    performances = relationship(Performance, back_populates="portfolio", cascade="all, delete")



