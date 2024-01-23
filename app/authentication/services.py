from datetime import datetime, timedelta

from fastapi import Request, Depends
from itsdangerous import URLSafeTimedSerializer
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.exceptions import (InvalidTokenException,
                            TokenDoesNotExist,
                            TokenTimeHasExpiredException,
                            AccessIsDeniedException,
                            InvalidURLTokenException)
from app.services.database import DatabaseService
from app.settings import settings
from app.users.models import Users
from app.users.schemas import UserSchema
from app.users.services import UserService

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hash_password: str) -> bool:
    return pwd_context.verify(plain_password, hash_password)


def get_jwt_token(data: dict) -> str:
    data_token = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    data_token.update({'exp': expire})
    return jwt.encode(data_token, settings.SECRET_KEY, settings.ALGORITHM)


def get_jwt_token_by_cookie(request: Request) -> str:
    access_token = request.cookies.get('access_token')
    if not access_token:
        raise TokenDoesNotExist
    return access_token


async def get_current_user(token=Depends(get_jwt_token_by_cookie)) -> UserSchema:
    try:
        data_token = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise InvalidTokenException
    if data_token.get('exp') and (int(data_token.get('exp')) < datetime.utcnow().timestamp()):
        raise TokenTimeHasExpiredException
    if not data_token.get('user') and not data_token.get('user').isdigit():
        raise InvalidTokenException
    user = await UserService.get_user(int(data_token.get('user')))
    if not user:
        raise InvalidTokenException
    return user


async def get_user_is_installer(user=Depends(get_current_user)) -> UserSchema:
    if not user.installer:
        raise AccessIsDeniedException
    return user


def get_token_url(data):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY_URL_TOKEN)
    return serializer.dumps(data, salt=settings.SECRET_PASSWORD_SALT_URL_TOKEN)


def check_token_url(token, expiration=4320 * 60):
    serializer = URLSafeTimedSerializer(settings.SECRET_KEY_URL_TOKEN)
    try:
        data = serializer.loads(
            token,
            salt=settings.SECRET_PASSWORD_SALT_URL_TOKEN,
            max_age=expiration
        )
    except Exception:
        raise InvalidURLTokenException
    return data


class RegistrationAndAuthService(DatabaseService):
    model = Users
