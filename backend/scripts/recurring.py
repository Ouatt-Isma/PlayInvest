import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
import signal
from contextlib import contextmanager
from datetime import datetime
from app.core.config import settings 
TZ_GMT = settings.TZ_GMT

import asyncio
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.update_assets import update_all_assets, update_all_assets_first, update_assets_from_csv
from app.services.update_perf import update_all_portfolio_performance
from app.services.update_news import add_news
from app.services.challenges_scheduler import seed_next_week
from app.services.challenge_result import update_all_challenge_result
from app.utils.email import send_admin_issue
from app.services.weekly_notifs import send_weekly_notif_all_users

from apscheduler.schedulers.blocking import BlockingScheduler
# ✅ Import and call the penalty function
from app.services.inflation_simulator import penalize_inactive_users, notify_users
            
# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)
log = logging.getLogger("scheduler")

# --- DB session helper ---
@contextmanager
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Jobs ---
def challenge(check=True):
    try:
        with get_db() as db:
            current_date = datetime.now(TZ_GMT)
            update_all_challenge_result(db, current_date, check)
            seed_next_week(db, check)
        log.info("challenge() completed")
    except Exception as e:
        log.exception("challenge() failed")
        asyncio.run(send_admin_issue("CHALLENGE UPDATE"))

def challenge_res(check=True):
    try:
        with get_db() as db:
            current_date = datetime.now(TZ_GMT)
            update_all_challenge_result(db, current_date, check)
        log.info("challenge_res() completed")
    except Exception as e:
        log.exception("challenge_res() failed")
        asyncio.run(send_admin_issue("CHALLENGE RESULT UPDATE"))
        
def challenge_seed(check=False):
    try:
        with get_db() as db:
            current_date = datetime.now(TZ_GMT)
            seed_next_week(db, check)
        log.info("challenge_seed() completed")
    except Exception as e:
        log.exception("challenge_seed() failed")
        asyncio.run(send_admin_issue("CHALLENGE SEED UPDATE"))
        
def assets():
    try:
        with get_db() as db:
            # update_all_assets_first(db)
            # update_assets_from_csv(db)
            update_all_assets(db)
        log.info("assets() completed")
    except Exception as e:
        log.exception("assets() failed")
        asyncio.run(send_admin_issue("ASSETS UPDATE"))

def assets_first():
    try:
        with get_db() as db:
            update_all_assets_first(db)
            update_assets_from_csv(db)
            # update_all_assets(db)
        log.info("assets First() completed")
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
            current_date = datetime.now(TZ_GMT)
            update_all_portfolio_performance(db, current_date)
        log.info("perf() completed")
    except Exception as e:
        log.exception("perf() failed")
        asyncio.run(send_admin_issue("PERFS UPDATE"))

def notif():
    try:
        with get_db() as db:
            send_weekly_notif_all_users(db)
        log.info("notif() completed")
    except Exception as e:
        log.exception("notif() failed")
        asyncio.run(send_admin_issue("notif send"))
        
def inflation():
    """
    Penalize users with no transactions in the previous month (-2% cash).
    """
    try:
        with get_db() as db:
            current_date = datetime.now(TZ_GMT)

            # ✅ Compute previous month/year
            if current_date.month == 1:
                month = 12
                year = current_date.year - 1
            else:
                month = current_date.month - 1
                year = current_date.year
            log.info(
                f"inflation() running on {month}/{year}"
            )
            result = penalize_inactive_users(db, month, year)

            log.info(
                f"inflation() completed: {result['message']}"
            )

    except Exception as e:
        log.exception("inflation() failed")
        asyncio.run(send_admin_issue("INFLATION PENALTY UPDATE"))

    
def inflation_notify():
    """
    Penalize users with no transactions in the previous month (-2% cash).
    """
    try:
        with get_db() as db:
            current_date = datetime.now(TZ_GMT)

            # ✅ Compute previous month/year
            if current_date.month == 1:
                month = 12
                year = current_date.year - 1
            else:
                month = current_date.month - 1
                year = current_date.year
            log.info(
                f"inflation_notify() running on {month}/{year}"
            )
            result = notify_users(db, month, year)

            log.info(
                f"inflation_notify() completed: {result['message']}"
            )

    except Exception as e:
        log.exception("inflation_notify() failed")
        asyncio.run(send_admin_issue("INFLATION NOTIFICATION ISSUE"))



# --- Scheduler setup ---
def main():
    tz = TZ_GMT
    job_defaults = {
        "coalesce": True,          # collapse backlog into one run
        "max_instances": 1,        # avoid overlapping runs
        "misfire_grace_time": 300  # 5 minutes grace
    }
    scheduler = BlockingScheduler(timezone=tz, job_defaults=job_defaults)

    scheduler.add_job(news,     trigger='cron', hour=8,  id="news_daily",     replace_existing=True)
    scheduler.add_job(assets,   trigger='cron', hour=23, id="assets_daily",   replace_existing=True)
    scheduler.add_job(perf,     trigger='cron', hour=12, id="perf_daily",     replace_existing=True)
 
    scheduler.add_job(challenge_seed, trigger='cron', day_of_week='sat', hour=11, id="challenge_saturday_10_seed", replace_existing=True)
    scheduler.add_job(challenge_res, trigger='cron', day_of_week='fri', hour=23, minute=59, id="challenge_fri_23_res", replace_existing=True)
    scheduler.add_job(notif, trigger='cron', day_of_week='sat', hour=10, minute=00, id="notif_sat_10", replace_existing=True)
    scheduler.add_job(
    inflation,
    trigger='cron',
    day=2,          # Run every 2nd day of the month
    hour=8,         # Choose a safe hour, e.g. 8:00 AM
    minute=0, id="inflation_monthly_2", replace_existing=True)
    
    scheduler.add_job(
    inflation_notify,
    trigger='cron',
    day=27,          # Run every 27th day of the month
    hour=9,         # Choose a safe hour, e.g. 9:00 AM
    minute=0, id="inflation_notify_monthly_27", replace_existing=True)
    
    
    # Graceful shutdown
    def _shutdown(signum, frame):
        log.info("Received signal %s, shutting down scheduler...", signum)
        scheduler.shutdown(wait=True)

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    log.info("Starting scheduler (GMT")
    scheduler.start()

if __name__ == '__main__':
    main()