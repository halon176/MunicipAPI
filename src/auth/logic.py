import time
from typing import Dict
from uuid import UUID

import jwt
from src.config import SECRET_AUTH, ALGORITHM


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: UUID) -> Dict[str, str]:
    payload = {
        "user_id": str(user_id),
        "expires": time.time() + 3600
    }
    token = jwt.encode(payload, SECRET_AUTH, algorithm=ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_AUTH, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
