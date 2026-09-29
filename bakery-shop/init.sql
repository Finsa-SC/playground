-- Create Table Products
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price NUMERIC(12, 2) NOT NULL DEFAULT 0,
    stock INT NOT NULL DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE NULL
);

-- Create Table Transactions
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    price NUMERIC(12, 2) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Relasi ke tabel products
    CONSTRAINT fk_product
        FOREIGN KEY(product_id) 
        REFERENCES products(id)
        ON DELETE RESTRICT
);

-- Seed Data Dummy buat Testing
INSERT INTO products (product_name, price, stock, description) VALUES
('Roti Tawar Bandung', 15000.00, 50, 'Roti tawar lembut cocok untuk sarapan'),
('Roti Cokelat Keju', 12000.00, 30, 'Roti manis isian keju cheddar dan meseres cokelat'),
('Croissant Butter', 22000.00, 15, 'Croissant gurih renyah dengan butter Perancis');

INSERT INTO transactions (product_id, count, price) VALUES
(1, 2, 30000.00), -- Beli 2 Roti Tawar
(3, 1, 22000.00); -- Beli 1 Croissant
