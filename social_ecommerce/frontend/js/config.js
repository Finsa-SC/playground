// Kosong = same-origin (request ke /api/... di host yang sama, mis. lewat reverse proxy).
// Untuk backend di host lain: localStorage.setItem('api_base','https://host:port')
export const API_BASE = localStorage.getItem('api_base') || '';
