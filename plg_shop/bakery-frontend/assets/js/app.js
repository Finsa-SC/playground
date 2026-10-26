import { api, session } from './api.js';
import { cart } from './cart.js';
import { $, $$, escapeHtml, money, toast, openOverlay, closeOverlay, setMessage, imageOrPlaceholder } from './ui.js';
import { initShop } from './pages/shop.js';
import { renderCustomerPage } from './pages/customer.js';
import { renderAdminPage } from './pages/admin.js';

const app = $('#app');
const homeMarkup = app.innerHTML;
let authMode = 'login';
let checkoutAfterLogin = false;

function updateHeader() {
  const user = session.user;
  $('.account-label').textContent = user ? user.full_name.split(' ')[0] : 'Sign in';
  $('.user-icon').textContent = user ? user.full_name.charAt(0).toUpperCase() : '♙';
  $$('.auth-nav').forEach(node => node.classList.toggle('hidden', !user));
  $$('.admin-nav').forEach(node => node.classList.toggle('hidden', !user || !['owner','admin'].includes(user.role)));
  $$('.main-nav a[data-nav]').forEach(node => node.classList.toggle('active', node.dataset.nav === (location.hash.replace('#','') || 'shop')));
}
function renderCart() {
  $('#cart-count').textContent = cart.count;
  $('#cart-heading-count').textContent = `(${cart.count})`;
  $('#cart-total').textContent = money(cart.total);
  const host = $('#cart-items');
  if (!cart.items.length) { host.innerHTML = '<div class="empty-state"><strong>Your bag is taking a little nap.</strong>Let’s find something freshly baked.<br><br><button class="button button-outline" id="cart-browse">Explore the bakery ↗</button></div>'; $('#cart-browse')?.addEventListener('click', () => { closeOverlay('cart-overlay'); location.hash = '#shop'; }); $('#checkout-button').disabled = true; return; }
  $('#checkout-button').disabled = false;
  host.innerHTML = cart.items.map(item => `<div class="cart-row"><div class="cart-thumb">${item.image ? imageOrPlaceholder(item.image,'cart-thumb-image').replace('class="cart-thumb-image"','class="cart-thumb" style="height:70px;width:70px;object-fit:cover"') : '🥐'}</div><div><div class="cart-item-name">${escapeHtml(item.name)}</div><div class="cart-item-price">${money(item.price)} each</div><div class="quantity-control"><button data-quantity="${item.id}" data-change="-1" aria-label="Remove one ${escapeHtml(item.name)}">−</button><span>${item.quantity}</span><button data-quantity="${item.id}" data-change="1" aria-label="Add one ${escapeHtml(item.name)}">+</button><button class="cart-remove" data-remove="${item.id}">Remove</button></div></div><strong class="product-price">${money(item.price * item.quantity)}</strong></div>`).join('');
  host.querySelectorAll('[data-quantity]').forEach(button => button.addEventListener('click', () => { try { cart.change(Number(button.dataset.quantity), Number(button.dataset.change)); } catch (error) { toast(error.message, 'error'); } }));
  host.querySelectorAll('[data-remove]').forEach(button => button.addEventListener('click', () => cart.remove(Number(button.dataset.remove))));
}

