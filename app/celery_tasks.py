from celery import Celery

from app.authentication.services import get_token_url
from app.mail.services import send_message
from app.mail.templates import confirmation_email_message
from app.settings import settings

app_celery = Celery('app_celery', broker=settings.REDIS_URL)


@app_celery.task
def send_email__for_verification_user(email):
    url_token = get_token_url(email)
    msg = confirmation_email_message(email, url_token)
    send_message(msg)
