WITH latest AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY id ORDER BY ingested_at DESC) AS rn
    FROM {{ ref('stg_markets') }}
)

SELECT
    id,
    symbol,
    name,
    image,
    market_cap,
    SUM(market_cap) OVER () as total_market_cap,
    market_cap / total_market_cap*100 as dominance
FROM latest
WHERE rn = 1
ORDER BY dominance DESC
