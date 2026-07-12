"""
FinSight - Security Utilities
-------------------------------
Password hashing, password verification, secure token generation,
and basic input validation (email format, password strength).
"""

import re
import secrets
import bcrypt
from datetime import datetime, timedelta


# ---------------- Password Hashing ----------------

def hash_password(plain_password: str) -> str:
    """Hash a plaintext password using bcrypt. Returns a string safe for DB storage."""
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, password_hash: str) -> bool:
    """Check a plaintext password against a stored bcrypt hash."""
    return bcrypt.checkpw(plain_password.encode("utf-8"), password_hash.encode("utf-8"))


# ---------------- Token Generation ----------------

def generate_token() -> str:
    """Generate a secure random URL-safe token for email verification / password reset."""
    return secrets.token_urlsafe(32)


def get_expiry(hours: int) -> datetime:
    """Return a datetime object `hours` from now, used for token expiry."""
    return datetime.now() + timedelta(hours=hours)


def is_token_expired(expires_at: datetime) -> bool:
    """Check whether a token's expiry datetime has passed."""
    return datetime.now() > expires_at


# ---------------- Input Validation ----------------

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def is_valid_email(email: str) -> bool:
    """Basic email format validation."""
    return bool(EMAIL_REGEX.match(email.strip()))


def is_strong_password(password: str) -> tuple[bool, str]:
    """
    Enforce minimum password strength rules.
    Returns (is_valid, error_message).
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    return True, ""
