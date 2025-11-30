# 🏗️ dsn-sync Package Architecture

## 📊 Overall System Structure

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         dsn-sync PACKAGE                                │
│                                                                         │
│  ┌──────────────────────┐         ┌──────────────────────┐            │
│  │   BACKEND PACKAGE    │         │  FRONTEND PACKAGE    │            │
│  │   (dsn-sync)         │         │  (dsn-sync-client)   │            │
│  └──────┬───────────────┘         └──────┬───────────────┘            │
│         │                                  │                            │
│         │                                  │                            │
│         └──────────┬───────────────────────┘                            │
│                    │                                                    │
│            ┌───────▼────────┐                                           │
│            │ EMBEDDED SERVER │                                           │
│            │ (HTTPS)         │                                           │
│            │ In-Memory Data  │                                           │
│            │ No Static Files │                                           │
│            └─────────────────┘                                           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Core Principles

1. **NO Static Files** - Everything in-memory or database
2. **NO Frameworks** - Package creates its own embedded server
3. **NO URL Keys** - Keys stored securely, never in URLs
4. **Dynamic Endpoints** - Auto-rotate every 100 requests
5. **Package Sync Key** - Separate from database primary key
6. **Encrypted Communication** - All data encrypted
7. **Two-Way Sync** - READ (Backend→Frontend) & WRITE (Frontend→Backend)

---

## 🔧 Backend Package Structure (dsn-sync)

```
dsn_sync/
│
├── __init__.py                    # Package initialization
│   └── Exports: DSNSync class
│
├── server/
│   ├── __init__.py
│   ├── embedded_server.py         # Lightweight HTTPS server
│   │   ├── start_server()         # Start embedded server
│   │   ├── stop_server()           # Stop server
│   │   ├── get_port()              # Get server port
│   │   └── handle_request()        # Handle incoming requests
│   │
│   └── endpoint_manager.py         # Dynamic endpoint rotation
│       ├── get_current_endpoint()  # Get current endpoint (001/002/003...)
│       ├── rotate_endpoint()       # Rotate after 100 requests
│       ├── increment_counter()     # Count requests
│       └── validate_endpoint()     # Validate endpoint number
│
├── core/
│   ├── __init__.py
│   ├── sync_manager.py            # Main sync management
│   │   ├── init_sync()            # Initialize sync system
│   │   ├── get_connection_url()   # Get connection URL (with endpoint)
│   │   └── generate_token()       # Generate authentication token
│   │
│   ├── schema_manager.py          # Schema definition & management
│   │   ├── define_table()         # Define table schema
│   │   ├── add_sync_key_field()   # Add package sync key to DB schema
│   │   ├── validate_schema()      # Validate schema structure
│   │   └── get_schema()           # Get schema by table name
│   │
│   ├── data_manager.py            # Data synchronization (READ)
│   │   ├── sync()                 # Sync data to frontend
│   │   ├── get_data()             # Get data from memory/DB
│   │   └── update_memory()        # Update in-memory registry
│   │
│   ├── receiver.py                # Receive data from frontend (WRITE)
│   │   ├── on_create()            # Decorator for create events
│   │   ├── on_update()            # Decorator for update events
│   │   ├── on_delete()            # Decorator for delete events
│   │   └── process_incoming()     # Process incoming data packets
│   │
│   └── memory_store.py            # In-memory data registry
│       ├── store_data()           # Store data in memory
│       ├── get_data()             # Retrieve from memory
│       ├── update_data()          # Update memory
│       └── clear_data()           # Clear memory
│
├── security/
│   ├── __init__.py
│   ├── key_manager.py             # Secure key management
│   │   ├── generate_key()         # Generate cryptographic key
│   │   ├── store_key()            # Store key in database (encrypted)
│   │   ├── get_key()              # Retrieve key from database
│   │   └── rotate_key()           # Rotate key if compromised
│   │
│   ├── encryption.py              # Encryption/decryption
│   │   ├── encrypt_data()         # Encrypt data before transmission
│   │   ├── decrypt_data()         # Decrypt received data
│   │   └── generate_signature()   # Generate request signature
│   │
│   └── token_manager.py           # Authentication token
│       ├── generate_token()       # Generate auth token
│       ├── validate_token()       # Validate token
│       ├── get_endpoint_from_token() # Extract endpoint from token
│       └── update_token()          # Update token on endpoint rotation
│
├── database/
│   ├── __init__.py
│   ├── connector.py               # Direct database connection
│   │   ├── connect()              # Connect to database
│   │   ├── execute_query()        # Execute SQL queries
│   │   └── add_sync_key_column()  # Add sync key field to table
│   │
│   └── schema_updater.py          # Database schema management
│       ├── add_column()           # Add sync key column
│       ├── check_column_exists()   # Check if column exists
│       └── update_schema()         # Update table schema
│
└── config/
    ├── __init__.py
    └── settings.py                # Package configuration
        ├── DEFAULT_PORT           # Default server port
        ├── SYNC_KEY_FIELD_NAME    # Default: 'dsn_sync_key'
        ├── ENDPOINT_ROTATION_COUNT # Default: 100 requests
        ├── ENCRYPTION_ALGORITHM   # AES-256
        └── TOKEN_EXPIRY           # Token expiry time
```

