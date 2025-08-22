from sqlalchemy import Column, Integer, Float, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base  # or your specific Base class path

class Performance(Base):
    __tablename__ = "performance"

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"), nullable=False)
    date = Column(Date, nullable=False)

    # Performance by category
    category_etf = Column(Float)
    category_crypto = Column(Float)
    category_stock = Column(Float)

    # Performance by region
    region_africa = Column(Float)
    region_usa = Column(Float)
    region_europe = Column(Float)
    region_world = Column(Float)
    
    global_perf = Column(Float)

    __table_args__ = (UniqueConstraint("portfolio_id", "date", name="_portfolio_date_uc"),)

    # Optional: if you want to access portfolio from perf
    portfolio = relationship("Portfolio", back_populates="performances")

