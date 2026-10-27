# FinSky frontend

React + Vite + React Router. Tema Catppuccin Mocha.

```bash
npm install
npm run dev          # http://localhost:5173, /api diproxy ke http://localhost:8000
VITE_API_TARGET=http://host:port npm run dev   # backend di tempat lain
npm run build        # output di dist/
```

- Taruh favicon kamu di `public/favicon.ico`.
- Frontend memanggil `/api/v1/...` (same-origin). Di produksi, reverse proxy `/api` ke backend
  dan fallback semua route lain ke `index.html` (SPA).
- JWT disimpan di localStorage dan dikirim sebagai `Authorization: Bearer`.
- Route: /login, /register, /foryou, /following, /profile (-> /profile/:username), /profile/edit, /post/:id
