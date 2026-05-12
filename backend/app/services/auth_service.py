from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.user import User


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.settings = get_settings()

    def ensure_default_user(self) -> User:
        existing = self.db.scalar(select(User).limit(1))
        if existing is not None:
            return existing

        user = User(
            username=self.settings.default_admin_username,
            password_hash=self.hash_password(self.settings.default_admin_password),
            role="admin",
            display_name="Default Admin",
            is_active=True,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate(self, username: str, password: str) -> User | None:
        self.ensure_default_user()
        user = self.db.scalar(select(User).where(User.username == username))
        if user is None or not user.is_active:
            return None
        if not self.verify_password(password, user.password_hash):
            return None
        return user

    def create_access_token(self, user: User) -> str:
        expires_at = int((datetime.now(UTC) + timedelta(minutes=self.settings.auth_token_ttl_minutes)).timestamp())
        payload = f"{user.id}:{expires_at}"
        signature = hmac.new(
            self.settings.secret_key.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        token = f"{payload}:{signature}"
        return base64.urlsafe_b64encode(token.encode("utf-8")).decode("utf-8").rstrip("=")

    def get_user_from_token(self, token: str) -> User | None:
        try:
            raw = _b64decode(token)
            user_id_text, expires_at_text, signature = raw.split(":", 2)
        except ValueError:
            return None

        payload = f"{user_id_text}:{expires_at_text}"
        expected_signature = hmac.new(
            self.settings.secret_key.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(signature, expected_signature):
            return None

        if int(expires_at_text) < int(datetime.now(UTC).timestamp()):
            return None

        try:
            user_id = int(user_id_text)
        except ValueError:
            return None
        user = self.db.get(User, user_id)
        if user is None or not user.is_active:
            return None
        return user

    @staticmethod
    def hash_password(password: str) -> str:
        iterations = 390000
        salt = secrets.token_hex(16)
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            iterations,
        ).hex()
        return f"pbkdf2_sha256${iterations}${salt}${digest}"

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        try:
            algorithm, iterations_text, salt, digest = password_hash.split("$", 3)
        except ValueError:
            return False
        if algorithm != "pbkdf2_sha256":
            return False
        derived = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            int(iterations_text),
        ).hex()
        return hmac.compare_digest(derived, digest)


def _b64decode(value: str) -> str:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(f"{value}{padding}".encode("utf-8")).decode("utf-8")

