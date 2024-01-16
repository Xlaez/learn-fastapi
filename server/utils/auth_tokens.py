import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from dotenv import load_dotenv

load_dotenv()

algorithm = os.getenv("ALGORITHM")
access_token_min = 30
refresh_token_min = 60*24*7
secret = os.getenv("JWT_REFRESH_SECRET_KEY")

def generate_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=access_token_min)

    to_encode = { "exp": expires_delta, "sub": str(subject) }
    encoded_jwt = jwt.encode(to_encode, algorithm)
    return encoded_jwt

def generate_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=refresh_token_min)

    to_encode = { "exp": expires_delta, "sub": str(subject) }
    encoded_jwt = jwt.encode(to_encode, algorithm)
    return encoded_jwt