function setAuthMode(mode) {
  authMode = mode;
  $$('.auth-tab').forEach(button => button.classList.toggle('active', button.dataset.authMode === mode));
  $('#auth-title').innerHTML = mode === 'login' ? 'Good to have <em>you here.</em>' : 'Make yourself <em>at home.</em>';
  $('#auth-name-field').classList.toggle('hidden', mode !== 'register');
  $('#auth-name').required = mode === 'register';
  $('#auth-password').autocomplete = mode === 'register' ? 'new-password' : 'current-password';
  $('#auth-password').minLength = mode === 'register' ? 12 : 1;
  $('#password-hint').classList.toggle('hidden', mode !== 'register');
  $('#auth-submit').innerHTML = mode === 'login' ? 'Sign in <span>→</span>' : 'Create my account <span>→</span>';
  setMessage($('#auth-message'), '');
}
async function submitAuth(event) {
  event.preventDefault();
  const submit = $('#auth-submit'); submit.disabled = true; setMessage($('#auth-message'), '');
  const email = $('#auth-email').value.trim(); const password = $('#auth-password').value;
  try {
    let tokens;
    if (authMode === 'register') {
      await api.post('/auth/register', { email, full_name: $('#auth-name').value.trim(), password });
      tokens = await api.post('/auth/login', { email, password });
      toast('Your account is ready. Welcome in!', 'success');
    } else tokens = await api.post('/auth/login', { email, password });
    session.set(tokens); updateHeader(); closeOverlay('auth-overlay'); $('#auth-form').reset();
    toast(`Welcome, ${tokens.user.full_name.split(' ')[0]}.`, 'success');
    if (['owner','admin'].includes(tokens.user.role)) { checkoutAfterLogin = false; location.hash = '#admin'; }
    else if (checkoutAfterLogin) { checkoutAfterLogin = false; renderCheckout(); openOverlay('checkout-overlay'); }
  } catch (error) { setMessage($('#auth-message'), error.message); }
  finally { submit.disabled = false; }
}
async function signOut() {
  const refreshToken = session.refreshToken;
  if (refreshToken && session.accessToken) { try { await api.post('/auth/logout', { refresh_token: refreshToken }); } catch { /* Local sign-out still clears this browser session. */ } }
  session.clear(); updateHeader(); toast('You’ve signed out. See you again soon.'); location.hash = '#shop';
}
function renderCheckout() {
  const summary = $('#checkout-summary');
  summary.innerHTML = cart.items.map(item => `<div class="checkout-line"><span>${escapeHtml(item.name)} × ${item.quantity}</span><strong>${money(item.price * item.quantity)}</strong></div>`).join('') + `<div class="checkout-line checkout-grand"><span>Order total</span><strong>${money(cart.total)}</strong></div>`;
  setMessage($('#checkout-message'), '');
}
async function placeOrder() {
  const button = $('#place-order-button'); button.disabled = true; setMessage($('#checkout-message'), 'Sending your order to the bakery…', true);
  try {
    const order = await api.post('/orders', { items: cart.items.map(item => ({ product_id: item.id, quantity: item.quantity })) });
    cart.clear(); closeOverlay('checkout-overlay'); closeOverlay('cart-overlay'); toast(`Order #${order.id} placed. Status: pending.`, 'success'); location.hash = '#orders';
  } catch (error) { setMessage($('#checkout-message'), error.message); }
  finally { button.disabled = false; }
}

async function route() {
  updateHeader();
  const routeName = location.hash.replace('#','') || 'shop';
  if (routeName === 'admin') { await renderAdminPage(); return; }
  if (routeName === 'orders' || routeName === 'account') { await renderCustomerPage(); return; }
  if (!app.querySelector('#product-grid')) app.innerHTML = homeMarkup;
  initShop();
  if (routeName === 'story') setTimeout(() => $('#story')?.scrollIntoView({ behavior: 'smooth' }), 30);
  else if (routeName === 'shop') window.scrollTo({ top: 0, behavior: 'smooth' });
}

$('#account-button').addEventListener('click', () => {
  const user = session.user;
  if (!user) { setAuthMode('login'); openOverlay('auth-overlay'); }
  else location.hash = ['owner','admin'].includes(user.role) ? '#admin' : '#orders';
});
$('#cart-open').addEventListener('click', () => { renderCart(); openOverlay('cart-overlay'); });
$('#checkout-button').addEventListener('click', () => {
  if (!cart.items.length) return;
  closeOverlay('cart-overlay');
  if (!session.user) { checkoutAfterLogin = true; setAuthMode('login'); openOverlay('auth-overlay'); toast('Sign in first to place your order.'); return; }
  renderCheckout(); openOverlay('checkout-overlay');
});
$('#place-order-button').addEventListener('click', placeOrder);
$('#auth-form').addEventListener('submit', submitAuth);
$$('[data-auth-mode]').forEach(button => button.addEventListener('click', () => setAuthMode(button.dataset.authMode)));
$$('[data-close]').forEach(button => button.addEventListener('click', () => closeOverlay(button.dataset.close)));
$$('.overlay').forEach(overlay => overlay.addEventListener('click', event => { if (event.target === overlay) closeOverlay(overlay.id); }));
$('#mobile-menu').addEventListener('click', () => $('.main-nav').classList.toggle('open'));
$$('.main-nav a').forEach(link => link.addEventListener('click', () => $('.main-nav').classList.remove('open')));
window.addEventListener('hashchange', () => { $('.main-nav').classList.remove('open'); route(); });
window.addEventListener('cart:change', renderCart);
window.addEventListener('auth:logout', signOut);
$('#year').textContent = new Date().getFullYear();
updateHeader(); renderCart(); route();
