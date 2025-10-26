from sqlalchemy.orm import Session
from app.db.models.user import User
from app.utils.email import send_email
from app.utils.template_loader import render_html_template
from app.utils.template_loader import render_html_template
import asyncio
    
def send_weekly_notif_all_users(db: Session):
    """
    Sends the weekly recap email to all active users.
    """
    users = db.query(User).all()
    sent_count = 0

    for user in users:
        if user.email == "harolddoue@gmail.com" or user.email == "ouattaraismael258852@gmail.com" :
            try:
                subject = "Votre résumé hebdomadaire sur PlayInvest 🚀"
                # Example dynamic data
                data = {"portfolio_value":10250.75,
                    "portfolio_currency":"EUR",
                    "weekly_perf":"+2.45 %",
                    "ytd_perf":"+8.10 %",
                    "rank":5,
                    "top1_name":"ASML Holding",
                    "top1_perf":"+6.2 %",
                    "top2_name":"Nestlé",
                    "top2_perf":"+4.8 %",
                    "top3_name":"BNP Paribas",
                    "top3_perf":"+3.5 %",
                    "user_email":"user@example.com",
                    "Actif1" : "AA",
                    "Actif2" : "BB"}
                    
                html = render_html_template(
                    "weekly_email.html",
                    **data
                    )
                
                html_message = render_html_template("weekly_email.html", **data)
                asyncio.run(
                    send_email(
                    to=user.email,
                    subject=subject,
                    content=html_message,  # <-- HTML message
                ))
                print(f"[✔] Email envoyé à {user.email}")
                sent_count += 1

            except Exception as e:
                print(f"[✘] Erreur d'envoi pour {user.email}: {e}")
                db.rollback()

    print(f"✅ {sent_count} emails envoyés au total.")
