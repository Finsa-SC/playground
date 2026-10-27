import { api } from '../api.js';
import { cart } from '../cart.js';
import { $, escapeHtml, money, toast, imageOrPlaceholder } from '../ui.js';

let products = [];
let categories = [];
let selectedCategory = 'all';
let searchText = '';

export async function loadShop() {
  const grid = $('#product-grid');
  grid.innerHTML = '<div class="loading-state">Warming up the oven…</div>';
  try {
    const [productData, categoryData] = await Promise.all([api.get('/products?page=1&page_size=100'), api.get('/categories')]);
    products = productData;
    categories = categoryData;
    renderCategories();
    renderProducts();
  } catch (error) {
    grid.innerHTML = `<div class="empty-state"><strong>We couldn’t load the bakery shelf.</strong>${escapeHtml(error.message)}<br><br><button class="button button-outline" id="retry-shop">Try again</button></div>`;
    $('#retry-shop')?.addEventListener('click', loadShop);
  }
}

function renderCategories() {
  const host = $('#category-filters');
  host.innerHTML = `<button class="filter-chip ${selectedCategory === 'all' ? 'active' : ''}" data-category="all">Everything</button>` + categories.map(category => `<button class="filter-chip ${String(selectedCategory) === String(category.id) ? 'active' : ''}" data-category="${category.id}">${escapeHtml(category.name)}</button>`).join('');
  host.querySelectorAll('[data-category]').forEach(button => button.addEventListener('click', () => {
    selectedCategory = button.dataset.category;
    renderCategories(); renderProducts();
  }));
}

function renderProducts() {
  const filtered = products.filter(product => (selectedCategory === 'all' || String(product.category_id) === String(selectedCategory)) && (!searchText || `${product.name} ${product.description || ''}`.toLowerCase().includes(searchText)));
  $('#catalog-status').textContent = `${filtered.length} ${filtered.length === 1 ? 'little delight' : 'little delights'} to discover`;
  const grid = $('#product-grid');
  if (!filtered.length) { grid.innerHTML = '<div class="empty-state"><strong>No crumbs found.</strong>Try another search or category.</div>'; return; }
  grid.innerHTML = filtered.map(product => {
    const image = product.images?.find(item => item.is_primary)?.url || product.images?.[0]?.url;
    const category = categories.find(item => item.id === product.category_id)?.name || 'From our kitchen';
    return `<article class="product-card"><div class="product-image-wrap">${imageOrPlaceholder(image)}<span class="product-badge">${Number(product.stock_quantity) > 0 ? 'BAKED WITH LOVE' : 'SOLD OUT'}</span><button class="quick-add" data-add="${product.id}" aria-label="Add ${escapeHtml(product.name)} to bag" ${Number(product.stock_quantity) < 1 ? 'disabled' : ''}>+</button></div><div class="product-meta"><div><h3 class="product-name">${escapeHtml(product.name)}</h3><span class="product-category">${escapeHtml(category)}</span></div><span class="product-price">${money(product.price)}</span></div>${product.description ? `<p class="product-description">${escapeHtml(product.description)}</p>` : ''}<div class="stock-note">${Number(product.stock_quantity) > 0 ? `${product.stock_quantity} available today` : 'Back soon, we hope'}</div></article>`;
  }).join('');
  grid.querySelectorAll('[data-add]').forEach(button => button.addEventListener('click', () => {
    const product = products.find(item => item.id === Number(button.dataset.add));
    try { cart.add(product); toast(`${product.name} added to your bag.`, 'success'); }
    catch (error) { toast(error.message, 'error'); }
  }));
}

export function initShop() {
  $('#product-search').addEventListener('input', event => { searchText = event.target.value.trim().toLowerCase(); renderProducts(); });
  $('#newsletter-shop').addEventListener('click', () => $('#catalog').scrollIntoView({ behavior: 'smooth' }));
  loadShop();
}
export function getProducts() { return products; }
