try:
    from backports.zoneinfo import ZoneInfo
except: 
    from zoneinfo import ZoneInfo
    
import os 
class Settings:
    FRONTEND_URL = "http://localhost:3000"
    EMAIL = "ouattaraismael258852@gmail.com"
    DATABASE_URL = os.getenv("DATABASE_URL")
    
    DEFAULT_AVATAR = 'icons/default.png'
    SECRET_KEY = "mykey"
    # EMAIL_PWD = "oswbxjdwsthvfreg"
    # EMAIL_PWD = "stmmpggbsapyysif"
    
    ALGORITHM = "HS256"
    EMAIL_PWD = "gnem sunc xoqn kpak"
    SECURITY_PASSWORD_SALT = "reset-password-salt"
    
    hostname = "smtp.gmail.com"
    port = 587
    start_tls = True
    amount_godfather = 50
    amount_qcm = 25
    amount_challenge = 50
    currency = 'EUR'
    ADMIN_EMAIL = "ouattaraismael1999@gmail.com"
    # TZ_FR = ZoneInfo("GMT")
    TZ_GMT = ZoneInfo("UTC")

settings = Settings()


# import os
# from dotenv import load_dotenv
# load_dotenv()

# email = os.getenv("EMAIL_USERNAME")
# password = os.getenv("EMAIL_PASSWORD")