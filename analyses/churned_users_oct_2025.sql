-- Assuming churned means a user had a subscription in the previous month (September 2025)
-- but does not have an active subscription in the current month (October 2025).
-- This considers subscriptions ONLY from raw_subscriptions.
WITH raw_subscriptions_data AS (
    SELECT user_id, start_date, expiry_date FROM `{{ dataset_name }}.raw_subscriptions`
),
active_users_september AS (
    SELECT DISTINCT user_id
    FROM raw_subscriptions_data
    WHERE
        start_date <= '2025-09-30' -- Started before or in September
        AND (expiry_date IS NULL OR expiry_date >= '2025-09-01') -- Ends after or in September, or ongoing
),
active_users_october AS (
    SELECT DISTINCT user_id
    FROM raw_subscriptions_data
    WHERE
        start_date <= '2025-10-31' -- Started before or in October
        AND (expiry_date IS NULL OR expiry_date >= '2025-10-01') -- Ends after or in October, or ongoing
)
SELECT
    COUNT(DISTINCT september.user_id) AS churned_users
FROM
    active_users_september AS september
LEFT JOIN
    active_users_october AS october
ON
    september.user_id = october.user_id
WHERE
    october.user_id IS NULL; -- User was active in September but not in October