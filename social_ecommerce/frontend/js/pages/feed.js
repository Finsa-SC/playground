import { api } from '../api.js';
import { h, top, empty, productCard } from '../ui.js';

// Infinite scroll dengan cursor (published_at + id) seperti timeline X.
export function feedPage() {
  const list = h('div'); const sentinel = h('div', { class: 'empty' }, 'Memuat…');
  let cursor = null, done = false, busy = false;
  async function more() {
    if (busy || done) return; busy = true;
    try {
      const res = await api.feed({ limit: 20, ...cursor });
      const items = Array.isArray(res) ? res : res.items || res.data || [];
      items.forEach((p) => list.append(productCard(p)));
      const next = res.next_cursor, last = items.at(-1);
      cursor = next ? { cursor_published_at: next.published_at ?? next.cursor_published_at, cursor_id: next.id ?? next.cursor_id }
        : last ? { cursor_published_at: last.published_at, cursor_id: last.id } : null;
      if (items.length < 20 || !cursor) {
        done = true;
        list.children.length ? (sentinel.textContent = 'Sudah di ujung 🎉') : sentinel.replaceWith(empty('Belum ada produk.'));
      }
    } catch (e) { sentinel.textContent = e.message; done = true; }
    busy = false;
  }
  const io = new IntersectionObserver((e) => e[0].isIntersecting && more(), { rootMargin: '400px' });
  const root = h('div', {}, top('Beranda'), list, sentinel);
  queueMicrotask(() => io.observe(sentinel));
  return root;
}
