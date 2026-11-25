USE master;
GO

-- 0. Buat database 'LatihanCRUD_DB' kalau belum ada
IF DB_ID(N'LatihanCRUD_DB') IS NULL
BEGIN
    CREATE DATABASE [LatihanCRUD_DB];
END
GO

-- 1. Buat Server Login 'siswa' (kalau belum ada)
IF SUSER_ID(N'siswa') IS NULL
BEGIN
    CREATE LOGIN siswa WITH PASSWORD = N'LatihanSQL#2026', CHECK_POLICY = OFF;
END
GO

USE [LatihanCRUD_DB];
GO

-- 2. Buat Database User 'siswa' untuk Login tersebut
IF USER_ID(N'siswa') IS NULL
BEGIN
    CREATE USER siswa FOR LOGIN siswa;
END
GO

-- 3. Kasih izin baca & tulis data saja (SELECT, INSERT, UPDATE, DELETE)
ALTER ROLE db_datareader ADD MEMBER siswa;
ALTER ROLE db_datawriter ADD MEMBER siswa;
GO
