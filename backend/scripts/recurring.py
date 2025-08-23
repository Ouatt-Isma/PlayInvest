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

from apscheduler.schedulers.blocking import BlockingScheduler

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
def challenge():
    try:
        with get_db() as db:
            current_date = datetime.now(TZ_GMT)
            update_all_challenge_result(db, current_date)
            seed_next_week(db)
        log.info("challenge() completed")
    except Exception as e:
        log.exception("challenge() failed")
        asyncio.run(send_admin_issue("CHALLENGE UPDATE"))

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
    # scheduler.add_job(challenge, trigger='cron', day_of_week='fri', hour=23,
    #                   id="challenge_fri_23", replace_existing=True)
    scheduler.add_job(
    challenge,
    trigger="cron",
    day_of_week="sat",   # Saturday
    hour=19,             # 21h
    minute=33,           # 21h22
    id="challenge_sat_2122",
    replace_existing=True
)
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