from itsdangerous import URLSafeTimedSerializer
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
SECURITY_PASSWORD_SALT = settings.SECURITY_PASSWORD_SALT

def generate_reset_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)

def confirm_reset_token(token: str, expiration=3600):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    return serializer.loads(token, salt=SECURITY_PASSWORD_SALT, max_age=expiration)
