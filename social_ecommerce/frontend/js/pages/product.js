import { api } from '../api.js';
import { h, top, empty, productCard } from '../ui.js';

export function productPage({ id }) {
  const root = h('div', {}, top('Produk'), empty('Memuat…'));
  api.product(id).then((p) => root.replaceChildren(top('Produk', h('a', { class: 'btn ghost', href: '#/feed' }, '←')),
    productCard(p, { onClick: () => {} }), h('div', { class: 'pad muted' }, `Dipublikasikan ${p.published_at ? new Date(p.published_at).toLocaleString('id-ID') : '-'}`)))
    .catch((e) => root.replaceChildren(top('Produk'), empty(e.message)));
  return root;
}
