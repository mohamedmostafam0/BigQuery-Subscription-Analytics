-- assert_unique_user_id.sql
-- Fails if user_id is not unique in the raw_subscriptions table.
SELECT
    user_id,
    COUNT(*) as count
FROM
    `{{ dataset_name }}.raw_subscriptions`
GROUP BY
    user_id
HAVING count > 1
