// State minimal + pub/sub. Satu-satunya tempat state global.
const subs = new Set();
const read = (k) => { try { return JSON.parse(localStorage.getItem(k)); } catch { return null; } };

// Normalisasi role dari bentuk apa pun (string/array/object/flag) ke admin|seller|customer.
const ALIAS = { admin:'admin', administrator:'admin', superadmin:'admin', moderator:'admin', mod:'admin', op:'admin', ops:'admin', operator:'admin',
  seller:'seller', merchant:'seller', vendor:'seller', customer:'customer', buyer:'customer', user:'customer' };
export function normRole(u) {
  if (!u) return null;
  const raw = [].concat(u.roles ?? u.role ?? u.user_role ?? u.type ?? []).map((r) => String(r?.name ?? r).toLowerCase());
  for (const want of ['admin', 'seller', 'customer']) if (raw.some((r) => ALIAS[r] === want)) return want;
  if (u.is_admin || u.is_superuser) return 'admin';
  if (u.is_seller) return 'seller';
  return 'customer';
}

export const session = {
  access: read('access'), refresh: read('refresh'), user: null,
  set({ access_token, refresh_token }) {
    this.access = access_token; this.refresh = refresh_token ?? this.refresh;
    localStorage.setItem('access', JSON.stringify(this.access));
    localStorage.setItem('refresh', JSON.stringify(this.refresh)); emit();
  },
  clear() {
    this.access = this.refresh = this.user = null;
    localStorage.removeItem('access'); localStorage.removeItem('refresh'); emit();
  },
  get role() { return normRole(this.user); },
};
export const onChange = (fn) => subs.add(fn);
export const emit = () => subs.forEach((f) => f());

export const theme = {
  get: () => localStorage.getItem('theme') || 'auto',
  toggle() {
    const dark = matchMedia('(prefers-color-scheme: dark)').matches;
    const cur = this.get() === 'auto' ? (dark ? 'dark' : 'light') : this.get();
    localStorage.setItem('theme', cur === 'dark' ? 'light' : 'dark'); this.apply();
  },
  apply() { const t = this.get(); t === 'auto' ? document.documentElement.removeAttribute('data-theme') : document.documentElement.dataset.theme = t; },
};
