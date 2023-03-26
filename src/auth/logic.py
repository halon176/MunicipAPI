import time
from typing import Dict

import jwt
from src.config import SECRET_AUTH, ALGORITHM


def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, SECRET_AUTH, algorithm=ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_AUTH, algorithms=[ALGORITHM])
        print(decoded_token, "token decodificato")
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}

