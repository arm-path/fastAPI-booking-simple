from email.message import EmailMessage
from pydantic import EmailStr

from app.settings import settings


def official_mail(email: EmailStr, subject: str, text: str):
    message = EmailMessage()

    message.add_header('From', settings.EMAIL_LOGIN)
    message.add_header('To', settings.EMAIL_LOGIN)  # TODO: Изменить на email.
    message.add_header('Subject', subject)

    content = f"""
    <h1 style="text-align:center">Сайт по бронированию отелей Booking</h1>
    <p>{text}</p>
    
    --- <br/>
    С Уважением, администрация сайта!
    """
    message.set_content(content, subtype='html')
    return message


def confirmation_email_message(email: EmailStr, token: str):
    message = EmailMessage()
    message.add_header('From', settings.EMAIL_LOGIN)
    message.add_header('To', settings.EMAIL_LOGIN)  # TODO: Изменить на email.
    message.add_header('Subject', 'Подтверждение электронной почты')

    content = f"""
    <h1 style="text-align:center">Подтверждение электронной почты</h1>
    <p>Для подтверждения электронной почты, на сайте {settings.SITE_NAME}, перейдите по ссылке:
    <a href="{settings.SITE_PROTOCOL}://{settings.SITE_DOMAIN}:{settings.SITE_PORT}/authentication/email-confirmation/{token}">
    Подтвердить электронную почту
    </a>
     </p>
    """

    message.set_content(content, subtype='html')
    return message
