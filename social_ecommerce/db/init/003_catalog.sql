BEGIN;

CREATE TABLE categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    parent_id UUID
        REFERENCES categories(id) ON DELETE RESTRICT,

    name VARCHAR(100) NOT NULL,
    slug CITEXT NOT NULL UNIQUE,
    description TEXT,

    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT categories_name_not_empty
        CHECK (LENGTH(TRIM(name)) > 0),

    CONSTRAINT categories_not_own_parent
        CHECK (parent_id IS NULL OR parent_id <> id)
);

CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    seller_id UUID NOT NULL
        REFERENCES users(id) ON DELETE RESTRICT,

    category_id UUID
        REFERENCES categories(id) ON DELETE RESTRICT,

    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL DEFAULT '',

    price NUMERIC(18, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'IDR',
    stock_quantity INTEGER NOT NULL DEFAULT 1,

    status product_status NOT NULL DEFAULT 'draft',

    submitted_at TIMESTAMPTZ,
    approved_at TIMESTAMPTZ,
    approved_by UUID
        REFERENCES users(id) ON DELETE SET NULL,

    rejection_reason TEXT,

    published_at TIMESTAMPTZ,
    archived_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT products_title_not_empty
        CHECK (LENGTH(TRIM(title)) > 0),

    CONSTRAINT products_price_nonnegative
        CHECK (price >= 0),

    CONSTRAINT products_stock_nonnegative
        CHECK (stock_quantity >= 0),

    CONSTRAINT products_currency_format
        CHECK (currency ~ '^[A-Z]{3}$'),

    CONSTRAINT products_approval_consistency
        CHECK (
            status <> 'approved'
            OR (
                approved_at IS NOT NULL
                AND approved_by IS NOT NULL
                AND published_at IS NOT NULL
            )
        )
);

CREATE TABLE product_media (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    product_id UUID NOT NULL
        REFERENCES products(id) ON DELETE RESTRICT,

    media_type media_type NOT NULL,
    storage_key TEXT NOT NULL,
    mime_type VARCHAR(100) NOT NULL,

    original_filename TEXT,
    file_size_bytes BIGINT,
    checksum_sha256 VARCHAR(64),

    width INTEGER,
    height INTEGER,
    duration_seconds NUMERIC(12, 3),

    position INTEGER NOT NULL DEFAULT 0,
    alt_text TEXT,

    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    verified_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT product_media_storage_key_not_empty
        CHECK (LENGTH(TRIM(storage_key)) > 0),

    CONSTRAINT product_media_size_positive
        CHECK (
            file_size_bytes IS NULL OR file_size_bytes > 0
        ),

    CONSTRAINT product_media_dimensions_positive
        CHECK (
            (width IS NULL OR width > 0)
            AND (height IS NULL OR height > 0)
        ),

    CONSTRAINT product_media_duration_nonnegative
        CHECK (
            duration_seconds IS NULL OR duration_seconds >= 0
        ),

    CONSTRAINT product_media_position_nonnegative
        CHECK (position >= 0),

    CONSTRAINT product_media_checksum_format
        CHECK (
            checksum_sha256 IS NULL
            OR checksum_sha256 ~ '^[a-fA-F0-9]{64}$'
        )
);

CREATE TABLE product_moderation_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    product_id UUID NOT NULL
        REFERENCES products(id) ON DELETE RESTRICT,

    moderator_id UUID
        REFERENCES users(id) ON DELETE SET NULL,

    action moderation_action NOT NULL,
    reason TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::JSONB,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMIT;