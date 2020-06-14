"""Views for project."""
import json

import jwt
from aiohttp import web

from constants import JWT_ALGORITHM, JWT_SECRET
from security import generate_password_hash, match_password
from utils.db import return_all_users_login, return_last_id
from utils.token import generate_tokens, update_token


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

    access_token, refresh_token, expires_in = await generate_tokens(user_id)

    if len(user['password']) < 8:
        return web.json_response(
            {
                'error': 'Password is to short',
            },
            status=web.HTTPBadRequest.status_code,
        )

    await db.user.insert_one(
        {
            'id': user_id,
            'login': user['login'],
            'refresh_token': refresh_token.decode('utf-8'),
            'pw_hash': generate_password_hash(user['password']),
        },
    )

    return web.json_response(
        {
            'id': user_id,
            'login': user['login'],
            'accessToken': access_token.decode('utf-8'),
            'refreshToken': refresh_token.decode('utf-8'),
            'expires_in': expires_in,
        },
        status=web.HTTPCreated.status_code,
    )


async def new_tokens(request):
    """
    Refresh token for auth.

    Args:
        request: instance of request from client

    Returns:
        New tokens
    """
    db = request.app['db']
    body = await request.json()

    try:
        payload = jwt.decode(
            body['token'], JWT_SECRET, algorithms=[JWT_ALGORITHM],
        )
    except jwt.DecodeError:
        return web.json_response(
            {
                'error': 'Token in request is invalid',
            },
            status=web.HTTPBadRequest.status_code,
        )
    except jwt.ExpiredSignatureError:
        return web.json_response(
            {
                'error': 'Token in request is expired',
            },
            status=web.HTTPUnauthorized.status_code,
        )

    database_data = await db.user.find_one(
        {'id': payload['user_id']},
        {'_id': 0, 'refresh_token': 1, 'id': 1, 'login': 1},
    )

    if database_data['refresh_token'] != body['token']:
        web.json_response(
            {
                'error': "Token don't match",
            },
            status=web.HTTPUnauthorized.status_code,
        )

    access_token, refresh_token, expires_in = await generate_tokens(
        database_data['id'],
    )

    update_token(db, payload['user_id'], refresh_token)

    return web.json_response(
        {
            'id': database_data['id'],
            'login': database_data['login'],
            'accessToken': access_token.decode('utf-8'),
            'refreshToken': refresh_token.decode('utf-8'),
            'expires_in': expires_in,
        },
        status=web.HTTPOk.status_code,
    )


async def login(request):
    """
    Login exists user.

    Args:
        request: instance of request from client

    Returns:
        information about auth user and new tokens
    """
    db = request.app['db']

    try:
        request_user = await request.json()
        if not request_user['login'] or not request_user['password']:
            return web.json_response(
                {
                    'error': 'Invalid user',
                },
                status=web.HTTPBadRequest.status_code,
            )
    except (json.decoder.JSONDecodeError, KeyError):
        return web.json_response(
            {
                'error': 'Invalid user',
            },
            status=web.HTTPBadRequest.status_code,
        )

    user = await db.user.find_one(
        {'login': request_user['login']},
        {'_id': 0, 'id': 1, 'pw_hash': 1, 'login': 1},
    )

    if user is None:
        return web.json_response(
            {
                'error': 'Invalid user',
            },
            status=web.HTTPUnauthorized.status_code,
        )

    if not match_password(user['pw_hash'], request_user['password']):
        return web.json_response(
            {
                'error': 'Invalid user',
            },
            status=web.HTTPUnauthorized.status_code,
        )

    access_token, refresh_token, expires_in = await generate_tokens(user['id'])

    update_token(db, user['id'], refresh_token)

    return web.json_response(
        {
            'id': user['id'],
            'login': user['login'],
            'accessToken': access_token.decode('utf-8'),
            'refreshToken': refresh_token.decode('utf-8'),
            'expires_in': expires_in,
        },
        status=web.HTTPOk.status_code,
    )
