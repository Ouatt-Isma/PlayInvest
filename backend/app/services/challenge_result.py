from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.models.portfolio_assets import PortfolioAsset
from app.db.models.performance import Performance
from app.db.models.asset import Asset
from app.db.models.portfolio import Portfolio
from datetime import datetime
from app.utils.currency import convert
from typing import Dict, Optional, List, Tuple, Set
from datetime import datetime, timedelta, timezone, time
import random

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.db.models.asset import Asset
from app.db.models.weekly_challenge import (
    WeeklyChallenge,
    WeeklyChallengeSide,
    WeeklyChallengePick,
    EntityKind,
)

def compute_last_5days_perf(asset: Asset, current_date, check=True):
    date_4_days_ago = current_date - timedelta(days=6)
    if(check):
        assert date_4_days_ago.weekday() == 0, f"Expected Monday, got {date_4_days_ago.strftime('%A')}"
    date_4_days_ago = date_4_days_ago.strftime("%Y-%m-%d")
    
    open = asset.get_price_at(date_4_days_ago, open=True)
    close = asset.get_price_at(current_date.strftime("%Y-%m-%d"))
    return (close - open)/open

    
# Function to update one challenge   
def update_challenge_result(db: Session, weekly_challenge_id: int, current_date: datetime, check=True):
    weekly_challenge = db.query(WeeklyChallenge).filter_by(id=weekly_challenge_id).first()
    if not weekly_challenge:
        return
    sides = db.query(WeeklyChallengeSide).filter(
        WeeklyChallengeSide.challenge_id == weekly_challenge_id
    ).all()
    if len(sides) != 2:
        raise NameError("Challenge is not properly configured")
    side_a, side_b = sides
    asset_a = db.query(Asset).filter(Asset.id == side_a.asset_id).first()
    asset_b = db.query(Asset).filter(Asset.id == side_b.asset_id).first()
    perf_a = compute_last_5days_perf(asset_a, current_date, check)
    perf_b = compute_last_5days_perf(asset_b, current_date, check)
    weekly_challenge.winning_side = side_a if perf_a >= perf_b else side_b
    db.add(weekly_challenge)  
    db.commit()
    
    
# Function to update one pick
def update_user_result_one(db: Session, weekly_pick: int, current_date: datetime):
    # Get portfolio in the session
    if not weekly_pick:
        return
    weekly_challenge = db.query(WeeklyChallenge).filter_by(id=weekly_pick.challenge_id).first()
    if(weekly_pick.side== weekly_challenge.winning_side):
        weekly_pick.result = True
    else:
        weekly_pick.result = False
    db.add(weekly_pick)  
    db.commit()
    

# Function to update challenge and all picks
def update_all_challenge_result(db: Session, current_date: datetime, check=True):
    weekly_challenge = db.query(WeeklyChallenge).filter_by(is_active=True).first()
    if(not weekly_challenge):
        return
    update_challenge_result(db, weekly_challenge.id, current_date, check)
    weekly_challenge.is_active = False 
    all_picks = db.query(WeeklyChallengePick).filter_by(challenge_id=weekly_challenge.id).all()
    for pick in all_picks:
        update_user_result_one(db, pick,current_date)
    