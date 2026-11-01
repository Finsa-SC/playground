import { api } from '../api.js';
import { session } from '../store.js';
import { h, top, empty, avatar, toast } from '../ui.js';

const view = (u) => h('div', { class: 'pad' },
  h('div', { class: 'row', style: 'align-items:center;gap:16px' }, avatar(u.display_name || u.username),
    h('div', {}, h('b', { style: 'font-size:18px' }, u.display_name || u.username), h('div', { class: 'muted' }, '@' + u.username),
      u.role && h('span', { class: 'badge' }, typeof u.role === 'string' ? u.role : JSON.stringify(u.role)))),
  u.bio && h('p', { class: 'desc' }, u.bio));

export function publicProfile({ username }) {
  const root = h('div', {}, top('@' + username), empty('Memuat…'));
  api.profile(username).then((u) => root.replaceChildren(top('@' + username), view(u))).catch((e) => root.replaceChildren(top('Profil'), empty(e.message)));
  return root;
}
export function myProfile() {
  const u = session.user;
  const f = h('form', { class: 'f', onsubmit: async (e) => {
    e.preventDefault();
    try { session.user = { ...u, ...(await api.updateMe(Object.fromEntries(new FormData(f)))) }; toast('Profil disimpan'); location.hash = '#/me'; } catch (x) { toast(x.message, true); }
  } },
    h('label', {}, 'Nama tampilan', h('input', { name: 'display_name', maxLength: 100, value: u.display_name || '' })),
    h('label', {}, 'Bio', h('textarea', { name: 'bio', maxLength: 1000, rows: 4, value: u.bio || '' })),
    h('button', { class: 'btn pri' }, 'Simpan'));
  const dbg = h('details', { class: 'pad muted' }, h('summary', {}, 'Debug: respons /users/me'),
    h('pre', { style: 'white-space:pre-wrap' }, `terbaca sebagai: ${session.role}\n` + JSON.stringify(u, null, 2)));
  return h('div', {}, top('Profil saya'), view(u), f, dbg);
}
