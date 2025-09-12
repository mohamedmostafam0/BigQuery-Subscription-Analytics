MERGE `{{ dataset_name }}.raw_subscriptions` AS T
USING `{{ dataset_name }}.raw_updated_subscriptions` AS S
ON T.id = S.id
WHEN MATCHED THEN
    UPDATE SET
        T.user_id = S.user_id,
        T.start_date = S.start_date,
        T.expiry_date = S.expiry_date,
        T.type_id = S.type_id,
        T.amount = S.amount
WHEN NOT MATCHED BY TARGET THEN
    INSERT (id, user_id, start_date, expiry_date, type_id, amount)
    VALUES (S.id, S.user_id, S.start_date, S.expiry_date, S.type_id, S.amount);
