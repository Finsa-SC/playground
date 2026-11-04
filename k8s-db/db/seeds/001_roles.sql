BEGIN;

INSERT INTO roles (name, description)
VALUES
    ('buyer', 'Can browse products and participate in purchases.'),
    ('seller', 'Can create and manage product listings.'),
    ('op', 'Application operator responsible for moderation and disputes.')
ON CONFLICT (name)
DO UPDATE SET
    description = EXCLUDED.description;

COMMIT;