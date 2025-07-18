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

router = APIRouter()

@router.get("/portfolio")
def get_portfolio( db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    user_id = current_user.id
    portfolio = db.query(Portfolio).filter_by(user_id=user_id).first()
  
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    assets = (
        db.query(PortfolioAsset, Asset)
        .join(Asset, PortfolioAsset.asset_id == Asset.id)
        .filter(PortfolioAsset.portfolio_id == portfolio.id and PortfolioAsset.sold==False)
        .all()
    )

    result = []
    tt = 0 
    for pa, asset in assets:
        asset_dict = asset.to_dict() 
        pa_dict = pa.to_dict()
        print(pa_dict)
        tt+= pa_dict["total_invest"]
        asset_dict.update(pa_dict) 
        # result.append()
        result.append(asset_dict )
        
    print({
    "assets": result,
    "cash": round(portfolio.cash,2),
    "total_investi": round(tt,2)
})
    return {
    "assets": result,
    "cash": round(portfolio.cash,2),
    "total_investi": round(tt,2)
}
