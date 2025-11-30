"""In-memory data registry."""

from typing import Dict, Any, Optional
import threading


class MemoryStore:
    """Thread-safe in-memory data storage."""
    
    def __init__(self):
        """Initialize memory store."""
        self._data: Dict[str, Dict[str, Any]] = {}  # {table_name: {key: data}}
        self._lock = threading.Lock()
    
    def store_data(self, table_name: str, key: str, data: Dict[str, Any]) -> None:
        """Store data in memory."""
        with self._lock:
            if table_name not in self._data:
                self._data[table_name] = {}
            self._data[table_name][key] = data
    
    def get_data(self, table_name: str, key: Optional[str] = None) -> Any:
        """Retrieve data from memory."""
        with self._lock:
            if table_name not in self._data:
                return None if key else {}
            
            if key:
                return self._data[table_name].get(key)
            return self._data[table_name].copy()
    
    def get_all_tables(self) -> Dict[str, Dict[str, Any]]:
        """Get all data from all tables."""
        with self._lock:
            return {table: data.copy() for table, data in self._data.items()}
    
    def update_data(self, table_name: str, key: str, data: Dict[str, Any]) -> bool:
        """Update existing data."""
        with self._lock:
            if table_name in self._data and key in self._data[table_name]:
                self._data[table_name][key].update(data)
                return True
            return False
    
    def delete_data(self, table_name: str, key: str) -> bool:
        """Delete data from memory."""
        with self._lock:
            if table_name in self._data and key in self._data[table_name]:
                del self._data[table_name][key]
                return True
            return False
    
    def clear_data(self, table_name: Optional[str] = None) -> None:
        """Clear data from memory."""
        with self._lock:
            if table_name:
                if table_name in self._data:
                    del self._data[table_name]
            else:
                self._data.clear()
    
    def load_from_dict(self, data: Dict[str, Dict[str, Any]]) -> None:
        """Load data from dictionary (for server restart)."""
        with self._lock:
            self._data = {table: data.copy() for table, data in data.items()}

