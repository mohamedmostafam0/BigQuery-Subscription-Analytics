-- Assuming downgraded means that the user downgraded their package to a less premium one.
-- Noticed by a decrease in type_id within the raw_subscriptions table for a user_id.
SELECT
    COUNT(DISTINCT user_id) AS downgraded_users
FROM (
    SELECT
        user_id,
        start_date,
        type_id,
        LAG(type_id) OVER (PARTITION BY user_id ORDER BY start_date) AS previous_type_id
    FROM
        `{{ dataset_name }}.raw_subscriptions` 
) AS user_history
WHERE
    type_id < previous_type_id 
    AND EXTRACT(YEAR FROM start_date) = 2025
    AND EXTRACT(MONTH FROM start_date) = 6;
