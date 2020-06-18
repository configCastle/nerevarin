"""Utils for tokens operation."""
from datetime import datetime, timedelta

import jwt

from constants import (
    JWT_ALGORITHM,
    JWT_EXP_DELTA_DAYS,
    JWT_EXP_DELTA_MINUTES,
    JWT_SECRET,
)


async def generate_tokens(user_id):
    """
    Generate new tokens.

    Args:
        user_id: id for user generate

    Returns:
        acces_token, refresh_token and expires_in
    """
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

    expires_in = datetime.utcnow() + timedelta(minutes=JWT_EXP_DELTA_MINUTES)
    expires_in = int(expires_in.timestamp())

    return access_token, refresh_token, expires_in


async def update_token(db, user_id, refresh_token):
    """
    Update refresh token.

    Args:
        db: instance of database
        user_id: id of user for update token
        refresh_token: token which write in bd
    """
    await db.user.update_one(
        {'id': user_id},
        {'$set': {'refresh_token': refresh_token.decode('utf-8')}},
    )
