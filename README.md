![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![Claude](https://img.shields.io/badge/Claude-D97757?logo=claude&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?logo=pytest&logoColor=white)
![Render](https://img.shields.io/badge/Render-46E3B7?logo=render&logoColor=black)

# WealthPulse API

WealthPulse is an AI-enhanced financial analytics API that reveals whether French savings products actually grow your wealth, or merely keep pace with inflation.

It combines a multi-source ETL pipeline, PostgreSQL storage, deterministic financial computations, and Claude-generated explanations deployed in production as a REST API built with FastAPI.

---

## Why this project

A savings account can show a positive interest rate while still losing purchasing power. WealthPulse makes this gap visible and explainable, combining transparent calculations with AI-generated context.

---

## Key Highlights

- Multi-source financial data ingestion pipeline
- Unified PostgreSQL storage layer
- Inflation-adjusted return calculations
- Real-return comparison across multiple assets
- Rolling average trend computation
- LLM-generated explanations constrained to backend-computed data
- REST API built with FastAPI
- Automated testing with Pytest

---

## Design Principles

The architecture separates numerical computations from natural language generation, so results stay consistent and verifiable.

- Financial computations are deterministic and reproducible.
- The LLM never performs calculations.
- AI-generated explanations are constrained to backend-computed data only.
- Missing values are never inferred or estimated.
- Data from heterogeneous sources is normalized into a unified schema before being stored in PostgreSQL.

---

## Live Demo

API deployed on Render:

- **Production URL**  
  https://wealthpulse-9u2y.onrender.com

- **API Documentation**  
  https://wealthpulse-9u2y.onrender.com/docs

- **Latest Rate Example**  
  https://wealthpulse-9u2y.onrender.com/rates/livret_a/latest

- **Real Return Example**  
  https://wealthpulse-9u2y.onrender.com/analyze/real-return?asset=livret_a&amount=10000

```json
  {
    "asset": "livret_a",
    "amount": 10000,
    "result": {
      "nominal_return": 150,
      "inflation_impact": 199.9,
      "real_return": -49.9,
      "real_rate": -0.5
    }
  }
```

   A Livret A at 1.5% with 2% inflation produces a **negative real return**: 
   despite earning 150€ in interest, the saver loses 49.90€ in purchasing power.

- **Comparison Example**  
  https://wealthpulse-9u2y.onrender.com/analyze/compare?assets=livret_a,lep&amount=10000

- **AI Analysis Example**  
  https://wealthpulse-9u2y.onrender.com/analyze/analyze?asset=livret_a&amount=10000

---

## API Preview

![alt text](<Swagger UI WealthPulse.png>)

---

## Architecture

<img src="Architecture WealthPulse.png" alt="Architecture WealthPulse" height="500">

---

## Data Flow

<img src="Data Flow WealthPulse.png" alt="Data Flow WealthPulse" height="500">

---

## Tech Stack

| Layer | Technology |
|----------|-----------------|
| Backend API | FastAPI |
| Database | PostgreSQL (Neon) |
| Data Processing | Pandas |
| AI Analysis | Anthropic Claude |
| HTTP Client | Requests |
| Testing | Pytest |
| Deployment | Render |
| Environment Management | python-dotenv |

---

## Project Structure

```text
wealthpulse/
│
├── api/
│   ├── main.py
│   └── routers/
│       ├── rates.py
│       └── analyze.py
│
├── llm/
│   ├── base.py
│   └── anthropic_provider.py
│
├── analysis.py
├── ingestion.py
├── ingest.py
├── database.py
├── config.py
│
├── tests/
│   └── test_api.py
│
├── requirements.txt
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/kevinoure-max/WealthPulse.git

cd wealthpulse
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate

Linux / Mac

```bash
source .venv/bin/activate
```

Windows

```bash
.venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
DATABASE_URL=postgresql://user:password@host:5432/database

ANTHROPIC_API_KEY=your_api_key

ANTHROPIC_MODEL=claude-sonnet-4-6
```

---

## Data Ingestion

Run the ingestion pipeline:

```bash
python ingest.py
```

Financial metrics originate from heterogeneous public sources and therefore require different ingestion strategies.

The pipeline automatically selects the appropriate fetcher for each metric, normalizes the resulting datasets into a common schema, and stores them in PostgreSQL.

Currently supported metrics include:

- Livret A
- LEP
- Inflation
- CAC 40

---

## Real Return Methodology

The project estimates purchasing power using the approximation:

```
real_rate ≈ asset_rate − inflation_rate
```

Nominal gains and inflation losses are computed independently before deriving the resulting real return expressed both as a percentage and in euros.

This approximation favors clarity over precision, the difference versus the exact Fisher formula is negligible below 5% rates.

---

## API Endpoints

The API is organized into two routers:

- `/rates` for financial data retrieval
- `/analyze` for deterministic computations and AI-generated explanations

### Retrieve Historical Data

```http
GET /rates/{metric}
```

Example:

```http
GET /rates/livret_a
```

Returns the complete historical series for the requested metric.

---

### Retrieve Latest Value

```http
GET /rates/{metric}/latest
```

Example:

```http
GET /rates/livret_a/latest
```

Returns the most recent value available in the database.

---

### Retrieve Rolling Average

```http
GET /rates/{metric}/trend
```

Example:

```http
GET /rates/cac40/trend?window=3
```

Returns the historical series enriched with a rolling average computed over the specified window.

---

### Compute Real Return

```http
GET /analyze/real-return
```

Example:

```http
GET /analyze/real-return?asset=livret_a&amount=10000
```

Returns:

- nominal return
- inflation impact
- real return
- real rate

---

### Compare Assets

```http
GET /analyze/compare
```

Example:

```http
GET /analyze/compare?assets=livret_a,lep&amount=10000
```

Returns a comparison of all requested assets sorted by real return.

---

### Generate AI Analysis

```http
GET /analyze/analyze
```

Example:

```http
GET /analyze/analyze?asset=livret_a&amount=10000
```

All financial computations are performed deterministically by the backend.

The LLM only receives precomputed values and is instructed to generate factual explanations using exclusively the provided data.

---

## Testing

Run the test suite:

```bash
pytest
```

Current test coverage includes:

- Valid historical rate retrieval
- Invalid metric handling
- Latest value endpoint
- Real return computation
- Asset comparison endpoint
- AI analysis endpoint with mocked Claude responses

---

## Data Sources

WealthPulse combines several independent public data providers:

- World Bank API for inflation
- Yahoo Finance for CAC 40 historical prices
- Historical regulated rates for French savings products (Livret A and LEP)

Despite their different update frequencies and formats, all datasets are normalized into a unified structure before being persisted.

---

## Future Improvements

- Additional French and European savings products
- Support for exact Fisher equation-based real return calculations
- Inflation forecasting
- Docker support
- CI/CD with GitHub Actions

---

## Author

**Kevin OURE**

[GitHub](https://github.com/kevinoure-max) · [LinkedIn](https://www.linkedin.com/in/kevin-oure/)

*Production-ready backend, data engineering, and AI integration project focused on financial analytics.*