from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.database import get_db
from app.db.models.asset import Asset

router = APIRouter()

PERIOD_TO_DAYS = {
    "7d": 7,
    "1m": 30,
    "3m": 90,
    "6m": 180,
    "1y": 360,
    "all": None,
}

@router.get("/graph/{symbol}")
def get_asset_graph(
    symbol: str,
    period: str = Query(default=None),
    start_date: str = Query(default=None),
    end_date: str = Query(default=None),
    db: Session = Depends(get_db)
):
    asset = db.query(Asset).filter(Asset.symbol == symbol).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    if not asset.financial_data or not isinstance(asset.financial_data, list):
        return {"symbol": symbol, "prices": []}

    # Parse financial data into usable structure
    try:
        parsed_data = [
            {
                "date": datetime.strptime(entry["date"], "%Y-%m-%d"),
                "price": round(entry["close"], 2)
            }
            for entry in asset.financial_data
            if "date" in entry and "close" in entry
        ]
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to parse financial_data: {e}")

    # Handle custom start_date and end_date
    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

        if start > end:
            raise HTTPException(status_code=400, detail="start_date must be before end_date")

        filtered = [entry for entry in parsed_data if start <= entry["date"] <= end]

    # Fallback to period
    elif period:
        if period not in PERIOD_TO_DAYS:
            raise HTTPException(status_code=400, detail="Invalid period")

        if period == "all":
            filtered = parsed_data
        else:
            cutoff = datetime.utcnow() - timedelta(days=PERIOD_TO_DAYS[period])
            filtered = [entry for entry in parsed_data if entry["date"] >= cutoff]

    else:
        raise HTTPException(status_code=400, detail="You must provide either period or start_date and end_date")

    # Sort chronologically
    sorted_filtered = sorted(filtered, key=lambda x: x["date"])

    # Return as ISO strings
    prices = [
        {"date": entry["date"].strftime("%Y-%m-%d"), "price": entry["price"]}
        for entry in sorted_filtered
    ]

    return {"symbol": symbol, "prices": prices}
