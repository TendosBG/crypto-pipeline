WITH latest AS (
    SELECT *
    FROM {{ ref('stg_markets') }}
    WHERE ingested_at = (SELECT MAX(ingested_at) FROM {{ ref('stg_markets') }})
),

bitcoin AS (
    SELECT currency, price_change_percentage_24h
    FROM latest
    WHERE id = 'bitcoin'
)

SELECT
    latest.id,
    latest.symbol,
    latest.name,
    latest.image,
    latest.currency,
    latest.price_change_percentage_24h AS variation,
    bitcoin.price_change_percentage_24h AS variationBTC,
    latest.price_change_percentage_24h - bitcoin.price_change_percentage_24h AS difference
FROM latest
JOIN bitcoin ON latest.currency = bitcoin.currency
ORDER BY latest.currency, ABS(difference) DESC
