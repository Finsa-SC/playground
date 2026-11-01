import { api } from '../api.js';
import { session } from '../store.js';
import { h, top, empty, toast, productCard } from '../ui.js';

// API tidak punya endpoint "produk saya", jadi ID produk yang dibuat disimpan lokal.
const key = () => 'my_products:' + (session.user.id || session.user.username);
const ids = () => JSON.parse(localStorage.getItem(key()) || '[]');
const remember = (id) => localStorage.setItem(key(), JSON.stringify([...new Set([id, ...ids()])]));

export function sellerPage() {
  const list = h('div');
  const load = async () => {
    list.replaceChildren(empty('Memuat…'));
    const rows = await Promise.allSettled(ids().map(api.product));
    const ok = rows.filter((r) => r.status === 'fulfilled').map((r) => r.value);
    list.replaceChildren(...(ok.length ? ok.map((p) => productCard(p, { onClick: () => {}, actions: [
      h('button', { class: 'btn ghost', onclick: () => (location.hash = `#/seller/edit/${p.id}`) }, 'Edit'),
      h('button', { class: 'btn pri', onclick: async () => { try { await api.submitProduct(p.id); toast('Dikirim ke moderasi'); load(); } catch (e) { toast(e.message, true); } } }, 'Ajukan'),
    ] })) : [empty('Belum ada produk. Buat yang pertama!')]));
  };
  load();
  return h('div', {}, top('Toko saya', h('a', { class: 'btn pri', href: '#/seller/new' }, '+ Produk')), list);
}

export function productForm({ id } = {}) {
  const f = h('form', { class: 'f', onsubmit: async (e) => {
    e.preventDefault();
    const b = Object.fromEntries(new FormData(f));
    b.price = Number(b.price); b.stock_quantity = Number(b.stock_quantity);
    if (id) delete b.currency; if (!b.category_id) delete b.category_id;
    try {
      if (id) await api.updateProduct(id, b); else remember((await api.createProduct(b)).id);
      toast('Tersimpan. Ajukan untuk moderasi dari halaman Toko'); location.hash = '#/seller';
    } catch (x) { toast(x.message, true); }
  } },
    h('label', {}, 'Judul', h('input', { name: 'title', required: true, maxLength: 200 })),
    h('label', {}, 'Deskripsi', h('textarea', { name: 'description', rows: 5, maxLength: 20000 })),
    h('div', { class: 'row' },
      h('label', { style: 'flex:2' }, 'Harga', h('input', { name: 'price', type: 'number', min: 1, step: 'any', required: true })),
      !id && h('label', { style: 'flex:1' }, 'Mata uang', h('input', { name: 'currency', value: 'IDR', pattern: '[A-Z]{3}' })),
      h('label', { style: 'flex:1' }, 'Stok', h('input', { name: 'stock_quantity', type: 'number', min: 0, value: 1 }))),
    h('label', {}, 'Category ID (opsional, UUID)', h('input', { name: 'category_id' })),
    h('button', { class: 'btn pri' }, id ? 'Simpan perubahan' : 'Buat produk'));
  if (id) api.product(id).then((p) => Object.entries(p).forEach(([k, v]) => f.elements[k] && (f.elements[k].value = v ?? '')));
  return h('div', {}, top(id ? 'Edit produk' : 'Produk baru'), f);
}
