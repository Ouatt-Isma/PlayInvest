from sqlalchemy.orm import Session
from sqlalchemy import extract
from app.db.models.transactions import Transaction
from app.db.models.portfolio import Portfolio
from app.db.models.user import User
from app.core.config import settings
from app.utils.email import send_inactivity_warning_email
import asyncio

def user_has_transaction_in_month(db: Session, user: User, month: int, year: int) -> bool:
    """
    Check if a user has any transactions in a given month/year.

    Args:
        db (Session): SQLAlchemy session
        user (User): The user object
        month (int): Month (1-12)
        year (int): Year (e.g., 2025)

    Returns:
        bool: True if at least one transaction exists, False otherwise.
    """

    # Join transactions -> portfolios -> user
    count = (
        db.query(Transaction)
        .join(Portfolio, Transaction.portfolio_id == Portfolio.id)
        .filter(
            Portfolio.user_id == user.id,
            extract("month", Transaction.transaction_date) == month,
            extract("year", Transaction.transaction_date) == year,
        )
        .count()
    )

    return count > 0


def penalize_inactive_users(db: Session, month: int, year: int):
    """
    Reduce cash by x% for users who had no transactions in the given month/year.
    Args:
        db (Session): SQLAlchemy session
        month (int): Month (1-12)
        year (int): Year (e.g. 2025)
    Returns:
        dict: Summary of how many users were penalized.
    """

    penalized_users = []

    # Fetch all users
    users = db.query(User).all()

    for user in users:
        # if(user.email!= "ouattaraismael258852@gmail.com"):
        #     continue 
        # ✅ Check if the user has a portfolio
        portfolio = db.query(Portfolio).filter(Portfolio.user_id == user.id).first()
        if not portfolio:
            continue

        # ✅ Check if the user made any transaction that month
        has_tx = (
            db.query(Transaction)
            .join(Portfolio, Transaction.portfolio_id == Portfolio.id)
            .filter(
                Portfolio.user_id == user.id,
                extract("month", Transaction.transaction_date) == month,
                extract("year", Transaction.transaction_date) == year,
            )
            .count()
            > 0
        )

        # ✅ If no transaction: reduce cash by 2%
        if not has_tx and portfolio.cash > 0:
            original_cash = portfolio.cash
            portfolio.cash *= (1-settings.INFLATION)  # reduce by 2%
            penalized_users.append({
                "user_id": user.id,
                "old_cash": round(original_cash, 2),
                "new_cash": round(portfolio.cash, 2)
            })

    db.commit()

    return {
        "message": f"{len(penalized_users)} users penalized for inactivity in {month}/{year}.",
        "details": penalized_users
    }


def notify_users(db: Session, month: int, year: int):
    """
    Reduce cash by x% for users who had no transactions in the given month/year.
    Args:
        db (Session): SQLAlchemy session
        month (int): Month (1-12)
        year (int): Year (e.g. 2025)
    Returns:
        dict: Summary of how many users were penalized.
    """

    penalized_users = []

    # Fetch all users
    users = db.query(User).all()

    for user in users:
        # ✅ Check if the user has a portfolio
        portfolio = db.query(Portfolio).filter(Portfolio.user_id == user.id).first()
        if not portfolio:
            continue

        # ✅ Check if the user made any transaction that month
        has_tx = (
            db.query(Transaction)
            .join(Portfolio, Transaction.portfolio_id == Portfolio.id)
            .filter(
                Portfolio.user_id == user.id,
                extract("month", Transaction.transaction_date) == month,
                extract("year", Transaction.transaction_date) == year,
            )
            .count()
            > 0
        )

        # ✅ If no transaction: reduce cash by 2%
        if not has_tx and portfolio.cash > 0:
            asyncio.run(send_inactivity_warning_email(user.email, user.username))
            penalized_users.append({
                "user_id": user.username,
            })


    return {
        "message": f"{len(penalized_users)} users penalized for inactivity in {month}/{year}.",
        "details": penalized_users
    }


