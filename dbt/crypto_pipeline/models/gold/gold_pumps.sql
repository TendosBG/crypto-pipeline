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
    current_price,
    price_change_percentage_24h,
    total_volume,
    ingested_at
FROM latest
WHERE price_change_percentage_24h >= 15 OR price_change_percentage_24h <= -15
ORDER BY currency, ABS(price_change_percentage_24h) DESC
