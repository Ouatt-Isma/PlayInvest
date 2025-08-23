# app/routers/ranking.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.models.portfolio import Portfolio
from app.db.models.user import User
from app.auth.auth import get_current_user

router = APIRouter()

@router.get("/ranking")
def get_ranking(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Returns current user's rank + top 3 users based on the `ranking` column
    in the Portfolio table. We only keep the best-ranked portfolio per user.
    """
    # Get the best portfolio for each user
    best_portfolios = (
        db.query(Portfolio)
        .order_by(Portfolio.user_id, Portfolio.rank)  # lowest rank first
        .all()
    )

    # Dictionary: user_id -> best portfolio
    best_per_user = {}
    for p in best_portfolios:
        if p.user_id not in best_per_user:
            best_per_user[p.user_id] = p  # keep first (best rank) portfolio

    # Convert to list and sort by ranking
    ranking_list = sorted(
    best_per_user.values(),
    key=lambda x: (x.rank is None, x.rank if x.rank is not None else float("inf"))
)
    
    # Build clean list
    ranking_data = [
        {
            "username": p.user.username,
            "rank": p.rank,
            "score": round(p.performance_pct or 0.0, 2)
        }
        for p in ranking_list
    ]

    # Current user entry
    me_entry = next(
        (r for r in ranking_data if r["username"] == current_user.username),
        None
    )

    return {
        "currentUser": me_entry,
        "top": ranking_data[:3]
    }