---

## 🎨 Frontend Package Structure (dsn-sync-client)

```
dsn_sync_client/
│
├── __init__.js                    # Package initialization
│   └── Exports: connectDSN function
│
├── core/
│   ├── __init__.js
│   ├── client.js                  # Main client class
│   │   ├── connect()              # Connect to embedded server
│   │   ├── disconnect()           # Disconnect
│   │   ├── isConnected()          # Check connection status
│   │   └── reconnect()            # Reconnect on failure
│   │
│   ├── connection_manager.js      # Connection management
│   │   ├── establish_connection() # Establish HTTPS connection
│   │   ├── handle_handshake()     # Initial key exchange
│   │   └── update_endpoint()      # Update endpoint on rotation
│   │
│   ├── reader.js                  # READ operations (Backend→Frontend)
│   │   ├── fetch_data()           # Fetch data from server
│   │   ├── parse_response()       # Parse encrypted response
│   │   └── sync_to_indexeddb()    # Sync to IndexedDB
│   │
│   └── writer.js                  # WRITE operations (Frontend→Backend)
│       ├── create()               # Create new data
│       ├── update()               # Update existing data
│       ├── delete()               # Delete data
│       └── send_packet()          # Send encrypted packet
│
├── security/
│   ├── __init__.js
│   ├── key_manager.js              # Frontend key management
│   │   ├── store_key()            # Store key securely (encrypted)
│   │   ├── get_key()              # Retrieve stored key
│   │   └── update_key()           # Update key if rotated
│   │
│   ├── encryption.js              # Client-side encryption
│   │   ├── encrypt_payload()      # Encrypt data before sending
│   │   ├── decrypt_response()     # Decrypt received data
│   │   └── generate_signature()   # Generate request signature
│   │
│   └── token_manager.js           # Token management
│       ├── store_token()          # Store auth token
│       ├── get_token()            # Get current token
│       ├── update_token()         # Update token on endpoint change
│       └── extract_endpoint()     # Extract endpoint from token
│
├── storage/
│   ├── __init__.js
│   ├── indexeddb_manager.js       # IndexedDB operations
│   │   ├── init_db()              # Initialize IndexedDB
│   │   ├── create_table()         # Create table from schema
│   │   ├── insert_data()          # Insert data
│   │   ├── update_data()          # Update data
│   │   ├── delete_data()          # Delete data
│   │   └── get_data()             # Retrieve data
│   │
│   └── schema_handler.js          # Schema management
│       ├── apply_schema()        # Apply schema to IndexedDB
│       └── validate_schema()      # Validate schema
│
└── config/
    ├── __init__.js
    └── settings.js                # Client configuration
        ├── POLL_INTERVAL          # Data polling interval
        ├── MAX_RETRIES            # Max retry attempts
        └── CONNECTION_TIMEOUT    # Connection timeout
```

---

## 🔄 Two-Way Data Flow Architecture

### Backend → Frontend (READ Operations)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    READ FLOW (Backend → Frontend)                   │
└─────────────────────────────────────────────────────────────────────┘

1. INITIALIZATION
   ┌─────────────┐
   │ pip install │
   │ dsn-sync    │
   └──────┬──────┘
          │
          ▼
   ┌─────────────────┐
   │ DSNSync()       │
   │ Initialize      │
   └──────┬──────────┘
          │
          ▼
   ┌─────────────────┐
   │ Start Embedded  │
   │ Server (HTTPS)  │
   └──────┬──────────┘
          │
          ▼
   ┌─────────────────┐      ┌──────────────────┐
   │ Generate Key    │─────▶│ Store in DB      │
   │ & Token         │      │ (Encrypted)      │
   └─────────────────┘      └──────────────────┘
          │
          ▼
   ┌─────────────────┐
   │ Load Data from  │ ◀─── Server Restart: Restore RAM
   │ Database to RAM │      (Read all data, populate memory)
   └──────┬──────────┘
          │
          ▼
   ┌─────────────────┐
   │ Endpoint: 001   │
   │ URL Generated   │
   └─────────────────┘

