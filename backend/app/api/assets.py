# app/routers/assets.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.models.asset import Asset
from datetime import datetime 
from app.db.models.portfolio import Portfolio
from app.db.models.portfolio_assets import PortfolioAsset
from app.db.models.user import User
from app.db.models.transactions import Transaction
from app.auth.auth import get_current_user

from app.utils.currency import convert 

from app.core.config import settings

router = APIRouter()

@router.get("/assets")
def list_assets(db: Session = Depends(get_db)):
    assets = db.query(Asset).all()
    print(len(assets))
    return [asset.to_dict() for asset in assets]

@router.get("/assets/{asset_id}")
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(404)
    return asset.to_dict()

@router.get("/buy")
def buy_asset(
    asset: int = Query(..., gt=0),
    amount: float = Query(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 0. check quantity 
    if(amount<settings.minimum_asset):
        raise HTTPException(status_code=400, detail=f"Quantité d'achat minimum est {settings.minimum_asset} > {amount}")
    
    
    # 1. Récupération de l'actif
    asset_obj = db.query(Asset).filter(Asset.id == asset).first()
    if not asset_obj:
        raise HTTPException(status_code=404, detail="Asset not found")
    if(asset_obj.isStock() and not amount.is_integer() ):
        raise HTTPException(status_code=400, detail=f"La quantité d'achat doit être entière pour les actions")

        

    
    
    
    # 3. Récupération ou création du portefeuille utilisateur
    portfolio = db.query(Portfolio).filter_by(user_id=current_user.id).first()
    if not portfolio:
        portfolio = Portfolio(user_id=current_user.id, cash=0.0, currency='EUR')
        db.add(portfolio)
        db.commit()
        db.refresh(portfolio)
        
    # 2. Calcul du prix total d’achat
    asset_dict = asset_obj.to_dict()
    total_price = asset_dict["buying_price"] * amount

    total_price_conv = convert(asset_obj.currency, portfolio.currency, total_price) 
    
    
    # 4. Vérification du solde
    
    
    print(portfolio.cash)
    print(total_price_conv)
    
    if portfolio.cash < total_price_conv:
        raise HTTPException(status_code=400, detail=f"Fonds insuffisants. Requis: {round(total_price,2)}{asset_dict['currency']}, disponible: {portfolio.cash}{portfolio.currency}")

    # 5. Déduction du cash
    portfolio.cash -= total_price_conv
    db.add(portfolio)

    # 6. Mise à jour ou ajout de la ligne dans portfolio_assets
    pa = db.query(PortfolioAsset).filter_by(portfolio_id=portfolio.id, asset_id=asset).first()
    
    if pa:
        if pa.sold:
            pa.sold=False
            pa.quantity = amount
            pa.selling_date = None
            pa.selling_price = None 
            pa.total_invest = total_price
        else:
            pa.quantity += amount
            pa.buying_price = (asset_dict["buying_price"]*amount +  pa.buying_price *pa.quantity) / (pa.quantity+amount) # optionnel : mise à jour du prix
            pa.total_invest = pa.total_invest+total_price
        pa.buying_price=asset_dict["buying_price"],
        pa.buying_date=datetime.now(),
    else:
        pa = PortfolioAsset(
            portfolio_id=portfolio.id,
            asset_id=asset,
            quantity=amount,
            buying_price=asset_dict["buying_price"],
            buying_date=datetime.now(),
            total_invest = total_price, 
            sold=False,
            performance_pct=0,
            
        )
        db.add(pa)

    transaction = Transaction(portfolio_id=portfolio.id,
        asset_id=asset,
        transaction_type="buy",
        quantity=amount,
        price_per_unit=asset_dict["buying_price"]
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    db.refresh(pa)
    return {
        "message": "Achat effectué avec succès",
        "asset_id": asset,
        "quantity": amount,
        "total_cost": total_price,
        "remaining_cash": portfolio.cash
    }
    
    
@router.get("/sell")
def sell_asset(
    asset: int = Query(..., gt=0),
    amount: float = Query(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. Récupérer l'actif
    asset_obj = db.query(Asset).filter(Asset.id == asset).first()
    if not asset_obj:
        raise HTTPException(status_code=404, detail="Asset not found")
    if(asset_obj.isStock() and not amount.is_integer() ):
        raise HTTPException(status_code=400, detail=f"La quantité de vente doit être entière pour les actions")
    # 0. check quantity 
    if(amount<settings.minimum_asset):
        raise HTTPException(status_code=400, detail=f"Quantité de vente minimum est {settings.minimum_asset} > {amount}")
    
    asset_dict = asset_obj.to_dict()
    current_price = asset_dict["buying_price"]

    # 2. Récupérer le portefeuille de l'utilisateur
    portfolio = db.query(Portfolio).filter_by(user_id=current_user.id).first()
    if not portfolio:
        raise HTTPException(status_code=400, detail="Aucun portefeuille trouvé")

    # 3. Vérifier que l’actif est bien dans le portefeuille
    pa = db.query(PortfolioAsset).filter_by(portfolio_id=portfolio.id, asset_id=asset, sold=False).first()
    if not pa or pa.quantity < amount:
        raise HTTPException(status_code=400, detail="Quantité à vendre invalide ou actif non détenu")
    if pa.quantity == amount:
        pa.sold = True
        pa.selling_price = current_price
        pa.selling_date = datetime.utcnow()
        
    ## update total_invest
    pa.total_invest-= pa.buying_price*amount
    # 4. Calcul du prix de vente et conversion vers la devise du portefeuille
    total_sale_price = current_price * amount

    total_sale_price = convert(asset_obj.currency, portfolio.currency, total_sale_price)
    
    # 5. Incrémenter le cash du portefeuille
    portfolio.cash += total_sale_price
    db.add(portfolio)

    # 6. Mettre à jour la ligne d’actif
    
    
    pa.quantity -= amount  # ou garder la quantité d’origine si tu veux un historique complet
    transaction = Transaction(portfolio_id=portfolio.id,
        asset_id=asset,
        transaction_type="sell",
        quantity=amount,
        price_per_unit=asset_dict["buying_price"]
    )
    db.add(transaction)
    db.add(pa)
    db.commit()
    db.refresh(transaction)
    db.refresh(pa)
    return {
        "message": "Vente effectuée avec succès",
        "asset_id": asset,
        "quantity": amount,
        "selling_price": current_price,
        "total_gain": total_sale_price,
        "new_cash_balance": portfolio.cash
    }