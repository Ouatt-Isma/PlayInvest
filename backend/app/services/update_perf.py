from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.models.portfolio_assets import PortfolioAsset
from app.db.models.performance import Performance
from app.db.models.asset import Asset
from app.db.models.portfolio import Portfolio
from datetime import datetime
from app.utils.currency import convert


# Function to update portfolio and asset performance
def update_portfolio_and_asset_performance(db: Session, portfolio_id: int, current_date: datetime):
    # Get portfolio in the session
    portfolio = db.query(Portfolio).filter_by(id=portfolio_id).first()
    if not portfolio:
        return
    
    # Query only PortfolioAsset objects with Asset joined
    assets = (
        db.query(PortfolioAsset)
        .join(Asset, PortfolioAsset.asset_id == Asset.id)
        .filter(PortfolioAsset.portfolio_id == portfolio_id)
        .all()
    )

    performance_data = {k: 0 for k in ['etf','crypto','stock','africa','usa','europe','world']}
    investment_data = {k: 0 for k in performance_data.keys()}
    total_investment = 0

    for pa in assets:
        asset = db.query(Asset).filter_by(id=pa.asset_id).first()   # requires relationship on PortfolioAsset
        if (not pa.sold):
            buying_price = pa.buying_price
            total_price = asset.to_dict()["latest_price"]
            current_price = convert(asset.currency, portfolio.currency, total_price)

            performance_pct = ((current_price - buying_price) / buying_price * 100) if buying_price else 0
            pa.performance_pct = performance_pct
            pa.total_invest = pa.quantity * buying_price
            
        total_investment += pa.total_invest
        weighted_perf = pa.performance_pct * pa.buying_price * pa.quantity 
        if asset.isETF():
            performance_data['etf'] += weighted_perf
            investment_data['etf'] += pa.total_invest
        elif asset.isCrypto():
            performance_data['crypto'] += weighted_perf
            investment_data['crypto'] += pa.total_invest
        elif asset.isStock():
            performance_data['stock'] += weighted_perf
            investment_data['stock'] += pa.total_invest

        if asset.isAfrica():
            performance_data['africa'] += weighted_perf
            investment_data['africa'] += pa.total_invest
        elif asset.isUSA():
            performance_data['usa'] += weighted_perf
            investment_data['usa'] += pa.total_invest
        elif asset.isEurope():
            performance_data['europe'] += weighted_perf
            investment_data['europe'] += pa.total_invest
        elif asset.isWorld():
            performance_data['world'] += weighted_perf
            investment_data['world'] += pa.total_invest

    # Update portfolio total performance
    portfolio.performance_pct = sum(performance_data.values()) / total_investment if total_investment else 0

    # Previous performance for carry-over
    prev_perf = (
        db.query(Performance)
        .filter(Performance.portfolio_id == portfolio_id)
        .order_by(Performance.date.desc())
        .first()
    )

    perf_record = Performance(
        portfolio_id=portfolio_id,
        date=current_date,
        category_etf=performance_data['etf'] / investment_data['etf'] if investment_data['etf'] else (prev_perf.category_etf if prev_perf else 0),
        category_crypto=performance_data['crypto'] / investment_data['crypto'] if investment_data['crypto'] else (prev_perf.category_crypto if prev_perf else 0),
        category_stock=performance_data['stock'] / investment_data['stock'] if investment_data['stock'] else (prev_perf.category_stock if prev_perf else 0),
        region_africa=performance_data['africa'] / investment_data['africa'] if investment_data['africa'] else (prev_perf.region_africa if prev_perf else 0),
        region_usa=performance_data['usa'] / investment_data['usa'] if investment_data['usa'] else (prev_perf.region_usa if prev_perf else 0),
        region_europe=performance_data['europe'] / investment_data['europe'] if investment_data['europe'] else (prev_perf.region_europe if prev_perf else 0),
        region_world=performance_data['world'] / investment_data['world'] if investment_data['world'] else (prev_perf.region_world if prev_perf else 0)
    )

    db.add(perf_record)
    db.add(portfolio)  # ensure portfolio is tracked for update
    for pa in assets:
        db.add(pa)  # ensure all portfolio_assets are tracked for update

    db.commit()


# Function to update all portfolios, then assign rankings
def update_all_portfolio_performance(db: Session, current_date: datetime):
    portfolios = db.query(Portfolio).all()
    for portfolio in portfolios:
        update_portfolio_and_asset_performance(db, portfolio.id, current_date)

    ranked = db.query(Portfolio).order_by(desc(Portfolio.performance_pct)).all()
    current_rank = 1
    last_score = None
    for idx, p in enumerate(ranked, start=1):
        if last_score is None or p.performance_pct != last_score:
            current_rank = idx
        p.rank = current_rank
        last_score = p.performance_pct
        db.add(p)
    db.commit()
