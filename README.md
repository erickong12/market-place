# 🛒 Marketplace API

A simplified **marketplace backend** built with **FastAPI**, **SQLAlchemy**, and **Pydantic**, supporting buyer/seller flows, product listings, cart management, and order handling.

---

## 🚀 Features

* **User Authentication**: Register, login, JWT-based auth.
* **Seller Management**: Register as a seller, manage profile.
* **Product Catalog**: CRUD for products linked to sellers.
* **Cart**: Add, update, remove, and view cart items.
* **Orders**: Create orders, view history, seller order management.
* **Landing Page API**: Show top sellers and products.
* **Extensible**: Clean separation of schemas, services, and repositories.

---

## 🏗 Tech Stack

* **Backend**: FastAPI (Python 3.11+)
* **Database**: PostgreSQL (via SQLAlchemy ORM + Alembic for migrations)
* **Auth**: JWT (PyJWT)
* **Schemas**: Pydantic
* **Testing**: Pytest
* **Dev tools**: Docker, Poetry/Pip

---

## ⚙️ Setup & Run

### 1. Clone repo

```bash
git clone https://github.com/erickong12/market-place.git
cd marketplace-api
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run database migrations

```bash
alembic upgrade head
```

### 4. Start server

```bash
uvicorn app.main:app --reload
```

---

## 🧪 Testing

```bash
pytest -v
```

---

## 📖 API Docs

FastAPI provides interactive docs:

* Swagger: `http://localhost:8000/docs`
* ReDoc: `http://localhost:8000/redoc`
