"""Data synchronization manager (READ operations)."""

from typing import Dict, Any, Optional
from .memory_store import MemoryStore


class DataManager:
    """Manages data synchronization to frontend."""
    
    def __init__(self, memory_store: MemoryStore):
        """Initialize data manager."""
        self.memory_store = memory_store
    
    def sync(self, table_name: str, key: str, data: Dict[str, Any]) -> bool:
        """Sync data to frontend (store in memory for READ operations)."""
        try:
            self.memory_store.store_data(table_name, key, data)
            return True
        except Exception:
            return False
    
    def get_data(self, table_name: str, key: Optional[str] = None) -> Any:
        """Get data from memory or database."""
        # First try memory
        data = self.memory_store.get_data(table_name, key)
        if data is not None:
            return data
        
        # If not in memory, would fetch from database
        # This will be implemented based on user's database
        return None
    
    def update_memory(self, table_name: str, key: str, data: Dict[str, Any]) -> bool:
        """Update in-memory registry."""
        return self.memory_store.update_data(table_name, key, data)
    
    def get_all_data(self, table_name: str) -> Dict[str, Any]:
        """Get all data for a table."""
        return self.memory_store.get_data(table_name) or {}
    
    def delete_data(self, table_name: str, key: str) -> bool:
        """Delete data from memory."""
        return self.memory_store.delete_data(table_name, key)

