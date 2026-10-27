const API_PREFIX = '/api/v1';
const ACCESS_KEY = 'crumb_cocoa_access';
const REFRESH_KEY = 'crumb_cocoa_refresh';
const USER_KEY = 'crumb_cocoa_user';

export const session = {
  get accessToken() { return sessionStorage.getItem(ACCESS_KEY); },
  get refreshToken() { return sessionStorage.getItem(REFRESH_KEY); },
  get user() { try { return JSON.parse(sessionStorage.getItem(USER_KEY) || 'null'); } catch { return null; } },
  set(tokens) {
    sessionStorage.setItem(ACCESS_KEY, tokens.access_token);
    sessionStorage.setItem(REFRESH_KEY, tokens.refresh_token);
    sessionStorage.setItem(USER_KEY, JSON.stringify(tokens.user));
  },
  setUser(user) { sessionStorage.setItem(USER_KEY, JSON.stringify(user)); },
  clear() { sessionStorage.removeItem(ACCESS_KEY); sessionStorage.removeItem(REFRESH_KEY); sessionStorage.removeItem(USER_KEY); }
};

async function request(path, options = {}, retry = true) {
  const headers = new Headers(options.headers || {});
  if (session.accessToken) headers.set('Authorization', `Bearer ${session.accessToken}`);
  if (options.body && !(options.body instanceof FormData) && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json');
  let response;
  try {
    response = await fetch(`${API_PREFIX}${path}`, { ...options, headers });
  } catch {
    throw new Error('Could not reach the bakery API. Check that the backend is running and the frontend can reach /api/v1.');
  }
  if (response.status === 401 && retry && session.refreshToken && !path.startsWith('/auth/')) {
    try {
      const tokens = await request('/auth/refresh', { method: 'POST', body: JSON.stringify({ refresh_token: session.refreshToken }) }, false);
      session.set(tokens);
      return request(path, options, false);
    } catch {
      session.clear();
    }
  }
  if (response.status === 204) return null;
  const raw = await response.text();
  let data = null;
  if (raw) { try { data = JSON.parse(raw); } catch { data = raw; } }
  if (!response.ok) {
    const detail = data?.detail;
    let message = typeof detail === 'string' ? detail : Array.isArray(detail) ? detail.map(item => item.msg || 'Invalid input').join(', ') : `Request failed (${response.status})`;
    throw new Error(message);
  }
  return data;
}

export const api = {
  get: path => request(path),
  post: (path, body) => request(path, { method: 'POST', body: JSON.stringify(body) }),
  patch: (path, body) => request(path, { method: 'PATCH', body: JSON.stringify(body) }),
  delete: path => request(path, { method: 'DELETE' }),
  upload: (path, formData) => request(path, { method: 'POST', body: formData })
};

export function imageUrl(url) {
  if (!url) return '';
  // Backend URLs may use localhost:8000; keep the API's supplied absolute URL intact.
  return url;
}
