
-- FinSky development seed
-- Requires 01-schema.sql and 02-media_storage_keys.sql to have run.
-- Test accounts only. Do not use these credentials in production.

BEGIN;

-- 1. USERS
INSERT INTO users (
    id,
    email,
    username,
    password_hash,
    is_active,
    is_verified
)
VALUES
    (
        '10000000-0000-4000-8000-000000000001',
        'suzuka@example.test',
        'suzuka',
        '$argon2id$v=19$m=65536,t=3,p=4$M04u2P4RXL0fC/4WqvJRKA$zilGBsg+IyPm9xfmrAhjNrcBTzUHWLEhWJEcutVfdAI',
        TRUE, TRUE
    ),
    (
        '10000000-0000-4000-8000-000000000002',
        'elaina@example.test',
        'elaina',
        '$argon2id$v=19$m=65536,t=3,p=4$fALLCXh+FvfsVs1aZKHd0g$Ce1bkaGasEAFYW6ANY3xMzRxJe2tKxbvnFAsXzs13uQ',
        TRUE, TRUE
    ),
    (
        '10000000-0000-4000-8000-000000000003',
        'acute@example.test',
        'wonder_acute',
        '$argon2id$v=19$m=65536,t=3,p=4$GUe4oojiqWwMh/sSdRlYBQ$uHGIkobfXIce0n3pDqBpCY8HxLL6EODEoluKOF+ArYM',
        TRUE, TRUE
    )
ON CONFLICT (id) DO UPDATE SET
    email = EXCLUDED.email,
    username = EXCLUDED.username,
    password_hash = EXCLUDED.password_hash,
    is_active = EXCLUDED.is_active,
    is_verified = EXCLUDED.is_verified,
    updated_at = NOW();


-- 2. PROFILES
-- Uses avatar_key/banner_key after migration 02.

INSERT INTO profiles (
    user_id,
    display_name,
    bio,
    avatar_key,
    banner_key,
    website_url,
    location
)
VALUES
    (
        '10000000-0000-4000-8000-000000000001',
        'Silence Suzuka',
        'Running toward the horizon. 🏇',
        NULL, NULL,
        'https://example.test/suzuka',
        'Japan'
    ),
    (
        '10000000-0000-4000-8000-000000000002',
        'Elaina',
        'A traveling witch, collecting stories along the way.',
        NULL, NULL, NULL,
        'Somewhere'
    ),
    (
        '10000000-0000-4000-8000-000000000003',
        'Wonder Acute',
        'A little kindness can change a whole day.',
        NULL, NULL, NULL,
        'Japan'
    )
ON CONFLICT (user_id) DO UPDATE SET
    display_name = EXCLUDED.display_name,
    bio = EXCLUDED.bio,
    avatar_key = EXCLUDED.avatar_key,
    banner_key = EXCLUDED.banner_key,
    website_url = EXCLUDED.website_url,
    location = EXCLUDED.location,
    updated_at = NOW();


-- 3. POSTS
INSERT INTO posts (
    id,
    author_id,
    content,
    visibility
)
VALUES
    (
        '20000000-0000-4000-8000-000000000001',
        '10000000-0000-4000-8000-000000000001',
        'The wind is perfect today. Time to run toward the horizon! 🏇',
        'public'
    ),
    (
        '20000000-0000-4000-8000-000000000002',
        '10000000-0000-4000-8000-000000000002',
        'Another journey, another story. I wonder what awaits me today.',
        'public'
    ),
    (
        '20000000-0000-4000-8000-000000000003',
        '10000000-0000-4000-8000-000000000003',
        'Remember to be kind to yourself and to the people around you.',
        'public'
    ),
    (
        '20000000-0000-4000-8000-000000000004',
        '10000000-0000-4000-8000-000000000001',
        'A quiet moment before the next race.',
        'followers'
    ),
    (
        '20000000-0000-4000-8000-000000000005',
        '10000000-0000-4000-8000-000000000002',
        'Some stories are better when shared with friends.',
        'public'
    )
ON CONFLICT (id) DO UPDATE SET
    author_id = EXCLUDED.author_id,
    content = EXCLUDED.content,
    visibility = EXCLUDED.visibility,
    updated_at = NOW();


-- 4. FOLLOWS
INSERT INTO follows (follower_id, followed_id)
VALUES
    (
        '10000000-0000-4000-8000-000000000001',
        '10000000-0000-4000-8000-000000000002'
    ),
    (
        '10000000-0000-4000-8000-000000000002',
        '10000000-0000-4000-8000-000000000001'
    ),
    (
        '10000000-0000-4000-8000-000000000003',
        '10000000-0000-4000-8000-000000000001'
    ),
    (
        '10000000-0000-4000-8000-000000000003',
        '10000000-0000-4000-8000-000000000002'
    )
ON CONFLICT (follower_id, followed_id) DO NOTHING;


-- 5. POST LIKES
INSERT INTO post_likes (user_id, post_id)
VALUES
    (
        '10000000-0000-4000-8000-000000000002',
        '20000000-0000-4000-8000-000000000001'
    ),
    (
        '10000000-0000-4000-8000-000000000003',
        '20000000-0000-4000-8000-000000000001'
    ),
    (
        '10000000-0000-4000-8000-000000000001',
        '20000000-0000-4000-8000-000000000002'
    ),
    (
        '10000000-0000-4000-8000-000000000001',
        '20000000-0000-4000-8000-000000000003'
    )
ON CONFLICT (user_id, post_id) DO NOTHING;


-- 6. COMMENTS
INSERT INTO comments (
    id,
    post_id,
    author_id,
    content
)
VALUES
    (
        '30000000-0000-4000-8000-000000000001',
        '20000000-0000-4000-8000-000000000001',
        '10000000-0000-4000-8000-000000000002',
        'Good luck on your run, Suzuka!'
    ),
    (
        '30000000-0000-4000-8000-000000000002',
        '20000000-0000-4000-8000-000000000001',
        '10000000-0000-4000-8000-000000000003',
        'Keep chasing your dreams! ✨'
    ),
    (
        '30000000-0000-4000-8000-000000000003',
        '20000000-0000-4000-8000-000000000002',
        '10000000-0000-4000-8000-000000000001',
        'Looking forward to hearing about your next adventure.'
    )
ON CONFLICT (id) DO UPDATE SET
    post_id = EXCLUDED.post_id,
    author_id = EXCLUDED.author_id,
    content = EXCLUDED.content,
    updated_at = NOW();

COMMIT;
