import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Clean sec-guardados
guardados_pattern = r'(<section id="sec-guardados" class="dash-section space-y-6">.*?<p class="text-xs text-gray-500 mt-1">Tus favoritos listos para testear</p>\s*</div>\s*</div>).*?(</section>)'
html = re.sub(guardados_pattern, r'\1\n      <div id="savedContent"></div>\n    \2', html, flags=re.DOTALL)

# 2. Clean sec-perfil
perfil_pattern = r'(<section id="sec-perfil" class="dash-section space-y-6">.*?<p class="text-xs text-gray-500 mt-1">Ajustes de cuenta</p>\s*</div>\s*</div>).*?(</section>)'
html = re.sub(perfil_pattern, r'\1\n      <div id="perfilContent"></div>\n    \2', html, flags=re.DOTALL)

# 3. Clean sec-negocio
negocio_pattern = r'(<section id="sec-negocio" class="dash-section space-y-6">.*?<p class="text-xs text-gray-500 mt-1">Registra tus ventas y sube de nivel</p>\s*</div>).*?(</section>)'
# Note: In dashboard.html, the button "Cargar Producto" is right after the <p> tag inside the flex container. We need to preserve it if it's outside, or let renderNegocio handle it. In original_index.html, it was outside. Let's just replace the body of the section.
negocio_replacement = r'\1\n        <button onclick="showAddProductModal()" class="bg-black text-white px-5 py-2.5 rounded-full text-xs font-bold uppercase tracking-wider saas-shadow hover:-translate-y-0.5 transition flex items-center gap-2"><i data-lucide="plus" class="w-4 h-4"></i> Cargar Producto</button>\n      </div>\n      <div id="negocioContent" class="space-y-6"></div>\n    \2'
html = re.sub(negocio_pattern, negocio_replacement, html, flags=re.DOTALL)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

