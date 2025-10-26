# utils/email.py

import aiosmtplib
from app.core.config import settings

from email.message import EmailMessage

async def send_email(to: str, subject, content:str):
    message = EmailMessage()
    message["From"] = f"PlayInvest <{settings.EMAIL}>"
    message["To"] = to
    message["Subject"] = subject
    message.add_alternative(content, subtype="html")

    await aiosmtplib.send(
        message,
        hostname=settings.hostname,
        port=settings.port,
        start_tls=settings.start_tls,
        username=settings.EMAIL,
        password=settings.EMAIL_PWD  # Use app password for Gmail
    )


async def send_confirmation_email(to_email: str, username: str, token: str):
    message = EmailMessage()
    message["From"] = f"PlayInvest <{settings.EMAIL}>"
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
        hostname=settings.hostname,
        port=settings.port,
        start_tls=settings.start_tls,
        username=settings.EMAIL,
        password=settings.EMAIL_PWD  # Use app password for Gmail
    )


async def send_password_reset_email(to_email: str, username: str, token: str):
    message = EmailMessage()
    message["From"] = f"PlayInvest <{settings.EMAIL}>"
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
        hostname=settings.hostname,
        port=settings.port,
        start_tls=settings.start_tls,
        username=settings.EMAIL,
        password=settings.EMAIL_PWD
    )

async def send_godfather_email(to_email: str, username: str, username_f: str, amount_conv=None, portfolio_curr=""):
    message = EmailMessage()
    message["From"] = f"PlayInvest <{settings.EMAIL}>"
    message["To"] = to_email
    message["Subject"] = "Bonus de Parrainage Playinvest!"
    conversion_part = (
    f" ({amount_conv} {portfolio_curr})"
    if settings.currency != portfolio_curr and amount_conv and portfolio_curr
    else "")   
    message.set_content(f"""
Bonjour {username},

Bonne nouvelle ! Un nouvel utilisateur ({username_f}) vient de vous désigner comme parrain lors de son inscription.

En guise de remerciement, votre solde vient d’être crédité de {settings.amount_godfather} {settings.currency}{conversion_part}. 🎁
Vous pouvez consulter votre nouveau solde depuis votre espace personnel: {settings.FRONTEND_URL}/dashboard .

Merci pour votre confiance et votre engagement. Continuez à parrainer pour cumuler encore plus de récompenses !

À très bientôt,
""")

    await aiosmtplib.send(
        message,
        hostname=settings.hostname,
        port=settings.port,
        start_tls=settings.start_tls,
        username=settings.EMAIL,
        password=settings.EMAIL_PWD
    )


async def send_admin_issue(subject):
    message = EmailMessage()
    message["From"] = f"PlayInvest <{settings.EMAIL}>"
    message["To"] = settings.ADMIN_EMAIL
    message["Subject"] = subject
    message.set_content(f"""
Bonjour,

Problème à voir urgemment,
""")

    await aiosmtplib.send(
        message,
        hostname=settings.hostname,
        port=settings.port,
        start_tls=settings.start_tls,
        username=settings.EMAIL,
        password=settings.EMAIL_PWD
    )
