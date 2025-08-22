from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date
from app.core.database import get_db
from app.db.models.performance import Performance

router = APIRouter()

@router.get("/performance")
def get_perf_data(
    filter: str,                 # 'category' or 'region'
    period: str = "1m",          # '7d', '1m', '3m', '6m', '1y', 'all'
    db: Session = Depends(get_db),
    portfolio_id: int = 1
):
    # Validate inputs
    
    valid_filters = {"category", "region", "all"}
    if filter not in valid_filters:
        raise HTTPException(status_code=400, detail=f"Invalid filter. Use one of {sorted(valid_filters)}.")

    period_days = {
        "7d": 7,
        "1m": 30,
        "3m": 90,
        "6m": 180,
        "1y": 365,
        "all": 10000,  # effectively "back to the beginning"
    }
    if period not in period_days:
        raise HTTPException(status_code=400, detail=f"Invalid period. Use one of {sorted(period_days)}.")

    today = date.today()
    start_date = today - timedelta(days=period_days[period])

    # Fetch available rows in the range
    rows = (
        db.query(Performance)
        .filter(
            Performance.portfolio_id == portfolio_id,
            Performance.date >= start_date,
            Performance.date <= today,
        )
        .order_by(Performance.date)
        .all()
    )

    # Map date -> row for quick lookup
    by_date = {r.date: r for r in rows}

    # Build continuous daily labels
    labels = []
    d = start_date
    while d <= today:
        labels.append(d.isoformat())
        d += timedelta(days=1)

    # Prepare metric keys per filter
    if filter == "category":
        metric_fields = [
            ("ETF", "category_etf"),
            ("Crypto", "category_crypto"),
            ("Stock", "category_stock"),
        ]
    elif filter == "region":
        metric_fields = [
            ("Africa", "region_africa"),
            ("USA", "region_usa"),
            ("Europe", "region_europe"),
            ("World", "region_world"),
        ]
    else: 
        metric_fields = [
            ("Global", "global_perf"),
        ]

    # Forward-fill values day by day (start at 0.0 before first known value)
    series = {public: [] for public, _ in metric_fields}
    last_vals = {public: 0.0 for public, _ in metric_fields}

    d = start_date
    while d <= today:
        row = by_date.get(d)
        if row is not None:
            for public_name, field in metric_fields:
                val = getattr(row, field, 0.0) or 0.0
                last_vals[public_name] = float(val)
        # append current value (either updated from row or forward-filled)
        for public_name, _ in metric_fields:
            series[public_name].append(last_vals[public_name])
        d += timedelta(days=1)

    # Shape response
    data = {public: series[public] for public, _ in metric_fields}

    return {
        "labels": labels,
        "data": data,
    }
