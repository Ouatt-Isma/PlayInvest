from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime
from app.db.models.asset import Asset
from app.core.database import get_db

router = APIRouter()

class PastPerfRequest(BaseModel):
    asset_id: int
    amount: float
    start_date: str  # format: YYYY-MM-DD
    end_date: str

@router.post("/pastperf")
def simulate_past_performance(payload: PastPerfRequest, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == payload.asset_id).first()
    if not asset or not isinstance(asset.financial_data, list):
        return {"performance": 0.0, "current_value": payload.amount}

    # Extract prices
    def get_price_at(date_str):
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        closest = min(
            asset.financial_data,
            key=lambda x: abs(datetime.strptime(x["date"], "%Y-%m-%d").date() - target_date),
            default=None
        )
        return closest["close"] if closest else None

    price_start = get_price_at(payload.start_date)
    price_end = get_price_at(payload.end_date)

    if not price_start or not price_end or price_start == 0:
        return {"performance": 0.0, "current_value": payload.amount}

    performance = round((price_end - price_start) / price_start * 100, 2)
    current_value = payload.amount * (price_end / price_start)
    print(payload.amount)
    return {"performance": performance, "current_value": current_value}
