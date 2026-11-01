// Router hash + guard role. Tambah halaman = tambah satu baris di routes.
import { session } from './store.js';
import { h, empty, top } from './ui.js';

const routes = [];
export const route = (pattern, render, roles = null) => {
  const keys = []; const re = new RegExp('^' + pattern.replace(/:(\w+)/g, (_, k) => (keys.push(k), '([^/]+)')) + '$');
  routes.push({ re, keys, render, roles });
};
export const homeFor = (role) => ({ admin: '#/admin', seller: '#/seller' }[role] || '#/feed');

export async function resolve() {
  const path = location.hash.slice(1) || '/feed';
  for (const r of routes) {
    const m = path.match(r.re); if (!m) continue;
    if (r.roles && !session.user) { location.hash = '#/login'; return null; }
    if (r.roles && !r.roles.includes(session.role))
      return h('div', {}, top('403'), empty('Kamu tidak punya akses ke halaman ini.'));
    const params = Object.fromEntries(r.keys.map((k, i) => [k, decodeURIComponent(m[i + 1])]));
    return r.render(params);
  }
  return h('div', {}, top('404'), empty('Halaman tidak ditemukan.'));
}
