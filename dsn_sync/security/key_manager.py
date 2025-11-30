"""Secure key management for dsn-sync."""

import secrets
import hashlib
from typing import Optional
from ..config.settings import KEY_SIZE


class KeyManager:
    """Manages cryptographic keys for encryption and authentication."""
    
    def __init__(self):
        self._key: Optional[bytes] = None
        self._key_hash: Optional[str] = None
    
    def generate_key(self) -> bytes:
        """Generate a new cryptographic key."""
        self._key = secrets.token_bytes(KEY_SIZE)
        self._key_hash = hashlib.sha256(self._key).hexdigest()
        return self._key
    
    def get_key(self) -> Optional[bytes]:
        """Retrieve the current key."""
        return self._key
    
    def store_key(self, key: bytes) -> str:
        """Store key and return hash identifier."""
        self._key = key
        self._key_hash = hashlib.sha256(key).hexdigest()
        return self._key_hash
    
    def get_key_hash(self) -> Optional[str]:
        """Get the hash of the current key."""
        return self._key_hash
    
    def rotate_key(self) -> bytes:
        """Rotate to a new key."""
        return self.generate_key()
    
    def key_exists(self) -> bool:
        """Check if a key exists."""
        return self._key is not None

