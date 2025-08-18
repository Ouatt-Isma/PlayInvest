import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
from contextlib import contextmanager
from datetime import datetime
from app.core.config import settings 
TZ_FR = settings.TZ_FR

import asyncio
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.update_assets import update_all_assets
from app.services.update_perf import update_all_portfolio_performance
from app.services.update_news import add_news
from app.services.challenges_scheduler import seed_next_week
from app.services.challenge_result import update_all_challenge_result
from app.utils.email import send_admin_issue

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)
log = logging.getLogger("manual_runner")

# --- DB session helper ---
@contextmanager
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Jobs ---
def challenge():
    try:
        with get_db() as db:
            current_date = datetime.now(TZ_FR)
            update_all_challenge_result(db, current_date)
            seed_next_week(db, False)
        log.info("challenge() completed")
    except Exception as e:
        log.exception("challenge() failed")
        asyncio.run(send_admin_issue("CHALLENGE UPDATE"))

def assets():
    try:
        with get_db() as db:
            update_all_assets(db)
        log.info("assets() completed")
    except Exception as e:
        log.exception("assets() failed")
        asyncio.run(send_admin_issue("ASSETS UPDATE"))

def news():
    try:
        with get_db() as db:
            add_news(db)
        log.info("news() completed")
    except Exception as e:
        log.exception("news() failed")
        asyncio.run(send_admin_issue("NEWS UPDATE"))

def perf():
    try:
        with get_db() as db:
            current_date = datetime.now(TZ_FR)
            update_all_portfolio_performance(db, current_date)
        log.info("perf() completed")
    except Exception as e:
        log.exception("perf() failed")
        asyncio.run(send_admin_issue("PERFS UPDATE"))

# --- Manual runner ---
if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Run maintenance tasks manually")
    parser.add_argument(
        "task",
        choices=["assets", "perf", "challenge", "news"],
        help="Which task to run"
    )
    args = parser.parse_args()

    if args.task == "assets":
        assets()
    elif args.task == "perf":
        perf()
    elif args.task == "challenge":
        challenge()
    elif args.task == "news":
        news()
