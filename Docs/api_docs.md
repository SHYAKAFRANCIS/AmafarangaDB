# Transaction API Server - Setup Guide

## Overview
A Python-based REST API server for managing financial transactions with efficient data structures (hash maps and binary search) for optimal performance.

## Prerequisites
- Python 3.x installed on your system
- Basic knowledge of command line/terminal
- curl or Postman for API testing (optional)

---

## Project Structure

Your project should be organized as follows:

```
project/
├── src/
│   ├── server.py          # Main server file
│   ├── auth.py            # ✓ Already created
│   └── indexer.py         # ✓ Already created
└── api_ready_transactions.json   # Need to create
```

---

## Setup Steps

### Step 1: Create the Data File

Create `api_ready_transactions.json` in the **parent directory** (one level up from `src/`).

**Option A - Start with an empty database (recommended):**
```json
[]
```

**Option B - Start with sample data:**
```json
[
    {
        "id": 0,
        "transaction_type": "payment",
        "amount": 100.50,
        "sender": "Alice",
        "receiver": "Bob",
        "timestamp": "2024-01-01T10:00:00Z"
    },
    {
        "id": 1,
        "transaction_type": "refund",
        "amount": 25.00,
        "sender": "Bob",
        "receiver": "Alice",
        "timestamp": "2024-01-02T14:30:00Z"
    },
    {
        "id": 2,
        "transaction_type": "payment",
        "amount": 200.00,
        "sender": "Charlie",
        "receiver": "Alice",
        "timestamp": "2024-01-03T09:15:00Z"
    }
]
```

### Step 2: Verify File Structure

Ensure all files are in place:
- ✓ `src/server.py` - Provided
- ✓ `src/auth.py` - Provided
- ✓ `src/indexer.py` - Provided
- ✓ `api_ready_transactions.json` - Created in step 1

### Step 3: Navigate to Source Directory

Open your terminal and navigate to the `src` directory:
```bash
cd path/to/project/src
```

### Step 4: Start the Server

Run the server:
```bash
python server.py
```

You should see output like:
```
Index initialized with 0 transactions
Starting server on port 8000...
```

The server is now running on `http://localhost:8000`

---

## Authentication

The API uses **HTTP Basic Authentication**:
- **Username:** `admin`
- **Password:** `password`

These credentials are defined in `auth.py` and can be changed if needed.

---

## API Endpoints

### 1. List All Transactions
**GET** `/transactions`

Returns all transactions or filtered results.

**Examples:**
```bash
# Get all transactions
curl -u admin:password http://localhost:8000/transactions

# Filter by transaction type
curl -u admin:password "http://localhost:8000/transactions?transaction_type=payment"

# Filter by sender
curl -u admin:password "http://localhost:8000/transactions?sender=Alice"

# Filter by receiver
curl -u admin:password "http://localhost:8000/transactions?receiver=Bob"
```

**Response:**
```json
{
    "status": "success",
    "data": [
        {
            "id": 0,
            "transaction_type": "payment",
            "amount": 100.50,
            "sender": "Alice",
            "receiver": "Bob",
            "timestamp": "2024-01-01T10:00:00Z"
        }
    ],
    "message": "Retrieved 1 transaction(s)"
}
```

### 2. Get Single Transaction
**GET** `/transactions/{id}`

Retrieve a specific transaction by ID.

**Example:**
```bash
curl -u admin:password http://localhost:8000/transactions/0
```

**Response:**
```json
{
    "status": "success",
    "data": {
        "id": 0,
        "transaction_type": "payment",
        "amount": 100.50,
        "sender": "Alice",
        "receiver": "Bob",
        "timestamp": "2024-01-01T10:00:00Z"
    },
    "message": "Transaction retrieved"
}
```

### 3. Create Transaction
**POST** `/transactions`

Create a new transaction.

**Required Fields:**
- `transaction_type` (string)
- `amount` (number)
- `sender` (string)
- `receiver` (string)
- `timestamp` (string, ISO 8601 format)

**Example:**
```bash
curl -u admin:password -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_type": "payment",
    "amount": 150.00,
    "sender": "Alice",
    "receiver": "Bob",
    "timestamp": "2024-01-15T12:00:00Z"
  }'
```

