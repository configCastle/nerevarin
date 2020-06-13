"""Views for project."""
from datetime import datetime, timedelta

import jwt
from aiohttp import web

from constants import (
    JWT_ALGORITHM,
    JWT_EXP_DELTA_DAYS,
    JWT_EXP_DELTA_MINUTES,
    JWT_SECRET,
)
from security import generate_password_hash
from utils.db import return_all_users_login, return_last_id


async def register(request):
    """
    Register new user.

    Args:
        request: instance of request.

    Returns:
        json with information about new user
    """
    db = request.app['db']
    user = await request.json()

    user_id = await return_last_id(db) + 1

    if user['login'] in await return_all_users_login(db):
        return web.json_response(
            {
                'error': 'User already exist',
            },
            status=web.HTTPUnauthorized.status_code,
        )

    if len(user['password']) < 8:
        return web.json_response(
            {
                'error': 'Password is to short',
            },
            status=web.HTTPBadRequest.status_code,
        )

    payload_access = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(minutes=JWT_EXP_DELTA_MINUTES),
    }
    access_token = jwt.encode(payload_access, JWT_SECRET, JWT_ALGORITHM)

    payload_refresh = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=JWT_EXP_DELTA_DAYS),
    }
    refresh_token = jwt.encode(payload_refresh, JWT_SECRET, JWT_ALGORITHM)

    await db.user.insert_one(
        {
            'id': user_id,
            'login': user['login'],
            'refresh_token': refresh_token.decode('utf-8'),
            'pw_hash': generate_password_hash(user['password']),
        },
    )

    expires_in = datetime.utcnow() + timedelta(minutes=JWT_EXP_DELTA_MINUTES)

    return web.json_response(
        {
            'id': user_id,
            'login': user['login'],
            'accessToken': access_token.decode('utf-8'),
            'refresToekn': refresh_token.decode('utf-8'),
            'expires_in': int(expires_in.timestamp()),
        },
        status=web.HTTPCreated.status_code,
    )


async def refresh_token(request):
    """
    Refresh token for auth.

    Args:
        request: instance of request from client

    Returns:
        New tokens
    """
    return web.json_response(
        {
            'message': 'OK',
        }
    )
