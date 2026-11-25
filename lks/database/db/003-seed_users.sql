USE LatihanCRUD_DB;
GO

TRUNCATE TABLE dbo.Users;
GO

INSERT INTO dbo.Users (Username, FullName, Role, IsActive) VALUES
(N'andi01', N'Andi Pratama', N'Admin', 1),
(N'budi02', N'Budi Santoso', N'Staff', 1),
(N'citra03', N'Citra Lestari', N'Staff', 1),
(N'dimas04', N'Dimas Saputra', N'Member', 1),
(N'eka05', N'Eka Wijaya', N'Member', 0),
(N'fajar06', N'Fajar Nugroho', N'Staff', 1),
(N'gita07', N'Gita Permata', N'Member', 1),
(N'hadi08', N'Hadi Kusuma', N'Member', 0),
(N'indah09', N'Indah Rahmawati', N'Staff', 1),
(N'joko10', N'Joko Susilo', N'Member', 1),
(N'kartika11', N'Kartika Sari', N'Admin', 1),
(N'lukman12', N'Lukman Hakim', N'Member', 0);
GO
