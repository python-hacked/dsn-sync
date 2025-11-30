"""Authentication token management."""

import time
import json
import hashlib
import hmac
from typing import Dict, Any, Optional
from ..config.settings import TOKEN_EXPIRY_HOURS


class TokenManager:
    """Manages authentication tokens with endpoint information."""
    
    def __init__(self, key: bytes):
        """Initialize with secret key."""
        self.secret_key = key
    
    def generate_token(self, endpoint_number: str, additional_data: Optional[Dict] = None) -> str:
        """Generate authentication token with endpoint number."""
        payload = {
            "endpoint_number": endpoint_number,
            "timestamp": time.time(),
            "expiry": time.time() + (TOKEN_EXPIRY_HOURS * 3600),
        }
        if additional_data:
            payload.update(additional_data)
        
        # Create signature
        payload_json = json.dumps(payload, sort_keys=True)
        signature = hmac.new(
            self.secret_key,
            payload_json.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        
        token_data = {
            "payload": payload,
            "signature": signature
        }
        
        # Encode token
        import base64
        token_json = json.dumps(token_data)
        return base64.urlsafe_b64encode(token_json.encode('utf-8')).decode('utf-8')
    
    def validate_token(self, token: str) -> bool:
        """Validate token signature and expiry."""
        try:
            import base64
            token_json = base64.urlsafe_b64decode(token.encode('utf-8')).decode('utf-8')
            token_data = json.loads(token_json)
            
            payload = token_data.get("payload", {})
            signature = token_data.get("signature", "")
            
            # Check expiry
            if time.time() > payload.get("expiry", 0):
                return False
            
            # Validate signature
            payload_json = json.dumps(payload, sort_keys=True)
            expected_signature = hmac.new(
                self.secret_key,
                payload_json.encode('utf-8'),
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(expected_signature, signature)
        except Exception:
            return False
    
    def get_endpoint_from_token(self, token: str) -> Optional[str]:
        """Extract endpoint number from token."""
        try:
            import base64
            token_json = base64.urlsafe_b64decode(token.encode('utf-8')).decode('utf-8')
            token_data = json.loads(token_json)
            payload = token_data.get("payload", {})
            return payload.get("endpoint_number")
        except Exception:
            return None
    
    def update_token(self, token: str, new_endpoint: str) -> str:
        """Update token with new endpoint number."""
        try:
            import base64
            token_json = base64.urlsafe_b64decode(token.encode('utf-8')).decode('utf-8')
            token_data = json.loads(token_json)
            payload = token_data.get("payload", {})
            payload["endpoint_number"] = new_endpoint
            payload["timestamp"] = time.time()
            payload["expiry"] = time.time() + (TOKEN_EXPIRY_HOURS * 3600)
            return self.generate_token(new_endpoint, payload)
        except Exception:
            return self.generate_token(new_endpoint)

