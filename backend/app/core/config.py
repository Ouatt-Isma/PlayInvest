import os
try:
    from backports.zoneinfo import ZoneInfo
except: 
    from zoneinfo import ZoneInfo
    
import os 
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)


class Settings:
    FRONTEND_URL = os.getenv("FRONTEND_URL", "https://www.playinvest-hd.com")  
    # EMAIL = "ouattaraismael258852@gmail.com"
    # EMAIL_PWD = "gnem sunc xoqn kpak"
    # hostname = "smtp.gmail.com"
    
    EMAIL = "ne-pas-repondre@playinvest-hd.com"
    EMAIL_PWD = "Play1nvest"
    hostname = "mail.privateemail.com"
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    DEFAULT_AVATAR = 'icons/default.png'
    SECRET_KEY = "mykey"
    
    ALGORITHM = "HS256"
    
    SECURITY_PASSWORD_SALT = "reset-password-salt"
    
    port = 587
    start_tls = True
    amount_godfather = 50
    amount_qcm = 25
    amount_challenge = 50
    amount_begin = 500
    currency = 'EUR'
    ADMIN_EMAIL = "ouattaraismael1999@gmail.com, harolddoue@gmail.com"
    # TZ_FR = ZoneInfo("GMT")
    TZ_GMT = ZoneInfo("UTC")
    minimum_asset = 0.01 
    fees = {"STOCK": {"EU": 0.0065, "US": 0.0140, "WORLD": 0.0145, "AFRIQUE": 0.0185}, "CRYPTO": 0.0175, "ETF": 0.002} #fees
    log = logging.getLogger("fastapi")

settings = Settings()


# import os
# from dotenv import load_dotenv
# load_dotenv()

# email = os.getenv("EMAIL_USERNAME")
# password = os.getenv("EMAIL_PASSWORD")