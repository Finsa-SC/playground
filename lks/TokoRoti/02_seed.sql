USE TokoRotiDB;
GO

-- --------------------------------------------------
-- Seed Data: Roles
-- --------------------------------------------------
INSERT INTO Roles (RoleName, Description) VALUES 
('Worker', 'Akses manajemen stok, kategori, dan pemrosesan pesanan'),
('Customer', 'Akses untuk browsing katalog dan melakukan pembelian');
GO

-- --------------------------------------------------
-- Seed Data: Users
-- --------------------------------------------------
-- Catatan: PasswordHash diisi dummy/placeholder hash
INSERT INTO Users (RoleID, FullName, Email, PasswordHash, PhoneNumber) VALUES 
(1, 'Admin Baker', 'admin@tokoroti.com', '$2a$12$eImiTXuWVxfM37uY4JANjO5E.8B.g...', '081234567890'), -- Worker (RoleID = 1)
(1, 'Staff Kasir', 'staff@tokoroti.com', '$2a$12$eImiTXuWVxfM37uY4JANjO5E.8B.g...', '081234567891'), -- Worker (RoleID = 1)
(2, 'Budi Santoso', 'budi@gmail.com', '$2a$12$eImiTXuWVxfM37uY4JANjO5E.8B.g...', '089876543210'),   -- Customer (RoleID = 2)
(2, 'Siti Rahma', 'siti@gmail.com', '$2a$12$eImiTXuWVxfM37uY4JANjO5E.8B.g...', '089876543211');     -- Customer (RoleID = 2)
GO

-- --------------------------------------------------
-- Seed Data: Categories
-- --------------------------------------------------
INSERT INTO Categories (CategoryName, Description) VALUES 
('Roti Tawar', 'Aneka varian roti tawar harian'),
('Roti Manis', 'Roti dengan isian cokelat, keju, atau selai'),
('Pastry & Croissant', 'Pastry renyah dengan olahan butter premium');
GO

-- --------------------------------------------------
-- Seed Data: Products
-- --------------------------------------------------
INSERT INTO Products (CategoryID, ProductName, Description, Price, Stock, ImagePath) VALUES 
(1, 'Roti Tawar Kupas', 'Roti tawar lembut tanpa kulit', 18000.00, 25, '/static/images/products/roti-tawar-kupas.jpg'),
(2, 'Roti Cokelat Lumer', 'Roti manis dengan isian cokelat meleleh', 9500.00, 40, '/static/images/products/roti-cokelat.jpg'),
(2, 'Roti Keju Spesial', 'Roti manis dengan parutan keju cheddar di dalam dan luar', 11000.00, 30, '/static/images/products/roti-keju.jpg'),
(3, 'Butter Croissant', 'Croissant klasik dengan lapisan butter gurih', 22000.00, 15, '/static/images/products/butter-croissant.jpg');
GO

-- --------------------------------------------------
-- Seed Data: Sample Orders & Details
-- --------------------------------------------------
-- Transaksi 1: Budi beli Roti Cokelat & Butter Croissant (Diproses oleh Admin Baker)
INSERT INTO Orders (CustomerID, WorkerID, Status, TotalAmount) VALUES 
(3, 1, 'Completed', 41000.00);

INSERT INTO OrderDetails (OrderID, ProductID, Quantity, UnitPrice) VALUES 
(1, 2, 2, 9500.00),  -- 2x Roti Cokelat (19.000)
(1, 4, 1, 22000.00); -- 1x Butter Croissant (22.000)

-- Transaksi 2: Siti beli Roti Tawar (Pending)
INSERT INTO Orders (CustomerID, WorkerID, Status, TotalAmount) VALUES 
(4, NULL, 'Pending', 18000.00);

INSERT INTO OrderDetails (OrderID, ProductID, Quantity, UnitPrice) VALUES 
(2, 1, 1, 18000.00); -- 1x Roti Tawar Kupas (18.000)
GO
