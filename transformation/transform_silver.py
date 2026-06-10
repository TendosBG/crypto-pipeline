import duckdb
from datetime import datetime, timezone
from pathlib import Path

BRONZE_PATH = Path(__file__).parent.parent / "data" / "bronze"
SILVER_PATH = Path(__file__).parent.parent / "data" / "silver"

ingested_at = datetime.now(timezone.utc)

fileIn = max(BRONZE_PATH.glob("*.parquet"), key=lambda f: f.stat().st_mtime)
fileOut = f"markets_{ingested_at.strftime('%Y%m%d_%H%M%S')}.parquet"
filepath = SILVER_PATH / fileOut

duckdb.sql("SELECT id, symbol, name, image, current_price, market_cap, market_cap_rank, total_volume, high_24h, low_24h, price_change_percentage_24h, price_change_percentage_7d_in_currency, price_change_percentage_30d_in_currency, circulating_supply, total_supply, max_supply, last_updated, ingested_at FROM '" + fileIn.as_posix() + "'").write_parquet(str(filepath))

print("Bronze to Silver done ✅")
