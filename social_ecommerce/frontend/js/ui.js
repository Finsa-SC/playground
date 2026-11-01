// Helper DOM kecil: h() membuat elemen, tanpa framework.
export function h(tag, props = {}, ...kids) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(props || {})) {
    if (v == null || v === false) continue;
    if (k.startsWith('on')) el.addEventListener(k.slice(2), v);
    else if (k === 'class') el.className = v;
    else if (k in el && k !== 'list') el[k] = v;
    else el.setAttribute(k, v);
  }
  el.append(...kids.flat().filter((x) => x != null && x !== false));
  return el;
}
export function toast(msg, bad) {
  const t = h('div', { class: 'toast' + (bad ? ' bad' : '') }, msg);
  document.getElementById('toasts').append(t); setTimeout(() => t.remove(), 3000);
}
const hue = (s) => [...s].reduce((a, c) => a + c.charCodeAt(0), 0) % 360;
export const avatar = (name = '?') => h('div', { class: 'av', style: `background:hsl(${hue(name)} 55% 45%)` }, name[0]?.toUpperCase());
export const money = (n, cur = 'IDR') => {
  try { return new Intl.NumberFormat('id-ID', { style: 'currency', currency: cur, maximumFractionDigits: 0 }).format(n); } catch { return `${cur} ${n}`; }
};
export function ago(iso) {
  if (!iso) return '';
  const s = (Date.now() - new Date(iso)) / 1000;
  if (s < 60) return 'baru saja'; if (s < 3600) return `${~~(s / 60)} mnt`;
  if (s < 86400) return `${~~(s / 3600)} j`; return new Date(iso).toLocaleDateString('id-ID', { day: 'numeric', month: 'short' });
}
export const top = (title, ...right) => h('div', { class: 'top' }, h('span', {}, title), h('span', { class: 'row' }, right));
export const empty = (t) => h('div', { class: 'empty' }, t);
// Bentuk data produk dari API dibaca toleran karena schema respons belum didefinisikan.
export const sellerOf = (p) => {
  const s = p.seller || p.owner || {};
  const username = s.username || p.seller_username || p.username || '';
  return { username, name: s.display_name || p.seller_display_name || username || 'Seller' };
};
export const productCard = (p, { onClick, actions } = {}) => {
  const s = sellerOf(p);
  return h('article', { class: 'post', onclick: onClick || (() => (location.hash = `#/product/${p.id}`)) },
    avatar(s.name),
    h('div', { class: 'body' },
      h('div', { class: 'head' }, h('b', {}, s.name), s.username && h('span', { class: 'muted' }, '@' + s.username),
        h('span', { class: 'muted' }, '· ' + ago(p.published_at || p.created_at)),
        p.status && h('span', { class: 'badge' }, p.status)),
      h('div', { class: 'title' }, p.title),
      p.description && h('div', { class: 'desc' }, p.description.length > 280 ? p.description.slice(0, 280) + '…' : p.description),
      h('div', { class: 'row' }, h('span', { class: 'price' }, money(p.price, p.currency)), h('span', { class: 'muted' }, `Stok ${p.stock_quantity ?? '-'}`)),
      actions && h('div', { class: 'row', onclick: (e) => e.stopPropagation(), style: 'margin-top:8px' }, actions)));
};
