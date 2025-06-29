from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, func, CheckConstraint
from sqlalchemy.orm import relationship
from app.core.database import Base
# from app.db.models.asset import Asset
from app.db.models.portfolio import Portfolio
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id", ondelete="CASCADE"))
    asset_id = Column(Integer, ForeignKey("assets.id", ondelete="CASCADE"))
    transaction_type = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    price_per_unit = Column(Float, nullable=False)
    transaction_date = Column(DateTime(timezone=True), server_default=func.now())

    portfolio = relationship(Portfolio, back_populates="transactions")
    asset = relationship("Asset", back_populates="transactions")

    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_quantity_positive"),
        CheckConstraint("price_per_unit >= 0", name="check_price_positive"),
        CheckConstraint("transaction_type IN ('buy', 'sell')", name="check_transaction_type_valid"),
    )
