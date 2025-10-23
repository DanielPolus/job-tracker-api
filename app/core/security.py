from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config import settings

ALGO = "HS256"

def create_token(sub: str, minutes: int) -> str:
    exp = datetime.utcnow() + timedelta(minutes=minutes)
    payload = {"sub": sub, "exp": exp}
    return jwt.encode(payload, settings.secret_key, algorithm=ALGO)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.secret_key, algorithms=[ALGO])
    except JWTError:
        raise
