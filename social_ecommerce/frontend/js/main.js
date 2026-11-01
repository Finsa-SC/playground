// Entry point: merakit shell (nav per-role) + router.
import { session, theme, onChange } from './store.js';
import { api } from './api.js';
import { h } from './ui.js';
import { route, resolve, homeFor } from './router.js';
import { loadUser, loginPage, registerPage } from './pages/auth.js';
import { feedPage } from './pages/feed.js';
import { productPage } from './pages/product.js';
import { publicProfile, myProfile } from './pages/profile.js';
import { sellerPage, productForm } from './pages/seller.js';
import { adminPage } from './pages/admin.js';

route('/feed', feedPage);
route('/login', loginPage);
route('/register', registerPage);
route('/product/:id', productPage);
route('/u/:username', publicProfile);
route('/me', myProfile, ['customer', 'seller', 'admin']);
route('/seller', sellerPage, ['seller']);
route('/seller/new', () => productForm(), ['seller']);
route('/seller/edit/:id', productForm, ['seller']);
route('/admin', adminPage, ['admin']);

const LINKS = [ // [label, hash, roles | null = publik]
  ['Beranda', '#/feed', null], ['Toko saya', '#/seller', ['seller']], ['Moderasi', '#/admin', ['admin']], ['Profil', '#/me', ['customer', 'seller', 'admin']],
];
async function render() {
  const cur = location.hash || '#/feed';
  const nav = h('nav', { class: 'nav' }, h('div', { class: 'brand' }, '🛍 Open Commerce'),
    ...LINKS.filter(([, , r]) => !r || r.includes(session.role)).map(([l, href]) => h('a', { href, class: cur.startsWith(href) ? 'on' : '' }, l)),
    h('div', { class: 'spacer' }),
    h('button', { class: 'link', onclick: () => theme.toggle() }, '🌓 Tema'),
    session.user
      ? h('button', { class: 'link', onclick: async () => { try { await api.logout(); } catch {} session.clear(); location.hash = '#/feed'; } }, `Keluar (@${session.user.username || ''})`)
      : h('a', { href: '#/login' }, 'Masuk'));
  const page = await resolve();
  if (page) document.getElementById('app').replaceChildren(h('div', { class: 'shell' }, nav, h('main', {}, page)));
}
theme.apply();
let last = '';
onChange(() => { const k = session.user?.id ?? session.access; if (last !== k) { last = k; render(); } });
addEventListener('hashchange', render);
(async () => { await loadUser(); if (!location.hash || location.hash === '#/') location.hash = homeFor(session.role); render(); })();
