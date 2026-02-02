merging the main branch  AmafarangaDB to commit our database
Members of Tricode group:
### SHYAKA Francis
### NGANJI Jospin
### MWIZERWA Keza Megane
### Lea Mugabo Abatoni

 ####Scrum Board Link ---- https://github.com/users/SHYAKAFRANCIS/projects/2

 ### Architecture Diagram Link ---- https://miro.com/welcomeonboard/a2NsMmM3K3NOOXRMRXdRazhxclN3Y01uMGxjOE0yVXZ2Zmt6Y2J2V2RZM2o4UTl6MVZkMHg4NEpycnBOMXRIaEhqSHQ4RDgwcWpQT050UEpsNWFUbTdRdW0yVVBEL2pUbTVkT2pwRVVhV3Z0eGZZOExhT0R6QWEwakFCUVJJaWRhWWluRVAxeXRuUUgwWDl3Mk1qRGVRPT0hdjE=?share_link_id=305152979926

This is a layered system architecture for AMAFARANGA DATABASE that shows how user uploads and views mobile money data, how the system security process and analyses it through API's and how cleared data is stored and monitored usind cloud infrastructures.
Here is the link to the team sheet that tracks the collaboration on this project : https://docs.google.com/spreadsheets/d/1Nn7axOub_srAbhR_4dG9ylsXlkstVROlOe4p1SZ70R4/edit?gid=0#gid=0

The sheet Team attendants for the second task, which is BUILDING AND SECURING A REST API: https://docs.google.com/spreadsheets/d/1oyffL8CKBQm1KgpFhHXjqIPKVIwPrqrF2k4gMlWqq78/edit?usp=sharing
Here is the link to our pdf REST API report https://github.com/SHYAKAFRANCIS/AmafarangaDB/blob/main/Docs/Building%20And%20Securing%20A%20REST%20API.pdf

# Transaction API Server

A Python REST API for managing financial transactions with efficient hash map indexing.

## Quick Start

1. **Create data file** `api_ready_transactions.json` in parent directory:
```json
[]
```

2. **Run server:**
```bash
cd src
python app.py
```

Server runs on `http://localhost:8000`

## Authentication
- Username: `admin`
- Password: `password`

## API Endpoints

```bash
# List all transactions
curl -u admin:password http://localhost:8000/transactions

# Get transaction by ID
curl -u admin:password http://localhost:8000/transactions/0

# Create transaction
curl -u admin:password -X POST http://localhost:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{"transaction_type":"payment","amount":100,"sender":"Alice","receiver":"Bob","timestamp":"2024-01-01T10:00:00Z"}'

# Update transaction
curl -u admin:password -X PUT http://localhost:8000/transactions/0 \
  -H "Content-Type: application/json" \
  -d '{"amount":150}'

# Delete transaction
curl -u admin:password -X DELETE http://localhost:8000/transactions/0

# Filter by field
curl -u admin:password "http://localhost:8000/transactions?sender=Alice"
```

## Project Structure
```
project/
├── src/
│   ├── app.py
│   ├── auth.py
│   └── indexer.py
└── api_ready_transactions.json
```

## Features
- O(1) lookups via hash map indexing
- Basic HTTP authentication
- RESTful CRUD operations
- Query filtering by sender, receiver, transaction_type
