from sqlalchemy import Column, Integer, String, JSON, DateTime
from app.core.database import Base  # adjust if your base is defined elsewhere
from datetime import datetime, timedelta
from sqlalchemy.orm import relationship
from app.db.models.transactions import Transaction
from sqlalchemy.sql import func
from app.core.config import settings
from app.utils.conv import to_float

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String)
    symbol = Column(String)
    country = Column(String)
    website = Column(String)
    financial_data = Column(JSON)
    currency = Column(String)
    type = Column(String)
    region = Column(String)
    description = Column(String)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
    transactions = relationship(Transaction, back_populates="asset", cascade="all, delete-orphan")

    # def get_latest_price(self):
    #     if isinstance(self.financial_data, list) and self.financial_data:
    #         # Parse and sort data by date descending
    #         sorted_data = sorted(
    #             self.financial_data,
    #             key=lambda d: d.get("date", ""),
    #             reverse=True
    #         )

    #         # Convert string dates to datetime objects
    #         for item in sorted_data:
    #             if isinstance(item["date"], str):
    #                 item["date"] = datetime.strptime(item["date"], "%Y-%m-%d")

    #         latest_data = sorted_data[0]
    #         latest_date = latest_data["date"]
    #         latest_close = float(latest_data.get("close", None))
    #     return latest_close
    
    
    def to_dict(self):
        latest_data = None
        variation_1 = None
        variation_7 = None
        variation_1M = None
        variation_3M = None
        variation_6M = None
        variation_1y = None
        variation_all = None
        
        if isinstance(self.financial_data, list) and self.financial_data:
            # Parse and sort data by date descending
            sorted_data = sorted(
                self.financial_data,
                key=lambda d: d.get("date", ""),
                reverse=True
            )

            # Convert string dates to datetime objects
            for item in sorted_data:
                if isinstance(item["date"], str):
                    item["date"] = datetime.strptime(item["date"], "%Y-%m-%d")

            latest_data = sorted_data[0]
            latest_date = latest_data["date"]
            # latest_close = to_float(latest_data.get("close", None))
            latest_close = latest_data.get("close", None)
        
            def find_closest(days):
                print(latest_date)
                print(datetime.utcnow())
                raise NotImplemented
                target_date = datetime.utcnow() - timedelta(days=days+1) 
                return self.get_price_at(target_date, open=False)
                
                # candidates = [entry for entry in sorted_data[1:] if entry["date"] >= target_date]
                # if not candidates:
                #     return None
                # closest = min(candidates, key=lambda x: (x["date"] - target_date).days)
                # return closest
            def compute_variation(past_entry):
                try:
                    # past_close = to_float(past_entry["close"])
                    past_close = past_entry["close"]
                    if not past_close:
                        return None
                    return round((latest_close - past_close) / past_close * 100, 2)
                except:
                    return None

            # Variations
            if len(sorted_data) > 1:
                variation_1 = compute_variation(sorted_data[1])
            if len(sorted_data) > 7:
                closest_7 = find_closest(7)
                variation_7 = compute_variation(closest_7)
            closest_30 = find_closest(30)
            closest_90 = find_closest(90)
            closest_180 = find_closest(180)
            closest_365 = find_closest(365)
            earliest = sorted_data[-1] if len(sorted_data) > 1 else None

            variation_1M = compute_variation(closest_30)
            variation_3M = compute_variation(closest_90)
            variation_6M = compute_variation(closest_180)
            variation_1y = compute_variation(closest_365)
            variation_all = compute_variation(earliest)
        # latest_price = to_float(latest_data.get("close")) if latest_data else None
        latest_price = latest_data.get("close") if latest_data else None
        return {
            "id": self.id,
            "name": self.name,
            "symbol": self.symbol,
            "latest_price": latest_price,
            "fees": self.get_fees(), 
            "buying_price": (1+self.get_fees())*latest_price,  #faire varier en fonction de commission
            "variation_1d": variation_1,
            "variation_7d": variation_7,
            "variation_1M": variation_1M,
            "variation_3M": variation_3M,
            "variation_6M": variation_6M,
            "variation_1y": variation_1y,
            "variation_all": variation_all,
            "country": self.country,
            "type": self.type,
            "region": self.region,
            "currency": self.currency,
            "description": self.description,
            "updated_at": self.updated_at,
        }

    def isETF(self) -> bool:
        return self.type == "ETF"

    def isCrypto(self) -> bool:
        return self.type == "Crypto"

    def isStock(self) -> bool:
        # If 'Action' appears anywhere in type, treat it as Stock
        return "Action" in (self.type or "")

    # --- Region checks ---
    def isAfrica(self) -> bool:
        return self.region == "Afrique"

    def isUSA(self) -> bool:
        return self.region == "États-Unis"

    def isEurope(self) -> bool:
        return self.region == "Europe"

    def isWorld(self) -> bool:
        return self.region == "Monde"
       
    # Extract prices
    def get_price_at(self, date_input, open=False):
        # Normalize to a date
        if isinstance(date_input, datetime):
            target_date = date_input.date()
        elif isinstance(date_input, str):
            target_date = datetime.strptime(date_input, "%Y-%m-%d").date()
        else:
            raise TypeError(f"Unsupported type for date_input: {type(date_input)}")

        closest = min(
            self.financial_data,
            key=lambda x: abs(
                (
                    x["date"].date() if isinstance(x["date"], datetime)
                    else datetime.strptime(x["date"], "%Y-%m-%d").date()
                ) - target_date
            ),
            default=None
        )

        if open:
            return closest["open"] if closest else None
        return closest["close"] if closest else None

    
    def get_fees(self):
        if (self.isETF):
            return settings.fees["ETF"]
        if (self.isStock):
            if (self.isAfrica):
                return settings.fees["AFRIQUE"]
            if (self.isEurope):
                return settings.fees["EU"]
            if (self.isWorld):
                return settings.fees["WORLD"]
            if (self.isUSA):
                return settings.fees["US"]
        if (self.isCrypto):
            return settings.fees["CRYPTO"]
