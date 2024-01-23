import smtplib
from email.message import EmailMessage

from app.settings import settings


def send_message(template_message: EmailMessage):
    with smtplib.SMTP_SSL(settings.EMAIL_SMTP, settings.EMAIL_PORT) as server:
        server.login(settings.EMAIL_LOGIN, settings.EMAIL_PASSWORD)
        server.send_message(template_message)
