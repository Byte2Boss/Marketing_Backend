<div align="center">

# ⚙️ RestroMind AI — Backend API & Lead Engine

**High-Performance Asynchronous REST API for the RestroMind AI Marketing Platform**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/PostgreSQL-15+-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/SQLAlchemy-2.0_Async-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy" />
  <img src="https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white" alt="Pydantic" />
  <img src="https://img.shields.io/badge/Uvicorn-Async_ASGI-499848?style=for-the-badge&logo=gunicorn&logoColor=white" alt="Uvicorn" />
  <img src="https://img.shields.io/badge/Pytest-Async_Tests-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="Pytest" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge" alt="License" />
</p>

</div>

---

## 📖 Overview

The **RestroMind AI Backend** is an enterprise-grade, asynchronous RESTful API engineered with **Python FastAPI** and **PostgreSQL**. It powers the marketing website by managing lead capture pipelines, scheduling 15-minute product walkthroughs, computing real-time restaurant ROI projections, and handling enterprise franchise inquiries with built-in anti-spam protection.

---

## ✨ Key Features

- 🚀 **High-Throughput Async Engine**: Native `async`/`await` architecture powered by `FastAPI` + `asyncpg` for sub-15ms response latency.
- 📥 **Lead Ingestion & Trial Signups**: Zero-loss capturing of restaurant leads with automated validation, source tracking, and status lifecycle.
- 📅 **Smart Demo Booking System**: Real-time slot availability checking, prevention of double-bookings, and unique confirmation code generation (`RM-XXXXX`).
- 💡 **Server-Side ROI Calculation Engine**: Calculates dynamic restaurant revenue uplift, average order value boosts, and labor hours saved based on empirical hospitality metrics.
- 📬 **Inquiries & Newsletter Subscriptions**: Idempotent subscriber management and enterprise franchise contact routing.
- 🛡️ **Security & Anti-Spam Safeguards**: Rate-limiting per client IP (`SlowAPI`), RFC 5322 email normalization, CORS security, and structured JSON envelopes.
- 🧪 **Comprehensive Automated Testing**: Async integration and unit tests using `pytest` and `httpx`.

---

## 🏗️ Architecture & Tech Stack

```
[ React Marketing Frontend ]
             │
             ▼  (HTTPS / JSON REST API)
[ FastAPI Async Engine (Uvicorn) ]
   ├── Rate Limiting (SlowAPI)
   ├── CORS Middleware & Request Logging
   ├── Pydantic v2 Serialization & Validation
   └── Service Layer (Lead, Demo, ROI, Contact)
             │
             ▼  (SQLAlchemy 2.0 Async + AsyncPG Driver)
[ PostgreSQL Database ]
   ├── leads
   ├── demo_bookings
   ├── roi_calculations
   ├── contact_inquiries
   └── newsletter_subscribers
```

---

## 🗄️ Database Schemas (PostgreSQL)

| Table Name | Description | Key Fields |
| :--- | :--- | :--- |
| **`leads`** | Restaurant trial signups & CTA leads | `id`, `restaurant_name`, `owner_name`, `email`, `phone`, `tables_count`, `city`, `source`, `status`, `created_at` |
| **`demo_bookings`** | Scheduled 15-minute live demo sessions | `id`, `lead_id` (FK), `preferred_date`, `time_slot`, `restaurant_type`, `confirmation_code`, `status`, `notes` |
| **`roi_calculations`** | Logged ROI calculations with financial projections | `id`, `email`, `restaurant_name`, `tables_count`, `avg_daily_orders`, `avg_order_value`, `projected_monthly_gain` |
| **`contact_inquiries`** | General and enterprise franchise inquiries | `id`, `full_name`, `email`, `phone`, `subject`, `message`, `is_resolved`, `created_at` |
| **`newsletter_subscribers`** | Email list subscribers with opt-in status | `id`, `email`, `source`, `is_active`, `unsubscribed_at`, `created_at` |

---

## 🔌 API Endpoints Reference

### Base URL: `/api/v1`

| Method | Endpoint | Description | Request Body Summary |
| :--- | :--- | :--- | :--- |
| `POST` | `/leads` | Register trial / lead | `restaurant_name`, `owner_name`, `email`, `tables_count`, `source` |
| `GET` | `/demo/available-slots` | Fetch open demo slots | Query: `?date=YYYY-MM-DD` |
| `POST` | `/demo/book` | Book demo walkthrough | `lead_id` or lead info + `preferred_date`, `time_slot`, `restaurant_type` |
| `POST` | `/roi/calculate` | Compute restaurant ROI | `tables_count`, `avg_daily_orders`, `avg_order_value`, `email` |
| `POST` | `/contact` | Submit contact inquiry | `full_name`, `email`, `phone`, `subject`, `message` |
| `POST` | `/newsletter/subscribe` | Subscribe to newsletter | `email`, `source` |
| `GET` | `/health` | Health & DB connectivity check | *None* |

---

## 📂 Project Structure

```
Marketing_Backend/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI app initialization & middlewares
│   │
│   ├── api/                        # API route handlers
│   │   ├── __init__.py
│   │   ├── deps.py                 # DB session dependencies & rate limiters
│   │   └── v1/
│   │       ├── router.py           # v1 aggregated router
│   │       ├── leads.py            # /api/v1/leads
│   │       ├── demo.py             # /api/v1/demo
│   │       ├── roi.py              # /api/v1/roi
│   │       ├── contact.py          # /api/v1/contact
│   │       ├── newsletter.py       # /api/v1/newsletter
│   │       └── health.py           # /api/v1/health
│   │
│   ├── core/                       # Configurations & Database connection
│   │   ├── config.py               # Pydantic BaseSettings (.env loader)
│   │   ├── database.py             # SQLAlchemy async engine & sessionmaker
│   │   └── security.py             # Confirmation code generator & sanitizers
│   │
│   ├── models/                     # SQLAlchemy 2.0 ORM Models
│   │   ├── lead.py                 # Lead & DemoBooking models
│   │   ├── roi.py                  # RoiCalculation model
│   │   ├── contact.py              # ContactInquiry model
│   │   └── newsletter.py           # NewsletterSubscriber model
│   │
│   ├── schemas/                    # Pydantic v2 validation models
│   │   ├── lead.py
│   │   ├── roi.py
│   │   ├── contact.py
│   │   └── common.py               # Standardized response envelopes
│   │
│   └── services/                   # Business Logic & Algorithms
│       ├── lead_service.py
│       ├── demo_service.py
│       └── roi_service.py
│
├── tests/                          # Async automated test suite
│   ├── conftest.py
│   ├── test_leads.py
│   ├── test_demo.py
│   ├── test_roi.py
│   └── test_health.py
│
├── .env.example
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- **Python**: `3.11+`
- **PostgreSQL**: `15+` (or Docker container)

### 1. Clone & Set Up Virtual Environment
```bash
cd Marketing_Backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory:
```env
APP_NAME="RestroMind AI Marketing API"
DEBUG=True
ENVIRONMENT=development
CORS_ORIGINS=["http://localhost:5173", "http://127.0.0.1:5173"]

# PostgreSQL Async Connection String
DATABASE_URL="postgresql+asyncpg://postgres:postgres@localhost:5432/restromind_marketing"
```

### 4. Run Database Migrations / Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Interactive API Documentation
Open your browser and navigate to:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Running Automated Tests

```bash
pytest -v
```

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

<div align="center">
  <sub>Built with ❤️ for <b>RestroMind AI</b>.</sub>
</div>
