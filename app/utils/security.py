"""Security utilities for password hashing"""

from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt
    
    Handles bcrypt's 72-byte limit by pre-hashing longer passwords with SHA256.
    """
    password_bytes = password.encode('utf-8')
    
    # If password exceeds 72 bytes, pre-hash with SHA256 (always 64 bytes)
    if len(password_bytes) > 72:
        # Pre-hash with SHA256 to get a fixed 64-byte hex string
        password = hashlib.sha256(password_bytes).hexdigest()
    # Otherwise use password as-is (it's already <= 72 bytes)
    
    # Pass as string to passlib (it will handle encoding internally)
    try:
        return pwd_context.hash(password)
    except ValueError as e:
        # If still fails, truncate and retry
        if "72 bytes" in str(e):
            password = password_bytes[:72].decode('utf-8', errors='ignore')
            return pwd_context.hash(password)
        raise

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    password_bytes = plain_password.encode('utf-8')
    
    # If password exceeds 72 bytes, pre-hash with SHA256
    if len(password_bytes) > 72:
        plain_password = hashlib.sha256(password_bytes).hexdigest()
    
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError:
        # If verification fails due to length, try truncated version
        plain_password = password_bytes[:72].decode('utf-8', errors='ignore')
        return pwd_context.verify(plain_password, hashed_password)