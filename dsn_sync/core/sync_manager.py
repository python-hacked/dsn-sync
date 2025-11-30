"""Main sync management."""

from typing import Optional
from ..security.key_manager import KeyManager
from ..security.token_manager import TokenManager
from ..server.endpoint_manager import EndpointManager


class SyncManager:
    """Main synchronization manager."""
    
    def __init__(self, key_manager: KeyManager, endpoint_manager: EndpointManager):
        """Initialize sync manager."""
        self.key_manager = key_manager
        self.endpoint_manager = endpoint_manager
        self.token_manager: Optional[TokenManager] = None
        self._initialized = False
    
    def init_sync(self) -> bool:
        """Initialize sync system."""
        if not self.key_manager.key_exists():
            self.key_manager.generate_key()
        
        key = self.key_manager.get_key()
        if key:
            self.token_manager = TokenManager(key)
            self._initialized = True
            return True
        return False
    
    def get_connection_url(self, host: str = "localhost", port: int = 3000) -> str:
        """Get connection URL with current endpoint."""
        endpoint = self.endpoint_manager.get_current_endpoint()
        return f"https://{host}:{port}/sync/{endpoint}"
    
    def generate_token(self) -> Optional[str]:
        """Generate authentication token."""
        if not self._initialized or not self.token_manager:
            return None
        
        endpoint = self.endpoint_manager.get_current_endpoint()
        return self.token_manager.generate_token(endpoint)
    
    def is_initialized(self) -> bool:
        """Check if sync is initialized."""
        return self._initialized

