"""
dsn-sync - Backend-Frontend Data Synchronization Without API Endpoints
"""

__version__ = "0.1.0"
__author__ = "Satish Choudhary"
__email__ = "satishchoudhary394@gmail.com"

from .core.sync_manager import SyncManager
from .core.schema_manager import SchemaManager
from .core.data_manager import DataManager
from .core.receiver import Receiver
from .core.memory_store import MemoryStore
from .security.key_manager import KeyManager
from .security.encryption import EncryptionManager
from .security.token_manager import TokenManager
from .server.embedded_server import EmbeddedServer
from .server.endpoint_manager import EndpointManager
from .database.connector import DatabaseConnector
from .database.schema_updater import SchemaUpdater
from .config.settings import DEFAULT_PORT


class DSNSync:
    """
    Main class for dsn-sync package.
    
    Provides backend-frontend data synchronization without API endpoints.
    """
    
    def __init__(self, port: int = DEFAULT_PORT, db_connection_string: str = None):
        """
        Initialize dsn-sync.
        
        Args:
            port: Port for embedded server (default: 3000)
            db_connection_string: Database connection string (optional)
        """
        # Initialize components
        self.key_manager = KeyManager()
        self.endpoint_manager = EndpointManager()
        self.memory_store = MemoryStore()
        self.receiver = Receiver()
        
        # Database
        self.db_connector = DatabaseConnector(db_connection_string)
        self.schema_updater = SchemaUpdater(self.db_connector)
        
        # Core managers
        self.schema_manager = SchemaManager(self.schema_updater)
        self.data_manager = DataManager(self.memory_store)
        self.sync_manager = SyncManager(self.key_manager, self.endpoint_manager)
        
        # Security
        self.encryption_manager: EncryptionManager = None
        
        # Server
        self.server = EmbeddedServer(port=port)
        self.port = port
        
        # Initialize sync system
        self.sync_manager.init_sync()
        
        # Setup encryption
        key = self.key_manager.get_key()
        if key:
            self.encryption_manager = EncryptionManager(key)
            self.token_manager = TokenManager(key)
    
    def get_url(self) -> str:
        """
        Get connection URL for frontend.
        
        Returns:
            Connection URL with current endpoint
        """
        return self.sync_manager.get_connection_url(port=self.port)
    
    def define_table(self, table_name: str, schema: dict) -> bool:
        """
        Define table schema.
        
        Args:
            table_name: Name of the table
            schema: Schema dictionary with 'key' and 'fields'
        
        Returns:
            True if successful
        """
        return self.schema_manager.define_table(table_name, schema)
    
    def sync(self, table_name: str, key: str, data: dict) -> bool:
        """
        Sync data to frontend (READ operation).
        
        Args:
            table_name: Name of the table
            key: Unique key for the data
            data: Data dictionary to sync
        
        Returns:
            True if successful
        """
        return self.data_manager.sync(table_name, key, data)
    
    def on_create(self, table_name: str):
        """
        Decorator for create event handler.
        
        Args:
            table_name: Name of the table
        
        Example:
            @sync.on_create('users')
            def handle_user_create(data):
                # Process data
                return True
        """
        return self.receiver.on_create(table_name)
    
    def on_update(self, table_name: str):
        """
        Decorator for update event handler.
        
        Args:
            table_name: Name of the table
        """
        return self.receiver.on_update(table_name)
    
    def on_delete(self, table_name: str):
        """
        Decorator for delete event handler.
        
        Args:
            table_name: Name of the table
        """
        return self.receiver.on_delete(table_name)
    
    def start(self) -> bool:
        """
        Start embedded server.
        
        Returns:
            True if server started successfully
        """
        return self.server.start_server()
    
    def stop(self) -> bool:
        """
        Stop embedded server.
        
        Returns:
            True if server stopped successfully
        """
        return self.server.stop_server()
    
    def get_token(self) -> str:
        """
        Get authentication token for frontend.
        
        Returns:
            Authentication token string
        """
        return self.sync_manager.generate_token() or ""
    
    def connect_database(self, connection_string: str) -> bool:
        """
        Connect to database.
        
        Args:
            connection_string: Database connection string
        
        Returns:
            True if connected successfully
        """
        return self.db_connector.connect(connection_string)


# Export main class
__all__ = ['DSNSync']
