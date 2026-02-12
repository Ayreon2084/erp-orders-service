-- 2.2. Количество дочерних элементов первого уровня вложенности по категориям
SELECT
    c.id AS category_id,
    c.name AS category_name,
    COUNT(child.id) AS first_level_children_count
FROM categories AS c
LEFT JOIN categories AS child ON child.parent_id = c.id AND child.is_deleted = false
WHERE c.is_deleted = false
GROUP BY c.id, c.name
ORDER BY c.id;
