BEGIN;

CREATE TABLE disputes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    order_id UUID NOT NULL UNIQUE
        REFERENCES orders(id) ON DELETE RESTRICT,

    opened_by UUID NOT NULL
        REFERENCES users(id) ON DELETE RESTRICT,

    status dispute_status NOT NULL DEFAULT 'open',

    reason VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,

    assigned_operator_id UUID
        REFERENCES users(id) ON DELETE SET NULL,

    resolution dispute_resolution,
    resolution_notes TEXT,

    resolved_by UUID
        REFERENCES users(id) ON DELETE SET NULL,

    resolved_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT disputes_description_not_empty
        CHECK (LENGTH(TRIM(description)) > 0),

    CONSTRAINT disputes_resolution_consistency
        CHECK (
            (
                status IN ('resolved', 'closed')
                AND resolution IS NOT NULL
                AND resolved_at IS NOT NULL
            )
            OR
            (
                status NOT IN ('resolved', 'closed')
                AND resolution IS NULL
                AND resolved_at IS NULL
            )
        )
);

CREATE TABLE dispute_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    dispute_id UUID NOT NULL
        REFERENCES disputes(id) ON DELETE RESTRICT,

    actor_user_id UUID
        REFERENCES users(id) ON DELETE SET NULL,

    event_type VARCHAR(80) NOT NULL,
    message TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::JSONB,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    order_id UUID NOT NULL
        REFERENCES orders(id) ON DELETE RESTRICT,

    reviewer_id UUID NOT NULL
        REFERENCES users(id) ON DELETE RESTRICT,

    target_user_id UUID
        REFERENCES users(id) ON DELETE RESTRICT,

    target_type review_target_type NOT NULL,

    product_id UUID
        REFERENCES products(id) ON DELETE RESTRICT,

    rating SMALLINT NOT NULL,
    body TEXT,

    is_visible BOOLEAN NOT NULL DEFAULT TRUE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT reviews_rating_range
        CHECK (rating BETWEEN 1 AND 5),

    CONSTRAINT reviews_target_consistency
        CHECK (
            (
                target_type IN ('buyer', 'seller')
                AND target_user_id IS NOT NULL
                AND product_id IS NULL
                AND reviewer_id <> target_user_id
            )
            OR
            (
                target_type = 'product'
                AND target_user_id IS NULL
                AND product_id IS NOT NULL
            )
        ),

    CONSTRAINT reviews_unique_user_target
        UNIQUE NULLS NOT DISTINCT (
            order_id,
            reviewer_id,
            target_type,
            target_user_id,
            product_id
        )
);

CREATE TABLE reports (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    reporter_id UUID NOT NULL
        REFERENCES users(id) ON DELETE RESTRICT,

    target_type report_target_type NOT NULL,

    target_user_id UUID
        REFERENCES users(id) ON DELETE RESTRICT,

    product_id UUID
        REFERENCES products(id) ON DELETE RESTRICT,

    review_id UUID
        REFERENCES reviews(id) ON DELETE RESTRICT,

    order_id UUID
        REFERENCES orders(id) ON DELETE RESTRICT,

    reason VARCHAR(100) NOT NULL,
    description TEXT,

    status report_status NOT NULL DEFAULT 'open',

    assigned_operator_id UUID
        REFERENCES users(id) ON DELETE SET NULL,

    resolution_notes TEXT,
    resolved_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT reports_target_consistency
        CHECK (
            (
                target_type = 'user'
                AND target_user_id IS NOT NULL
                AND product_id IS NULL
                AND review_id IS NULL
                AND order_id IS NULL
            )
            OR
            (
                target_type = 'product'
                AND target_user_id IS NULL
                AND product_id IS NOT NULL
                AND review_id IS NULL
                AND order_id IS NULL
            )
            OR
            (
                target_type = 'review'
                AND target_user_id IS NULL
                AND product_id IS NULL
                AND review_id IS NOT NULL
                AND order_id IS NULL
            )
            OR
            (
                target_type = 'order'
                AND target_user_id IS NULL
                AND product_id IS NULL
                AND review_id IS NULL
                AND order_id IS NOT NULL
            )
        ),

    CONSTRAINT reports_resolution_consistency
        CHECK (
            (
                status IN ('resolved', 'dismissed')
                AND resolved_at IS NOT NULL
            )
            OR
            (
                status IN ('open', 'investigating')
                AND resolved_at IS NULL
            )
        )
);

COMMIT;