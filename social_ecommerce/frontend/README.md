# Open Commerce Frontend
Jalankan: `python3 -m http.server 5173` di folder ini → buka http://localhost:5173
Backend: default same-origin (`API_BASE=''`), jadi `/api/...` harus di-proxy ke backend oleh web server. Untuk host lain: `localStorage.setItem('api_base','https://host:port')` (butuh CORS).

Struktur: api.js (HTTP+refresh) · store.js (session/tema) · router.js (route+guard role) · ui.js (helper DOM) · pages/* (satu file per area)
