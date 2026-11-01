# Open Commerce API

A modular FastAPI backend for a public, scroll-based social-commerce playground.

## Included in this first implementation

- Async PostgreSQL access with SQLAlchemy 2.x.
- Configuration via environment variables.
- JWT access tokens and rotating, revocable refresh sessions.
- Argon2 password hashing.
- Registration, login, refresh, logout, and current-user endpoints.
- Public product feed with cursor pagination.
- Seller product creation, editing, submission for moderation.
- Operator approval and rejection endpoints.
- Profile read/update endpoints.
- Local storage adapter interface for future S3-compatible storage.
- Health/readiness endpoints and basic tests.

Order settlement, escrow ledger workflows, shipment evidence, disputes, reviews, reports,
email delivery, and production object-storage integration are intentionally not represented
as completed features in this milestone. They need dedicated transactional workflows and tests.

## Requirements

- Python 3.13+
- PostgreSQL 17
- Existing database schema from `db/init/` in the companion project.

## Setup

```bash
uv sync --extra dev
cp .env.example .env
# Edit DATABASE_URL and JWT_SECRET.
uv run uvicorn app.main:app --reload
```

API docs: `http://localhost:8000/docs`

## Database note

The API maps the existing `users`, `roles`, `user_roles`, `categories`, `products`,
`product_media`, and `product_moderation_events` tables.

This API also needs `auth_sessions` for refresh-token rotation. Apply the included Alembic
migration after configuring `alembic.ini` / `DATABASE_URL`:

```bash
uv run alembic upgrade head
```

The migration is additive and does not recreate the existing init schema.

## Seed requirements

Run the SQL seed files after schema initialization. Registration assigns the `buyer` role
to new accounts. Seller and operator privileges must be granted by a trusted operator or
database administrator; public registration cannot request elevated roles.

## Security notes

- Set a cryptographically random `JWT_SECRET` in every environment.
- Use HTTPS in deployment.
- Keep `.env` out of version control.
- Local storage is for development only; private evidence storage and S3-compatible
  integration must be implemented before handling real customer evidence.
- CORS origins should be explicitly configured.
- Add rate limiting at the ingress/API gateway before public deployment.
- The dummy project does not move real money and must not be used to hold real funds.

## API overview

| Method | Path | Access |
|---|---|---|
| GET | `/health/live` | Public |
| GET | `/health/ready` | Public |
| POST | `/api/v1/auth/register` | Public |
| POST | `/api/v1/auth/login` | Public |
| POST | `/api/v1/auth/refresh` | Public |
| POST | `/api/v1/auth/logout` | Authenticated |
| GET | `/api/v1/users/me` | Authenticated |
| PATCH | `/api/v1/users/me` | Authenticated |
| GET | `/api/v1/users/{username}` | Public |
| GET | `/api/v1/feed` | Public |
| POST | `/api/v1/products` | Seller |
| GET | `/api/v1/products/{product_id}` | Public if approved; owner/operator otherwise |
| PATCH | `/api/v1/products/{product_id}` | Owner |
| POST | `/api/v1/products/{product_id}/submit` | Owner |
| GET | `/api/v1/moderation/products` | Operator |
| POST | `/api/v1/moderation/products/{product_id}/approve` | Operator |
| POST | `/api/v1/moderation/products/{product_id}/reject` | Operator |

All monetary values are represented as decimal strings by Pydantic/JSON serialization.
