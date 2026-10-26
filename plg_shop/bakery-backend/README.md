# Bakery Shop API

A starter REST API for a bakery shop using FastAPI, PostgreSQL, SQLAlchemy, JWT access tokens, rotating refresh tokens, role-based authorization, and server-side image storage.

## Features

- Public product/category reads
- Customer registration and login
- Short-lived JWT access tokens and opaque, hashed, rotating refresh tokens
- Roles: `customer`, `owner`, `admin`; public registration can only create customers
- Owner/admin product and category management
- Product images stored on the server; only public URLs and metadata are stored in PostgreSQL
- Image validation using Pillow (JPEG, PNG, WEBP; 5 MB default)
- Docker Compose for local deployment
- SQL schema and repeatable starter seed data

## Start locally with Docker

1. Copy `.env.example` to `.env`.
2. Set `POSTGRES_PASSWORD` in `.env` to a strong, unique password. Also set `DATABASE_URL`'s password consistently if running without Compose; Compose overrides it for the container.
3. Generate a long secret for `JWT_SECRET_KEY`, for example with `openssl rand -hex 32`.
4. Start services: `docker compose up --build -d`.
5. Apply `sql/init.sql` to the database once, then optionally `sql/seed.sql`.

For a new empty Compose database, you can initialize schema and seed data using:

```sh
docker compose exec -T db psql -U bakery_app -d bakery_shop < sql/init.sql
docker compose exec -T db psql -U bakery_app -d bakery_shop < sql/seed.sql
```

`sql/init.sql` is for a fresh database only. For future schema changes, use Alembic migrations; do not repeatedly run the init script on an existing database.

## Create the first owner

After initializing the schema, run the script inside the API container with a strong password. Avoid placing secrets in shell history on a shared machine.

```sh
docker compose exec -e OWNER_EMAIL=owner@example.com -e OWNER_NAME='Bakery Owner' -e OWNER_PASSWORD='replace-with-a-long-unique-password' api python -m scripts.create_owner
```

Do not expose an endpoint that allows users to choose their own role. The public registration endpoint always assigns `customer`.

## API endpoints

Prefix: `/api/v1`

| Method | Path | Access | Purpose |
|---|---|---|---|
| POST | `/auth/register` | Public | Register customer |
| POST | `/auth/login` | Public | Login and receive tokens |
| POST | `/auth/refresh` | Refresh token | Rotate refresh token |
| POST | `/auth/logout` | Authenticated | Revoke refresh token |
| GET | `/auth/me` | Authenticated | Current account |
| GET | `/categories` | Public | List categories |
| POST | `/categories` | Owner/admin | Create category |
| GET | `/products` | Public | List products, optional `search`, `category_id`, `page`, `page_size` |
| GET | `/products/{id}` | Public | Product details |
| POST | `/products` | Owner/admin | Create product |
| PATCH | `/products/{id}` | Owner/admin | Update product |
| DELETE | `/products/{id}` | Owner/admin | Hide product from public catalog |
| POST | `/orders` | Authenticated | Create order; validates stock and calculates totals server-side |
| GET | `/orders/mine` | Authenticated | List own orders |
| GET | `/orders` | Owner/admin | List all orders |
| PATCH | `/orders/{id}` | Owner/admin | Update order status |
| POST | `/products/{id}/images` | Owner/admin | Upload product image (`multipart/form-data`: `file`, optional `alt_text`, `is_primary`) |
| DELETE | `/products/{id}/images/{image_id}` | Owner/admin | Delete image record and local file |
| GET | `/health` | Public | Liveness check |

Interactive docs are at `/docs` in development mode. Set `ENVIRONMENT=production` to disable docs.

## Token use

Send `Authorization: Bearer <access_token>` to protected endpoints. Access tokens expire quickly; use the refresh token endpoint to rotate refresh tokens. Store refresh tokens in a secure, HttpOnly, Secure, SameSite cookie in a browser-based production deployment rather than localStorage. Add CSRF protection if cookies are used. Keep `JWT_SECRET_KEY` private and rotate it through a planned process.

## Images

Images are stored in `IMAGE_STORAGE_DIR` with random filenames. The database stores a URL in `product_images.url`, not binary data. Configure `PUBLIC_BASE_URL` to the API's externally reachable base URL. The local static route is suitable for a small deployment; for larger production workloads, consider object storage/CDN, backups, image re-encoding, malware scanning, and a cleanup job for orphaned files.

## Production checklist before public launch

- Put the API behind HTTPS and a reverse proxy; do not expose the database port publicly.
- Use a dedicated DB account with only the permissions needed by the application; use a separate migration account for schema changes.
- Use Alembic migrations rather than `create_all` or rerunning `init.sql`.
- Add payment-provider integration, idempotency keys, and a stricter tested order-state transition policy before accepting real orders.
- Add rate limiting for login/register, audit logging, monitoring, backups and restore tests, and automated tests.
- Set exact CORS origins, secrets, storage permissions, and production environment values.
- Run the app as a non-root user (Dockerfile does this) and keep dependencies updated.

This is a production-oriented starter, not a claim that all production requirements are complete. Checkout/payments, password reset/email verification, rate limiting, audit events, automated migrations, and comprehensive tests remain to be implemented before launch.
