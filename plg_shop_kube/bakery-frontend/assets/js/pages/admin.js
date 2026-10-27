import { api, session } from '../api.js';
import { $, escapeHtml, money, toast, setMessage, imageOrPlaceholder } from '../ui.js';

let products = [], categories = [], orders = [], editingId = null;
const orderStatuses = ['pending','confirmed','preparing','completed','cancelled'];

export async function renderAdminPage() {
  const user = session.user;
  if (!user || !['owner','admin'].includes(user.role)) { location.hash = '#shop'; toast('The management workspace is for bakery owners and admins.'); return; }
  $('#app').innerHTML = `<section class="workspace"><div class="workspace-heading"><div><span class="eyebrow">BEHIND THE COUNTER</span><h1>Bakery <em>workspace.</em></h1><p>Manage your products, stock, images, and customer orders.</p></div><button class="button button-outline" id="admin-refresh">Refresh data ↻</button></div><div class="workspace-grid"><aside class="workspace-sidebar"><button class="workspace-tab active" data-admin-tab="products">Products</button><button class="workspace-tab" data-admin-tab="orders">Orders</button><button class="workspace-tab" data-admin-tab="categories">Categories</button><button class="workspace-tab" data-admin-tab="account">Account</button><button class="workspace-tab" id="admin-shop-link">View shop ↗</button></aside><div class="workspace-content"><section class="workspace-card" data-admin-panel="products"><div class="admin-toolbar"><div><h2>Product shelf</h2><p>Keep your catalogue fresh and accurate.</p></div><button class="button button-dark button-small" id="new-product">+ Add product</button></div><div id="product-form-wrap" class="hidden"></div><div id="admin-products" class="workspace-empty">Loading products…</div></section><section class="workspace-card hidden" data-admin-panel="orders"><div class="admin-toolbar"><div><h2>Customer orders</h2><p>Update the order status as each order moves through the bakery.</p></div></div><div id="admin-orders" class="workspace-empty">Loading orders…</div></section><section class="workspace-card hidden" data-admin-panel="categories"><h2>Categories</h2><p>Group products so customers can browse with ease.</p><form id="category-form" class="admin-form-grid"><div class="field"><label for="category-name">Category name</label><input id="category-name" required maxlength="100" placeholder="e.g. Breads"></div><div class="field"><label for="category-description">Description (optional)</label><input id="category-description" placeholder="A little description"></div><div class="field full"><div id="category-message" class="form-message"></div><button class="button button-dark button-small" type="submit">Create category →</button></div></form><div id="admin-categories" style="margin-top:20px"></div></section><section class="workspace-card hidden" data-admin-panel="account"><h2>Your account</h2><p>Signed in as a trusted bakery manager.</p><div class="account-summary"><div class="account-avatar">${escapeHtml(user.full_name.charAt(0).toUpperCase())}</div><div><strong>${escapeHtml(user.full_name)}</strong><small>${escapeHtml(user.email)}</small><small>Role: ${escapeHtml(user.role)}</small></div></div><div class="account-actions"><button class="button button-outline" id="admin-signout">Sign out</button></div></section></div></div></section>`;
  document.querySelectorAll('[data-admin-tab]').forEach(button => button.addEventListener('click', () => showPanel(button.dataset.adminTab)));
  $('#admin-shop-link').addEventListener('click', () => location.hash = '#shop');
  $('#admin-refresh').addEventListener('click', refreshAll);
  $('#new-product').addEventListener('click', () => showProductForm());
  $('#category-form').addEventListener('submit', createCategory);
  $('#admin-signout').addEventListener('click', () => window.dispatchEvent(new CustomEvent('auth:logout')));
  await refreshAll();
}
function showPanel(name) {
  document.querySelectorAll('[data-admin-tab]').forEach(button => button.classList.toggle('active', button.dataset.adminTab === name));
  document.querySelectorAll('[data-admin-panel]').forEach(panel => panel.classList.toggle('hidden', panel.dataset.adminPanel !== name));
}
async function refreshAll() {
  const [productResult, categoryResult, orderResult] = await Promise.allSettled([api.get('/products?page=1&page_size=100'), api.get('/categories'), api.get('/orders?page=1&page_size=100')]);
  if (productResult.status === 'fulfilled') products = productResult.value; else toast(`Products: ${productResult.reason.message}`, 'error');
  if (categoryResult.status === 'fulfilled') categories = categoryResult.value; else toast(`Categories: ${categoryResult.reason.message}`, 'error');
  if (orderResult.status === 'fulfilled') orders = orderResult.value; else toast(`Orders: ${orderResult.reason.message}`, 'error');
  renderProductTable(); renderOrderTable(); renderCategoryList();
}
function renderProductTable() {
  const host = $('#admin-products'); if (!host) return;
  if (!products.length) { host.innerHTML = '<div class="workspace-empty"><h3>A fresh shelf awaits.</h3>Add your first product to start building the catalogue.</div>'; return; }
  host.innerHTML = `<div class="table-wrap"><table><thead><tr><th>Product</th><th>Price</th><th>Stock</th><th>Category</th><th>Actions</th></tr></thead><tbody>${products.map(product => {
    const image = product.images?.find(item => item.is_primary)?.url || product.images?.[0]?.url;
    const category = categories.find(item => item.id === product.category_id)?.name || '—';
    return `<tr><td><div class="admin-product-cell">${imageOrPlaceholder(image,'admin-thumb')}<div><strong>${escapeHtml(product.name)}</strong><small>#${product.id} · ${product.is_available ? 'Available' : 'Hidden'}</small></div></div></td><td>${money(product.price)}</td><td>${product.stock_quantity}</td><td>${escapeHtml(category)}</td><td><div class="table-actions"><button class="table-action" data-edit-product="${product.id}">Edit</button><button class="table-action danger" data-hide-product="${product.id}">Hide</button></div></td></tr>`;
  }).join('')}</tbody></table></div>`;
  host.querySelectorAll('[data-edit-product]').forEach(button => button.addEventListener('click', () => showProductForm(products.find(item => item.id === Number(button.dataset.editProduct)))));
  host.querySelectorAll('[data-hide-product]').forEach(button => button.addEventListener('click', async () => {
    const product = products.find(item => item.id === Number(button.dataset.hideProduct));
    if (!confirm(`Hide “${product.name}” from the public shop? Existing order history will be preserved.`)) return;
    try { await api.delete(`/products/${product.id}`); toast('Product hidden from the public catalogue.', 'success'); await refreshAll(); }
    catch (error) { toast(error.message, 'error'); }
  }));
}
function showProductForm(product = null) {
  editingId = product?.id ?? null;
  const wrap = $('#product-form-wrap'); wrap.classList.remove('hidden');
  wrap.innerHTML = `<section class="workspace-card" style="background:#fcf7f1;margin:0 0 18px"><div class="admin-toolbar"><h2>${product ? 'Edit product' : 'Add a product'}</h2><button class="close-button" id="cancel-product-form" aria-label="Close product form">×</button></div><form id="product-form"><div class="admin-form-grid"><div class="field full"><label for="product-name">Product name</label><input id="product-name" required maxlength="150" value="${escapeHtml(product?.name || '')}" placeholder="e.g. Chocolate babka"></div><div class="field"><label for="product-category">Category</label><select id="product-category" required><option value="">Choose category…</option>${categories.map(category => `<option value="${category.id}" ${product?.category_id === category.id ? 'selected' : ''}>${escapeHtml(category.name)}</option>`).join('')}</select></div><div class="field"><label for="product-price">Price (IDR)</label><input id="product-price" type="number" min="0" step="1" required value="${escapeHtml(product?.price ?? '')}" placeholder="35000"></div><div class="field"><label for="product-stock">Stock quantity</label><input id="product-stock" type="number" min="0" step="1" required value="${escapeHtml(product?.stock_quantity ?? 0)}"></div><div class="field"><label for="product-available">Availability</label><select id="product-available"><option value="true" ${product?.is_available !== false ? 'selected' : ''}>Available in shop</option><option value="false" ${product?.is_available === false ? 'selected' : ''}>Hidden from shop</option></select></div><div class="field full"><label for="product-description">Description</label><textarea id="product-description" placeholder="Tell customers what makes it special…">${escapeHtml(product?.description || '')}</textarea></div><div class="field full"><label for="product-image">Product photo ${product ? '(optional: upload another)' : '(optional)'}</label><input id="product-image" type="file" accept="image/jpeg,image/png,image/webp"><small class="field-hint">JPEG, PNG or WEBP. Backend limit: 5 MB.</small></div><div class="field full"><label><input id="product-primary" type="checkbox" checked style="width:auto;margin-right:6px"> Set uploaded image as primary photo</label></div></div><div id="product-form-message" class="form-message"></div><div class="admin-form-actions"><button type="button" class="button button-outline button-small" id="cancel-product-button">Cancel</button><button class="button button-dark button-small" type="submit">${product ? 'Save changes' : 'Create product'} →</button></div></form></section>`;
  $('#cancel-product-form').addEventListener('click', closeProductForm); $('#cancel-product-button').addEventListener('click', closeProductForm);
  $('#product-form').addEventListener('submit', saveProduct);
  wrap.scrollIntoView({ behavior: 'smooth', block: 'start' });
}
function closeProductForm() { const wrap = $('#product-form-wrap'); wrap.classList.add('hidden'); wrap.innerHTML = ''; editingId = null; }
async function saveProduct(event) {
  event.preventDefault();
  const message = $('#product-form-message');
  const payload = { category_id: Number($('#product-category').value), name: $('#product-name').value.trim(), price: Number($('#product-price').value).toFixed(2), stock_quantity: Number($('#product-stock').value), is_available: $('#product-available').value === 'true', description: $('#product-description').value.trim() || null };
  const file = $('#product-image').files[0];
  try {
    let product;
    if (editingId) product = await api.patch(`/products/${editingId}`, payload);
    else product = await api.post('/products', payload);
    if (file) {
      const form = new FormData(); form.append('file', file); form.append('alt_text', payload.name); form.append('is_primary', $('#product-primary').checked ? 'true' : 'false');
      await api.upload(`/products/${product.id}/images`, form);
    }
    toast(editingId ? 'Product updated.' : 'Product added to the shelf.', 'success'); closeProductForm(); await refreshAll();
  } catch (error) { setMessage(message, error.message); }
}
async function createCategory(event) {
  event.preventDefault(); const message = $('#category-message');
  try {
    await api.post('/categories', { name: $('#category-name').value.trim(), description: $('#category-description').value.trim() || null });
    $('#category-form').reset(); setMessage(message, 'Category created.', true); await refreshAll();
  } catch (error) { setMessage(message, error.message); }
}
function renderCategoryList() {
  const host = $('#admin-categories'); if (!host) return;
  host.innerHTML = categories.length ? `<div class="table-wrap"><table><thead><tr><th>Category</th><th>Description</th><th>ID</th></tr></thead><tbody>${categories.map(category => `<tr><td><strong>${escapeHtml(category.name)}</strong></td><td>${escapeHtml(category.description || '—')}</td><td>${category.id}</td></tr>`).join('')}</tbody></table></div>` : '<div class="workspace-empty">No categories yet.</div>';
}
function renderOrderTable() {
  const host = $('#admin-orders'); if (!host) return;
  if (!orders.length) { host.innerHTML = '<div class="workspace-empty"><h3>All quiet in the kitchen.</h3>No customer orders to manage right now.</div>'; return; }
  host.innerHTML = `<div class="table-wrap"><table><thead><tr><th>Order</th><th>Customer ID</th><th>Date</th><th>Items</th><th>Total</th><th>Status</th><th>Update</th></tr></thead><tbody>${orders.map(order => `<tr><td>#${order.id}</td><td>${order.customer_id ?? 'Guest'}</td><td>${new Date(order.created_at).toLocaleDateString('en-ID',{day:'2-digit',month:'short'})}</td><td>${order.items.reduce((sum,item)=>sum+item.quantity,0)}</td><td>${money(order.total_amount)}</td><td><span class="status-pill ${escapeHtml(order.status)}">${escapeHtml(order.status)}</span></td><td>${['completed','cancelled'].includes(order.status) ? '—' : `<select class="status-select" data-order-status="${order.id}" aria-label="Update status for order ${order.id}">${orderStatuses.map(status => `<option value="${status}" ${status === order.status ? 'selected' : ''}>${status}</option>`).join('')}</select>`}</td></tr>`).join('')}</tbody></table></div><p class="small muted" style="margin-top:14px">Cancelling an order restores stock on the backend. Completed or cancelled orders cannot be changed.</p>`;
  host.querySelectorAll('[data-order-status]').forEach(select => select.addEventListener('change', async () => {
    const orderId = Number(select.dataset.orderStatus); const status = select.value;
    if (status === 'cancelled' && !confirm(`Cancel order #${orderId}? The backend will restore its stock.`)) { await refreshAll(); return; }
    select.disabled = true;
    try { await api.patch(`/orders/${orderId}`, { status }); toast(`Order #${orderId} updated to ${status}.`, 'success'); await refreshAll(); }
    catch (error) { toast(error.message, 'error'); await refreshAll(); }
  }));
}
