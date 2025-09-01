# app/routers/challenges.py
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.core.database import get_db
from app.auth.auth import get_current_user
from app.db.models.user import User
from app.db.models.asset import Asset

# ⬇️ Replace with your actual model paths/names
from app.db.models.weekly_challenge import WeeklyChallenge, WeeklyChallengeSide, WeeklyChallengePick
from sqlalchemy.orm import joinedload

router = APIRouter()


# ---------- Schemas ----------
class SubmitBody(BaseModel):
    # Prefer sideId with the new schema; keep assetId for backward compatibility
    sideId: Optional[int] = None


# ---------- Helpers ----------
def now_utc() -> datetime:
    # Use timezone-aware UTC for robust comparisons
    return datetime.now(timezone.utc)

def serialize_asset(a: Asset) -> dict:
    """
    Map your Asset model to the UI shape expected by the modal.
    Adapt as needed if your `Asset` doesn't have these attributes.
    """
    # If you already have `asset.to_dict()` with these keys, you can just return that.
    # Here’s a defensive mapper:
    d = getattr(a, "to_dict", lambda: {})() or {}
    return {
        "id": d.get("id", a.id),
        "symbol": d.get("symbol", getattr(a, "symbol", "")),
        "name": d.get("name", getattr(a, "name", "")),
        "type": d.get("type", getattr(a, "type", "Asset")),         # e.g. 'Stock' | 'ETF' | 'Crypto'
        "currency": d.get("currency", getattr(a, "currency", "USD")),
        "price": d.get("latest_price", getattr(a, "latest_price", 0.0)),
        "change24h": d.get("change_24h", getattr(a, "change_24h", 0.0)) or 0.0,
        "logoUrl": d.get("logo_url", getattr(a, "logo_url", None)),
        "sparkline": d.get("sparkline", getattr(a, "sparkline", [])),
    }


def get_active_challenge(db: Session, oldest=True) -> WeeklyChallenge:
    """
    Returns the current active challenge (this week).
    Strategy:
      - Prefer a row with is_active=True AND (start_at <= now <= end_at)
      - Fallback: latest row where (start_at <= now <= end_at)
    """
    now = now_utc()

    # Prefer explicitly active
   
    if (oldest):
        challenge = (
        db.query(WeeklyChallenge)
        .filter(WeeklyChallenge.is_active.is_(True))
        .order_by(WeeklyChallenge.start_at.asc())
        .first())   

    else:
        q = (
        db.query(WeeklyChallenge)
        .filter(
            WeeklyChallenge.is_active.is_(True),
            # WeeklyChallenge.start_at <= now,
            # WeeklyChallenge.end_at >= now,
        )
        .order_by(WeeklyChallenge.start_at.desc())
        )
        challenge = q.first()
    
    if challenge:
        return challenge

    # Fallback: any challenge covering now
    q2 = (
        db.query(WeeklyChallenge)
        .filter(
            WeeklyChallenge.start_at <= now,
            WeeklyChallenge.end_at >= now,
        )
        .order_by(WeeklyChallenge.start_at.desc())
    )
    challenge = q2.first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Aucun challenge actif pour cette semaine.")
    return challenge


