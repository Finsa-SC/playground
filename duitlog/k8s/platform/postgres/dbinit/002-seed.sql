-- ============================================================================
-- DuitLog Database Seed Script (Sample Data)
-- Jalankan setelah init.sql dieksekusi
-- ============================================================================

-- 1. Seed Categories
INSERT INTO categories (id, name, type, color_hex) VALUES
    (1, 'Makan & Minum', 'EXPENSE', '#F97316'),
    (2, 'Transportasi', 'EXPENSE', '#3B82F6'),
    (3, 'Langganan Digital', 'EXPENSE', '#8B5CF6'),
    (4, 'Tagihan & Utilitas', 'EXPENSE', '#EF4444'),
    (5, 'Belanja Harian', 'EXPENSE', '#10B981'),
    (6, 'Gaji & Pemasukan', 'INCOME', '#14B8A6');

-- 2. Seed Subscriptions
INSERT INTO subscriptions
    (id, category_id, service_name, amount, billing_cycle, next_billing_date, is_active, notes)
VALUES
    (1, 3, 'Cloud VPS Server', 150000.00, 'MONTHLY', '2026-12-01', TRUE, 'Server hosting project pribadi'),
    (2, 3, 'Spotify Premium', 54990.00, 'MONTHLY', '2026-12-05', TRUE, 'Paket individual'),
    (3, 3, 'Domain .com Tahunan', 210000.00, 'YEARLY', '2027-06-15', TRUE, 'Perpanjangan domain utama'),
    (4, 4, 'Internet Fiber Rumah', 350000.00, 'MONTHLY', '2026-12-10', TRUE, 'Tagihan WiFi bulanan');

-- 3. Seed Transactions
INSERT INTO transactions
    (category_id, subscription_id, amount, tx_date, note)
VALUES
    (6, NULL, 7500000.00, '2026-11-01', 'Gaji bulan November'),
    (3, 1, 150000.00, '2026-11-01', 'Perpanjangan Cloud VPS November'),
    (3, 2, 54990.00, '2026-11-05', 'Tagihan Spotify November'),
    (4, 4, 350000.00, '2026-11-10', 'Bayar WiFi November'),
    (1, NULL, 35000.00, '2026-11-15', 'Makan siang ayam bakar + es teh'),
    (2, NULL, 50000.00, '2026-11-16', 'Isi bensin motor'),
    (5, NULL, 125000.00, '2026-11-18', 'Belanja kebutuhan mandi & kopi'),
    (1, NULL, 28000.00, '2026-11-20', 'Kopi susu & roti');
