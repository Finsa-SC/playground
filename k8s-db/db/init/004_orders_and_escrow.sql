BEGIN;

CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    order_number VARCHAR(40) NOT NULL UNIQUE,

    buyer_id UUID NOT NULL
        REFERENCES users(id) ON DELETE RESTRICT,

    seller_id UUID NOT NULL
        REFERENCES users(id) ON DELETE RESTRICT,

    status order_status NOT NULL DEFAULT 'pending_payment',

    currency VARCHAR(3) NOT NULL DEFAULT 'IDR',

    subtotal NUMERIC(18, 2) NOT NULL DEFAULT 0,
    shipping_fee NUMERIC(18, 2) NOT NULL DEFAULT 0,
    platform_fee NUMERIC(18, 2) NOT NULL DEFAULT 0,
    total_amount NUMERIC(18, 2) NOT NULL DEFAULT 0,

    shipping_address_snapshot JSONB NOT NULL DEFAULT '{}'::JSONB,

    paid_at TIMESTAMPTZ,
    shipped_at TIMESTAMPTZ,
    delivered_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    cancelled_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT orders_different_parties
        CHECK (buyer_id <> seller_id),

    CONSTRAINT orders_amounts_nonnegative
        CHECK (
            subtotal >= 0
            AND shipping_fee >= 0
            AND platform_fee >= 0
            AND total_amount >= 0
        ),

    CONSTRAINT orders_total_consistency
        CHECK (total_amount = subtotal + shipping_fee + platform_fee),

    CONSTRAINT orders_currency_format
        CHECK (currency ~ '^[A-Z]{3}$')
);

CREATE TABLE order_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    order_id UUID NOT NULL
        REFERENCES orders(id) ON DELETE RESTRICT,

    product_id UUID
        REFERENCES products(id) ON DELETE RESTRICT,

    -- Immutable-at-checkout snapshot fields.
    product_title VARCHAR(200) NOT NULL,
    unit_price NUMERIC(18, 2) NOT NULL,
    quantity INTEGER NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT order_items_price_nonnegative
        CHECK (unit_price >= 0),

    CONSTRAINT order_items_quantity_positive
        CHECK (quantity > 0)
);

CREATE TABLE shipments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    order_id UUID NOT NULL
        REFERENCES orders(id) ON DELETE RESTRICT,

    status shipment_status NOT NULL DEFAULT 'pending',

    carrier VARCHAR(100),
    tracking_number VARCHAR(200),

    shipped_at TIMESTAMPTZ,
    delivered_at TIMESTAMPTZ,

    return_tracking_number VARCHAR(200),
    return_shipped_at TIMESTAMPTZ,
    return_delivered_at TIMESTAMPTZ,

    metadata JSONB NOT NULL DEFAULT '{}'::JSONB,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- A record of evidence, not the video itself.
-- Keep the object private in storage and authorize access in the backend.
CREATE TABLE order_evidence (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    order_id UUID NOT NULL
        REFERENCES orders(id) ON DELETE RESTRICT,

    shipment_id UUID
        REFERENCES shipments(id) ON DELETE RESTRICT,

    uploader_id UUID
        REFERENCES users(id) ON DELETE RESTRICT,

    evidence_type evidence_type NOT NULL,

    storage_key TEXT NOT NULL,
    mime_type VARCHAR(100) NOT NULL,

    file_size_bytes BIGINT,
    checksum_sha256 VARCHAR(64) NOT NULL,

    captured_at TIMESTAMPTZ,
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    metadata JSONB NOT NULL DEFAULT '{}'::JSONB,

    CONSTRAINT order_evidence_storage_key_not_empty
        CHECK (LENGTH(TRIM(storage_key)) > 0),

    CONSTRAINT order_evidence_size_positive
        CHECK (
            file_size_bytes IS NULL OR file_size_bytes > 0
        ),

    CONSTRAINT order_evidence_checksum_format
        CHECK (checksum_sha256 ~ '^[a-fA-F0-9]{64}$')
);

-- Ledger accounts are logical accounting accounts, not real bank accounts.
CREATE TABLE ledger_accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    account_type ledger_account_type NOT NULL,

    owner_user_id UUID
        REFERENCES users(id) ON DELETE RESTRICT,

    currency VARCHAR(3) NOT NULL DEFAULT 'IDR',

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT ledger_account_currency_format
        CHECK (currency ~ '^[A-Z]{3}$'),

    CONSTRAINT ledger_account_owner_consistency
        CHECK (
            (account_type = 'user_wallet' AND owner_user_id IS NOT NULL)
            OR
            (account_type IN ('escrow', 'platform') AND owner_user_id IS NULL)
        ),

    CONSTRAINT ledger_account_unique_identity
        UNIQUE NULLS NOT DISTINCT (account_type, owner_user_id, currency)
);

CREATE TABLE ledger_transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    order_id UUID
        REFERENCES orders(id) ON DELETE RESTRICT,

    kind ledger_transaction_kind NOT NULL,

    -- Caller-generated key prevents duplicate processing on retries.
    idempotency_key VARCHAR(200) NOT NULL UNIQUE,

    currency VARCHAR(3) NOT NULL DEFAULT 'IDR',
    description TEXT,

    metadata JSONB NOT NULL DEFAULT '{}'::JSONB,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT ledger_transaction_currency_format
        CHECK (currency ~ '^[A-Z]{3}$')
);

CREATE TABLE ledger_entries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    transaction_id UUID NOT NULL
        REFERENCES ledger_transactions(id) ON DELETE RESTRICT,

    account_id UUID NOT NULL
        REFERENCES ledger_accounts(id) ON DELETE RESTRICT,

    side ledger_entry_side NOT NULL,
    amount NUMERIC(18, 2) NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT ledger_entry_amount_positive
        CHECK (amount > 0)
);

COMMIT;