2. SCHEMA DEFINITION
   ┌─────────────────┐
   │ define_table()  │
   │ ('users', {...})│
   └──────┬──────────┘
          │
          ▼
   ┌─────────────────┐
   │ Add Sync Key    │
   │ Field to DB     │
   │ (dsn_sync_key)  │
   └──────┬──────────┘
          │
          ▼
   ┌─────────────────┐
   │ Schema Stored  │
   │ in Memory      │
   └─────────────────┘

3. DATA SYNC (READ)
   ┌─────────────────┐
   │ sync()          │
   │ (table, key,    │
   │  data)          │
   └──────┬──────────┘
          │
          ▼
   ┌─────────────────┐
   │ Store in Memory │
   │ Registry        │
   └──────┬──────────┘
          │
          ▼
   ┌─────────────────┐
   │ Frontend        │
   │ Requests Data   │
   │ (with token)    │
   └──────┬──────────┘
          │
          ▼
   ┌─────────────────┐
   │ Validate Token  │
   │ & Endpoint      │
   └──────┬──────────┘
          │
          ▼
   ┌─────────────────┐
   │ Get from Memory │
   │ Encrypt Data    │
   └──────┬──────────┘
          │
          ▼
   ┌─────────────────┐      ┌──────────────────┐
   │ Send Encrypted  │─────▶│ Frontend         │
   │ Data            │      │ Decrypts & Stores│
   └─────────────────┘      └──────────────────┘
```

### Frontend → Backend (WRITE Operations)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    WRITE FLOW (Frontend → Backend)                   │
└─────────────────────────────────────────────────────────────────────┘

1. USER ACTION
   ┌─────────────────┐
   │ User Fills Form │
   │ & Submits       │
   └──────┬──────────┘
          │
          ▼
   ┌─────────────────┐
   │ client.create() │
   │ (table, key,    │
   │  data)          │
   └──────┬──────────┘
          │
          ▼
   ┌─────────────────┐
   │ Encrypt Data    │
   │ with Stored Key │
   └──────┬──────────┘
          │
          ▼
   ┌─────────────────┐
   │ Generate        │
   │ Signature       │
   └──────┬──────────┘
          │
          ▼
   ┌─────────────────┐
   │ Send Packet     │
   │ (Encrypted +    │
   │  Signature)     │
   └──────┬──────────┘

2. BACKEND RECEIVES
   ┌─────────────────┐
   │ Embedded Server │
   │ Receives Packet │
   └──────┬──────────┘
          │
          ▼
   ┌─────────────────┐
   │ Validate        │
   │ Signature       │
   └──────┬──────────┘
          │
          ▼
   ┌─────────────────┐
   │ Decrypt with    │
   │ Stored Key      │
   └──────┬──────────┘
          │
          ▼
   ┌─────────────────┐
   │ Validate Data   │
   │ Structure       │
   └──────┬──────────┘
          │
          ▼
   ┌─────────────────┐      ┌──────────────────┐
   │ Trigger Event   │─────▶│ @app.on_create() │
   │ Handler         │      │ User Function     │
   └─────────────────┘      └──────────────────┘
          │
          ▼
   ┌─────────────────┐
   │ Save to Database│ ◀─── Simultaneous Save
   │ AND             │
   │ Update RAM      │ ◀─── Both at Same Time
   └─────────────────┘
   (Data persisted in both places immediately)
```

---

## 💾 Data Persistence & Server Restart

### WRITE Operation: Dual Storage

**When data arrives (WRITE operation):**

1. **Frontend sends encrypted data packet**
2. **Backend decrypts and validates**
3. **Trigger event handler** (`@app.on_create()`)
4. **Simultaneous Storage:**
   - ✅ **Save to Database** - Data immediately written to database
   - ✅ **Update RAM** - Data simultaneously stored in memory registry
   - Both operations happen at the same time
   - No delay between database and RAM storage

**Flow:**
```
WRITE Request → Decrypt → Validate → @app.on_create()
                                          │
                                          ▼
                          ┌───────────────────────────┐
                          │   Simultaneous Save       │
                          │                           │
                          │  ┌──────────┐ ┌─────────┐│
                          │  │ Database │ │   RAM   ││
                          │  │   Save   │ │  Update ││
                          │  └──────────┘ └─────────┘│
                          │      ✅           ✅      │
                          └───────────────────────────┘
```

### Server Restart: RAM Restoration

