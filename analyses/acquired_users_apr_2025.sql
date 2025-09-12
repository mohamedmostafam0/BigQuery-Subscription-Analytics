SELECT
    COUNT(DISTINCT user_id) AS acquired_users
FROM
    `{{ dataset_name }}.{{ table_name }}` 
WHERE
    EXTRACT(YEAR FROM start_date) = 2025
    AND EXTRACT(MONTH FROM start_date) = 4;
