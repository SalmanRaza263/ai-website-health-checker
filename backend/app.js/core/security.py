from fastapi import Request, HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address
import time
import hashlib
import hmac
import os

limiter = Limiter(key_func=get_remote_address)

def hash_password(password: str) -> str:
    """Hash a password"""
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt.hex() + ':' + key.hex()

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password"""
    salt_hex, key_hex = hashed.split(':')
    salt = bytes.fromhex(salt_hex)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return key.hex() == key_hex

def generate_api_key() -> str:
    """Generate API key"""
    return hashlib.sha256(os.urandom(32)).hexdigest()

def validate_url(url: str) -> bool:
    """Validate URL format"""
    import re
    pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(pattern, url) is not None

def sanitize_url(url: str) -> str:
    """Sanitize URL"""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url.strip()