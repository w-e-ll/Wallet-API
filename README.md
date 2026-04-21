# Wallet API

A simple wallet service built with FastAPI, demonstrating idempotent operations, concurrency handling, and clean architecture.

---

## 🚀 Features

- Create wallets
- Deposit & withdraw funds
- Idempotent operations (safe retries)
- Thread-safe in-memory implementation
- Decimal-based money handling (no float errors)
- #### Clean layered architecture:
  - API layer
  - Service layer
  - Repository layer
  - Domain models

---

## 🧱 Tech Stack

- Python 3.11+
- FastAPI
- Pydantic v2
- uv (dependency management)
- Uvicorn (ASGI server)

---

## 📂 Project Structure

```
- lib/
    - models.py # Domain models
    - types.py # Shared types
    - validation.py # Request/Response schemas
    - wallet_repository.py # Data access layer
    - wallet_service.py # Business logic
    - response_object.py # DTO mapping

- main.py # FastAPI entrypoint
```

---

## ⚙️ Setup

### 1. Install dependencies

```
uv sync
```

#### Run the application
```
uv run uvicorn main:app --reload
```
3. Open API docs
```
http://127.0.0.1:8000/docs
```

📌 API Endpoints
### Create wallet
```
POST /wallets
{
  "owner": "Valentin"
}
```

### Deposit
```
POST /wallets/{wallet_id}/deposit
{
  "amount": "100.00",
  "idempotency_key": "abc-123"
}
```

### Withdraw
```
POST /wallets/{wallet_id}/withdraw
{
  "amount": "50.00",
  "idempotency_key": "xyz-789"
}
```

# Get wallet
```
GET /wallets/{wallet_id}
```

# List operations
```
GET /wallets/{wallet_id}/operations
```

# Transfer
```
POST /wallets/transfer
{
  "from_wallet_id": "uuid",
  "to_wallet_id": "uuid",
  "amount": "100.00",
  "idempotency_key": "transfer-123"
}
```
### 🔐 Idempotency

Operations use an idempotency_key to guarantee safe retries.

Same key + same payload → returns existing operation
Same key + different payload → 409 Conflict

### ⚠️ Concurrency

The service uses a lock to ensure thread safety in the in-memory implementation.

#### Note: This is a simplified approach. In production, database transactions should be used instead.

### 💰 Money Handling
- Uses Decimal for precision

Validates:
- positive amounts
- max 2 decimal places

### 🧠 Design Notes
- In-memory storage for simplicity
- Repository pattern separates data access
- Service layer encapsulates business logic
- DTO mapping isolates API representation

### 🚧 Limitations
- No persistent storage (in-memory only)
- Global lock may become a bottleneck
- No pagination for operations
- No transfer endpoint

### 🔮 Future Improvements
- PostgreSQL integration with transactions
- Per-wallet locking strategy
- Transfer between wallets
- Pagination & filtering
- Dependency injection (FastAPI Depends)
- Distributed idempotency (Redis / DB)

### 🐳 Docker

#### Build:
```
docker build -t wallet-api .
```
#### Run:
```
docker run -p 8000:8000 wallet-api
```

### 👤 Author

Valentin Sheboldaev
