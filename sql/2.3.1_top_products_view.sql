-- 2.3.1. VIEW «Топ-5 самых покупаемых товаров за последний месяц» (по количеству штук)
-- Отчёт: Наименование товара, Категория 1-го уровня (root), Общее количество проданных единиц
CREATE OR REPLACE VIEW top_5_products_last_month AS
SELECT
    p.name AS "Product Name",
    COALESCE(root_.name, cat.name) AS "Root Category",
    SUM(op.quantity) AS "Total Sold Quantity"
FROM order_products op
JOIN orders o ON op.order_id = o.id
JOIN products p ON op.product_id = p.id
JOIN categories AS cat ON p.category_id = cat.id AND cat.is_deleted = false
LEFT JOIN categories AS root_ ON cat.root_category_id = root_.id AND root_.is_deleted = false
WHERE o.created_at >= DATE_TRUNC('month', CURRENT_DATE - INTERVAL '1 month')
  AND o.created_at < DATE_TRUNC('month', CURRENT_DATE)
  AND p.is_deleted = false
GROUP BY p.id, p.name, "Root Category"
ORDER BY "Total Sold Quantity" DESC
LIMIT 5;
