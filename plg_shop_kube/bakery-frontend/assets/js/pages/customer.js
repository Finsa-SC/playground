import { api, session } from '../api.js';
import { $, escapeHtml, money, toast, setMessage } from '../ui.js';

const statusOptions = ['pending', 'confirmed', 'preparing', 'completed', 'cancelled'];
function statusPill(status) { return `<span class="status-pill ${escapeHtml(status)}">${escapeHtml(status)}</span>`; }

export async function renderCustomerPage() {
  const user = session.user;
  if (!user) { location.hash = '#shop'; toast('Sign in to see your orders.'); return; }
  const app = $('#app');
  app.innerHTML = `<section class="workspace"><div class="workspace-heading"><div><span class="eyebrow">YOUR LITTLE CORNER</span><h1>Welcome back, <em>${escapeHtml(user.full_name.split(' ')[0])}.</em></h1><p>All your bakery moments, together in one place.</p></div><button class="button button-outline" id="customer-refresh">Refresh orders ↻</button></div><div class="workspace-grid"><aside class="workspace-sidebar"><button class="workspace-tab active">My orders</button><button class="workspace-tab" id="account-details-tab">Account details</button><button class="workspace-tab" id="customer-shop-link">Back to the shop ↗</button></aside><div class="workspace-content"><section class="workspace-card" id="customer-main"><h2>Order history</h2><p>Here's where the good stuff is headed.</p><div id="customer-orders" class="workspace-empty">Loading your orders…</div></section><section class="workspace-card hidden" id="account-details"><h2>Your account</h2><p>These details are associated with your bakery account.</p><div class="account-summary"><div class="account-avatar">${escapeHtml(user.full_name.charAt(0).toUpperCase())}</div><div><strong>${escapeHtml(user.full_name)}</strong><small>${escapeHtml(user.email)}</small><small>Account type: ${escapeHtml(user.role)}</small></div></div><div class="account-actions"><button class="button button-outline" id="customer-signout">Sign out</button></div></section></div></div></section>`;
  $('#customer-refresh').addEventListener('click', loadOrders);
  $('#account-details-tab').addEventListener('click', () => { $('#customer-main').classList.add('hidden'); $('#account-details').classList.remove('hidden'); $('#account-details-tab').classList.add('active'); $('#customer-main-tab')?.classList.remove('active'); });
  $('#customer-shop-link').addEventListener('click', () => location.hash = '#shop');
  $('#customer-signout').addEventListener('click', () => window.dispatchEvent(new CustomEvent('auth:logout')));
  await loadOrders();
}

async function loadOrders() {
  const host = $('#customer-orders'); if (!host) return;
  host.innerHTML = '<div class="workspace-empty">Fetching your orders…</div>';
  try {
    const orders = await api.get('/orders/mine');
    if (!orders.length) { host.innerHTML = '<div class="workspace-empty"><h3>Your next favourite is waiting.</h3>You haven’t placed an order yet.<br><br><a class="button button-dark" href="#shop">Explore the bakery ↗</a></div>'; return; }
    host.innerHTML = `<div class="table-wrap"><table><thead><tr><th>Order</th><th>Date</th><th>Items</th><th>Total</th><th>Status</th></tr></thead><tbody>${orders.map(order => `<tr><td>#${order.id}</td><td>${new Date(order.created_at).toLocaleDateString('en-ID',{day:'2-digit',month:'short',year:'numeric'})}</td><td>${order.items.reduce((sum,item)=>sum+item.quantity,0)} item(s)</td><td>${money(order.total_amount)}</td><td>${statusPill(order.status)}</td></tr>`).join('')}</tbody></table></div><p class="small muted" style="margin-top:14px">Order placement does not process payment. Please follow the payment arrangements provided by the bakery.</p>`;
  } catch (error) { host.innerHTML = `<div class="workspace-empty">${escapeHtml(error.message)}<br><br><button class="button button-outline" id="retry-orders">Try again</button></div>`; $('#retry-orders')?.addEventListener('click', loadOrders); }
}
