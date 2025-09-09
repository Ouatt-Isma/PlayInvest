from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.models.user import User
from app.db.models.portfolio import Portfolio
from app.core.database import get_db
from app.core.config import settings
from app.utils.currency import convert 
from app.db.models.portfolio import Portfolio
from fastapi import BackgroundTasks
from app.utils.email import send_godfather_email

router = APIRouter()

@router.get("/confirm")
def confirm_email(token: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.confirmation_token == token).first()
    if not user:
        raise HTTPException(status_code=404, detail="Token invalide")

    user.validated = True
    portfolio = Portfolio(user_id=user.id, cash=0.0, currency=user.currency)
    portfolio.cash += convert(settings.currency, portfolio.currency, settings.amount_begin)
    db.add(portfolio)
    parrain_uid = None 
    if(user.referrer_id):
        parrain_uid = user.referrer_id
        print()
        print(user.referrer_id)
        print()
        parrain = db.query(User).filter(User.uid == user.referrer_id).first()
        if not parrain:
            raise HTTPException(status_code=400, detail="Nom d'utilisateur du parrain inexistant")
        parrain_uid = parrain.uid
        
    if(parrain_uid):
        portfolio_parrain = db.query(Portfolio).filter_by(user_id=parrain.id).first()
        if not portfolio_parrain:
            raise NotImplementedError
        print()
        print(portfolio_parrain.cash)
        print(portfolio_parrain.currency)
        print(settings.currency)
        portfolio_parrain.cash += convert(settings.currency, portfolio_parrain.currency, settings.amount_godfather)
        print(portfolio_parrain.cash)
        print()
        db.add(portfolio_parrain)
        background_tasks.add_task(send_godfather_email, parrain.email, parrain.username, user.username, convert(settings.currency, portfolio.currency, settings.amount_godfather), portfolio_parrain.currency)
        
        
    db.commit()
    db.refresh(portfolio)
    if (parrain_uid):
        db.refresh(portfolio_parrain)

    return {"message": "Email confirmé avec succès"}
