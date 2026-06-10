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
    current_price,
    price_change_percentage_24h,
    total_volume,
    ingested_at
FROM latest
WHERE price_change_percentage_24h >= 15 OR price_change_percentage_24h <= -15 AND rn = 1
ORDER BY ABS(price_change_percentage_24h) DESC
