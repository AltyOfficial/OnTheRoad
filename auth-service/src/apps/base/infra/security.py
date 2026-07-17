import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Tuple
from uuid import UUID

import bcrypt
import jwt

from src.apps.users.exceptions import InvalidTokenError
from src.config.settings import settings


class Security:
    def __init__(
        self,
        secret_key: str,
        algorithm: str = "HS256",
        access_token_expire_minutes: int = 15,
        refresh_token_expire_days: int = 30,
    ):
        """Security class Initializer."""

        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes
        self.refresh_token_expire_days = refresh_token_expire_days

    def hash_password(self, password: str) -> str:
        """Hash password with bcrypt."""

        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)

        return hashed_password.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:

        password_byte_enc = plain_password.encode('utf-8')
        hashed_password_enc = hashed_password.encode('utf-8')

        return bcrypt.checkpw(
            password=password_byte_enc,
            hashed_password=hashed_password_enc,
        )

    def hash_token_sha256(self, token: str) -> str:
        """Hash password with SHA256. Used for storing refresh tokens in DB."""

        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def create_access_token(self, user_id: UUID) -> str:

        expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
        payload = {
            "sub": str(user_id),
            "type": "access",
            "exp": expire,
            "iat": datetime.now(timezone.utc),
        }

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, user_id: UUID) -> Tuple[str, datetime]:

        expire = datetime.now(timezone.utc) + timedelta(days=self.refresh_token_expire_days)
        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": expire,
            "iat": datetime.now(timezone.utc),
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token, expire

    def decode_token(self, token: str, expected_type: str = "refresh") -> Dict[str, Any]:

        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
    
            if payload.get("type") != expected_type:
                raise InvalidTokenError("Invalid token type")
                
            return payload
            
        except jwt.ExpiredSignatureError:
            raise InvalidTokenError("Token has expired")
        except jwt.InvalidTokenError:
            raise InvalidTokenError("Invalid token")


def get_security():
    return Security(secret_key=settings.jwt.JWT_SECRET_KEY)
