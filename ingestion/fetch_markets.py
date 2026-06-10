import requests
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
BRONZE_PATH = Path(__file__).parent.parent / "data" / "bronze"


def fetch_top_coins(n: int = 50) -> list[dict]:
    """Fetch top N coins by market cap from CoinGecko."""
    url = f"{COINGECKO_BASE_URL}/coins/markets"
    params = {
        "vs_currency": "eur",
        "order": "market_cap_desc",
        "per_page": n,
        "page": 1,
        "sparkline": False,
        "price_change_percentage": "24h,7d,30d",
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def save_to_bronze(data: list[dict]) -> Path:
    """Save raw API response as Parquet in the bronze layer."""
    df = pd.DataFrame(data)

    ingested_at = datetime.now(timezone.utc)
    df["ingested_at"] = ingested_at

    BRONZE_PATH.mkdir(parents=True, exist_ok=True)
    filename = f"markets_{ingested_at.strftime('%Y%m%d_%H%M%S')}.parquet"
    filepath = BRONZE_PATH / filename

    df.to_parquet(filepath, index=False)
    print(f"Saved {len(df)} rows → {filepath}")
    return filepath


if __name__ == "__main__":
    print("Fetching top 50 coins from CoinGecko...")
    raw_data = fetch_top_coins(n=50)
    save_to_bronze(raw_data)
