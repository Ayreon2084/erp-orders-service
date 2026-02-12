-- 2.1. Сумма товаров по клиентам (Наименование клиента, сумма)
SELECT
    c.full_name AS "Client Name",
    COALESCE(SUM(op.quantity * op.price_at_order), 0) AS "Total price"
FROM clients AS c
LEFT JOIN orders AS o ON c.id = o.client_id
LEFT JOIN order_products AS op ON o.id = op.order_id
WHERE c.is_deleted = false
GROUP BY c.id, c.full_name
ORDER BY "Total price" DESC;
