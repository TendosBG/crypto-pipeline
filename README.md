# Crypto Analytics Pipeline

End-to-end data engineering pipeline ingesting live crypto market data from CoinGecko, transforming it through a medallion architecture, and exposing analytics via a live dashboard.

**[Live Dashboard →](https://tendos-cryptoanalytics.streamlit.app)**

---

## Architecture

```
CoinGecko API (free, no auth)
        │
        ▼
┌───────────────────┐
│  Ingestion        │  Python + requests
│  fetch_markets.py │  Top 50 coins by market cap
└────────┬──────────┘
         │ Parquet files
         ▼
┌───────────────────┐
│  Bronze Layer     │  Raw data, append-only
│  data/bronze/     │  Timestamped snapshots
└────────┬──────────┘
         │ dbt (read_parquet glob)
         ▼
┌───────────────────┐
│  Silver Layer     │  stg_markets (view)
│  MotherDuck       │  Cleaned, typed, renamed columns
└────────┬──────────┘
         │ dbt refs
         ▼
┌───────────────────┐
│  Gold Layer       │  Aggregated metrics (tables)
│  MotherDuck       │  4 analytical models
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Dashboard        │  Streamlit + Plotly
│  Streamlit Cloud  │  Reads from MotherDuck
└───────────────────┘
```

Orchestrated by **Prefect** locally and scheduled via **GitHub Actions** (hourly).

---

## Stack

| Layer | Tool | Purpose |
|---|---|---|
| Ingestion | Python, requests | CoinGecko API calls |
| Storage | Parquet | Bronze raw snapshots |
| Warehouse | DuckDB / MotherDuck | SQL on Parquet + cloud hosting |
| Transformation | dbt-duckdb | Silver & Gold models |
| Orchestration | Prefect 3 | Flow & task management |
| Scheduling | GitHub Actions | Hourly pipeline runs |
| Visualization | Streamlit, Plotly | Live analytics dashboard |

---

## Data Models

### Silver
| Model | Materialization | Description |
|---|---|---|
| `stg_markets` | View | Cleaned Bronze data — typed columns, renamed fields |

### Gold
| Model | Materialization | Description |
|---|---|---|
| `gold_dominance` | Table | Market cap share per coin (window function) |
| `gold_volatility` | Table | Absolute price change 7d / 30d |
| `gold_pumps` | Table | Coins with 24h change > ±15% |
| `gold_btc_correlation` | Table | Each coin's 24h variation vs BTC |

---

## Project Structure

```
crypto-pipeline/
├── .github/
│   └── workflows/
│       └── pipeline.yml     # GitHub Actions — hourly schedule
├── ingestion/
│   └── fetch_markets.py     # CoinGecko → Bronze Parquet
├── orchestration/
│   └── pipeline.py          # Prefect flow (ingest + dbt run)
├── dbt/
│   └── crypto_pipeline/
│       └── models/
│           ├── silver/      # stg_markets
│           └── gold/        # dominance, volatility, pumps, correlation
├── dashboard/
│   └── app.py               # Streamlit dashboard
├── data/
│   └── bronze/              # Local Parquet snapshots (gitignored)
├── requirements.txt
└── runtime.txt
```

---

## Local Setup

### Prerequisites
- Python 3.12
- A [MotherDuck](https://motherduck.com) account and token

### Installation

```bash
git clone https://github.com/TendosBG/crypto-pipeline.git
cd crypto-pipeline
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### Environment

Create a `.env` file at the project root:

```env
MOTHERDUCK_TOKEN=your_token_here
```

### dbt Profile

Create `~/.dbt/profiles.yml`:

```yaml
crypto_pipeline:
  target: dev
  outputs:
    dev:
      type: duckdb
      path: md:crypto_pipeline
```

### Run

```bash
# From the project root
python -m orchestration.pipeline
```

This will:
1. Fetch top 50 coins from CoinGecko and save a Bronze Parquet snapshot
2. Run dbt to build Silver + Gold models on MotherDuck

---

## Automated Scheduling

The pipeline runs automatically every hour via GitHub Actions (`.github/workflows/pipeline.yml`).

The `MOTHERDUCK_TOKEN` must be added as a repository secret under **Settings → Secrets and variables → Actions**.
