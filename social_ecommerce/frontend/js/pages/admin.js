import { api } from '../api.js';
import { h, top, empty, toast, productCard } from '../ui.js';

export function adminPage() {
  const list = h('div');
  const load = async () => {
    try {
      const res = await api.queue(); const items = Array.isArray(res) ? res : res.items || [];
      const act = (fn, msg) => async () => { try { await fn(); toast(msg); load(); } catch (e) { toast(e.message, true); } };
      list.replaceChildren(...(items.length ? items.map((p) => productCard(p, { onClick: () => {}, actions: [
        h('button', { class: 'btn pri', onclick: act(() => api.approve(p.id), 'Disetujui') }, 'Setujui'),
        h('button', { class: 'btn bad', onclick: () => {
          const reason = prompt('Alasan penolakan (min 3 karakter):');
          if (reason && reason.trim().length >= 3) act(() => api.reject(p.id, reason.trim()), 'Ditolak')();
        } }, 'Tolak'),
      ] })) : [empty('Antrian moderasi kosong 🎉')]));
    } catch (e) { list.replaceChildren(empty(e.message)); }
  };
  load();
  return h('div', {}, top('Moderasi produk'), list);
}
