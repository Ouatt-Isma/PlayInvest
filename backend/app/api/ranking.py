# app/routers/ranking.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, contains_eager
from sqlalchemy import case, func
from app.core.database import get_db
from app.db.models.portfolio import Portfolio
from app.db.models.user import User
from app.auth.auth import get_current_user

router = APIRouter()

@router.get("/ranking")
def get_ranking(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Returns current user's position + top 3 users based on the `rank` column.
    We only keep the best-ranked portfolio per user (lowest rank; NULLs last).
    """

    # Treat NULL ranks as "worst" for ordering
    nulls_last = case((Portfolio.rank.is_(None), 1), else_=0)

    # Row-number portfolios within each user by (best rank first, NULL last)
    rn = func.row_number().over(
        partition_by=Portfolio.user_id,
        order_by=(nulls_last.asc(), Portfolio.rank.asc())
    )

    # Subquery: id of best (rn=1) portfolio per user; join Users to avoid orphans
    subq = (
        db.query(
            Portfolio.id.label("pid"),
            Portfolio.user_id.label("uid"),
            rn.label("rn"),
        )
        .join(User, User.id == Portfolio.user_id)  # filters out orphans
        .subquery()
    )

    # Fetch the best portfolio per user, with eager-loaded User
    best_per_user = (
        db.query(Portfolio)
        .join(subq, subq.c.pid == Portfolio.id)
        .join(User, User.id == Portfolio.user_id)
        .options(contains_eager(Portfolio.user))
        .filter(subq.c.rn == 1)
        .order_by(nulls_last.asc(), Portfolio.rank.asc())
        .all()
    )

    # Build clean list
    ranking_list = [
        {
            "username": p.user.username,
            "rank": p.rank,
            "score": round(p.performance_pct or 0.0, 2),
            "user_id": p.user_id,
        }
        for p in best_per_user
    ]

    # Remove "user_id" from the payload later; keep it internally to find "me"
    user_id_to_pos = {row["user_id"]: i + 1 for i, row in enumerate(ranking_list)}
    me_pos = user_id_to_pos.get(current_user.id)

    me_entry = None
    if me_pos is not None:
        me_portfolio = next(r for r in ranking_list if r["user_id"] == current_user.id)
        me_entry = {
            "username": me_portfolio["username"],
            "rank": me_portfolio["rank"],
            "score": me_portfolio["score"],
            "position": me_pos,
        }


    return {
        "currentUser": me_entry,
        "top": ranking_list[:3]
    }
