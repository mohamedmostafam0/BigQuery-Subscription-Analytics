/*
Assuming converted means that a user changed their subscription plan (type_id changed).
Noticed by a change in type_id within the raw_subscriptions table for a user_id.
Note that since raw_updated_subcriptions only has data starting from 13/7, we use raw_subscriptions for april analysis.
*/
SELECT
    COUNT(DISTINCT user_id) AS converted_users
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
    type_id != previous_type_id 
    AND EXTRACT(YEAR FROM start_date) = 2025
    AND EXTRACT(MONTH FROM start_date) = 4;


