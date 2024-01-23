from fastapi import APIRouter

from app.mail.schemas import MailSchema
from app.mail.services import send_message
from app.mail.templates import official_mail

router = APIRouter(
    prefix='/mail',
    tags=['Электронная почта']
)


@router.post('/send')
def send_mail(data: MailSchema):
    msg = official_mail(data.to, data.subject, data.text)
    send_message(msg)
    return {'detail': 'success'}
