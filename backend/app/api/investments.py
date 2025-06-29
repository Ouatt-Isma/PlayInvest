from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.database import get_db
from app.db.models.asset import Asset
from app.db.models.portfolio import Portfolio
from app.db.models.transactions import Transaction
from app.auth.auth import get_current_user


router = APIRouter()

@router.get("/history")
def get_transaction_history(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    portfolio = db.query(Portfolio).filter_by(user_id=current_user.id).first()
    if not portfolio:
        return []

    transactions = (
        db.query(Transaction, Asset)
        .join(Asset, Transaction.asset_id == Asset.id)
        .filter(Transaction.portfolio_id == portfolio.id)
        .order_by(Transaction.transaction_date.desc())
        .all()
    )

    history = []
    for tx, asset in transactions:
        amount_invested = tx.quantity * tx.price_per_unit
        current_value = tx.quantity * asset.current_price if hasattr(asset, 'current_price') else amount_invested

        history.append({
            "date": tx.transaction_date,
            "asset_name": asset.name,
            "symbol": asset.symbol,
            "transaction_type": tx.transaction_type,
            "amount_invested": round(amount_invested, 2),
            "current_value": round(current_value, 2),
            "currency": asset.currency,
        })

    return history