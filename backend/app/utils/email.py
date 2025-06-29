# utils/email.py

import aiosmtplib
from app.core.config import settings

from email.message import EmailMessage

async def send_confirmation_email(to_email: str, username: str, token: str):
    message = EmailMessage()
    message["From"] = settings.EMAIL
    message["To"] = to_email
    message["Subject"] = "Confirmez votre compte PlayInvest"
    message.set_content(f"""
Bonjour {username},

Merci de vous être inscrit à PlayInvest.

Cliquez sur ce lien pour confirmer votre compte :
{settings.FRONTEND_URL}/confirm?token={token}

Merci !
""")

    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username=settings.EMAIL,
        password=settings.EMAIL_PWD  # Use app password for Gmail
    )


async def send_password_reset_email(to_email: str, username: str, token: str):
    message = EmailMessage()
    message["From"] = settings.EMAIL
    message["To"] = to_email
    message["Subject"] = "Réinitialisez votre mot de passe PlayInvest"
    message.set_content(f"""
Bonjour {username},

Vous avez demandé à réinitialiser votre mot de passe PlayInvest.

Cliquez sur le lien suivant pour définir un nouveau mot de passe :
{settings.FRONTEND_URL}/reset-password?token={token}

Ce lien expirera dans 1 heure.

Si vous n'avez pas demandé cela, vous pouvez ignorer ce message.

PlayInvest
""")

    await aiosmtplib.send(
        message,
        hostname="smtp.gmail.com",
        port=587,
        start_tls=True,
        username=settings.EMAIL,
        password=settings.EMAIL_PWD
    )
