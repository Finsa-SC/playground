const KEY = 'crumb_cocoa_cart_v1';
function read() { try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch { return []; } }
let items = read();
function persist() { localStorage.setItem(KEY, JSON.stringify(items)); window.dispatchEvent(new CustomEvent('cart:change', { detail: items })); }
export const cart = {
  get items() { return [...items]; },
  get count() { return items.reduce((sum, item) => sum + item.quantity, 0); },
  get total() { return items.reduce((sum, item) => sum + Number(item.price) * item.quantity, 0); },
  add(product) {
    const existing = items.find(item => item.id === product.id);
    if (existing) {
      if (existing.quantity >= Number(product.stock_quantity)) throw new Error('That is all the stock currently available.');
      existing.quantity += 1;
    } else {
      if (Number(product.stock_quantity) < 1) throw new Error('This item is currently out of stock.');
      items.push({ id: product.id, name: product.name, price: Number(product.price), stock_quantity: Number(product.stock_quantity), image: product.images?.find(image => image.is_primary)?.url || product.images?.[0]?.url || '', quantity: 1 });
    }
    persist();
  },
  change(id, amount) {
    const item = items.find(entry => entry.id === id); if (!item) return;
    const next = item.quantity + amount;
    if (next < 1) items = items.filter(entry => entry.id !== id);
    else if (next > item.stock_quantity) throw new Error('That is all the stock currently available.');
    else item.quantity = next;
    persist();
  },
  remove(id) { items = items.filter(item => item.id !== id); persist(); },
  clear() { items = []; persist(); }
};
