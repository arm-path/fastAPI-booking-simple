from fastapi import APIRouter, Response
from pydantic import EmailStr

from app.authentication.schemas import RegistrationUserSchema, LoginUserSchema
from app.authentication.services import (
    RegistrationAndAuthService,
    get_jwt_token,
    get_password_hash,
    verify_password,
    check_token_url)
from app.celery_tasks import send_email__for_verification_user
from app.exceptions import EmailOrPasswordIsIncorrect, UserAlreadyExistsException, InvalidURLTokenException
from app.logging import logger

router = APIRouter(
    prefix='/authentication',
    tags=['Авторизация']
)


@router.post('/registration')
async def registration(data: RegistrationUserSchema):
    user = await RegistrationAndAuthService.get_object(email=data.email)
    if user:
        raise UserAlreadyExistsException
    await RegistrationAndAuthService.create_object(email=data.email, hashed_password=get_password_hash(data.password_1))
    # send_email__for_verification_user.delay(data.email)  # TODO: Верификация email.
    logger.info('Registration User', extra={'email': data.email})
    return {'detail': 'success'}


@router.post('/login')
async def login(response: Response, data: LoginUserSchema):
    user = await RegistrationAndAuthService.get_object(email=data.email)
    if not user or not verify_password(data.password, user.hashed_password):
        raise EmailOrPasswordIsIncorrect
    access_token = get_jwt_token({'user': str(user.id)})
    response.set_cookie('access_token', access_token, httponly=True)
    return {'detail': 'success'}


@router.post('/logout')
def logout(response: Response):
    response.delete_cookie('access_token')
    return {'detail': 'success'}


@router.get('/email-confirmation/{token}')
async def email_confirmation(token: str):
    email: EmailStr = check_token_url(token)
    user = await RegistrationAndAuthService.get_object(email=email)
    if not user:
        raise InvalidURLTokenException
    if not user.email_verified:
        await RegistrationAndAuthService.update_object(user.id, email_verified=True)
    logger.info('Verification Email', extra={'user_id': user.id, 'email': email})
    return {'detail': 'success'}
