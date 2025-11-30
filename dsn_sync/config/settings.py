"""Package configuration settings."""

# Server Configuration
DEFAULT_PORT = 3000
SERVER_HOST = "0.0.0.0"

# Sync Key Configuration
SYNC_KEY_FIELD_NAME = "dsn_sync_key"

# Endpoint Rotation
ENDPOINT_ROTATION_COUNT = 100  # Rotate endpoint after 100 requests

# Encryption
ENCRYPTION_ALGORITHM = "AES-256"
KEY_SIZE = 32  # 256 bits

# Token Configuration
TOKEN_EXPIRY_HOURS = 24
TOKEN_SECRET_LENGTH = 32

# Database Configuration
DB_CONNECTION_TIMEOUT = 30

# File Paths
DATA_DIR = ".dsn_sync"
KEYS_FILE = "keys.db"
SCHEMAS_FILE = "schemas.json"

