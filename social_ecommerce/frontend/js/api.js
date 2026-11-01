// Client HTTP: bearer token, auto-refresh saat 401, error terstruktur.
import { API_BASE } from './config.js';
import { session } from './store.js';

export class ApiError extends Error {
  constructor(status, message) { super(message); this.status = status; }
}
const errMsg = (d) => Array.isArray(d?.detail) ? d.detail.map((e) => `${e.loc?.slice(1).join('.')}: ${e.msg}`).join('; ') : d?.detail || 'Terjadi kesalahan';

async function raw(path, { method = 'GET', body, query, auth = true } = {}) {
  const url = new URL(API_BASE + path, window.location.origin);
  Object.entries(query || {}).forEach(([k, v]) => v != null && url.searchParams.set(k, v));
  const headers = {};
  if (body) headers['Content-Type'] = 'application/json';
  if (auth && session.access) headers.Authorization = `Bearer ${session.access}`;
  return fetch(url, { method, headers, body: body ? JSON.stringify(body) : undefined });
}
let refreshing;
async function refresh() {
  try {
    const r = await raw('/api/v1/auth/refresh', { method: 'POST', query: { refresh_token: session.refresh }, auth: false });
    if (!r.ok) return false; session.set(await r.json()); return true;
  } catch { return false; }
}
export async function request(path, opts = {}) {
  let res = await raw(path, opts);
  if (res.status === 401 && session.refresh && opts.auth !== false) {
    refreshing ??= refresh().finally(() => (refreshing = null));
    if (await refreshing) res = await raw(path, opts); else session.clear();
  }
  const data = res.status === 204 ? null : await res.json().catch(() => null);
  if (!res.ok) throw new ApiError(res.status, errMsg(data));
  return data;
}

export const api = {
  register: (b) => request('/api/v1/auth/register', { method: 'POST', body: b, auth: false }),
  login: (b) => request('/api/v1/auth/login', { method: 'POST', body: b, auth: false }),
  logout: () => request('/api/v1/auth/logout', { method: 'POST', query: { refresh_token: session.refresh } }),
  me: () => request('/api/v1/users/me'),
  updateMe: (b) => request('/api/v1/users/me', { method: 'PATCH', body: b }),
  profile: (u) => request(`/api/v1/users/${encodeURIComponent(u)}`, { auth: false }),
  feed: (q) => request('/api/v1/feed', { query: q, auth: false }),
  product: (id) => request(`/api/v1/products/${id}`, { auth: false }),
  createProduct: (b) => request('/api/v1/products', { method: 'POST', body: b }),
  updateProduct: (id, b) => request(`/api/v1/products/${id}`, { method: 'PATCH', body: b }),
  submitProduct: (id) => request(`/api/v1/products/${id}/submit`, { method: 'POST' }),
  queue: () => request('/api/v1/moderation/products'),
  approve: (id) => request(`/api/v1/moderation/products/${id}/approve`, { method: 'POST' }),
  reject: (id, reason) => request(`/api/v1/moderation/products/${id}/reject`, { method: 'POST', body: { reason } }),
};
