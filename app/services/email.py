import smtplib
import ssl
from email.message import EmailMessage

from app.config import settings


def send_verification_email(to_email: str, code: str) -> None:
    """Send a verification code to the given email using SMTP settings from app config."""
    host = settings.smtp_host
    port = settings.smtp_port or 465
    username = settings.smtp_username
    password = settings.smtp_password
    from_email = settings.smtp_from or username

    if not all([host, username, password, from_email]):
        raise RuntimeError("SMTP configuration is incomplete. Check env vars.")

    msg = EmailMessage()
    msg["Subject"] = "Your verification code"
    msg["From"] = from_email
    msg["To"] = to_email
    msg.set_content(f"Your verification code is: {code}")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.send_message(msg)