@router.get("/challenges/weekly/pair")
def get_weekly_pair(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    print("avant")
    challenge = get_active_challenge(db)
    print("apres")
    if not challenge:
        raise HTTPException(status_code=404, detail="No active challenge")

    sides = db.query(WeeklyChallengeSide).filter(
        WeeklyChallengeSide.challenge_id == challenge.id
    ).all()
    print(len(sides))
    if len(sides) != 2:
        raise HTTPException(status_code=500, detail="Challenge is not properly configured")

    side_a, side_b = sides

    asset_a = db.query(Asset).filter(Asset.id == side_a.asset_id).first()
    asset_b = db.query(Asset).filter(Asset.id == side_b.asset_id).first()

    # Check if user has already picked
    pick = (
        db.query(WeeklyChallengePick, WeeklyChallengeSide, Asset)
        .join(WeeklyChallengeSide, WeeklyChallengePick.side_id == WeeklyChallengeSide.id)
        .join(Asset, WeeklyChallengeSide.asset_id == Asset.id)
        .filter(
            WeeklyChallengePick.challenge_id == challenge.id,
            WeeklyChallengePick.user_id == current_user.id,
        )
        .first()
    )

    already_picked = pick is not None
    my_pick_data = None
    if already_picked:
        pick_row, side_row, asset_row = pick
        my_pick_data = {
            "sideId": pick_row.side_id,
            "asset": {
                "id": asset_row.id,
                "symbol": asset_row.symbol,
                "name": asset_row.name,
                "type": asset_row.type,
            },
        }
    print("man")
    print(challenge.selection_end_at.isoformat(),)
    return {
        "pair": [
            asset_a.to_dict(),
            asset_b.to_dict()
        ],
        "endAt": challenge.end_at.isoformat(),
        "selectionEndAt": challenge.selection_end_at.isoformat(),
        "description": challenge.description,
        "alreadyPicked": already_picked,
        "myPick": my_pick_data
    }

@router.post("/challenges/weekly/pick", status_code=status.HTTP_200_OK)
def submit_weekly_pick(
    body: SubmitBody,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    challenge = get_active_challenge(db)
    sides = (
        db.query(WeeklyChallengeSide)
        .filter(WeeklyChallengeSide.challenge_id == challenge.id)
        .all()
    )
    # deadline
    if now_utc() > challenge.end_at or now_utc() <challenge.start_at:
        raise HTTPException(status_code=400, detail="Le challenge est clôturé.")

    # load both sides for this challenge
    sides = (
        db.query(WeeklyChallengeSide)
        .filter(WeeklyChallengeSide.challenge_id == challenge.id)
        .all()
    )
    
    if len(sides) != 2:
        raise HTTPException(status_code=500, detail="Challenge mal configuré.")


    # asset_to_side = {s.asset_id: s.id for s in sides if s.asset_id is not None}
    
    
    picked_side_id = body.sideId
    # enforce one pick per user/challenge
    existing = (
        db.query(WeeklyChallengePick)
        .filter(
            WeeklyChallengePick.challenge_id == challenge.id,
            WeeklyChallengePick.user_id == current_user.id,
        )
        .first())
    if existing:
        raise HTTPException(status_code=409, detail="Vous avez déjà participé à ce challenge.")

    # persist pick
    pick = WeeklyChallengePick(
        challenge_id=challenge.id,
        user_id=current_user.id,
        # 👉 choose ONE of the two lines below depending on your model:
        side_id=sides[picked_side_id-1].id,      # new schema (recommended)
        # picked_asset_id=body.assetId,    # old schema (if your table still uses this column)
    )
    db.add(pick)
    db.commit()

    return {"ok": True, "challengeId": challenge.id, "sideId": picked_side_id}



@router.get("/challenges/history")
def get_picks_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    # Fetch picks for this user, only for finished challenges (winner decided),
    # and eager-load: pick.challenge.sides.asset + pick.side.asset
    picks = (
        db.query(WeeklyChallengePick)
        .join(WeeklyChallenge, WeeklyChallenge.id == WeeklyChallengePick.challenge_id)
        .options(
            joinedload(WeeklyChallengePick.challenge)
                .joinedload(WeeklyChallenge.sides)
                .joinedload(WeeklyChallengeSide.asset),
            joinedload(WeeklyChallengePick.side)
                .joinedload(WeeklyChallengeSide.asset),
        )
        .filter(
            WeeklyChallengePick.user_id == current_user.id,
            WeeklyChallenge.winning_side_id.isnot(None),
        )
        .order_by(WeeklyChallengePick.created_at.desc())
        .all()
    )

    if not picks:
        return []

    history = []
    for pick in picks:
        challenge = pick.challenge
        # Find the opponent side among the two sides of this challenge
        # (challenge.sides is eager-loaded and should contain exactly 2)
        opponent_side = next((s for s in challenge.sides if s.id != pick.side_id), None)
        picked_asset = db.query(Asset).filter(Asset.id == pick.side.asset_id).first() if pick.side else None
        opponent_asset = db.query(Asset).filter(Asset.id == opponent_side.asset_id).first()  if opponent_side else None
        history.append({
            "date": pick.created_at.isoformat(),
            "challenge_id": challenge.id,
            "picked": picked_asset.to_dict(),
            "opponent": opponent_asset.to_dict(),
            "result": pick.result,
        })

    return history