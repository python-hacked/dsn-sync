"""Schema definition and management."""

from typing import Dict, Any, Optional
from ..config.settings import SYNC_KEY_FIELD_NAME
from ..database.schema_updater import SchemaUpdater


class SchemaManager:
    """Manages table schemas and sync key fields."""
    
    def __init__(self, schema_updater: SchemaUpdater):
        """Initialize schema manager."""
        self.schema_updater = schema_updater
        self._schemas: Dict[str, Dict[str, Any]] = {}  # {table_name: schema}
    
    def define_table(self, table_name: str, schema: Dict[str, Any]) -> bool:
        """Define table schema."""
        if not isinstance(schema, dict):
            raise ValueError("Schema must be a dictionary")
        
        if "key" not in schema:
            raise ValueError("Schema must contain 'key' field")
        
        if "fields" not in schema:
            raise ValueError("Schema must contain 'fields' list")
        
        # Validate schema structure
        self.validate_schema(schema)
        
        # Store schema
        self._schemas[table_name] = schema.copy()
        
        # Add sync key field to database
        self.schema_updater.add_sync_key_column(table_name)
        
        return True
    
    def validate_schema(self, schema: Dict[str, Any]) -> bool:
        """Validate schema structure."""
        if not isinstance(schema, dict):
            raise ValueError("Schema must be a dictionary")
        
        if "key" not in schema:
            raise ValueError("Schema must have 'key' field")
        
        if "fields" not in schema or not isinstance(schema["fields"], list):
            raise ValueError("Schema must have 'fields' as a list")
        
        return True
    
    def get_schema(self, table_name: str) -> Optional[Dict[str, Any]]:
        """Get schema for table."""
        return self._schemas.get(table_name)
    
    def get_all_schemas(self) -> Dict[str, Dict[str, Any]]:
        """Get all schemas."""
        return self._schemas.copy()
    
    def add_sync_key_field(self, table_name: str) -> bool:
        """Add sync key field to database table."""
        return self.schema_updater.add_sync_key_column(table_name)
    
    def table_exists(self, table_name: str) -> bool:
        """Check if table schema is defined."""
        return table_name in self._schemas

