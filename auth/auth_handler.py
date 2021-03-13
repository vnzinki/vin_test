from models.user import User
import time
from typing import Dict

import jwt
from config import SECRET_KEY

JWT_SECRET = SECRET_KEY
JWT_ALGORITHM = "HS256"


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user: User) -> Dict[str, str]:
    payload = {
        "uid": user.id,
        "exp": time.time() + 600,
        "scope": user.role
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except Exception:
        return {}
