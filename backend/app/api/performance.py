
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.database import get_db
from app.db.models.asset import Asset
from app.db.models.portfolio import Portfolio
from app.db.models.transactions import Transaction
from app.auth.auth import get_current_user
from datetime import date 
from app.db.models.performance import Performance

router = APIRouter()

@router.get("/performance")
def get_perf_data(
    filter: str,  # 'category' or 'region'
    period: str = '1m',  # '7d', '1m', '3m', '1y', 'all'
    db: Session = Depends(get_db),
    portfolio_id: int = 1
):
    assert filter in ['category', 'region']

    # Compute start date
    today = date.today()
    days = {
        '7d': 7,
        '1m': 30,
        '3m': 90,
        '6m': 180,
        '1y': 365,
        'all': 10000
    }
    start_date = today - timedelta(days=days[period])

    # Query rows
    results = db.query(Performance).filter(
        Performance.portfolio_id == portfolio_id,
        Performance.date >= start_date
    ).order_by(Performance.date).all()

    labels = [r.date.isoformat() for r in results]

    if filter == 'category':
        data = {
            "ETF": [r.category_etf for r in results],
            "Crypto": [r.category_crypto for r in results],
            "Stock": [r.category_stock for r in results],
        }
    else:
        data = {
            "Africa": [r.region_africa for r in results],
            "USA": [r.region_usa for r in results],
            "Europe": [r.region_europe for r in results],
            "World": [r.region_world for r in results],
        }

    return {
        "labels": labels,
        "data": data
    }
