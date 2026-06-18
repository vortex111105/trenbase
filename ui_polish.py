import re

# --- DASHBOARD.HTML ---
with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix Titles
html = html.replace('<h2 class="text-3xl font-extrabold text-white tracking-tight">Dashboard Financiero de Ventas</h2>',
                    '<h2 class="text-3xl font-extrabold text-gray-900 tracking-tight">Dashboard Financiero de Ventas</h2>')
html = html.replace('<p class="text-xs text-gray-400 mt-1">Estadísticas reales de facturación e inversión publicitaria</p>',
                    '<p class="text-xs text-gray-500 mt-1">Estadísticas reales de facturación e inversión publicitaria</p>')
html = html.replace('<h2 class="text-3xl font-extrabold text-white tracking-tight">Mis Productos Guardados</h2>',
                    '<h2 class="text-3xl font-extrabold text-gray-900 tracking-tight">Mis Productos Guardados</h2>')
html = html.replace('<p class="text-xs text-gray-400 mt-1">Lista de productos seleccionados para seguimiento</p>',
                    '<p class="text-xs text-gray-500 mt-1">Lista de productos seleccionados para seguimiento</p>')

# 2. Fix Sidebar PRO Button
# It's likely <a href="#" class="flex items-center justify-center lg:justify-start w-full px-4 py-3 text-sm font-bold rounded-2xl text-black bg-champagne ...
old_pro_btn_match = re.search(r'(<a href="#" class="[^"]*bg-champagne[^"]*">.*?</a>)', html, re.DOTALL)
if old_pro_btn_match:
    old_pro_btn = old_pro_btn_match.group(1)
    new_pro_btn = """<a href="#" class="group flex items-center justify-center lg:justify-start w-full px-4 py-3 text-sm font-bold rounded-2xl text-black bg-champagne hover:bg-yellow-400 transition-all duration-300 saas-shadow-sm shadow-yellow-500/20">
          <i data-lucide="star" class="w-5 h-5 flex-shrink-0"></i>
          <span class="opacity-0 w-0 group-hover:opacity-100 group-hover:w-auto transition-all duration-300 group-hover:ml-3 overflow-hidden whitespace-nowrap">Obtener Plan PRO</span>
        </a>"""
    html = html.replace(old_pro_btn, new_pro_btn)

# 3. Update sec-perfil
match_perfil = re.search(r'(<section id="sec-perfil".*?</section>)', html, re.DOTALL)
if match_perfil:
    old_perfil = match_perfil.group(1)
    new_perfil = """<section id="sec-perfil" class="dash-section space-y-6">
      <div class="flex justify-between items-center mb-6">
        <div>
          <h2 class="text-3xl font-extrabold text-gray-900 tracking-tight">Mi Perfil de Vendedor</h2>
          <p class="text-xs text-gray-500 mt-1">Configura las monedas de tu negocio y metas</p>
        </div>
      </div>
      <div class="bg-[#15151B] rounded-[2rem] p-8 max-w-2xl border border-gray-800 saas-shadow-lg">
        <div class="flex items-center gap-4 mb-8 pb-8 border-b border-gray-800">
          <div class="w-16 h-16 bg-champagne text-black rounded-full flex items-center justify-center text-2xl font-black">?</div>
          <div>
            <h3 class="text-xl font-bold text-white">Tu Nombre</h3>
            <p class="text-xs text-gray-500">País no definido · Plan STARTER</p>
          </div>
        </div>
        <div class="space-y-6">
          <div>
            <label class="text-[10px] text-gray-500 font-bold uppercase tracking-widest block mb-2">Nombre o Apodo</label>
            <input type="text" placeholder="Ej: Ignacio" class="w-full bg-[#1E1E26] border border-gray-800 rounded-xl py-3 px-4 text-sm font-medium text-white focus:outline-none focus:border-champagne transition">
          </div>
          <div>
            <label class="text-[10px] text-gray-500 font-bold uppercase tracking-widest block mb-2">País</label>
            <select class="w-full bg-[#1E1E26] border border-gray-800 rounded-xl py-3 px-4 text-sm font-medium text-white focus:outline-none focus:border-champagne transition appearance-none">
              <option>Selecciona tu país</option>
              <option>Argentina</option>
              <option>México</option>
              <option>Colombia</option>
              <option>Chile</option>
              <option>España</option>
            </select>
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="text-[10px] text-gray-500 font-bold uppercase tracking-widest block mb-2">Moneda de Venta</label>
              <select class="w-full bg-[#1E1E26] border border-gray-800 rounded-xl py-3 px-4 text-sm font-medium text-white focus:outline-none focus:border-champagne transition appearance-none">
                <option>ARS</option>
                <option>USD</option>
                <option>MXN</option>
                <option>COP</option>
                <option>CLP</option>
                <option>EUR</option>
              </select>
            </div>
            <div>
              <label class="text-[10px] text-gray-500 font-bold uppercase tracking-widest block mb-2">Moneda de Compra</label>
              <select class="w-full bg-[#1E1E26] border border-gray-800 rounded-xl py-3 px-4 text-sm font-medium text-white focus:outline-none focus:border-champagne transition appearance-none">
                <option>USD</option>
                <option>EUR</option>
              </select>
            </div>
          </div>
          <div>
            <label class="text-[10px] text-gray-500 font-bold uppercase tracking-widest block mb-2">Meta Mensual de Ventas</label>
            <input type="number" value="10" class="w-32 bg-[#1E1E26] border border-gray-800 rounded-xl py-3 px-4 text-sm font-medium text-white focus:outline-none focus:border-champagne transition">
          </div>
          <button class="w-full bg-champagne text-black font-extrabold py-4 rounded-xl mt-4 hover:bg-yellow-500 transition saas-shadow shadow-yellow-500/20 uppercase tracking-widest text-sm">Guardar Perfil</button>
        </div>
      </div>
    </section>"""
    html = html.replace(old_perfil, new_perfil)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

