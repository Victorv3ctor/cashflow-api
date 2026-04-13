# 🏦 Cashflow API (FastAPI + MySQL + JWT)

> A backend system simulating core banking logic: authentication, transactions, and account-based financial operations.

This project focuses on **real-world backend architecture**, security, and clean separation of responsibilities.

---

## ⚡ What this project demonstrates

✔ Authentication system (JWT + bcrypt)  
✔ Secure account-based data isolation  
✔ Transaction engine (income / expense)  
✔ Balance mutation logic  
✔ Filtering + analytics  
✔ Layered backend architecture  

---

## 🧠 Tech Stack

- FastAPI 
- MySQL 
- JWT 
- bcrypt 
- Pydantic 
- Python 3.10+

---

## 🏗 Architecture (backend design)
    Client
    ↓
    FastAPI (API Layer)
    ↓
    Service Layer (Business Logic)
    ↓
    Storage Layer (SQL / Database)
    ↓
    MySQL
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

## 📌 API Overview
### Endpoints

- POST /register
- POST /login
- POST /transactions
- GET /transactions
- GET /account
- DELETE /transactions/{id}

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
- Storage layer → persistence logic

---

## ⚠️ Current Limitations (MVP scope)

This is an MVP backend system.
- No pagination for large datasets
- No refresh token mechanism yet

---

## 🚀 Future Improvements

- refresh token authentication
- pagination system
- Dockerized deployment
- automated testing (pytest)
- improved query builder / filtering engine

---
## ❓ Why this project exists ?
Built to simulate production-grade backend patterns with authentication, transactional consistency, and layered architecture using raw SQL.
## 👨‍💻 Author

Built by **Wiktor**

Backend-focused developer.



