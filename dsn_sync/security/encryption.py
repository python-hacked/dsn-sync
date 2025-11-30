"""Encryption and decryption utilities."""

import json
import hashlib
import hmac
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64


class EncryptionManager:
    """Handles encryption and decryption of data."""
    
    def __init__(self, key: bytes):
        """Initialize with encryption key."""
        self.key = key
        self._fernet = self._create_fernet(key)
    
    def _create_fernet(self, key: bytes) -> Fernet:
        """Create Fernet cipher from key."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'dsn_sync_salt',
            iterations=100000,
            backend=default_backend()
        )
        key_bytes = kdf.derive(key)
        return Fernet(base64.urlsafe_b64encode(key_bytes))
    
    def encrypt_data(self, data: Dict[str, Any]) -> str:
        """Encrypt data dictionary."""
        data_json = json.dumps(data, ensure_ascii=False)
        encrypted = self._fernet.encrypt(data_json.encode('utf-8'))
        return base64.urlsafe_b64encode(encrypted).decode('utf-8')
    
    def decrypt_data(self, encrypted_data: str) -> Dict[str, Any]:
        """Decrypt encrypted data string."""
        encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
        decrypted = self._fernet.decrypt(encrypted_bytes)
        return json.loads(decrypted.decode('utf-8'))
    
    def generate_signature(self, data: Dict[str, Any], timestamp: float) -> str:
        """Generate HMAC signature for request validation."""
        message = json.dumps(data, sort_keys=True) + str(timestamp)
        signature = hmac.new(
            self.key,
            message.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature
    
    def validate_signature(self, data: Dict[str, Any], timestamp: float, signature: str) -> bool:
        """Validate request signature."""
        expected_signature = self.generate_signature(data, timestamp)
        return hmac.compare_digest(expected_signature, signature)

