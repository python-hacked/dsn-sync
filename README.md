# 🚀 dsn-sync

<div align="center">

![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
[![PyPI](https://img.shields.io/badge/pypi-published-brightgreen.svg)](https://pypi.org/project/dsn-sync/0.1.0/)

**Revolutionary Backend-Frontend Data Synchronization Without API Endpoints**

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Usage Examples](#-usage-examples) • [Advanced Features](#-advanced-features)

</div>

---

## 📖 Overview

**dsn-sync** is a groundbreaking Python package that enables seamless data synchronization between your backend and frontend **without requiring any API endpoints, REST APIs, WebSocket connections, Firebase, Celery, Redis, or Webhooks**.

Simply install the package, define your schemas, and watch as your frontend automatically syncs data in real-time through a secure, encrypted channel.

### ✨ Why dsn-sync?

- 🚫 **No API Endpoints** - Zero REST API or WebSocket setup required
- 🚫 **No Firebase** - Self-hosted solution, no vendor lock-in
- 🚫 **No Celery/Redis** - Built-in auto-tasks without external dependencies
- 🚫 **No Webhooks** - Direct encrypted communication
- ⚡ **Auto-Sync** - Frontend automatically creates tables and syncs data
- 🔑 **Key-Based** - Simple key-based data synchronization
- 🔐 **Secure** - Encrypted communication, dynamic endpoints
- 📦 **Easy Setup** - Install and start using in minutes
- 🔄 **Real-Time** - Automatic data synchronization
- 🎯 **Schema-Driven** - Define once, sync everywhere

---

## 🎯 Features

- ✅ **Zero API Configuration** - No need to create API endpoints
- ✅ **Automatic URL Generation** - Unique sync URL generated on installation
- ✅ **Schema Definition** - Define your data structure once
- ✅ **Auto Table Creation** - Frontend automatically creates matching tables
- ✅ **Key-Based Sync** - Simple and efficient data synchronization
- ✅ **Real-Time Updates** - Data changes reflect automatically
- ✅ **CRUD Operations** - Create, Read, Update, Delete data
- ✅ **Get All Data** - Fetch all records from a table
- ✅ **Get Single Data** - Fetch single record by ID/key
- ✅ **Auto Tasks** - Background tasks without Celery/Redis
- ✅ **Notifications** - Real-time notifications without Firebase/WebSocket
- ✅ **Chat System** - Chat functionality without WebSocket/API
- ✅ **Chart Data Flow** - Real-time data for charts and analytics
- ✅ **Lightweight** - Minimal dependencies, fast performance

---

## 📦 Installation

### Backend (Python)

Install from PyPI:

```bash
pip install dsn-sync
```

📦 **PyPI Package:** [https://pypi.org/project/dsn-sync/0.1.0/](https://pypi.org/project/dsn-sync/0.1.0/)

### Frontend (JavaScript)

```bash
npm install dsn-sync-client
```

---

## 🚀 Quick Start

### Backend Setup

```python
from dsn_sync import DSNSync

# Initialize dsn-sync
sync = DSNSync(port=3000)

# Start embedded server
sync.start()

# Get the unique sync URL (share this with frontend)
sync_url = sync.get_url()
print(f"Sync URL: {sync_url}")

# Get authentication token
token = sync.get_token()
print(f"Token: {token}")

# Define your schema
sync.define_table('users', {
    'key': 'user_id',
    'fields': ['name', 'email', 'cart', 'status']
})

# Sync data (READ operation - Backend → Frontend)
sync.sync('users', 'user_123', {
    'name': 'John Doe',
    'email': 'john@example.com',
    'cart': [],
    'status': 'active'
})
```

### Frontend Setup

```javascript
import { connectDSN } from 'dsn-sync-client';

// Connect using the URL and token from backend
const client = connectDSN('https://localhost:3000/sync/001', 'YOUR_TOKEN');

// Data automatically syncs to IndexedDB
// Tables are created automatically based on schema
```

---

## 📚 Usage Examples

### 1. Get All Data

**Backend:**
```python
# Sync multiple records
sync.sync('users', 'user_001', {'name': 'John', 'email': 'john@example.com'})
sync.sync('users', 'user_002', {'name': 'Jane', 'email': 'jane@example.com'})
sync.sync('users', 'user_003', {'name': 'Bob', 'email': 'bob@example.com'})
```

**Frontend:**
```javascript
// Get all users
const allUsers = await client.getAll('users');
console.log(allUsers);
// Output: {
//   'user_001': {name: 'John', email: 'john@example.com'},
//   'user_002': {name: 'Jane', email: 'jane@example.com'},
//   'user_003': {name: 'Bob', email: 'bob@example.com'}
// }
```

### 2. Get Single Data by ID/Key

**Frontend:**
```javascript
// Get single user by ID
const user = await client.get('users', 'user_001');
console.log(user);
// Output: {name: 'John', email: 'john@example.com'}
```

### 3. Create Data (WRITE - Frontend → Backend)

**Backend:**
```python
# Register event handler for create
@sync.on_create('users')
def handle_user_create(data):
    # data contains: {'user_id': 'user_004', 'name': 'Alice', ...}
    print(f"New user created: {data['name']}")
    
    # Save to your database
    # db.save_user(data)
    
    # Update RAM (automatic)
    # sync.sync('users', data['user_id'], data)
    
    return True
```

**Frontend:**
```javascript
// Create new user
await client.create('users', 'user_004', {
    name: 'Alice',
    email: 'alice@example.com',
    cart: [],
    status: 'active'
});
// This triggers @sync.on_create('users') in backend
```

### 4. Update Data

**Backend:**
```python
@sync.on_update('users')
def handle_user_update(data):
    # data contains updated fields
    print(f"User updated: {data}")
    
    # Update your database
    # db.update_user(data['user_id'], data)
    
    return True
```

**Frontend:**
```javascript
// Update user
await client.update('users', 'user_001', {
    name: 'John Updated',
    status: 'inactive'
});
// This triggers @sync.on_update('users') in backend
```

### 5. Delete Data

**Backend:**
```python
@sync.on_delete('users')
def handle_user_delete(data):
    # data contains: {'user_id': 'user_001'}
    print(f"User deleted: {data['user_id']}")
    
    # Delete from your database
    # db.delete_user(data['user_id'])
    
    return True
```

**Frontend:**
```javascript
// Delete user
await client.delete('users', 'user_001');
// This triggers @sync.on_delete('users') in backend
```

---

## 🔄 Complete Data Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    TWO-WAY DATA FLOW                                 │
└─────────────────────────────────────────────────────────────────────┘

BACKEND → FRONTEND (READ)
─────────────────────────
Backend: sync('users', 'user_123', {...})
    ↓
Encrypt Data
    ↓
Embedded Server
    ↓
Frontend: Receives & Decrypts
    ↓
Store in IndexedDB
    ↓
UI Updates Automatically

FRONTEND → BACKEND (WRITE)
───────────────────────────
Frontend: client.create('users', 'user_123', {...})
    ↓
Encrypt & Sign
    ↓
Send to Backend
    ↓
Backend: Decrypt & Validate
    ↓
Trigger @sync.on_create()
    ↓
Save to Database + RAM
    ↓
Response to Frontend
```

---

## 🎯 Advanced Features

### 1. Auto Tasks (Without Celery/Redis)

**Backend:**
```python
import time
from threading import Thread

# Auto task example - runs in background
def auto_task():
    while True:
        # Your background task logic
        print("Auto task running...")
        
        # Sync data automatically
        sync.sync('tasks', 'task_001', {
            'status': 'running',
            'timestamp': time.time()
        })
        
        time.sleep(60)  # Run every minute

# Start auto task
task_thread = Thread(target=auto_task, daemon=True)
task_thread.start()

# No Celery, No Redis needed!
```

### 2. Notifications (Without Firebase/WebSocket)

**Backend:**
```python
# Define notifications table
sync.define_table('notifications', {
    'key': 'notification_id',
    'fields': ['user_id', 'message', 'type', 'read', 'timestamp']
})

# Send notification
sync.sync('notifications', 'notif_001', {
    'user_id': 'user_123',
    'message': 'You have a new message',
    'type': 'info',
    'read': False,
    'timestamp': time.time()
})
```

**Frontend:**
```javascript
// Listen for notifications
client.onDataChange('notifications', (notifications) => {
    const unread = Object.values(notifications).filter(n => !n.read);
    showNotificationBadge(unread.length);
});

// Mark as read
await client.update('notifications', 'notif_001', {read: true});
```

### 3. Chat System (Without WebSocket/API)

**Backend:**
```python
# Define messages table
sync.define_table('messages', {
    'key': 'message_id',
    'fields': ['from_user', 'to_user', 'message', 'timestamp', 'read']
})

@sync.on_create('messages')
def handle_new_message(data):
    # data contains new message
    print(f"New message: {data['message']}")
    
    # Save to database
    # db.save_message(data)
    
    # Notify recipient
    sync.sync('notifications', f"notif_{data['message_id']}", {
        'user_id': data['to_user'],
        'message': f"New message from {data['from_user']}",
        'type': 'message',
        'read': False,
        'timestamp': time.time()
    })
    
    return True
```

**Frontend:**
```javascript
// Send message
await client.create('messages', `msg_${Date.now()}`, {
    from_user: 'user_123',
    to_user: 'user_456',
    message: 'Hello!',
    timestamp: Date.now(),
    read: false
});

// Get all messages
const messages = await client.getAll('messages');

// Get messages for specific user
const userMessages = Object.values(messages).filter(
    msg => msg.to_user === 'user_123' || msg.from_user === 'user_123'
);
```

### 4. Chart Data Flow (Real-time Analytics)

**Backend:**
```python
# Define analytics table
sync.define_table('analytics', {
    'key': 'record_id',
    'fields': ['metric', 'value', 'timestamp', 'category']
})

# Auto-update chart data
def update_chart_data():
    while True:
        # Collect metrics
        metrics = {
            'users_online': get_online_users_count(),
            'sales_today': get_sales_today(),
            'page_views': get_page_views()
        }
        
        for metric, value in metrics.items():
            sync.sync('analytics', f"{metric}_{int(time.time())}", {
                'metric': metric,
                'value': value,
                'timestamp': time.time(),
                'category': 'realtime'
            })
        
        time.sleep(5)  # Update every 5 seconds

# Start chart data updates
chart_thread = Thread(target=update_chart_data, daemon=True)
chart_thread.start()
```

**Frontend:**
```javascript
// Get chart data
const chartData = await client.getAll('analytics');

// Filter by metric
const salesData = Object.values(chartData)
    .filter(d => d.metric === 'sales_today')
    .sort((a, b) => a.timestamp - b.timestamp);

// Update chart
updateChart(salesData);

// Real-time updates
client.onDataChange('analytics', (data) => {
    const salesData = Object.values(data)
        .filter(d => d.metric === 'sales_today')
        .sort((a, b) => a.timestamp - b.timestamp);
    updateChart(salesData);
});
```

---

## 🔧 Complete Example: E-commerce Application

### Backend

```python
from dsn_sync import DSNSync
import time
from threading import Thread

sync = DSNSync(port=3000)
sync.start()

url = sync.get_url()
token = sync.get_token()
print(f"URL: {url}")
print(f"Token: {token}")

# Define schemas
sync.define_table('products', {
    'key': 'product_id',
    'fields': ['name', 'price', 'description', 'image', 'stock']
})

sync.define_table('cart', {
    'key': 'user_id',
    'fields': ['items', 'total']
})

sync.define_table('orders', {
    'key': 'order_id',
    'fields': ['user_id', 'items', 'total', 'status', 'timestamp']
})

# Event handlers
@sync.on_create('cart')
def handle_cart_update(data):
    print(f"Cart updated for user: {data['user_id']}")
    # Save to database
    return True

@sync.on_create('orders')
def handle_order_create(data):
    print(f"New order: {data['order_id']}")
    # Process order
    # Update inventory
    return True

# Sync products
sync.sync('products', 'prod_001', {
    'name': 'Laptop',
    'price': 999.99,
    'description': 'High-performance laptop',
    'image': 'laptop.jpg',
    'stock': 50
})

# Auto task - update stock
def update_stock():
    while True:
        # Check and update stock
        sync.sync('products', 'prod_001', {
            'stock': get_current_stock('prod_001')
        })
        time.sleep(300)  # Every 5 minutes

Thread(target=update_stock, daemon=True).start()
```

### Frontend

```javascript
import { connectDSN } from 'dsn-sync-client';

const client = connectDSN('YOUR_URL', 'YOUR_TOKEN');

// Get all products
const products = await client.getAll('products');

// Get single product
const laptop = await client.get('products', 'prod_001');

// Add to cart
await client.create('cart', 'user_123', {
    items: ['prod_001', 'prod_002'],
    total: 1499.98
});

// Get cart
const cart = await client.get('cart', 'user_123');

// Place order
await client.create('orders', `order_${Date.now()}`, {
    user_id: 'user_123',
    items: cart.items,
    total: cart.total,
    status: 'pending',
    timestamp: Date.now()
});

// Real-time updates
client.onDataChange('products', (products) => {
    updateProductList(products);
});

client.onDataChange('orders', (orders) => {
    updateOrderStatus(orders);
});
```

---

## 📊 API Reference

### Backend (Python)

#### `DSNSync(port=3000, db_connection_string=None)`
Initialize dsn-sync instance.

#### `get_url() -> str`
Get connection URL for frontend.

#### `get_token() -> str`
Get authentication token.

#### `start() -> bool`
Start embedded server.

#### `stop() -> bool`
Stop embedded server.

#### `define_table(table_name: str, schema: dict) -> bool`
Define table schema.

#### `sync(table_name: str, key: str, data: dict) -> bool`
Sync data to frontend (READ operation).

#### `on_create(table_name: str)`
Decorator for create event handler.

#### `on_update(table_name: str)`
Decorator for update event handler.

#### `on_delete(table_name: str)`
Decorator for delete event handler.

### Frontend (JavaScript)

#### `connectDSN(url: string, token: string) -> Client`
Connect to dsn-sync server.

#### `client.getAll(table_name: string) -> Promise<Object>`
Get all data from table.

#### `client.get(table_name: string, key: string) -> Promise<Object>`
Get single record by key.

#### `client.create(table_name: string, key: string, data: Object) -> Promise<boolean>`
Create new record.

#### `client.update(table_name: string, key: string, data: Object) -> Promise<boolean>`
Update existing record.

#### `client.delete(table_name: string, key: string) -> Promise<boolean>`
Delete record.

#### `client.onDataChange(table_name: string, callback: Function) -> void`
Listen for data changes.

---

## 🛠️ Requirements

- Python 3.7+
- cryptography>=41.0.0
- Node.js 14+ (for frontend package)

---

## 🔐 Security Features

- ✅ Encrypted communication (HTTPS)
- ✅ Dynamic endpoint rotation (every 100 requests)
- ✅ Secure key management (never in URLs)
- ✅ Token-based authentication
- ✅ Signature validation

---

## 📝 License

This project is licensed under the MIT License.

---

## 👤 Author

**Satish Choudhary**

- Email: satishchoudhary394@gmail.com
- GitHub: [@python-hacked](https://github.com/python-hacked)

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/python-hacked/dsn-sync/issues).

---

## ⭐ Show Your Support

Give a ⭐️ if this project helped you!

---

<div align="center">

**Made with ❤️ by Satish Choudhary**

[⬆ Back to Top](#-dsn-sync)

</div>
