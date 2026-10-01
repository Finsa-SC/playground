// Ubah kalau backend jalan di alamat lain
const API_URL = "http://localhost:8000";

const $ = (sel) => document.querySelector(sel);
const rupiah = (n) => "Rp " + Number(n || 0).toLocaleString("id-ID");
const emojis = ["🍞", "🥐", "🥖", "🥯", "🥨", "🧁"];

// ---------- Helper ----------
async function api(path, options = {}) {
  const res = await fetch(API_URL + path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    let msg = `Error ${res.status}`;
    try {
      const err = await res.json();
      if (typeof err.detail === "string") msg = err.detail;
      else if (Array.isArray(err.detail)) msg = err.detail.map((d) => d.msg).join(", ");
    } catch (_) {}
    throw new Error(msg);
  }
  return res.status === 204 ? null : res.json();
}

let toastTimer;
function toast(msg, isError = false) {
  const el = $("#toast");
  el.textContent = msg;
  el.className = "toast" + (isError ? " error" : "");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => el.classList.add("hidden"), 2800);
}

// Cegah XSS dari data produk
const esc = (s) =>
  String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

// Backend mengembalikan { data: [...] }
const toList = (data) => (Array.isArray(data) ? data : data?.data || data?.items || []);

// ---------- Health ----------
async function checkHealth() {
  const dot = $("#status");
  try {
    await api("/health");
    dot.className = "status on";
    dot.title = "API terhubung";
  } catch {
    dot.className = "status off";
    dot.title = "API tidak terhubung";
  }
}

// ---------- Toko ----------
function productCard(p) {
  const soldOut = p.stock !== undefined && p.stock <= 0;
  return `
    <article class="card">
      <div class="emoji">${emojis[p.id % emojis.length] || "🍞"}</div>
      <h4>${esc(p.product_name)}</h4>
      <p>${esc(p.description || "")}</p>
      <div class="meta">
        <span class="price">${rupiah(p.price)}</span>
        ${p.stock !== undefined ? `<span>Stok: ${esc(p.stock)}</span>` : ""}
      </div>
      <button class="btn" data-buy="${p.id}" ${soldOut ? "disabled" : ""}>
        ${soldOut ? "Habis" : "Beli"}
      </button>
    </article>`;
}

function renderGrid(el, list) {
  el.innerHTML = list.length ? list.map(productCard).join("") : '<p class="empty">Belum ada produk.</p>';
}

async function loadShop() {
  try {
    const [all, popular] = await Promise.all([api("/products/"), api("/products/popular")]);
    renderGrid($("#products"), toList(all));
    renderGrid($("#popular"), toList(popular));
  } catch (e) {
    toast("Gagal memuat produk: " + e.message, true);
  }
}

async function buyProduct(id) {
  try {
    await api(`/products/${id}/buy`, {
      method: "POST",
      body: JSON.stringify({ count: 1 })
    });
    toast("Berhasil dibeli! 🍞");
    loadShop();
  } catch (e) {
    toast(e.message, true);
  }
}

document.addEventListener("click", (e) => {
  const buy = e.target.closest("[data-buy]");
  if (buy) buyProduct(buy.dataset.buy);
});

// ---------- Admin ----------
async function loadAdmin() {
  const body = $("#admin-body");
  try {
    const list = toList(await api("/admin/products/"));
    body.innerHTML = list.length
      ? list.map((p) => `
          <tr>
            <td>${p.id}</td>
            <td>${esc(p.product_name)}</td>
            <td>${rupiah(p.price)}</td>
            <td>${esc(p.stock ?? "-")}</td>
            <td>
              <button class="btn small ghost" data-edit='${esc(JSON.stringify(p))}'>Edit</button>
              <button class="btn small danger" data-del="${p.id}">Hapus</button>
            </td>
          </tr>`).join("")
      : '<tr><td colspan="5" class="empty">Belum ada produk. Tambahkan lewat form di atas.</td></tr>';
  } catch (e) {
    toast("Gagal memuat data admin: " + e.message, true);
  }
}

function resetForm() {
  $("#product-form").reset();
  $("#f-id").value = "";
  $("#form-title").textContent = "Tambah produk";
  $("#f-cancel").classList.add("hidden");
}

$("#product-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const id = $("#f-id").value;
  const payload = {
    product_name: $("#f-name").value.trim(),
    price: Number($("#f-price").value),
    stock: Number($("#f-stock").value || 0),
    description: $("#f-desc").value.trim(),
  };
  try {
    if (id) {
      await api(`/admin/products/${id}`, { method: "PATCH", body: JSON.stringify(payload) });
      toast("Produk diperbarui");
    } else {
      await api("/admin/products/", { method: "POST", body: JSON.stringify(payload) });
      toast("Produk ditambahkan");
    }
    resetForm();
    loadAdmin();
  } catch (err) {
    toast(err.message, true);
  }
});

$("#f-cancel").addEventListener("click", resetForm);

$("#admin-body").addEventListener("click", async (e) => {
  const edit = e.target.closest("[data-edit]");
  const del = e.target.closest("[data-del]");
  if (edit) {
    const p = JSON.parse(edit.dataset.edit);
    $("#f-id").value = p.id;
    $("#f-name").value = p.product_name ?? "";
    $("#f-price").value = p.price ?? "";
    $("#f-stock").value = p.stock ?? "";
    $("#f-desc").value = p.description ?? "";
    $("#form-title").textContent = `Edit produk #${p.id}`;
    $("#f-cancel").classList.remove("hidden");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
  if (del && confirm("Hapus produk ini?")) {
    try {
      await api(`/admin/products/${del.dataset.del}`, { method: "DELETE" });
      toast("Produk dihapus");
      loadAdmin();
    } catch (err) {
      toast(err.message, true);
    }
  }
});

// ---------- Tab ----------
document.querySelectorAll(".tab").forEach((btn) =>
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((b) => b.classList.toggle("active", b === btn));
    const view = btn.dataset.view;
    $("#view-shop").classList.toggle("hidden", view !== "shop");
    $("#view-admin").classList.toggle("hidden", view !== "admin");
    view === "shop" ? loadShop() : loadAdmin();
  })
);

// ---------- Start ----------
checkHealth();
loadShop();