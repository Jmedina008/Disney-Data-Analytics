"""
Security utilities for the MCP server.
Handles authentication, encryption, and token management.
"""

from datetime import datetime, timedelta
from typing import Any, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet
from app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Encryption for API keys
fernet = Fernet(settings.ENCRYPTION_KEY.encode())

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta | None = None
) -> str:
    """
    Create JWT access token.
    Args:
        subject: Token subject (usually user ID)
        expires_delta: Token expiration time
    Returns:
        str: Encoded JWT token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm="HS256"
    )
    return encoded_jwt

def verify_token(token: str) -> dict:
    """
    Verify JWT token.
    Args:
        token: JWT token to verify
    Returns:
        dict: Decoded token payload
    Raises:
        JWTError: If token is invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        return payload
    except JWTError as e:
        raise JWTError(f"Invalid token: {e}")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hash.
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password
    Returns:
        bool: True if password matches hash
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash password.
    Args:
        password: Plain text password
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)

def encrypt_api_key(api_key: str) -> bytes:
    """
    Encrypt API key.
    Args:
        api_key: Plain text API key
    Returns:
        bytes: Encrypted API key
    """
    return fernet.encrypt(api_key.encode())

def decrypt_api_key(encrypted_key: bytes) -> str:
    """
    Decrypt API key.
    Args:
        encrypted_key: Encrypted API key
    Returns:
        str: Decrypted API key
    """
    return fernet.decrypt(encrypted_key).decode()

def generate_api_key() -> str:
    """
    Generate a new API key.
    Returns:
        str: Generated API key
    """
    return Fernet.generate_key().decode() 