# Crumb & Cocoa — Bakery Frontend

A responsive, modular vanilla HTML/CSS/JavaScript frontend for the FastAPI bakery backend. The entry point is `index.html`; scripts are ES modules under `assets/js/`.

## Features

- Chocolate-brown, cream, and white visual theme; responsive desktop/mobile layout
- Public product catalog, search, category filters, stock indicators, product photos
- Shopping bag with quantity controls and subtotal
- Customer registration/login, access-token auth, refresh-token retry, sign out
- Customer order history
- Owner/admin workspace: create/edit/hide products, upload product images, create categories, review orders, update order status
- Checkout creates an order using the backend's `POST /api/v1/orders` endpoint. **No payment is charged or processed** because the backend currently has no payment-provider integration.

## API integration

The JavaScript API client in `assets/js/api.js` uses the exact relative prefix `/api/v1` and the backend routes:

- `/auth/register`, `/auth/login`, `/auth/refresh`, `/auth/logout`, `/auth/me`
- `/categories`, `/products`, `/products/{id}`, `/products/{id}/images`
- `/orders`, `/orders/mine`, `/orders/{id}`

The frontend expects to be served from the **same origin** as the API, or behind a reverse proxy that forwards `/api/` and `/media/` to the backend. This keeps API requests at `/api/v1` as requested and avoids hardcoding a development hostname.

## Run with Docker

Build the frontend image from this directory:

```sh
docker build -t bakery-frontend .
docker run --rm -p 8080:80 --network YOUR_BAKERY_COMPOSE_NETWORK bakery-frontend
```

The included `nginx.conf` proxies API and image requests to the Docker hostname `bakery-backend:8000`. The backend container must be reachable by that name on the same Docker network. If your backend has a different Docker DNS name, update both `proxy_pass` directives in `nginx.conf` and rebuild the image.

Open `http://localhost:8080`.

Alternatively, add the frontend as a service in the same Compose project as the backend so it joins the same default network. Example service snippet (adjust the backend service dependency to match your Compose file):

```yaml
frontend:
  build: ./bakery-frontend
  ports:
    - "8080:80"
  depends_on:
    - backend
```

The Compose **service name** in `depends_on` may be `api` or something else in your project. The proxy hostname must resolve to the backend container (`bakery-backend` in the logs you shared).

## Important integration notes

- The backend currently returns only available products from `GET /api/v1/products`. A product hidden with the backend's soft-delete endpoint will no longer appear in this admin list; the backend does not currently expose an all-products management endpoint.
- The backend currently has no payment endpoint. Checkout submits an order and the backend deducts stock, with initial status `pending`. Do not treat this as proof of payment.
- The backend registration schema requires passwords of at least 12 characters.
- Tokens are stored in `sessionStorage` for this starter frontend, so they are cleared when the browser tab session ends. For a public production deployment, prefer server-managed Secure, HttpOnly, SameSite cookies with CSRF protection; that requires corresponding backend changes.
- Admin/owner accounts must be created/assigned on the backend. Public registration only creates customers.
- Backend image URLs are rendered using their `/media/product-images/...` path, assuming the reverse proxy forwards `/media/` to the API.

## Project structure

```text
bakery-frontend/
├── index.html
├── Dockerfile
├── nginx.conf
├── README.md
└── assets/
    ├── css/styles.css
    └── js/
        ├── api.js
        ├── app.js
        ├── cart.js
        ├── ui.js
        └── pages/
            ├── shop.js
            ├── customer.js
            └── admin.js
```
