WITH latest AS (
    SELECT *
    FROM {{ ref('stg_markets') }}
    WHERE ingested_at = (SELECT MAX(ingested_at) FROM {{ ref('stg_markets') }})
)

SELECT
    id,
    symbol,
    name,
    image,
    currency,
    price_change_pct_7d,
    price_change_pct_30d,
    ABS(price_change_pct_7d)  AS volatility_7d,
    ABS(price_change_pct_30d) AS volatility_30d
FROM latest
ORDER BY currency, volatility_30d DESC
