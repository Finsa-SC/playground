export const $ = (selector, root = document) => root.querySelector(selector);
export const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
export const escapeHtml = value => String(value ?? '').replace(/[&<>"']/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[char]));
export const money = value => new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', maximumFractionDigits: 0 }).format(Number(value || 0));
export function toast(message, type = '') {
  const region = $('#toast-region'); if (!region) return;
  const element = document.createElement('div'); element.className = `toast ${type}`; element.textContent = message; region.append(element);
  setTimeout(() => element.remove(), 4200);
}
export function openOverlay(id) { const element = document.getElementById(id); if (!element) return; element.classList.add('open'); element.setAttribute('aria-hidden', 'false'); document.body.classList.add('locked'); }
export function closeOverlay(id) { const element = document.getElementById(id); if (!element) return; element.classList.remove('open'); element.setAttribute('aria-hidden', 'true'); if (!document.querySelector('.overlay.open')) document.body.classList.remove('locked'); }
export function imageOrPlaceholder(url, className = 'product-image') {
  if (!url) return `<div class="product-placeholder" aria-label="No product photo">🥐</div>`;
  let displayUrl = url;
  try { const parsed = new URL(url, window.location.origin); if (parsed.pathname.startsWith('/media/product-images/')) displayUrl = parsed.pathname + parsed.search; } catch { /* Use the provided URL as-is. */ }
  return `<img class="${className}" src="${escapeHtml(displayUrl)}" alt="" loading="lazy" onerror="this.replaceWith(Object.assign(document.createElement('div'),{className:'product-placeholder',textContent:'🥐'}))">`;
}
export function setMessage(element, message, success = false) { if (!element) return; element.textContent = message || ''; element.classList.toggle('success', Boolean(success && message)); }