**Response:**
```json
{
    "status": "success",
    "data": {
        "id": 3,
        "transaction_type": "payment",
        "amount": 150.00,
        "sender": "Alice",
        "receiver": "Bob",
        "timestamp": "2024-01-15T12:00:00Z"
    },
    "message": "Transaction created"
}
```

### 4. Update Transaction
**PUT** `/transactions/{id}`

Update an existing transaction.

**Example:**
```bash
curl -u admin:password -X PUT http://localhost:8000/transactions/0 \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 200.00,
    "transaction_type": "refund"
  }'
```

**Response:**
```json
{
    "status": "success",
    "data": {
        "id": 0,
        "transaction_type": "refund",
        "amount": 200.00,
        "sender": "Alice",
        "receiver": "Bob",
        "timestamp": "2024-01-01T10:00:00Z"
    },
    "message": "Transaction updated"
}
```

### 5. Delete Transaction
**DELETE** `/transactions/{id}`

Delete a transaction by ID.

**Example:**
```bash
curl -u admin:password -X DELETE http://localhost:8000/transactions/0
```

**Response:**
```json
{
    "status": "success",
    "data": {
        "id": 0,
        "transaction_type": "payment",
        "amount": 100.50,
        "sender": "Alice",
        "receiver": "Bob",
        "timestamp": "2024-01-01T10:00:00Z"
    },
    "message": "Transaction deleted"
}
```

---

## Testing with Postman

If you prefer using Postman:

1. **Set Authorization:**
   - Type: Basic Auth
   - Username: `admin`
   - Password: `password`

2. **Set Headers:**
   - For POST/PUT requests: `Content-Type: application/json`

3. **Use the endpoints** as documented above

---

## Performance Features

The server uses optimized data structures:

### Hash Map Indexing (O(1) Lookups)
- Instant lookups by `sender`, `receiver`, and `transaction_type`
- Much faster than linear search for large datasets

### Binary Search (O(log n) Range Queries)
- Efficient amount range queries
- Efficient timestamp range queries
- Sorted indexes maintained automatically

### Auto-Rebuild
- Indexes automatically rebuild after POST, PUT, DELETE operations
- Ensures data consistency

---

## Troubleshooting

### Error: "Data file not found"
**Cause:** `api_ready_transactions.json` is missing or in wrong location.

**Solution:** Ensure the file is in the parent directory of `src/`, not inside `src/`.

### Error: "Port already in use"
**Cause:** Port 8000 is already occupied by another process.

**Solution:** Change the port in `server.py`:
```python
server_address = ("", 8001)  # Use port 8001 instead
```

### Error: "Import error" for auth or indexer
**Cause:** Files are not in the same directory.

**Solution:** Ensure `server.py`, `auth.py`, and `indexer.py` are all in the `src/` directory.

### 401 Unauthorized
**Cause:** Missing or incorrect authentication credentials.

**Solution:** Ensure you're using `-u admin:password` in curl or setting Basic Auth in Postman.

### 400 Bad Request (POST/PUT)
**Cause:** Missing required fields or invalid JSON.

**Solution:** Verify your JSON includes all required fields with correct formatting.

---

## Security Notes

**Important:** This is a demonstration server with basic security:
- Credentials are hardcoded (not suitable for production)
- No HTTPS (data sent in plain text over network)
- No rate limiting
- No input sanitization beyond basic validation

**For production use, implement:**
- Environment variables for credentials
- HTTPS/TLS encryption
- Token-based authentication (JWT)
- Input validation and sanitization
- Rate limiting
- Proper error logging
- Database instead of JSON file

---

## Stopping the Server

Press `Ctrl + C` in the terminal to stop the server.

---

## Next Steps

1. Start the server and test basic operations
2. Try creating, reading, updating, and deleting transactions
3. Test the search functionality with query parameters
4. Monitor the console for index rebuild messages
5. Experiment with different transaction types and amounts

---

## Support

If you encounter issues:
1. Check the terminal output for error messages
2. Verify file structure matches the guide
3. Ensure JSON formatting is correct
4. Test with simple curl commands first

---

## License

This is a demonstration project for educational purposes.