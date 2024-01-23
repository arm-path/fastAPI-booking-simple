from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.authentication.services import RegistrationAndAuthService, verify_password, get_jwt_token, get_current_user
from app.settings import settings


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        user = await RegistrationAndAuthService.get_object(email=email)
        if not user or not verify_password(password, user.hashed_password):
            return False
        access_token = get_jwt_token({'user': str(user.id)})
        request.session.update({"token": access_token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        if not token:
            return False
        user = await get_current_user(token=token)
        if not user or not user.installer:
            return False
        return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY_ADMIN_AUTH)