js_code = """
// --- DATA MANAGEMENT ---
function getProfile() {
  try { return JSON.parse(localStorage.getItem('tb_profile')) || { sellCurrency: 'ARS', buyCurrency: 'USD' }; }
  catch(e){ return { sellCurrency: 'ARS', buyCurrency: 'USD' }; }
}
function saveProfile(data) { localStorage.setItem('tb_profile', JSON.stringify(data)); }

function getNegocioProducts() {
  try { return JSON.parse(localStorage.getItem('tb_negocio')) || []; }
  catch(e){ return []; }
}
function saveNegocioProducts(arr) { localStorage.setItem('tb_negocio', JSON.stringify(arr)); }

function getSavedProducts() {
  try { return JSON.parse(localStorage.getItem('tb_saved')) || []; }
  catch(e){ return []; }
}

// --- RENDER PERFIL ---
function renderPerfil() {
  const el = document.getElementById('perfilContent');
  if(!el) return;
  const p = getProfile();
  
  el.innerHTML = `
    <div class="bg-white rounded-[2rem] p-8 saas-shadow border border-gray-100 max-w-3xl">
      <div class="flex items-center gap-6 mb-8 border-b border-gray-100 pb-8">
        <div class="w-20 h-20 bg-gray-900 rounded-full flex items-center justify-center text-white text-3xl font-bold">U</div>
        <div>
          <h3 class="text-xl font-bold text-gray-900">Usuario TrendBase</h3>
          <p class="text-sm text-gray-500">${p.email || 'usuario@trendbase.com'}</p>
          <div class="mt-2 inline-block bg-black text-white text-[10px] font-bold px-2 py-1 rounded-md uppercase tracking-wider">Plan Pro</div>
        </div>
      </div>
      
      <div class="space-y-6">
        <div>
          <label class="text-[10px] font-bold text-gray-500 uppercase tracking-wider block mb-2">Nombre de tu Tienda</label>
          <input type="text" id="profStore" value="${p.storeName || ''}" placeholder="Ej: TechStore Argentina" class="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 outline-none focus:border-gray-400 saas-shadow-sm transition">
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="text-[10px] font-bold text-gray-500 uppercase tracking-wider block mb-2">Moneda de Venta</label>
            <select id="profSellCurr" class="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 outline-none focus:border-gray-400 saas-shadow-sm transition">
              <option value="ARS" ${p.sellCurrency==='ARS'?'selected':''}>ARS (Pesos Arg)</option>
              <option value="CLP" ${p.sellCurrency==='CLP'?'selected':''}>CLP (Pesos Chi)</option>
              <option value="USD" ${p.sellCurrency==='USD'?'selected':''}>USD (Dólares)</option>
              <option value="EUR" ${p.sellCurrency==='EUR'?'selected':''}>EUR (Euros)</option>
            </select>
          </div>
          <div>
            <label class="text-[10px] font-bold text-gray-500 uppercase tracking-wider block mb-2">Moneda de Compra (Costo)</label>
            <select id="profBuyCurr" class="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 outline-none focus:border-gray-400 saas-shadow-sm transition">
              <option value="USD" ${p.buyCurrency==='USD'?'selected':''}>USD (Dólares)</option>
              <option value="EUR" ${p.buyCurrency==='EUR'?'selected':''}>EUR (Euros)</option>
              <option value="ARS" ${p.buyCurrency==='ARS'?'selected':''}>ARS (Pesos Arg)</option>
            </select>
          </div>
        </div>
        <button onclick="savePerfil()" class="mt-4 bg-black text-white px-6 py-3 rounded-xl text-xs font-extrabold uppercase tracking-wider saas-shadow hover:-translate-y-0.5 transition w-full">Guardar Cambios</button>
      </div>
    </div>
  `;
}

window.savePerfil = function() {
  const p = getProfile();
  p.storeName = document.getElementById('profStore').value;
  p.sellCurrency = document.getElementById('profSellCurr').value;
  p.buyCurrency = document.getElementById('profBuyCurr').value;
  saveProfile(p);
  alert('Perfil actualizado.');
  renderPerfil();
};

// --- RENDER NEGOCIO ---
function renderNegocio() {
  const el = document.getElementById('negocioContent');
  if(!el) return;
  const products = getNegocioProducts();
  const profile = getProfile();
  const sellCurrency = profile.sellCurrency || 'ARS';
  const buyCurrency = profile.buyCurrency || 'USD';

  let totalInverted=0, totalRevenue=0, totalAds=0, totalStock=0, totalSold=0;
  products.forEach(p => {
    const costConverted = p.cost * p.fx;
    totalInverted += costConverted * p.stock;
    totalRevenue += p.price * p.sold;
    totalAds += p.ads;
    totalStock += p.stock;
    totalSold += p.sold;
  });

  const totalProfit = totalRevenue - totalInverted - totalAds;
  const roi = totalInverted > 0 ? Math.round(totalProfit / (totalInverted + totalAds) * 100) : 0;
  const stockValue = products.reduce((a, p) => a + p.cost * (p.fx || 1100) * (p.stock - p.sold), 0);

  el.innerHTML = `
    <!-- KPIs Financieros -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <div class="bg-white border border-gray-100 rounded-2xl p-5 saas-shadow saas-card-hover">
        <div class="text-[9px] text-gray-500 uppercase font-mono tracking-wider font-bold">Ingresos totales</div>
        <div class="text-2xl font-extrabold text-green-500 mt-1">$${totalRevenue.toLocaleString()} ${sellCurrency}</div>
        <div class="text-[9px] text-gray-400 font-mono mt-1 font-bold">${totalSold} unidades vendidas</div>
      </div>
      <div class="bg-white border border-gray-100 rounded-2xl p-5 saas-shadow saas-card-hover">
        <div class="text-[9px] text-gray-500 uppercase font-mono tracking-wider font-bold">Ganancia Neta</div>
        <div class="text-2xl font-extrabold mt-1 ${totalProfit>=0?'text-green-500':'text-red-500'}">$${totalProfit.toLocaleString()} ${sellCurrency}</div>
        <div class="text-[9px] text-gray-400 font-mono mt-1 font-bold">ROI: ${roi}%</div>
      </div>
      <div class="bg-white border border-gray-100 rounded-2xl p-5 saas-shadow saas-card-hover">
        <div class="text-[9px] text-gray-500 uppercase font-mono tracking-wider font-bold">Inversión Stock</div>
        <div class="text-2xl font-extrabold text-gray-900 mt-1">$${(totalInverted+totalAds).toLocaleString()} ${sellCurrency}</div>
        <div class="text-[9px] text-gray-400 font-mono mt-1 font-bold">Stock + Publicidad</div>
      </div>
      <div class="bg-white border border-gray-100 rounded-2xl p-5 saas-shadow saas-card-hover">
        <div class="text-[9px] text-gray-500 uppercase font-mono tracking-wider font-bold">Valor en Stock</div>
        <div class="text-2xl font-extrabold text-gray-900 mt-1">$${stockValue.toLocaleString()} ${sellCurrency}</div>
        <div class="text-[9px] text-gray-400 font-mono mt-1 font-bold">${totalStock-totalSold} unidades disponibles</div>
      </div>
    </div>

    <!-- Tabla Negocio -->
    <div class="bg-white border border-gray-100 rounded-[2rem] overflow-hidden saas-shadow">
      <div class="p-6 border-b border-gray-100 bg-gray-50">
        <h3 class="text-xs font-mono text-gray-800 font-bold uppercase tracking-widest">Mis Productos de Venta</h3>
      </div>
      
      <div class="overflow-x-auto">
        <table class="w-full text-xs text-left">
          <thead>
            <tr class="border-b border-gray-100 text-gray-500 font-mono uppercase text-[9px] font-bold">
              <th class="p-4">Producto</th>
              <th class="p-4 text-right">Costo</th>
              <th class="p-4 text-right">Venta</th>
              <th class="p-4 text-right">Stock</th>
              <th class="p-4 text-right">Vendido</th>
              <th class="p-4 text-right">Ganancia</th>
              <th class="p-4 text-right">Acciones</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-50 text-gray-900 font-medium">
            ${products.length ? products.map((p, i) => {
              const costSell = p.cost * p.fx;
              const profit = (p.price - costSell) * p.sold - p.ads;
              return `
                <tr class="hover:bg-gray-50 transition text-xs">
                  <td class="p-4 font-extrabold text-gray-900">${p.name}</td>
                  <td class="p-4 text-right font-mono">${p.cost} ${buyCurrency} <br> <span class="text-[9px] text-gray-400 font-bold">$${costSell.toFixed(0)} ARS</span></td>
                  <td class="p-4 text-right font-mono font-extrabold">$${p.price.toLocaleString()}</td>
                  <td class="p-4 text-right font-mono">${p.stock - p.sold}/${p.stock}</td>
                  <td class="p-4 text-right font-mono text-green-500 font-bold">${p.sold}</td>
                  <td class="p-4 text-right font-mono font-extrabold ${profit>=0?'text-green-500':'text-red-500'}">$${profit.toFixed(0)}</td>
                  <td class="p-4 text-right">
                    <div class="flex gap-2 justify-end">
                      <button onclick="quickSale(${i})" class="bg-green-100 hover:bg-green-200 text-green-700 border border-green-200 px-2.5 py-1 rounded-lg text-[10px] font-bold transition">+1 Venta</button>
                      <button onclick="showAddProductModal(${i})" class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-2.5 py-1 border border-gray-200 rounded-lg text-[10px] font-bold transition">Editar</button>
                    </div>
                  </td>
                </tr>
              `;
            }).join('') : `<tr><td colspan="7" class="p-8 text-center text-gray-500 font-mono font-bold">No has agregado productos. Haz click en "+ Cargar Producto" para iniciar.</td></tr>`}
          </tbody>
        </table>
      </div>
    </div>
  `;
}

// Negocio Modal
var editingNegocioIdx = null;
window.showAddProductModal = function(idx) {
  if (typeof idx === 'object' || idx instanceof Event) idx = undefined; // Fix click passing event
  editingNegocioIdx = idx !== undefined ? idx : null;
  const products = getNegocioProducts();
  const p = idx !== undefined ? products[idx] : {};
  
  const overlay = document.createElement('div');
  overlay.id = 'negocioModal';
  overlay.className = 'fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm';

  overlay.innerHTML = `
    <div class="bg-white border border-gray-100 rounded-[2.5rem] w-full max-w-md overflow-hidden saas-shadow p-8">
      <div class="flex items-center justify-between border-b border-gray-100 pb-4 mb-6">
        <h3 class="text-base font-bold text-gray-900">${idx !== undefined ? 'Editar' : 'Agregar'} Producto</h3>
        <button onclick="document.getElementById('negocioModal').remove()" class="text-gray-400 hover:text-gray-900"><i data-lucide="x" class="w-5 h-5"></i>✕</button>
      </div>

      <div class="space-y-4 text-xs font-mono">
        <div>
          <label class="text-[9px] text-gray-500 uppercase block mb-1 font-bold tracking-wider">Nombre del producto</label>
          <input id="np-name" value="${p.name || ''}" placeholder="Ej: Mini proyector" class="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 outline-none focus:border-gray-400 saas-shadow-sm transition">
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="text-[9px] text-gray-500 uppercase block mb-1 font-bold tracking-wider">Costo Unitario (USD)</label>
            <input id="np-cost" type="number" step="0.01" value="${p.cost || ''}" class="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 outline-none focus:border-gray-400 saas-shadow-sm transition">
          </div>
          <div>
            <label class="text-[9px] text-gray-500 uppercase block mb-1 font-bold tracking-wider">Venta Unitario (ARS)</label>
            <input id="np-price" type="number" value="${p.price || ''}" class="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 outline-none focus:border-gray-400 saas-shadow-sm transition">
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="text-[9px] text-gray-500 uppercase block mb-1 font-bold tracking-wider">Stock Comprado</label>
            <input id="np-stock" type="number" value="${p.stock || ''}" class="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 outline-none focus:border-gray-400 saas-shadow-sm transition">
          </div>
          <div>
            <label class="text-[9px] text-gray-500 uppercase block mb-1 font-bold tracking-wider">Vendidos</label>
            <input id="np-sold" type="number" value="${p.sold || 0}" class="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 outline-none focus:border-gray-400 saas-shadow-sm transition">
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="text-[9px] text-gray-500 uppercase block mb-1 font-bold tracking-wider">Inversión Ads</label>
            <input id="np-ads" type="number" value="${p.ads || 0}" class="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 outline-none focus:border-gray-400 saas-shadow-sm transition">
          </div>
          <div>
            <label class="text-[9px] text-gray-500 uppercase block mb-1 font-bold tracking-wider">Tipo de cambio FX</label>
            <input id="np-fx" type="number" value="${p.fx || 1100}" class="w-full bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 text-gray-900 outline-none focus:border-gray-400 saas-shadow-sm transition">
          </div>
        </div>

        <div class="flex gap-3 pt-4 border-t border-gray-100">
          <button onclick="saveNegocioProduct()" class="flex-1 py-3 bg-black text-white font-extrabold uppercase rounded-xl tracking-wider saas-shadow hover:-translate-y-0.5 transition">Guardar</button>
          ${idx !== undefined ? `<button onclick="deleteNegocioProduct(${idx})" class="py-3 px-4 border border-red-200 text-red-500 bg-red-50 rounded-xl hover:bg-red-100 transition font-bold">Eliminar</button>` : ''}
        </div>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);
};

window.saveNegocioProduct = function() {
  const products = getNegocioProducts();
  const p = {
    name: document.getElementById('np-name').value.trim(),
    cost: parseFloat(document.getElementById('np-cost').value) || 0,
    price: parseFloat(document.getElementById('np-price').value) || 0,
    stock: parseInt(document.getElementById('np-stock').value) || 0,
    sold: parseInt(document.getElementById('np-sold').value) || 0,
    ads: parseFloat(document.getElementById('np-ads').value) || 0,
    fx: parseFloat(document.getElementById('np-fx').value) || 1100,
    status: 'activo'
  };

  if(!p.name) return alert('Ingresá el nombre');
  
  if(editingNegocioIdx !== null) {
    products[editingNegocioIdx] = p;
  } else {
    products.push(p);
  }
  
  saveNegocioProducts(products);
  document.getElementById('negocioModal').remove();
  renderNegocio();
};

window.deleteNegocioProduct = function(idx) {
  if(!confirm('¿Eliminar producto?')) return;
  const products = getNegocioProducts();
  products.splice(idx, 1);
  saveNegocioProducts(products);
  document.getElementById('negocioModal').remove();
  renderNegocio();
};

window.quickSale = function(idx) {
  const products = getNegocioProducts();
  if(!products[idx]) return;
  if(products[idx].sold >= products[idx].stock) {
    alert('Sin stock disponible');
    return;
  }
  products[idx].sold = (products[idx].sold || 0) + 1;
  saveNegocioProducts(products);
  renderNegocio();
};

// --- RENDER GUARDADOS ---
function renderSaved() {
  const el = document.getElementById('savedContent');
  if(!el) return;
  const saved = getSavedProducts();
  
  if(saved.length === 0) {
    el.innerHTML = `
      <div class="bg-white rounded-[2rem] p-12 text-center saas-shadow border border-gray-100">
        <div class="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mx-auto mb-4 border border-gray-200">
          <i data-lucide="bookmark" class="w-8 h-8 text-gray-300"></i>
        </div>
        <h3 class="text-gray-900 font-bold mb-2">Aún no hay productos guardados</h3>
        <p class="text-xs text-gray-500 max-w-sm mx-auto">Explora la sección de Tendencias y haz clic en el ícono de guardado para añadir productos aquí.</p>
      </div>
    `;
    return;
  }

  el.innerHTML = `
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      ${saved.map(p => `
        <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover border border-gray-100 relative group">
          <div class="w-12 h-12 bg-gray-50 rounded-xl mb-4 flex items-center justify-center border border-gray-200">
            <i data-lucide="package" class="w-6 h-6 text-gray-400"></i>
          </div>
          <h3 class="font-bold text-gray-900 text-sm mb-1">${p.name || 'Producto Guardado'}</h3>
          <div class="text-[11px] font-bold text-green-500 mb-4">${p.score || 80} TrendScore</div>
          <button class="w-full py-2 bg-gray-50 hover:bg-gray-100 text-gray-900 text-[10px] font-bold uppercase tracking-wider rounded-xl transition border border-gray-200">Ver Análisis</button>
        </div>
      `).join('')}
    </div>
  `;
}

// Hook into showSection to auto-render dynamic sections
const origShowSection = window.showSection;
window.showSection = function(id, el) {
  if (origShowSection) origShowSection(id, el);
  else {
    document.querySelectorAll('.dash-section').forEach(s => s.classList.add('hidden'));
    const sec = document.getElementById(id);
    if(sec) sec.classList.remove('hidden');
  }
  
  if (id === 'sec-negocio') renderNegocio();
  if (id === 'sec-perfil') renderPerfil();
  if (id === 'sec-guardados') renderSaved();
};

// Initialize renders
setTimeout(() => {
  renderNegocio();
  renderPerfil();
  renderSaved();
}, 1000);
"""

with open('app.js', 'a', encoding='utf-8') as f:
    f.write('\n' + js_code)
