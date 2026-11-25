-- Create Database (opsional, sesuaikan jika database sudah ada)
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'TokoRotiDB')
BEGIN
    CREATE DATABASE TokoRotiDB;
END
GO

USE TokoRotiDB;
GO

-- --------------------------------------------------
-- Drop Tables (jika ingin reset ulang, jalankan urut)
-- --------------------------------------------------
DROP TABLE IF EXISTS OrderDetails;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Roles;
GO

-- --------------------------------------------------
-- 1. Tabel Roles
-- --------------------------------------------------
CREATE TABLE Roles (
    RoleID INT IDENTITY(1,1) PRIMARY KEY,
    RoleName VARCHAR(50) NOT NULL UNIQUE, -- 'Worker' / 'Customer'
    Description NVARCHAR(255) NULL
);
GO

-- --------------------------------------------------
-- 2. Tabel Users
-- --------------------------------------------------
CREATE TABLE Users (
    UserID INT IDENTITY(1,1) PRIMARY KEY,
    RoleID INT NOT NULL,
    FullName NVARCHAR(100) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    PasswordHash VARCHAR(255) NOT NULL,
    PhoneNumber VARCHAR(20) NULL,
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (RoleID) REFERENCES Roles(RoleID)
);
GO

-- --------------------------------------------------
-- 3. Tabel Categories (Kategori Roti)
-- --------------------------------------------------
CREATE TABLE Categories (
    CategoryID INT IDENTITY(1,1) PRIMARY KEY,
    CategoryName NVARCHAR(100) NOT NULL UNIQUE,
    Description NVARCHAR(255) NULL
);
GO

-- --------------------------------------------------
-- 4. Tabel Products (Roti & Pastry)
-- --------------------------------------------------
CREATE TABLE Products (
    ProductID INT IDENTITY(1,1) PRIMARY KEY,
    CategoryID INT NOT NULL,
    ProductName NVARCHAR(150) NOT NULL,
    Description NVARCHAR(MAX) NULL,
    Price DECIMAL(18,2) NOT NULL CHECK (Price >= 0),
    Stock INT NOT NULL DEFAULT 0 CHECK (Stock >= 0),
    ImagePath NVARCHAR(500) NULL, -- Path ke file gambar (misal: /uploads/products/roti-tawar.png)
    IsActive BIT DEFAULT 1,
    CreatedAt DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);
GO

-- --------------------------------------------------
-- 5. Tabel Orders (Header Transaksi)
-- --------------------------------------------------
CREATE TABLE Orders (
    OrderID INT IDENTITY(1,1) PRIMARY KEY,
    CustomerID INT NOT NULL,
    WorkerID INT NULL, -- Worker/Admin yang memproses pesanan
    OrderDate DATETIME2 DEFAULT GETDATE(),
    Status VARCHAR(50) DEFAULT 'Pending', -- Pending, Processing, Completed, Cancelled
    TotalAmount DECIMAL(18,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (CustomerID) REFERENCES Users(UserID),
    FOREIGN KEY (WorkerID) REFERENCES Users(UserID)
);
GO

-- --------------------------------------------------
-- 6. Tabel OrderDetails (Item Transaksi)
-- --------------------------------------------------
CREATE TABLE OrderDetails (
    OrderDetailID INT IDENTITY(1,1) PRIMARY KEY,
    OrderID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL CHECK (Quantity > 0),
    UnitPrice DECIMAL(18,2) NOT NULL,
    Subtotal AS (Quantity * UnitPrice), -- Calculated column
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID) ON DELETE CASCADE,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
GO
