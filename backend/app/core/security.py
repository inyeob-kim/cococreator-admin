import base64
import hashlib
import hmac
import secrets
import time

from app.core.config import settings

PASSWORD_SCHEME = "pbkdf2_sha256"
PBKDF2_ITERATIONS = 120_000


def hash_password(plain_password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", plain_password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return (
        f"{PASSWORD_SCHEME}${PBKDF2_ITERATIONS}$"
        f"{base64.urlsafe_b64encode(salt).decode()}$"
        f"{base64.urlsafe_b64encode(digest).decode()}"
    )


def verify_password(plain_password: str, stored_password_hash: str) -> bool:
    try:
        scheme, iteration_raw, salt_raw, digest_raw = stored_password_hash.split("$", 3)
        if scheme != PASSWORD_SCHEME:
            return False
        iterations = int(iteration_raw)
        salt = base64.urlsafe_b64decode(salt_raw.encode("utf-8"))
        expected = base64.urlsafe_b64decode(digest_raw.encode("utf-8"))
    except (ValueError, TypeError):
        return False

    actual = hashlib.pbkdf2_hmac(
        "sha256", plain_password.encode("utf-8"), salt, iterations
    )
    return hmac.compare_digest(expected, actual)


def hash_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def create_access_token(*, user_id: int, role: str, expires_in_seconds: int) -> str:
    expiry = int(time.time()) + expires_in_seconds
    payload = f"{user_id}.{role}.{expiry}"
    signature = hmac.new(
        settings.AUTH_SECRET_KEY.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    token = f"{payload}.{signature}"
    return base64.urlsafe_b64encode(token.encode("utf-8")).decode("utf-8")


def decode_access_token(token: str) -> dict[str, str | int] | None:
    try:
        raw = base64.urlsafe_b64decode(token.encode("utf-8")).decode("utf-8")
        user_id_raw, role, expiry_raw, signature = raw.split(".", 3)
        payload = f"{user_id_raw}.{role}.{expiry_raw}"
        expected_sig = hmac.new(
            settings.AUTH_SECRET_KEY.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(signature, expected_sig):
            return None
        expiry = int(expiry_raw)
        if expiry < int(time.time()):
            return None
        return {"user_id": int(user_id_raw), "role": role, "exp": expiry}
    except (ValueError, TypeError):
        return None
