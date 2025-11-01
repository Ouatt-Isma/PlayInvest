from app.db.models.asset import Asset
from app.core.database import SessionLocal
from app.scrapper.yahoo import YahooScraper
from app.scrapper.investing import InvestingScraper
from sqlalchemy.orm.attributes import flag_modified
from datetime import datetime
import os 
import pandas as pd 
from app.utils.conv import to_float_inv
    


from sqlalchemy.orm import Session
import tldextract

def get_website_name(url):
    try:
        extracted = tldextract.extract(url)

        if not extracted.domain:
            return url  # Not a valid URL

        return extracted.domain  # 'investing' in your case

    except Exception:
        return url

scraper_map = {
    "yfinance": YahooScraper(),
    "investing": InvestingScraper(),
}

def update_all_assets(db: Session):

    assets = db.query(Asset).all()

    for asset in assets:
        # print("Before:", asset.financial_data)
        
        url = get_website_name(asset.website)
        # print(f"[{asset.symbol}] source = {url}")

        try:
            scraper = scraper_map.get(url)
            if not scraper:
                print(f"No scraper for {url}")
                continue
            
            data = scraper.scrape(asset.symbol, asset.website)

            if not data or 'error' in data:
                print(f"Skipping {asset.symbol} due to bad data: {data}")
                continue

            # ✅ Safely handle append
            print("data: ", data)
            existing = asset.financial_data if isinstance(asset.financial_data, list) else []
            existing_dates = {d.get("date") for d in existing}
            if data.get("date") not in existing_dates:
                existing.append(data)
                asset.financial_data = list(existing)  # 🔥 this is critical!
                flag_modified(asset, "financial_data") 
                # flag_modified(asset, "updated_at")
                db.commit()
                print(f"[✔] Updated {asset.symbol} with new data for {data['date']}")
            else:
                print(f"[⏭] Skipped {asset.symbol} – entry for {data['date']} already exists.")
        except Exception as e:
            print(f"[✘] Error on {asset.symbol}: {e}")
            db.rollback()
            # raise NotADirectoryError
        # print("After:", asset.financial_data)
    db.close()



def update_all_assets_first(db: Session):
    import yfinance as yf
    assets = db.query(Asset).all()

    for asset in assets:
        url = get_website_name(asset.website)
        print(f"[{asset.symbol}] source = {url}")

        try:
            # Only support Yahoo Finance for now
            if url != "yfinance":
                print(f"[⏭] No scraper implemented for: {url}")
                continue

            # Get historical weekly data from Yahoo
            yf_data = yf.download(
                asset.symbol,  # Yahoo Finance ticker (make sure it's correct!)
                start="2000-01-01",
                interval="1d"
            )

            if yf_data.empty:
                print(f"[⏭] No data for {asset.symbol}")
                continue

            # Prepare existing dates for deduplication
            existing = asset.financial_data if isinstance(asset.financial_data, list) else []
            existing_dates = {d.get("date") for d in existing}

            added = 0
            for index, row in yf_data.iterrows():
                entry_date = str(index.date())
                if entry_date in existing_dates:
                    continue

                new_data = {
                    "date": entry_date,
                    "open": float(row["Open"]) if not isinstance(row["Open"], float) or not row["Open"] != row["Open"] else None,
                    "close": float(row["Close"]) if not isinstance(row["Close"], float) or not row["Close"] != row["Close"] else None,
                }

                existing.append(new_data)
                added += 1

            if added >= 0:
                asset.financial_data = list(existing)
                
                flag_modified(asset, "financial_data")
                # flag_modified(asset, "updated_at")
                db.commit()
                print(f"[✔] {asset.symbol} updated with {added} new weekly entries.")
            else:
                print(f"[⏭] No new data to update for {asset.symbol}.")

        except Exception as e:
            print(f"[✘] Error on {asset.symbol}: {e}")
            db.rollback()

        # print("After:", asset.financial_data)

    db.close()
    
def update_assets_brvm(db: Session):
    return update_assets_from_csv(db)

def update_assets_from_csv(db: Session, folder_path="backend/app/services/Historique BRVM"):
   # Iterate over all CSV files in the folder
    for filename in os.listdir(folder_path):
        # Ensure that the file is a CSV and the filename matches a symbol
        if filename.endswith(".csv"):
            symbol = filename.replace(".csv", "")  # Get the symbol (remove file extension)
            print(f"[{symbol}] Processing CSV data...")

            # Find the asset from the database by symbol
            asset = db.query(Asset).filter(Asset.symbol == symbol).first()

            if not asset:
                print(f"[⏭] Asset with symbol {symbol} not found in database.")
                continue

            try:
                # Read the CSV file into a DataFrame
                csv_path = os.path.join(folder_path, filename)
                data = pd.read_csv(csv_path, converters={'Ouv.': lambda x: str(x), "Dernier": lambda x: str(x)})

                # Ensure the CSV has necessary columns
                if 'Date' not in data.columns or 'Ouv.' not in data.columns:
                    print(f"[⏭] Missing necessary columns in {filename}. Skipping.")
                    continue
                not_dernier = False
                if 'Dernier' not in data.columns:
                    not_dernier = True 
                # Prepare existing dates for deduplication
                existing = asset.financial_data if isinstance(asset.financial_data, list) else []
                existing_dates = {d.get("date") for d in existing}

                added = 0
                # Process each row of the CSV
                for _, row in data.iterrows():
                    # Convert the Date format to %Y-%m-%d
                    entry_date = pd.to_datetime(row['Date'], format='%d/%m/%Y').strftime('%Y-%m-%d')
                    if entry_date in existing_dates:
                        continue

                    new_data = {
                        "date": entry_date,
                        "open": to_float_inv(row['Ouv.']),
                        "close": to_float_inv(row['Ouv.']) if not_dernier else to_float_inv(row['Dernier']),
                        # "open": row['Ouv.'],
                        # "close": row['Dernier'],
                    }
                    added+=1
                    existing.append(new_data)

                # if added > 0:
                asset.financial_data = list(existing)
                flag_modified(asset, "financial_data")
                db.commit()
                print(f"[✔] {symbol} updated with {added} new entries from {filename}.")
                # else:
                #     print(f"[⏭] No new data to update for {symbol} from {filename}.")

            except Exception as e:
                print(f"[✘] Error processing {symbol} from {filename}: {e}")
                db.rollback()

    db.close()