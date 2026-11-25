USE LatihanCRUD_DB;
GO

TRUNCATE TABLE dbo.Products;
GO

INSERT INTO dbo.Products (Sku, Name, Price, Stock) VALUES
(N'PRD-001', N'Mouse Wireless', 125000.00, 20),
(N'PRD-002', N'Keyboard Mechanical', 450000.00, 12),
(N'PRD-003', N'Monitor 24 Inch', 1650000.00, 6),
(N'PRD-004', N'Flashdisk 32GB', 65000.00, 35),
(N'PRD-005', N'Kabel HDMI 2M', 45000.00, 40),
(N'PRD-006', N'Headset Gaming', 320000.00, 10),
(N'PRD-007', N'Mousepad XL', 85000.00, 25),
(N'PRD-008', N'Webcam HD', 275000.00, 8),
(N'PRD-009', N'USB Hub 4 Port', 95000.00, 18),
(N'PRD-010', N'Stand Laptop', 150000.00, 15),
(N'PRD-011', N'SSD SATA 256GB', 380000.00, 9),
(N'PRD-012', N'Kabel LAN Cat6 5M', 35000.00, 50);
GO
