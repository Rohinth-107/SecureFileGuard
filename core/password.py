import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from core.alert import log_event
from core import config

def generate_salt() -> bytes:
    """Generates a secure, random salt using config defined size."""
    salt = os.urandom(config.SALT_SIZE)
    log_event("info", "New cryptographic salt generated.")
    return salt

def derive_key(password: str, salt: bytes) -> bytes:
    """
    Stretches a password into a key using PBKDF2 with config iterations.
    """
    try:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=config.KEY_LENGTH,
            salt=salt,
            iterations=config.KDF_ITERATIONS,
        )
        raw_key = kdf.derive(password.encode('utf-8'))
        return base64.urlsafe_b64encode(raw_key)
    except Exception as e:
        log_event("error", f"Key derivation failed: {str(e)}")
        return None

def salt_to_str(salt: bytes) -> str:
    """Converts bytes to string for JSON storage."""
    return base64.b64encode(salt).decode('utf-8')

def str_to_salt(salt_str: str) -> bytes:
    """Converts string back to bytes for logic."""
    return base64.b64decode(salt_str)