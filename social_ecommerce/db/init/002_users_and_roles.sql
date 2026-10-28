BEGIN;

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    email CITEXT NOT NULL UNIQUE,
    username CITEXT NOT NULL UNIQUE,
    display_name VARCHAR(100) NOT NULL,

    password_hash TEXT,

    bio TEXT,
    avatar_key TEXT,
    banner_key TEXT,

    status user_status NOT NULL DEFAULT 'active',
    email_verified_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,

    CONSTRAINT users_username_format
        CHECK (username::TEXT ~ '^[A-Za-z0-9_]{3,30}$'),

    CONSTRAINT users_email_not_empty
        CHECK (LENGTH(TRIM(email::TEXT)) > 0),

    CONSTRAINT users_display_name_not_empty
        CHECK (LENGTH(TRIM(display_name)) > 0)
);

CREATE TABLE roles (
    id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    name VARCHAR(30) NOT NULL UNIQUE,
    description TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT roles_name_valid
        CHECK (name IN ('buyer', 'seller', 'op'))
);

CREATE TABLE user_roles (
    user_id UUID NOT NULL
        REFERENCES users(id) ON DELETE RESTRICT,

    role_id SMALLINT NOT NULL
        REFERENCES roles(id) ON DELETE RESTRICT,

    granted_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    granted_by UUID
        REFERENCES users(id) ON DELETE SET NULL,

    PRIMARY KEY (user_id, role_id)
);

-- Record who performed sensitive actions.
-- Application authorization must still enforce permissions.
CREATE TABLE user_security_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    user_id UUID
        REFERENCES users(id) ON DELETE SET NULL,

    actor_user_id UUID
        REFERENCES users(id) ON DELETE SET NULL,

    event_type VARCHAR(80) NOT NULL,
    ip_address INET,
    user_agent TEXT,
    metadata JSONB NOT NULL DEFAULT '{}'::JSONB,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

COMMIT;