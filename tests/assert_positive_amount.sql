-- assert_positive_amount.sql
-- Fails if amount is less than or equal to 0.
SELECT
    user_id,
    amount
FROM
    `{{ dataset_name }}.raw_subscriptions`
WHERE
    amount <= 0
