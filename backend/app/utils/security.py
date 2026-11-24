from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError
from pwdlib.hashers.argon2 import Argon2Hasher
from pwdlib.hashers.bcrypt import BcryptHasher

from app.config import JWT_ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET_KEY

password_hasher = PasswordHash((BcryptHasher(), Argon2Hasher()))


class TokenConfigurationError(Exception):
    pass


class InvalidAccessTokenError(Exception):
    pass


def hash_password(password: str) -> str:
    return password_hasher.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return password_hasher.verify(password, password_hash)
    except (UnknownHashError, ValueError):
        return False


def create_access_token(user_id: int) -> tuple[str, int]:
    if not JWT_SECRET_KEY or len(JWT_SECRET_KEY.encode("utf-8")) < 32:
        raise TokenConfigurationError(
            "JWT_SECRET_KEY must contain at least 32 bytes."
        )

    expires_in = JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
    issued_at = datetime.now(timezone.utc)
    token = jwt.encode(
        {
            "sub": str(user_id),
            "iat": issued_at,
            "exp": issued_at + timedelta(seconds=expires_in),
            "token_type": "access",
        },
        JWT_SECRET_KEY,
        algorithm="HS256",
    )
    return token, expires_in


def decode_access_token(token: str) -> int:
    if not JWT_SECRET_KEY or len(JWT_SECRET_KEY.encode("utf-8")) < 32:
        raise TokenConfigurationError(
            "JWT_SECRET_KEY must contain at least 32 bytes."
        )

    try:
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=["HS256"],
            options={"require": ["exp", "iat", "sub"]},
        )
        if payload.get("token_type") != "access":
            raise InvalidAccessTokenError
        user_id = int(payload["sub"])
        if user_id < 1:
            raise InvalidAccessTokenError
        return user_id
    except (jwt.InvalidTokenError, KeyError, TypeError, ValueError) as error:
        raise InvalidAccessTokenError from error