-- Buat database kalau belum ada
IF DB_ID(N'LatihanCRUD_DB') IS NULL
BEGIN
    CREATE DATABASE LatihanCRUD_DB;
END
GO

USE LatihanCRUD_DB;
GO

-- 1. Tabel Users (tanpa FK)
IF OBJECT_ID(N'dbo.Users', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Users (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Username NVARCHAR(50) NOT NULL,
        FullName NVARCHAR(100) NOT NULL,
        Role NVARCHAR(30) NOT NULL,
        IsActive BIT NOT NULL DEFAULT 1
    );
END
GO

-- 2. Tabel Products (tanpa FK)
IF OBJECT_ID(N'dbo.Products', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Products (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Sku NVARCHAR(30) NOT NULL,
        Name NVARCHAR(100) NOT NULL,
        Price DECIMAL(10,2) NOT NULL,
        Stock INT NOT NULL
    );
END
GO

-- 3. Tabel Notes / Todo (tanpa FK)
IF OBJECT_ID(N'dbo.Notes', N'U') IS NULL
BEGIN
    CREATE TABLE dbo.Notes (
        Id INT IDENTITY(1,1) PRIMARY KEY,
        Title NVARCHAR(120) NOT NULL,
        Content NVARCHAR(300) NULL,
        IsDone BIT NOT NULL DEFAULT 0
    );
END
GO