**When server restarts:**

1. **Package Initialization**
   - Embedded server starts
   - Package connects to database

2. **Automatic RAM Restoration**
   - Package reads all data from database
   - Data loaded into RAM/memory registry
   - RAM is populated with complete dataset
   - No data loss - everything restored

3. **Ready State**
   - RAM fully populated
   - Server ready to serve requests
   - All data available in memory for fast access

**Flow:**
```
Server Restart → Package Init → Connect to Database
                                        │
                                        ▼
                          ┌───────────────────────────┐
                          │  Read All Data from DB   │
                          │  (All tables, all rows)  │
                          └────────────┬──────────────┘
                                       │
                                       ▼
                          ┌───────────────────────────┐
                          │   Populate RAM Registry   │
                          │   (In-Memory Store)       │
                          └────────────┬──────────────┘
                                       │
                                       ▼
                          ┌───────────────────────────┐
                          │   Server Ready             │
                          │   (RAM fully loaded)       │
                          └───────────────────────────┘
```

### Why This Approach?

1. **Dual Storage (WRITE)**
   - Database = Permanent storage (survives restarts)
   - RAM = Fast access (real-time performance)
   - Both updated simultaneously = Data consistency

2. **RAM Restoration (Restart)**
   - Fast access after restart
   - No need to query database for every request
   - Complete data available in memory
   - Optimal performance

3. **Data Safety**
   - Database ensures data persistence
   - RAM ensures fast access
   - Server restart doesn't lose data
   - Automatic recovery

---

## 🔑 Secure Key Management

### Key Generation & Storage

1. **Backend Key Generation**
   - Package generates unique cryptographic key on initialization
   - Key stored in database (encrypted)
   - Key never exposed in logs or URLs
   - Key can be rotated if compromised

2. **Frontend Key Distribution**
   - Initial connection: One-time secure handshake
   - Key transmitted over HTTPS (encrypted)
   - Frontend stores key in encrypted IndexedDB/localStorage
   - Key never sent in subsequent requests

3. **Key Usage (Never in URL)**
   - Key used for encryption/decryption
   - Key used to generate request signatures
   - Signature sent in headers (not the key)
   - Each request has unique signature (timestamp-based)

### Package Sync Key (Separate from Database Primary Key)

**Database Primary Key:**
- User's existing primary key (ID, UUID, etc.)
- Used for database operations
- Managed by user/database

**Package Sync Key (`dsn_sync_key`):**
- Separate field specified by package
- Used only for package communication
- Automatically added to database schema
- Package tells user what field name to use (default: `dsn_sync_key`)
- Independent from database primary key

**Example:**
```
Database Table: users
├── id (Primary Key - Integer/UUID) - For database
├── name (String)
├── email (String)
└── dsn_sync_key (String) - For package communication
```

---

## 🔄 Dynamic Endpoint Rotation

### How It Works

1. **Initial Endpoint**
   - Package generates endpoint `001` on installation
   - Endpoint included in authentication token
   - Token provided to frontend during handshake

2. **Request Counting**
   - Backend counts every incoming request
   - Counter stored in memory/database

3. **Auto-Rotation (Every 100 Requests)**
   - On 100th request: Endpoint rotates to `002`
   - Token automatically updated with new endpoint
   - Frontend receives updated token
   - Next 100 requests use endpoint `002`

4. **Concurrent Requests Handling**
   - If 100 requests arrive simultaneously:
     - First request: Rotates endpoint to `002`, updates token
     - Remaining 99 requests: Automatically use endpoint `002`
   - All requests processed with new endpoint

5. **Token Update**
   - Token contains current endpoint number
   - Frontend reads endpoint from token
   - No manual endpoint update needed
   - Automatic synchronization

**Flow:**
```
Request 1-99:   Endpoint 001
Request 100:    Endpoint rotates to 002 (token updated)
Request 101-199: Endpoint 002
Request 200:    Endpoint rotates to 003 (token updated)
...and so on
```

---

## 🔐 Security Architecture

### Authentication Token Structure

```
Token contains:
├── endpoint_number    # Current endpoint (001, 002, 003...)
├── timestamp          # Token creation time
├── signature          # Hash of key + endpoint + timestamp
└── encrypted_payload  # Additional encrypted data
```

### Request Flow with Token

1. **Frontend Request**
   - Reads endpoint from stored token
   - Generates signature (key + endpoint + timestamp + data)
   - Sends encrypted payload + signature
   - Endpoint number in token (not in URL)

2. **Backend Validation**
   - Validates token signature
   - Checks endpoint number matches current
   - Validates timestamp (prevents replay)
   - Processes request if valid

