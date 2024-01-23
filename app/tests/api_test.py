import pytest
from httpx import AsyncClient
from fastapi import Response

from app.users.services import UserService


@pytest.mark.parametrize('data, status_code', [
    ({'email': 'str@example.com', 'password_1': 'password', 'password_2': 'password'}, 200),
    ({'email': 'str@example.com', 'password_1': 'password', 'password_2': 'password'}, 409),
    ({'email': 'str', 'password_1': 'password', 'password_2': 'password'}, 422),
    ({'email': 'strTest@example.com', 'password_1': 'passWord', 'password_2': 'password'}, 409)
])
async def test_registration(ac: AsyncClient, data, status_code):
    response = await ac.post('/authentication/registration', json=data)
    assert response.status_code == status_code


async def test_entering_into_db_during_registration(ac: AsyncClient):
    data = {'email': 'strUser@example.com', 'password_1': 'password', 'password_2': 'password'}
    response = await ac.post('/authentication/registration', json=data)
    user = await UserService.get_object(email='strUser@example.com')
    assert user and not user.installer and not user.email_verified


@pytest.mark.parametrize('email, password, status_code', [
    ('user@example.com', 'string', 200),
    ('user@example.com', 'stringTest', 401),
    ('example.com', 'stringTest', 422),
])
async def test_login(ac: AsyncClient, email, password, status_code):
    response = await ac.post('/authentication/login', json={'email': email, 'password': password})
    assert response.status_code == status_code


async def test_logout(ac: AsyncClient):
    response = await ac.post('/authentication/logout')
    assert response.cookies.get('access_token') is None


@pytest.mark.parametrize('url, method, status_code', [
    ('/user/detail', 'get', 401), ('/booking/', 'get', 401), ('/booking/create', 'post', 401),
    ('/hotels/create', 'post', 401), ('/hotels/update/1', 'put', 401), ('/hotels/delete/1', 'delete', 401)
])
async def test_401_UNAUTHORIZED(ac: AsyncClient, url, method, status_code):
    if method == 'post':
        response = await ac.post(url)
    elif method == 'put':
        response = await ac.put(url)
    elif method == 'delete':
        response = await ac.delete(url)
    else:
        response = await ac.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize('url, method, status_code', [
    ('/hotels/create', 'post', 403), ('/hotels/update/1', 'put', 403), ('/hotels/delete/1', 'delete', 403),
    ('/rooms/create', 'post', 403), ('/rooms/update/1', 'put', 403), ('/rooms/delete/1', 'delete', 403),
])
async def test_403_FORBIDDEN(ac: AsyncClient, url, method, status_code):
    response = await ac.post('/authentication/login', json={'email': 'user@example.com', 'password': 'string'})
    if method == 'post':
        response = await ac.post(url)
    elif method == 'put':
        response = await ac.put(url)
    elif method == 'delete':
        response = await ac.delete(url)
    else:
        response = await ac.get(url)
    assert response.status_code == status_code
