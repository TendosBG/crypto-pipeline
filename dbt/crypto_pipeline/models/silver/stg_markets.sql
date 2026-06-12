SELECT
    id,
    symbol,
    name,
    image,
    currency,
    current_price,
    market_cap,
    market_cap_rank,
    total_volume,
    high_24h,
    low_24h,
    price_change_percentage_24h,
    price_change_percentage_7d_in_currency  AS price_change_pct_7d,
    price_change_percentage_30d_in_currency AS price_change_pct_30d,
    circulating_supply,
    total_supply,
    max_supply,
    last_updated::TIMESTAMP AS last_updated,
    ingested_at
-- union_by_name tolerates legacy bronze files written before the `currency`
-- column existed (those rows get currency = NULL). The Gold models keep only
-- the latest snapshot, so that pre-schema data is naturally excluded.
FROM read_parquet('../../data/bronze/*.parquet', union_by_name = true)
