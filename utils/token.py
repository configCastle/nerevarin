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
