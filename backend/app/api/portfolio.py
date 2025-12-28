# routes.py
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from app.core.database import get_db
from app.db.models.user import User
from app.db.models.portfolio import Portfolio
from app.db.models.asset import Asset
from app.db.models.portfolio_assets import PortfolioAsset
from app.auth.auth import get_current_user
from app.utils.currency import convert 
from app.core.config import settings

router = APIRouter()

@router.get("/portfolio")
def get_portfolio( db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    portfolio = db.query(Portfolio).filter_by(user_id=user_id).first()
  
    settings.log.info(f"hhhhhhhhhhhhhhhhhhhhhhhhhhhhh {portfolio.cash}{portfolio.performance_pct}")
    
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    assets = (
    db.query(PortfolioAsset, Asset)
    .select_from(PortfolioAsset)  # make PA the lead entity (optional but clear)
    .outerjoin(Asset, PortfolioAsset.asset_id == Asset.id)
    .filter(
        PortfolioAsset.portfolio_id == portfolio.id,
        PortfolioAsset.sold.is_(False),   # safer than == False
    )
    .all()
    )
    result = []
    tt = 0 
    for pa, asset in assets:
        asset_dict = asset.to_dict() 
        pa_dict = pa.to_dict()
        tt+= convert(asset.currency, portfolio.currency, pa_dict["total_invest"]) 
        asset_dict.update(pa_dict) 
        result.append(asset_dict) 
    settings.log.info(f' cash: {round(portfolio.cash,2)}')
    settings.log.info(f'total_investi: {round(tt,2)},')
    settings.log.info(f' user_id: {user_id},')

    merged = {
    "assets": result, "total_investi":round(tt,2), "last_update": portfolio.updated_at}
    merged.update(portfolio.to_dict())
    return merged 



@router.get("/portfolio/last_update")
def get_portfolio_last( db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    portfolio = db.query(Portfolio).filter_by(user_id=user_id).first()
    return {"last_update": portfolio.updated_at}