3. **Endpoint Rotation**
   - After 100 requests: Endpoint increments
   - New token generated with new endpoint
   - Token sent to frontend
   - Frontend updates stored token

---

## 📊 Component Interactions

```
┌──────────────┐                                    ┌──────────────┐
│   Frontend   │                                    │   Backend    │
│  (Browser)   │                                    │  (Python)    │
└──────┬───────┘                                    └──────┬───────┘
       │                                                   │
       │ 1. INITIAL CONNECTION                             │
       │ ---- (HTTPS Handshake) -----------------------> │
       │                                                   │
       │ <---- (Token with Endpoint 001 + Key) ---------- │
       │                                                   │
       │ 2. READ OPERATION                                 │
       │ ---- (Request with Token) ---------------------> │
       │                                                   │
       │ <---- (Encrypted Data) -------------------------- │
       │                                                   │
       │ 3. WRITE OPERATION                                │
       │ ---- (Encrypted Packet + Signature) -----------> │
       │                                                   │
       │                                                   │ ▶ [Validate]
       │                                                   │      │
       │                                                   │      ▼
       │                                                   │  [Decrypt]
       │                                                   │      │
       │                                                   │      ▼
       │                                                   │  [Trigger Event]
       │                                                   │  @app.on_create
       │                                                   │
       │ <---- (Encrypted Confirmation) ------------------ │
       │                                                   │
       │ 4. ENDPOINT ROTATION (After 100 requests)         │
       │ <---- (New Token with Endpoint 002) ------------- │
       │                                                   │
       │ 5. NEXT REQUESTS                                  │
       │ ---- (Request with Updated Token) --------------> │
       │                                                   │
```

---

## 🎯 Key Features

### 1. No Static Files
- ✅ All data in memory or database
- ✅ No file corruption risk
- ✅ No file deletion vulnerability
- ✅ Real-time data updates

### 2. Embedded Server
- ✅ Package creates its own server
- ✅ No framework dependency
- ✅ Minimal overhead
- ✅ Full control

### 3. Secure Key Management
- ✅ Keys never in URLs
- ✅ Encrypted storage
- ✅ One-time handshake
- ✅ Signature-based validation

### 4. Dynamic Endpoints
- ✅ Auto-rotation every 100 requests
- ✅ Automatic token update
- ✅ Concurrent request handling
- ✅ No manual configuration

### 5. Package Sync Key
- ✅ Separate from database primary key
- ✅ Package-specified field name
- ✅ Auto-added to schema
- ✅ Independent management

### 6. Two-Way Communication
- ✅ READ: Backend → Frontend (encrypted)
- ✅ WRITE: Frontend → Backend (encrypted packets)
- ✅ Event-driven processing
- ✅ Real-time synchronization

---

## 🚀 Why This Architecture is Superior

### vs Static Files
- ✅ No file vulnerabilities
- ✅ Real-time data
- ✅ Secure transmission
- ✅ Dynamic updates

### vs REST APIs
- ✅ No endpoint definition needed
- ✅ No URL-based keys
- ✅ Automatic encryption
- ✅ Built-in authentication

### vs WebSockets
- ✅ Standard HTTPS
- ✅ Better compatibility
- ✅ Simpler implementation
- ✅ No persistent connection

### vs Firebase
- ✅ Self-hosted
- ✅ No vendor lock-in
- ✅ Full control
- ✅ No usage limits

---

## 📝 Summary

**dsn-sync Architecture:**

- **Embedded Server**: Lightweight HTTPS server (no framework)
- **In-Memory Data**: No static files, everything in memory/database
- **Secure Keys**: Never in URLs, encrypted storage, signature validation
- **Dynamic Endpoints**: Auto-rotate every 100 requests
- **Package Sync Key**: Separate field for package communication
- **Two-Way Sync**: READ and WRITE operations
- **Encrypted Communication**: All data encrypted
- **Event-Driven**: Decorator-based event handlers

**Result:** A secure, fast, dynamic, framework-free solution that eliminates all vulnerabilities of traditional approaches.

---

## ✅ Architecture Guarantees

✅ No static files = No corruption/deletion/hacking risk
✅ No URL keys = Secure authentication
✅ Encrypted communication = Data protection
✅ In-memory operations = Real-time and fast
✅ Dynamic endpoints = Enhanced security
✅ Package sync key = Independent from DB primary key
✅ Embedded server = Self-contained solution
✅ Two-way sync = Complete data flow
✅ Event-driven = Flexible processing

**This is the future of backend-frontend communication.**
