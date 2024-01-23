from fastapi import APIRouter, Depends

from app.authentication.services import get_current_user


router = APIRouter(
    prefix='/user',
    tags=['Пользователи']
)


@router.get('/detail')
async def get_user(user=Depends(get_current_user)):
    return user