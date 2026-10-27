-- FinSky social media database schema
-- PostgreSQL 16+
-- Run once against a fresh database. Keep application-level validation in the API too.

BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS users (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email           TEXT NOT NULL,
    username        TEXT NOT NULL,
    password_hash   TEXT NOT NULL,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified     BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT users_email_not_blank CHECK (length(trim(email)) > 0),
    CONSTRAINT users_username_format CHECK (
        username ~ '^[A-Za-z0-9_]{3,30}$'
    ),
    CONSTRAINT users_password_hash_not_blank CHECK (length(password_hash) > 0)
);

-- Case-insensitive uniqueness without requiring the citext extension.
CREATE UNIQUE INDEX IF NOT EXISTS users_email_lower_uq
    ON users (lower(email));
CREATE UNIQUE INDEX IF NOT EXISTS users_username_lower_uq
    ON users (lower(username));

CREATE TABLE IF NOT EXISTS profiles (
    user_id         UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    display_name    VARCHAR(50) NOT NULL,
    bio             VARCHAR(280),
    avatar_url      TEXT,
    banner_url      TEXT,
    website_url     TEXT,
    location        VARCHAR(100),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT profiles_display_name_not_blank CHECK (length(trim(display_name)) > 0)
);

CREATE TABLE IF NOT EXISTS posts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    author_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    content         VARCHAR(5000),
    visibility      TEXT NOT NULL DEFAULT 'public'
                    CHECK (visibility IN ('public', 'followers')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    edited_at       TIMESTAMPTZ,
    deleted_at      TIMESTAMPTZ,

    -- A post must contain text or at least one media item. Enforced by the API
    -- because the media rows live in a separate table.
    CONSTRAINT posts_content_length CHECK (
        content IS NULL OR length(content) <= 5000
    )
);

CREATE INDEX IF NOT EXISTS posts_author_created_idx
    ON posts (author_id, created_at DESC)
    WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS posts_public_created_idx
    ON posts (created_at DESC)
    WHERE deleted_at IS NULL AND visibility = 'public';

CREATE TABLE IF NOT EXISTS post_media (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id         UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    media_type      TEXT NOT NULL CHECK (media_type IN ('image', 'video')),
    media_url       TEXT NOT NULL,
    alt_text        VARCHAR(500),
    mime_type       VARCHAR(100),
    file_size_bytes BIGINT CHECK (file_size_bytes IS NULL OR file_size_bytes >= 0),
    width           INTEGER CHECK (width IS NULL OR width > 0),
    height          INTEGER CHECK (height IS NULL OR height > 0),
    duration_seconds NUMERIC(10, 3) CHECK (
        duration_seconds IS NULL OR duration_seconds >= 0
    ),
    position        SMALLINT NOT NULL DEFAULT 0 CHECK (position >= 0),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    CONSTRAINT post_media_url_not_blank CHECK (length(trim(media_url)) > 0),
    CONSTRAINT post_media_video_duration CHECK (
        media_type = 'video' OR duration_seconds IS NULL
    ),
    CONSTRAINT post_media_post_position_uq UNIQUE (post_id, position)
);

CREATE INDEX IF NOT EXISTS post_media_post_idx ON post_media (post_id, position);

CREATE TABLE IF NOT EXISTS follows (
    follower_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    followed_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (follower_id, followed_id),
    CONSTRAINT follows_no_self_follow CHECK (follower_id <> followed_id)
);

CREATE INDEX IF NOT EXISTS follows_followed_idx
    ON follows (followed_id, created_at DESC);

CREATE TABLE IF NOT EXISTS post_likes (
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    post_id         UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    PRIMARY KEY (user_id, post_id)
);

CREATE INDEX IF NOT EXISTS post_likes_post_idx
    ON post_likes (post_id, created_at DESC);

CREATE TABLE IF NOT EXISTS comments (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id         UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
    author_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    parent_comment_id UUID REFERENCES comments(id) ON DELETE CASCADE,
    content         VARCHAR(2000) NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    edited_at       TIMESTAMPTZ,
    deleted_at      TIMESTAMPTZ,

    CONSTRAINT comments_content_not_blank CHECK (length(trim(content)) > 0)
);

CREATE INDEX IF NOT EXISTS comments_post_created_idx
    ON comments (post_id, created_at ASC)
    WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS comments_author_created_idx
    ON comments (author_id, created_at DESC)
    WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS comments_parent_idx
    ON comments (parent_comment_id)
    WHERE parent_comment_id IS NOT NULL;

COMMIT;
