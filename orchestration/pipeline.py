import os
import subprocess
from prefect import flow, task
from ingestion.fetch_markets import fetch_top_coins, save_to_bronze
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

@task
def ingest():
    top_coins = fetch_top_coins()
    return save_to_bronze(top_coins)

@task
def transform():
    subprocess.run(
        ["dbt", "run"],
        cwd=Path(__file__).parent.parent / "dbt" / "crypto_pipeline",
        env={**os.environ, "motherduck_token": os.getenv("MOTHERDUCK_TOKEN")},
    )

@flow
def crypto_pipeline():
    ingest()
    transform()
    
if __name__ == "__main__":
    crypto_pipeline()