import { api } from '../api.js';
import { session } from '../store.js';
import { h, top, toast } from '../ui.js';
import { homeFor } from '../router.js';

export async function loadUser() {
  if (!session.access) return;
  try { session.user = await api.me(); } catch { session.clear(); }
}
const field = (label, name, type = 'text', extra = {}) => h('label', {}, label, h('input', { name, type, required: true, ...extra }));

function form(title, fields, submit, alt) {
  const err = h('div', { class: 'err' });
  const btn = h('button', { class: 'btn pri', type: 'submit' }, title);
  const f = h('form', { class: 'f', onsubmit: async (e) => {
    e.preventDefault(); btn.disabled = true; err.textContent = '';
    try { await submit(Object.fromEntries(new FormData(f))); } catch (x) { err.textContent = x.message; }
    btn.disabled = false;
  } }, ...fields, err, btn, alt);
  return h('div', {}, top(title), f);
}
export const loginPage = () => form('Masuk', [field('Email', 'email', 'email'), field('Password', 'password', 'password', { maxLength: 128 })],
  async (b) => { session.set(await api.login(b)); await loadUser(); location.hash = homeFor(session.role); },
  h('a', { href: '#/register', class: 'muted' }, 'Belum punya akun? Daftar'));

export const registerPage = () => form('Daftar', [
  field('Email', 'email', 'email'),
  field('Username (3-30, huruf/angka/_)', 'username', 'text', { minLength: 3, maxLength: 30, pattern: '[A-Za-z0-9_]+' }),
  field('Nama tampilan', 'display_name', 'text', { maxLength: 100 }),
  field('Password (min 12 karakter)', 'password', 'password', { minLength: 12, maxLength: 128 })],
  async (b) => { await api.register(b); toast('Akun dibuat, silakan masuk'); location.hash = '#/login'; },
  h('a', { href: '#/login', class: 'muted' }, 'Sudah punya akun? Masuk'));
