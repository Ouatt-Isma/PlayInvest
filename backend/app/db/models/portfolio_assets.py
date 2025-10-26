from sqlalchemy import Column, Integer, Date, Float, ForeignKey, Boolean
from sqlalchemy.orm import Session, relationship
from app.core.database import Base
from datetime import datetime

class PortfolioAsset(Base):
    __tablename__ = "portfolio_assets"
    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    asset_id = Column(Integer, ForeignKey("assets.id"))
    quantity = Column(Float)
    buying_date = Column(Date)
    selling_date = Column(Date, nullable=True)
    buying_price = Column(Float)
    selling_price = Column(Float, nullable=True)
    performance = Column(Float)
    performance_pct = Column(Float)
    total_invest = Column(Float)
    sold = Column(Boolean)
    
    portfolio = relationship("Portfolio", back_populates="passets")
    asset = relationship("Asset", backref="portfolio_assets")
    
    def to_dict(self):
        return {"quantity": self.quantity, "buying_price": self.buying_price, "performance": self.performance, "performance_pct": self.performance_pct, "total_invest": self.total_invest, "sold":self.sold}