from sqlalchemy.orm import Session
from app.db.models.user import User
from app.utils.email import send_email
from app.utils.template_loader import render_html_template
from app.utils.template_loader import render_html_template
import asyncio
from sqlalchemy.orm import joinedload
from sqlalchemy import func, desc
from datetime import date, timedelta
from app.db.models.weekly_challenge import WeeklyChallenge
from app.db.models.weekly_challenge import WeeklyChallengeSide
from app.db.models.portfolio import Portfolio
from app.db.models.asset import Asset
from app.db.models.portfolio_assets import PortfolioAsset
from app.db.models.performance import Performance
from app.utils.currency import convert 
from app.api.challenge import get_active_challenge

# def get_data(db, user):
#     portfolio = (
#         db.query(Portfolio)
#         .filter(Portfolio.user_id == user.id)
#         .first()
#     )
#     if not portfolio:
#         return None  # user has no portfolio

#     portfolio_value = 0 
#     assets = (
#     db.query(PortfolioAsset, Asset)
#     .select_from(PortfolioAsset)  # make PA the lead entity (optional but clear)
#     .outerjoin(Asset, PortfolioAsset.asset_id == Asset.id)
#     .filter(
#         PortfolioAsset.portfolio_id == portfolio.id,
#         PortfolioAsset.sold.is_(False),   # safer than == False
#     )
#     .all()
#     )
#     for pa, asset in assets:
#         pa_dict = pa.to_dict()
#         portfolio_value+= convert(asset.currency, portfolio.currency, pa_dict["total_invest"]) 
#         # --- Étape 3 : construire le dictionnaire data ---
#     data = {
#         "portfolio_value": round(portfolio_value, 2),
#         "portfolio_currency": portfolio.currency,
#         "cash": portfolio.cash,
#         "weekly_perf": weekly_perf,
#         "ytd_perf": ytd_perf,
#         "rank": portfolio.rank,
#     }
#     return data 

def get_data(db, user):
    # --- Get portfolio ---
    portfolio = (
        db.query(Portfolio)
        .filter(Portfolio.user_id == user.id)
        .first()
    )
    if not portfolio:
        return None  # user has no portfolio

    # --- Compute portfolio value ---
    portfolio_value = 0
    assets = (
        db.query(PortfolioAsset, Asset)
        .select_from(PortfolioAsset)
        .outerjoin(Asset, PortfolioAsset.asset_id == Asset.id)
        .filter(
            PortfolioAsset.portfolio_id == portfolio.id,
            PortfolioAsset.sold.is_(False),
        )
        .all()
    )

    for pa, asset in assets:
        pa_dict = pa.to_dict()
        portfolio_value += convert(asset.currency, portfolio.currency, pa_dict["total_invest"])

    # --- Compute Weekly & YTD performance ---
    today = date.today()
    week_ago = today - timedelta(days=7)
    start_of_year = date(today.year, 1, 1)

    # Get latest performance record (today or most recent)
    latest_perf = (
        db.query(Performance)
        .filter(Performance.portfolio_id == portfolio.id)
        .order_by(desc(Performance.date))
        .first()
    ).global_perf

    # Weekly performance (compare to value 7 days ago)
    week_ago_perf = (
        db.query(Performance.global_perf)
        .filter(
            Performance.portfolio_id == portfolio.id,
            Performance.date <= week_ago,
        )
        .order_by(Performance.date.desc())
        .limit(1)
        .scalar()
    ) or 0.0

    # YTD start
    ytd_perf_start = (
        db.query(Performance.global_perf)
        .filter(
            Performance.portfolio_id == portfolio.id,
            Performance.date <= start_of_year,
        )
        .order_by(Performance.date.desc())
        .limit(1)
        .scalar()
    ) or 0.0

    def calc_delta(curr, prev):
        if curr and prev:
            return curr - prev
        elif curr:
            return curr
        return 0.0

    weekly_perf_value = calc_delta(latest_perf, week_ago_perf)
    ytd_perf_value = calc_delta(latest_perf, ytd_perf_start)

    weekly_perf = f"{weekly_perf_value:+.2f} %"
    ytd_perf = f"{ytd_perf_value:+.2f} %"

    # --- Build the data dictionary ---
    data = {
        "portfolio_value": round(portfolio_value, 2),
        "currency": portfolio.currency,
        "cash": round(portfolio.cash,2) or 0.0,
        "weekly_perf": weekly_perf,
        "ytd_perf": ytd_perf,
        "rank": portfolio.rank,
    }

    return data

def send_weekly_notif_all_users(db: Session):
    """
    Sends the weekly recap email to all active users.
    """
    users = db.query(User).all()
    sent_count = 0
        # --- Étape 1 : récupérer le challenge actif et ses deux actifs (A et B) ---
    active_challenge = get_active_challenge(db)
    
    Actif1_name = Actif2_name = description = None

    if active_challenge:
        description = active_challenge.description
        # on récupère les sides A et B (les actifs associés)
        sides = {s.side: s for s in active_challenge.sides if s.entity_kind == "ASSET"}
        if "A" in sides and sides["A"].asset:
            Actif1_name = sides["A"].asset.name
        if "B" in sides and sides["B"].asset:
            Actif2_name = sides["B"].asset.name
            
        # --- Étape 2 : données de performance et de portefeuille ---
    assets = db.query(Asset).all()
    # --- Calcul de la performance hebdomadaire de chaque actif ---
    for a in assets:
        dc = a.to_dict()
        a.weekly_perf_pct = dc["variation_7d"]

    # --- Classement des top actifs ---
    top_assets = sorted(
        [a for a in assets if a.weekly_perf_pct is not None],
        key=lambda a: a.weekly_perf_pct,
        reverse=True
    )[:3]
    
    data_all = {   
        "top1_name": top_assets[0].name if len(top_assets) > 0 else None,
        "top1_perf": f"{top_assets[0].weekly_perf_pct:+.1f} %" if len(top_assets) > 0 else None,
        "top2_name": top_assets[1].name if len(top_assets) > 1 else None,
        "top2_perf": f"{top_assets[1].weekly_perf_pct:+.1f} %" if len(top_assets) > 1 else None,
        "top3_name": top_assets[2].name if len(top_assets) > 2 else None,
        "top3_perf": f"{top_assets[2].weekly_perf_pct:+.1f} %" if len(top_assets) > 2 else None,
        "Actif1":Actif1_name,
        "Actif2": Actif2_name,
        "Chall_description": description,
        }    
    for user in users:
        # if user.email != "cewiney225@gmail.com" and user.email != "guyangejordan@gmail.com" :
            try:
                subject = "Votre résumé hebdomadaire sur PlayInvest 🚀"
                
                # Example dynamic data
                
                data = get_data(db, user)
                data.update(data_all)
                html_message = render_html_template("weekly_email.html", **data)
                asyncio.run(
                    send_email(
                    to=user.email,
                    subject=subject,
                    content=html_message,  # <-- HTML message
                ))
                print(f"[✔] Email envoyé à {user.email}")
                sent_count += 1

            except Exception as e:
                print(f"[✘] Erreur d'envoi pour {user.email}: {e}")
                db.rollback()

    print(f"✅ {sent_count} emails envoyés au total.")
