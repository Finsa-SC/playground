BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE EXTENSION IF NOT EXISTS citext;

-- User and account lifecycle
CREATE TYPE user_status AS ENUM (
    'active',
    'suspended',
    'disabled',
    'pending_verification'
);

-- Product moderation lifecycle
CREATE TYPE product_status AS ENUM (
    'draft',
    'pending',
    'approved',
    'rejected',
    'suspended',
    'archived'
);

CREATE TYPE moderation_action AS ENUM (
    'submitted',
    'approved',
    'rejected',
    'suspended',
    'reinstated'
);

-- Media
CREATE TYPE media_type AS ENUM (
    'image',
    'video'
);

CREATE TYPE evidence_type AS ENUM (
    'packing',
    'shipping',
    'delivery',
    'unboxing',
    'return_packing',
    'return_shipping',
    'return_unboxing',
    'other'
);

-- Order and shipment lifecycle
CREATE TYPE order_status AS ENUM (
    'pending_payment',
    'paid',
    'processing',
    'shipped',
    'delivered',
    'inspection',
    'completed',
    'disputed',
    'return_requested',
    'return_shipped',
    'refunded',
    'cancelled',
    'expired'
);

CREATE TYPE shipment_status AS ENUM (
    'pending',
    'packed',
    'shipped',
    'in_transit',
    'delivered',
    'return_requested',
    'return_shipped',
    'return_delivered',
    'lost',
    'cancelled'
);

-- Escrow and accounting
CREATE TYPE ledger_account_type AS ENUM (
    'user_wallet',
    'escrow',
    'platform'
);

CREATE TYPE ledger_entry_side AS ENUM (
    'debit',
    'credit'
);

CREATE TYPE ledger_transaction_kind AS ENUM (
    'dummy_deposit',
    'escrow_fund',
    'escrow_release',
    'buyer_refund',
    'seller_refund',
    'platform_fee',
    'adjustment'
);

-- Reviews and moderation reports
CREATE TYPE review_target_type AS ENUM (
    'buyer',
    'seller',
    'product'
);

CREATE TYPE report_target_type AS ENUM (
    'user',
    'product',
    'review',
    'order'
);

CREATE TYPE report_status AS ENUM (
    'open',
    'investigating',
    'resolved',
    'dismissed'
);

-- Dispute resolution
CREATE TYPE dispute_status AS ENUM (
    'open',
    'investigating',
    'awaiting_evidence',
    'resolved',
    'closed'
);

CREATE TYPE dispute_resolution AS ENUM (
    'release_to_seller',
    'refund_to_buyer',
    'partial_refund',
    'return_to_seller',
    'cancel_order',
    'other'
);

COMMIT;