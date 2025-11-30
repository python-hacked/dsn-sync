"""Receive and process data from frontend (WRITE operations)."""

from typing import Dict, Any, Callable, Optional
from functools import wraps


class Receiver:
    """Handles incoming data from frontend."""
    
    def __init__(self):
        """Initialize receiver."""
        self._event_handlers: Dict[str, Dict[str, Callable]] = {
            "create": {},
            "update": {},
            "delete": {}
        }
    
    def on_create(self, table_name: str):
        """Decorator for create event handler."""
        def decorator(func: Callable):
            self._event_handlers["create"][table_name] = func
            return func
        return decorator
    
    def on_update(self, table_name: str):
        """Decorator for update event handler."""
        def decorator(func: Callable):
            self._event_handlers["update"][table_name] = func
            return func
        return decorator
    
    def on_delete(self, table_name: str):
        """Decorator for delete event handler."""
        def decorator(func: Callable):
            self._event_handlers["delete"][table_name] = func
            return func
        return decorator
    
    def process_incoming(self, operation: str, table_name: str, key: str, data: Dict[str, Any]) -> bool:
        """Process incoming data packet."""
        operation = operation.lower()
        
        if operation not in self._event_handlers:
            return False
        
        if table_name not in self._event_handlers[operation]:
            return False
        
        handler = self._event_handlers[operation][table_name]
        
        try:
            # Call user's event handler
            result = handler(data)
            return result is not False
        except Exception as e:
            # Log error in production
            return False
    
    def has_handler(self, operation: str, table_name: str) -> bool:
        """Check if handler exists for operation."""
        return table_name in self._event_handlers.get(operation.lower(), {})

