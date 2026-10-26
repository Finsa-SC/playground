INSERT INTO categories (name, description) VALUES
    ('Bread', 'Freshly baked bread and loaves'),
    ('Cake', 'Cakes for everyday occasions and celebrations'),
    ('Pastry', 'Croissants, danishes, and other pastries')
ON CONFLICT (name) DO NOTHING;

INSERT INTO products (category_id, name, description, price, stock_quantity)
SELECT c.id, seed.name, seed.description, seed.price, seed.stock_quantity
FROM (VALUES
    ('Bread', 'White Bread', 'Soft and freshly baked white bread', 15000.00::numeric, 30),
    ('Cake', 'Chocolate Cake', 'Chocolate cake with rich chocolate frosting', 85000.00::numeric, 10),
    ('Pastry', 'Butter Croissant', 'Flaky croissant made with butter', 12000.00::numeric, 25)
) AS seed(category_name, name, description, price, stock_quantity)
JOIN categories c ON c.name = seed.category_name
WHERE NOT EXISTS (SELECT 1 FROM products p WHERE p.name = seed.name);
