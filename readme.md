# 🏦 Cashflow API

> A backend system simulating core banking logic: authentication, transactions, and account-based financial operations.

This project focuses on **real-world backend architecture**, security, and clean separation of responsibilities.

---

## 🧠 Tech Stack

- FastAPI 
- MySQL 
- JWT 
- bcrypt 
- Pydantic 
- Python 3.10+

---
## 📌 API Overview
### Endpoints

- POST /register
- POST /login
- POST /transactions
- GET /transactions
- GET /account
- DELETE /transactions/{id}

---
## 🏗 Architecture (backend design)
- **dependencies** – shared dependencies:
  - JWT authentication
  - database connection
  - repos
  - services
- **models** – core domain models:
  - Account (OOP)
  - Transaction (OOP)
  - Schemas (validation layer)

- **repositories** – data access layer (DB operations)
    - account repository
    - transaction repository

- **services** – business logic layer
    - account service
    - transaction service
    - auth service

- **storage** – database / persistence layer
### Design principles:
- Separation of concerns
- Stateless authentication
- Minimal ORM dependency (raw SQL control)
- Explicit business logic layer

---

## 🔐 Authentication Flow
JWT-based stateless authentication is used to secure all account-scoped operations, ensuring isolation between users and protected access to transaction data.
### Design principles:
- Explicit business logic layer
- Token-based auth (Bearer)
- Expiration handling
- Account-scoped access control
---
## 💰 Core Features

### 👤 Account System
- User registration
- Secure login
- Balance tracking per account

---

### 💳 Transaction Engine
- Add income / expense transactions
- Automatic balance updates
- Delete transactions (account-scoped)
- Strict account isolation

---

### 🔎 Filtering & Querying
- Filter by transaction type
- Order by:
  - date
  - amount
- Flexible query handling via service layer

---

### 📊 Analytics
- Transaction count per account
- Income vs expense aggregation
- Basic financial overview endpoint

---

## 🧩 Engineering Decisions

### Why no ORM?
Direct SQL was used to:
- maintain full query control
- improve learning depth of relational databases
- avoid abstraction hiding logic

---

### Why layered architecture?
To simulate real backend systems:
- API layer → request handling only
- Service layer → business rules
- Repository layer -> persistence logic

---

## ❓ Why this project exists ?
Built to simulate production-grade backend patterns with authentication, transactional consistency, and layered architecture using raw SQL.
## 👨‍💻 Author

Built by **Wiktor**

Backend-focused developer.