# --- APP.JS ---
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace product modal generation entirely to add interactive tabs
match_modal = re.search(r'const modal = `(.*?)`;\s*document\.body\.insertAdjacentHTML', js, re.DOTALL)
if match_modal:
    new_modal_js = """
    // Guardamos la info del producto en variable global para las pestañas
    window.currentProductData = product;
    window.currentProductIdx = idx;

    const modal = `
    <div id="productModal" class="fixed inset-0 z-50 bg-[#0D0D12]/90 backdrop-blur-md flex items-center justify-center p-4 sm:p-6 opacity-0 transition-opacity duration-300">
      <div class="bg-[#1E1E26] w-full max-w-4xl rounded-3xl saas-shadow-2xl relative flex flex-col md:flex-row overflow-hidden border border-gray-800 transform scale-95 transition-transform duration-300" id="productModalContent">
        
        <button onclick="closeProductModal()" class="absolute top-4 right-4 bg-gray-800 text-gray-400 hover:text-white p-2 rounded-full z-10 transition"><i data-lucide="x" class="w-4 h-4"></i></button>

        <div class="w-full md:w-2/5 h-64 md:h-auto bg-gray-900 relative">
          <img src="${product.image}" class="w-full h-full object-cover opacity-80" alt="${product.name}">
          <div class="absolute inset-0 bg-gradient-to-t from-[#1E1E26] to-transparent"></div>
        </div>
        
        <div class="w-full md:w-3/5 p-8 flex flex-col h-[600px] overflow-y-auto custom-scrollbar">
          
          <h2 class="text-2xl font-extrabold text-white mb-6 leading-tight">${product.name}</h2>
          
          <div class="flex items-end gap-3 mb-8">
            <span class="text-5xl font-black text-white">${product.score}</span>
            <div class="pb-1 flex items-center gap-2">
              <span class="text-xs text-gray-400 font-bold tracking-widest uppercase">Trendscore</span>
              <span class="bg-champagne text-black text-[10px] font-black px-2 py-0.5 rounded-sm uppercase tracking-wider">HOT</span>
            </div>
          </div>

          <div class="flex gap-6 border-b border-gray-800 mb-6 relative">
            <button onclick="switchModalTab('info')" id="tab-info" class="pb-2 text-sm font-bold text-champagne border-b-2 border-champagne transition-colors">Información</button>
            <button onclick="switchModalTab('historial')" id="tab-historial" class="pb-2 text-sm font-bold text-gray-500 border-b-2 border-transparent hover:text-gray-300 transition-colors">Historial 90 días</button>
            <button onclick="switchModalTab('proveedores')" id="tab-proveedores" class="pb-2 text-sm font-bold text-gray-500 border-b-2 border-transparent hover:text-gray-300 transition-colors">Proveedores</button>
            <button onclick="switchModalTab('marketing')" id="tab-marketing" class="pb-2 text-sm font-bold text-gray-500 border-b-2 border-transparent hover:text-gray-300 flex items-center gap-1 transition-colors"><i data-lucide="sparkles" class="w-3 h-3"></i> Marketing IA</button>
          </div>

          <!-- Contenedor dinámico de pestañas -->
          <div id="modal-tab-content" class="flex-1 flex flex-col">
            ${getTabInfoHTML(product, idx)}
          </div>

        </div>
      </div>
    </div>
    `;
    """
    js = js[:match_modal.start()] + new_modal_js + js[match_modal.end():]

