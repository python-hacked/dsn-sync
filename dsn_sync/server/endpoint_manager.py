"""Dynamic endpoint rotation management."""

import threading
from ..config.settings import ENDPOINT_ROTATION_COUNT


class EndpointManager:
    """Manages dynamic endpoint rotation."""
    
    def __init__(self):
        """Initialize endpoint manager."""
        self._current_endpoint = "001"
        self._request_count = 0
        self._lock = threading.Lock()
    
    def get_current_endpoint(self) -> str:
        """Get current endpoint number."""
        with self._lock:
            return self._current_endpoint
    
    def increment_counter(self) -> str:
        """Increment request counter and rotate if needed."""
        with self._lock:
            self._request_count += 1
            
            # Check if rotation needed
            if self._request_count >= ENDPOINT_ROTATION_COUNT:
                self.rotate_endpoint()
                self._request_count = 0
            
            return self._current_endpoint
    
    def rotate_endpoint(self) -> str:
        """Rotate to next endpoint."""
        with self._lock:
            current_num = int(self._current_endpoint)
            next_num = current_num + 1
            self._current_endpoint = f"{next_num:03d}"  # Format as 001, 002, etc.
            return self._current_endpoint
    
    def validate_endpoint(self, endpoint: str) -> bool:
        """Validate endpoint number format."""
        try:
            num = int(endpoint)
            return 1 <= num <= 999
        except ValueError:
            return False
    
    def get_request_count(self) -> int:
        """Get current request count."""
        with self._lock:
            return self._request_count
    
    def reset_counter(self) -> None:
        """Reset request counter."""
        with self._lock:
            self._request_count = 0

