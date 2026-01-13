import os
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Professional constants
ITERATIONS = 480000
KEY_LENGTH = 32

def generate_salt() -> bytes:
    """Generates a secure, random 16-byte salt using OS entropy."""
    return os.urandom(16)

def derive_key(password: str, salt: bytes) -> bytes:
    """
    Stretches a password into a 32-byte key using PBKDF2.
    The result is base64 encoded to satisfy Fernet's requirements.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=ITERATIONS,
    )
    # Derive and immediately encode to base64
    raw_key = kdf.derive(password.encode('utf-8'))
    return base64.urlsafe_b64encode(raw_key)

def salt_to_str(salt: bytes) -> str:
    return base64.b64encode(salt).decode('utf-8')

def str_to_salt(salt_str: str) -> bytes:
    return base64.b64decode(salt_str)