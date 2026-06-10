WITH latest AS (
    SELECT *,
        ROW_NUMBER() OVER (PARTITION BY id ORDER BY ingested_at DESC) AS rn
    FROM {{ ref('stg_markets') }}
),

bitcoin AS (
    SELECT *
    FROM latest
    WHERE id = 'bitcoin' and rn = 1
)

SELECT
    latest.id,
    latest.symbol,
    latest.name,
    latest.image,
    latest.price_change_percentage_24h as variation,
    bitcoin.price_change_percentage_24h as variationBTC,
    variation-variationBTC as difference
FROM latest
CROSS JOIN bitcoin
WHERE latest.rn = 1
ORDER BY ABS(difference) DESC