# Now append the new functions at the end of app.js
tab_logic_js = """
// --- Lógica de Pestañas del Modal ---
window.getTabInfoHTML = function(product, idx) {
  return `
    <div class="grid grid-cols-2 lg:grid-cols-3 gap-3 mb-8 fade-in">
      <div class="bg-[#15151B] border border-gray-800 rounded-2xl p-4 flex flex-col items-center justify-center text-center">
        <span class="text-champagne text-lg font-bold">down</span>
        <span class="text-[9px] text-gray-500 uppercase tracking-widest font-bold mt-1">Cambio 24hs</span>
      </div>
      <div class="bg-[#15151B] border border-gray-800 rounded-2xl p-4 flex flex-col items-center justify-center text-center">
        <span class="text-green-400 text-lg font-bold">${product.roi}% ROI</span>
        <span class="text-[9px] text-gray-500 uppercase tracking-widest font-bold mt-1">Margen Est.</span>
      </div>
      <div class="bg-[#15151B] border border-gray-800 rounded-2xl p-4 flex flex-col items-center justify-center text-center">
        <span class="text-white text-base font-bold">${product.category || 'Moda'}</span>
        <span class="text-[9px] text-gray-500 uppercase tracking-widest font-bold mt-1">Categoría</span>
      </div>
      <div class="bg-[#15151B] border border-gray-800 rounded-2xl p-4 flex flex-col items-center justify-center text-center col-span-2 lg:col-span-1">
        <span class="text-white text-lg font-bold">$131 - $159</span>
        <span class="text-[9px] text-gray-500 uppercase tracking-widest font-bold mt-1">Precio Venta Est.</span>
      </div>
      <div class="bg-[#15151B] border border-gray-800 rounded-2xl p-4 flex flex-col items-center justify-center text-center col-span-2">
        <span class="text-green-500 border border-green-500/50 px-3 py-1 rounded-sm text-xs font-bold uppercase">Baja</span>
        <span class="text-[9px] text-gray-500 uppercase tracking-widest font-bold mt-2">Competencia</span>
      </div>
    </div>
    <div class="space-y-6 flex-1 fade-in">
      <div>
        <span class="text-[10px] text-gray-500 font-bold uppercase tracking-widest mb-3 block">Plataformas donde es tendencia</span>
        <div class="flex gap-2">
          <span class="bg-[#2A2A35] text-white text-xs px-3 py-1.5 rounded-md">Pinterest</span>
          <span class="bg-[#2A2A35] text-white text-xs px-3 py-1.5 rounded-md">TikTok</span>
        </div>
      </div>
      <div>
        <span class="text-[10px] text-gray-500 font-bold uppercase tracking-widest mb-3 block">Regiones Activas</span>
        <div class="flex gap-2">
          <span class="bg-[#2A2A35] border border-gray-700 text-white text-xs px-3 py-1.5 rounded-md flex items-center gap-2">🇨🇱 CL</span>
        </div>
      </div>
      <div>
        <span class="text-[10px] text-champagne font-bold uppercase tracking-widest mb-3 flex items-center gap-2"><i data-lucide="shopping-bag" class="w-3 h-3"></i> Recomendado vender en:</span>
        <div class="flex gap-2 flex-wrap">
          <span class="text-white border border-white/20 px-2 py-1 rounded-md text-[11px] font-bold flex items-center gap-1"><i data-lucide="shopping-cart" class="w-3 h-3 text-champagne"></i> Shopify</span>
          <span class="text-blue-400 border border-blue-400/20 px-2 py-1 rounded-md text-[11px] font-bold flex items-center gap-1"><i data-lucide="cloud" class="w-3 h-3"></i> TiendaNube</span>
        </div>
      </div>
    </div>
    <div class="mt-8 pt-6 border-t border-gray-800 grid grid-cols-2 gap-3 fade-in">
      <button onclick="alert('Comparador Abierto')" class="w-full bg-[#2A2A35] hover:bg-gray-700 text-white font-extrabold text-sm py-4 rounded-xl transition flex items-center justify-center gap-2">
        <i data-lucide="git-compare" class="w-5 h-5"></i> Comparar
      </button>
      <button onclick="window.startImportWorkflow(${idx})" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-sm py-4 rounded-xl saas-shadow transition hover:-translate-y-0.5 flex items-center justify-center gap-2">
        <i data-lucide="cloud-lightning" class="w-5 h-5"></i> Importar
      </button>
    </div>
  `;
}

window.getTabProveedoresHTML = function() {
  return `
    <div class="fade-in flex-1 flex flex-col">
      <span class="text-[10px] text-gray-500 font-bold uppercase tracking-widest mb-4 block">Dónde comprar (Est. AliExpress)</span>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        <!-- AliExpress -->
        <div class="bg-[#15151B] border border-gray-800 rounded-2xl p-4 hover:border-champagne transition cursor-pointer group">
          <h4 class="text-white font-bold text-sm mb-1 group-hover:text-champagne transition flex items-center gap-1"><i data-lucide="shopping-cart" class="w-4 h-4"></i> AliExpress</h4>
          <p class="text-[9px] text-gray-500 mb-1">10-25 días · Envío gratis</p>
          <p class="text-[10px] text-gray-400 mb-3">El más popular para dropshipping</p>
          <span class="text-green-400 font-black text-sm">~USD 7.92</span>
        </div>
        <!-- Alibaba -->
        <div class="bg-[#15151B] border border-gray-800 rounded-2xl p-4 hover:border-champagne transition cursor-pointer group">
          <h4 class="text-white font-bold text-sm mb-1 group-hover:text-champagne transition flex items-center gap-1"><i data-lucide="building" class="w-4 h-4 text-orange-400"></i> Alibaba</h4>
          <p class="text-[9px] text-gray-500 mb-1">28-35 días · Mayorista</p>
          <p class="text-[10px] text-gray-400 mb-3">Precios más bajos, mínimo por lote</p>
          <span class="text-green-400 font-black text-sm">~USD 7.92</span>
        </div>
        <!-- CJ Dropshipping -->
        <div class="bg-[#15151B] border border-gray-800 rounded-2xl p-4 hover:border-champagne transition cursor-pointer group">
          <h4 class="text-white font-bold text-sm mb-1 group-hover:text-champagne transition flex items-center gap-1"><i data-lucide="rocket" class="w-4 h-4 text-red-500"></i> CJ Dropshipping</h4>
          <p class="text-[9px] text-gray-500 mb-1">7-12 días · Bodega LATAM</p>
          <p class="text-[10px] text-gray-400 mb-3">Bodega en Brasil y México</p>
          <span class="text-green-400 font-black text-sm">~USD 7.92</span>
        </div>
        <!-- Dropdeal -->
        <div class="bg-[#15151B] border border-gray-800 rounded-2xl p-4 hover:border-champagne transition cursor-pointer group">
          <h4 class="text-white font-bold text-sm mb-1 group-hover:text-champagne transition flex items-center gap-1"><i data-lucide="package" class="w-4 h-4 text-amber-600"></i> Dropdeal</h4>
          <p class="text-[9px] text-gray-500 mb-1">5-10 días · Envío LATAM</p>
          <p class="text-[10px] text-gray-400 mb-3">Especializado en Latinoamérica</p>
          <span class="text-green-400 font-black text-sm">~USD 7.92</span>
        </div>
        <!-- Droppi -->
        <div class="bg-[#15151B] border border-gray-800 rounded-2xl p-4 hover:border-champagne transition cursor-pointer group">
          <h4 class="text-white font-bold text-sm mb-1 group-hover:text-champagne transition flex items-center gap-1"><i data-lucide="truck" class="w-4 h-4 text-blue-400"></i> Droppi</h4>
          <p class="text-[9px] text-gray-500 mb-1">2-5 días · Contra Entrega</p>
          <p class="text-[10px] text-gray-400 mb-3">Pago Contra Entrega en Colombia</p>
          <span class="text-green-400 font-black text-sm">~USD 7.92</span>
        </div>
        <!-- Rocketfy -->
        <div class="bg-[#15151B] border border-gray-800 rounded-2xl p-4 hover:border-champagne transition cursor-pointer group">
          <h4 class="text-white font-bold text-sm mb-1 group-hover:text-champagne transition flex items-center gap-1"><i data-lucide="zap" class="w-4 h-4 text-purple-500"></i> Rocketfy</h4>
          <p class="text-[9px] text-gray-500 mb-1">3-6 días · Nacional</p>
          <p class="text-[10px] text-gray-400 mb-3">Envíos Nacionales en LATAM</p>
          <span class="text-green-400 font-black text-sm">~USD 7.92</span>
        </div>
      </div>
    </div>
  `;
}

window.getTabHistorialHTML = function() {
  return `
    <div class="fade-in flex-1 flex items-center justify-center border border-dashed border-gray-800 rounded-2xl bg-[#15151B] flex-col p-8 text-center">
      <i data-lucide="line-chart" class="w-12 h-12 text-gray-600 mb-4"></i>
      <h3 class="text-lg font-bold text-white">Historial de 90 Días</h3>
      <p class="text-xs text-gray-400 mt-2 max-w-xs">El gráfico detallado de ventas históricas estará disponible muy pronto.</p>
    </div>
  `;
}

window.getTabMarketingHTML = function() {
  return `
    <div class="fade-in flex-1 flex flex-col space-y-4">
      <span class="text-[10px] text-gray-500 font-bold uppercase tracking-widest block">Copys generados por IA</span>
      <div class="bg-[#15151B] border border-gray-800 rounded-2xl p-4">
        <h4 class="text-white font-bold text-sm mb-2"><i data-lucide="tiktok" class="w-3 h-3 inline"></i> Para TikTok Ads</h4>
        <p class="text-xs text-gray-400 italic mb-3">"¿Cansado de [problema]? Mira cómo este producto revolucionó mi rutina. ¡Consíguelo a mitad de precio hoy en el link de mi bio! 🔥"</p>
        <button class="text-[10px] bg-champagne text-black font-bold uppercase px-3 py-1 rounded-md">Copiar</button>
      </div>
      <div class="bg-[#15151B] border border-gray-800 rounded-2xl p-4">
        <h4 class="text-white font-bold text-sm mb-2"><i data-lucide="facebook" class="w-3 h-3 inline"></i> Para Facebook Ads</h4>
        <p class="text-xs text-gray-400 italic mb-3">"✨ El secreto mejor guardado de 2024. Diseñado para [beneficio]. Oferta limitada 50% OFF + Envío Gratis. Compra segura 🔒"</p>
        <button class="text-[10px] bg-champagne text-black font-bold uppercase px-3 py-1 rounded-md">Copiar</button>
      </div>
    </div>
  `;
}

window.switchModalTab = function(tabName) {
  // Update Tab Styles
  const tabs = ['info', 'historial', 'proveedores', 'marketing'];
  tabs.forEach(t => {
    const btn = document.getElementById('tab-' + t);
    if(btn) {
      if(t === tabName) {
        btn.classList.remove('text-gray-500', 'border-transparent');
        btn.classList.add('text-champagne', 'border-champagne');
      } else {
        btn.classList.remove('text-champagne', 'border-champagne');
        btn.classList.add('text-gray-500', 'border-transparent');
      }
    }
  });

  // Update Content
  const container = document.getElementById('modal-tab-content');
  if(container) {
    if(tabName === 'info') container.innerHTML = getTabInfoHTML(window.currentProductData, window.currentProductIdx);
    if(tabName === 'proveedores') container.innerHTML = getTabProveedoresHTML();
    if(tabName === 'historial') container.innerHTML = getTabHistorialHTML();
    if(tabName === 'marketing') container.innerHTML = getTabMarketingHTML();
    lucide.createIcons();
  }
}
"""

js += '\n' + tab_logic_js

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("UI Polished and Interactive Tabs applied!")
