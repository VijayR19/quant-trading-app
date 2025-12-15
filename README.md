# Quant Trading App 🚀

A full-stack quantitative trading platform built with **FastAPI**, **PostgreSQL**, and a modular services + routers architecture. Supports authentication, market data ingestion, ML-based prediction, and paper trading.

> ⚠️ **Paper-trading / research platform only.** No real money is traded.

---

## 🧠 Architecture Overview

```
Frontend (HTML/CSS/JS)
    ↓
FastAPI Routers (HTTP API)
    ↓
Services (Business Logic)
    ↓
Database / External APIs
```

### Separation of Concerns

| Layer | Responsibility |
|-------|---|
| **Routers** | HTTP request handling |
| **Services** | Business logic & API integrations |
| **Core** | Config, security, shared utilities |
| **Models** | Database schema (SQLAlchemy) |
| **Schemas** | Request/response validation (Pydantic) |

This architecture ensures the system is testable, scalable, and production-ready.

---

## 📁 Project Structure

```
quant-trading-app/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py              # Configuration
│   │   │   └── security.py            # Auth & hashing
│   │   ├── routers/
│   │   │   ├── auth.py                # Login / register
│   │   │   ├── market.py              # Market data
│   │   │   ├── predict.py             # ML predictions
│   │   │   └── trade.py               # Paper trading
│   │   ├── services/
│   │   │   ├── market_data.py         # External API integration
│   │   │   └── predictor.py           # ML inference
│   │   ├── models.py                  # DB models
│   │   ├── schemas.py                 # Request/response schemas
│   │   ├── db.py                      # Database setup
│   │   ├── deps.py                    # FastAPI dependencies
│   │   ├── seed_data.py               # Dev seed script
│   │   └── main.py                    # App entrypoint
│   ├── .env                           # Env variables (git-ignored)
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── venv/
├── .gitignore
└── README.md
```

---

## ⚙️ Tech Stack

**Backend:** FastAPI · PostgreSQL · SQLAlchemy · Pydantic · JWT · bcrypt

**Frontend:** Vanilla HTML/CSS/JS (desktop-first)

**Market Data:** Pluggable external APIs (Finnhub / AlphaVantage / Alpaca)

---

## 🔐 Authentication

1. User registers → password hashed with **bcrypt**
2. User logs in → **JWT access token** issued
3. Protected routes require valid JWT
4. User identity injected via FastAPI dependencies

---

## 📈 Data & Prediction Flow

```
Market API → market_data service → feature extraction → 
predictor service (ML) → API response
```

- Market service is **read-only**
- Predictor **never places trades**
- ML only informs decisions

---

## 💱 Paper Trading Flow

```
User Request → Trade Router → Market Price Lookup → 
Record Trade in DB → Calculate Position & PnL
```

- Trades are simulated
- Filled at current market prices
- Stored in PostgreSQL

---

## 🚀 Quick Start

### 1. Setup environment
```bash
git clone <repo-url>
cd quant-trading-app
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
pip install -r backend/requirements.txt
```

### 3. Configure `.env`
Create `backend/.env`:
```env
APP_NAME=Trading App
JWT_SECRET=CHANGE_ME

DB_USER=trading_app_user
DB_PASSWORD=dev_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=trading_app

MARKET_PROVIDER=finnhub
FINNHUB_API_KEY=your_api_key_here
```

### 4. Initialize database
```bash
sudo -u postgres createdb trading_app
```

### 5. Seed test data
```bash
cd backend
python3 -m app.seed_data
```

Test users: `test@tradingapp.com`, `admin@tradingapp.com`

### 6. Run server
```bash
uvicorn app.main:app --reload
```

Visit: http://127.0.0.1:8000/docs

---

## 📚 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/auth/register` | Register user |
| POST | `/api/auth/login` | Login & get JWT |
| GET | `/api/market/price?symbol=AAPL` | Get current price |
| POST | `/api/predict` | Get ML prediction |
| POST | `/api/trade` | Place paper trade |
| GET | `/api/trade/my` | View your trades |

---

## 🧩 Design Principles

- ✅ Explicit boundaries between data, logic, and transport
- ✅ Async I/O for external APIs
- ✅ Environment-based configuration
- ✅ Provider-agnostic market data (swappable)
- ✅ Paper trading first → real trading later

---

## 🚧 Roadmap

- [ ] Candlestick data & technical indicators
- [ ] Backtesting engine
- [ ] Position & PnL reporting endpoints
- [ ] WebSocket price streaming
- [ ] Broker integration (Alpaca / Interactive Brokers)

---

## ⚠️ Disclaimer

**Educational & research purposes only.** This project does not provide financial advice and does not execute real trades.
