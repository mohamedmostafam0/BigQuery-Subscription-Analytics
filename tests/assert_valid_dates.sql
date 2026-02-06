-- assert_valid_dates.sql
-- Fails if start_date is after expiry_date (and expiry_date is not null).
SELECT
    user_id,
    start_date,
    expiry_date
FROM
    `{{ dataset_name }}.raw_subscriptions`
WHERE
    expiry_date IS NOT NULL
    AND start_date > expiry_date
