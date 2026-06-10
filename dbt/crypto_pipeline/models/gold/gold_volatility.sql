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
    price_change_pct_7d,
    price_change_pct_30d,
    ABS(price_change_pct_7d)  AS volatility_7d,
    ABS(price_change_pct_30d) AS volatility_30d
FROM latest
WHERE rn = 1
ORDER BY volatility_30d DESC
