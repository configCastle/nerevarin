"""Security for project."""
import base64

import bcrypt


def match_password(encoded, password):
    """
    Match passwords of user.

    Args:
        encoded: hash of object
        password: text of password from client

    Returns:
        true of false
    """
    password = password.encode('utf-8')
    encoded = encoded.encode('utf-8')

    hashed = base64.b64decode(encoded)
    return bcrypt.hashpw(password, hashed) == hashed


def generate_password_hash(password, salt_rounds=12):
    """
    Generate has for password of user.

    Args:
        password: password from client
        salt_rounds: number of salt round

    Returns:
        hash of password for database
    """
    password_bin = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bin, bcrypt.gensalt(salt_rounds))
    encoded = base64.b64encode(hashed)
    return encoded.decode('utf-8')
