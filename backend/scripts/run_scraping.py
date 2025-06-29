import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.services.update_assets import update_all_assets, update_all_assets_first

def main():
    db: Session = SessionLocal()
    # update_all_assets(db)
    update_all_assets_first(db)
    db.close()

if __name__ == '__main__':
    main()
