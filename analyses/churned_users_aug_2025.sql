-- Assuming churned means a user had a subscription in the previous month (July 2025)
-- but does not have an active subscription in the current month (August 2025).
-- This considers subscriptions ONLY from raw_subscriptions.
WITH raw_subscriptions AS (
    SELECT user_id, start_date, expiry_date FROM `{{ dataset_name }}.raw_subscriptions`
),
active_users_july AS (
    SELECT DISTINCT user_id
    FROM raw_subscriptions
    WHERE
        start_date <= '2025-07-31' -- Started before or in July
        AND (expiry_date IS NULL OR expiry_date >= '2025-07-01') -- Ends after or in July, or ongoing
),
active_users_august AS (
    SELECT DISTINCT user_id
    FROM raw_subscriptions
    WHERE
        start_date <= '2025-08-31' -- Started before or in August
        AND (expiry_date IS NULL OR expiry_date >= '2025-08-01') -- Ends after or in August, or ongoing
)
SELECT
    COUNT(DISTINCT july.user_id) AS churned_users
FROM
    active_users_july AS july
LEFT JOIN
    active_users_august AS august
ON
    july.user_id = august.user_id
WHERE
    august.user_id IS NULL; -- User was active in July but not in August