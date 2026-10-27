-- FinSky migration 001: store stable relative keys instead of domain-specific URLs.
-- Run once against an existing database. Back up the database first.
-- This renames columns and preserves existing values; if old values are full URLs,
-- normalize those values before enabling the new media-serving code.

BEGIN;

ALTER TABLE post_media RENAME COLUMN media_url TO storage_key;
ALTER TABLE post_media
    RENAME CONSTRAINT post_media_url_not_blank TO post_media_storage_key_not_blank;

ALTER TABLE profiles RENAME COLUMN avatar_url TO avatar_key;
ALTER TABLE profiles RENAME COLUMN banner_url TO banner_key;

COMMIT;
