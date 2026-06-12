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
    market_cap,
    SUM(market_cap) OVER (PARTITION BY currency) AS total_market_cap,
    market_cap / total_market_cap * 100 AS dominance
FROM latest
ORDER BY currency, dominance DESC
