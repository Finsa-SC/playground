USE LatihanCRUD_DB;
GO

TRUNCATE TABLE dbo.Notes;
GO

INSERT INTO dbo.Notes (Title, Content, IsDone) VALUES
(N'Belajar SELECT', N'Coba tampilkan semua data dari tabel Users', 1),
(N'Belajar WHERE', N'Filter data produk berdasarkan harga atau stok', 1),
(N'Latihan INSERT', N'Tambahkan 1 baris data baru ke tabel Products', 0),
(N'Latihan UPDATE', N'Ubah stok barang tertentu dengan klausa WHERE', 0),
(N'Latihan DELETE', N'Hapus data uji coba tanpa menghapus semua isi tabel', 0),
(N'Cek Stok Gudang', N'Periksa barang dengan stok di bawah 10 unit', 0),
(N'Update Harga Promo', N'Turunkan harga produk aksesoris minggu ini', 0),
(N'Nonaktifkan Akun Lama', N'Ubah IsActive menjadi 0 untuk user yang tidak aktif', 1),
(N'Rapikan Data Produk', N'Pastikan format kode Sku konsisten', 0),
(N'Backup Query Harian', N'Simpan skrip SQL latihan ke folder masing-masing', 0),
(N'Review Tipe Data', N'Pahami beda INT, NVARCHAR, DECIMAL, dan BIT', 1),
(N'Uji Coba Mandiri', N'Kerjakan studi kasus CRUD tanpa bantuan AI', 0);
GO
