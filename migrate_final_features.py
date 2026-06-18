import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. ADD IDs TO FILTERS IN TENDENCIAS
html = html.replace(
    '<input type="text" placeholder="Buscar producto..." class="bg-white border border-gray-200 rounded-xl pl-8 pr-4 py-2 text-xs font-medium text-gray-900 placeholder-gray-400 outline-none focus:border-gray-400 transition w-44 saas-shadow-sm">',
    '<input type="text" id="filterSearch" onkeyup="filterText()" placeholder="Buscar producto..." class="bg-white border border-gray-200 rounded-xl pl-8 pr-4 py-2 text-xs font-medium text-gray-900 placeholder-gray-400 outline-none focus:border-gray-400 transition w-44 saas-shadow-sm">'
)
html = html.replace(
    '<select class="bg-white border border-gray-200 rounded-xl px-4 py-2 text-xs font-bold text-gray-700 outline-none focus:border-gray-400 saas-shadow-sm">\n            <option value="">Región (Todas)</option>',
    '<select id="filterRegion" onchange="filterRegionChange(this.value)" class="bg-white border border-gray-200 rounded-xl px-4 py-2 text-xs font-bold text-gray-700 outline-none focus:border-gray-400 saas-shadow-sm">\n            <option value="">Región (Todas)</option>'
)
html = html.replace(
    '<select class="bg-white border border-gray-200 rounded-xl px-4 py-2 text-xs font-bold text-gray-700 outline-none focus:border-gray-400 saas-shadow-sm">\n            <option value="">Categorías (Todas)</option>',
    '<select id="filterCat" onchange="filterCatChange(this.value)" class="bg-white border border-gray-200 rounded-xl px-4 py-2 text-xs font-bold text-gray-700 outline-none focus:border-gray-400 saas-shadow-sm">\n            <option value="">Categorías (Todas)</option>'
)
html = html.replace(
    '<select class="bg-white border border-gray-200 rounded-xl px-4 py-2 text-xs font-bold text-gray-700 outline-none focus:border-gray-400 saas-shadow-sm">\n            <option value="">Plataformas (Todas)</option>',
    '<select id="filterPlt" onchange="filterPltChange(this.value)" class="bg-white border border-gray-200 rounded-xl px-4 py-2 text-xs font-bold text-gray-700 outline-none focus:border-gray-400 saas-shadow-sm">\n            <option value="">Plataformas (Todas)</option>'
)
html = html.replace(
    '<select class="bg-white border border-gray-200 rounded-xl px-4 py-2 text-xs font-bold text-gray-700 outline-none focus:border-gray-400 saas-shadow-sm">\n            <option value="score">TrendScore</option>',
    '<select id="filterSort" onchange="filterSortChange(this.value)" class="bg-white border border-gray-200 rounded-xl px-4 py-2 text-xs font-bold text-gray-700 outline-none focus:border-gray-400 saas-shadow-sm">\n            <option value="score">TrendScore</option>'
)
html = html.replace(
    '<button class="bg-gray-50 hover:bg-gray-100 text-gray-600 px-4 py-2 rounded-xl text-xs font-bold transition border border-gray-200">Exportar CSV</button>',
    '<button onclick="exportDataCSV()" class="bg-gray-50 hover:bg-gray-100 text-gray-600 px-4 py-2 rounded-xl text-xs font-bold transition border border-gray-200">Exportar CSV</button>'
)

# 2. REPLACE prodModal WITH FULL MODAL
modal_pattern = r'<!-- Product Modal \(Slide Over / Floater\) -->.*?</div>\s*</div>'

full_modal_html = """<!-- Product Modal (Slide Over / Floater) -->
  <div id="prodModal" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-gray-900/40 backdrop-blur-sm" onclick="closeModal(event)">
    <div class="bg-white rounded-[2.5rem] w-full max-w-4xl overflow-y-auto max-h-[90vh] shadow-2xl flex flex-col transform transition-all scale-95 opacity-0 duration-300" id="modalContent">
      <div class="p-8 pb-4 flex justify-between items-start border-b border-gray-100">
        <div>
          <span id="pmCat" class="text-[10px] font-bold text-gray-500 uppercase tracking-widest bg-gray-100 px-2 py-1 rounded-md">Categoría</span>
          <h2 id="pmTitle" class="text-3xl font-extrabold mt-3 text-gray-900 tracking-tight">Producto Nombre</h2>
        </div>
        <button onclick="closeModalDirect()" class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-gray-500 hover:bg-gray-200 transition"><i data-lucide="x" class="w-4 h-4"></i></button>
      </div>
      
      <!-- Tabs Nav -->
      <div class="flex gap-6 px-8 border-b border-gray-100 bg-gray-50/50">
        <button onclick="switchModalTab('info',this)" class="modal-tab py-4 text-xs font-bold text-black border-b-2 border-black">Información</button>
        <button onclick="switchModalTab('history',this)" class="modal-tab py-4 text-xs font-bold text-gray-400 hover:text-gray-900 transition">Historial 90 días</button>
        <button onclick="switchModalTab('suppliers',this)" class="modal-tab py-4 text-xs font-bold text-gray-400 hover:text-gray-900 transition">Proveedores</button>
        <button onclick="switchModalTab('marketing',this)" class="modal-tab py-4 text-xs font-bold text-gray-400 hover:text-gray-900 transition flex items-center gap-1.5"><i data-lucide="sparkles" class="w-3.5 h-3.5 text-yellow-500"></i> Marketing IA</button>
      </div>

      <!-- Tab Content: INFO -->
      <div id="mtab-info" class="p-8 space-y-6">
        <div class="flex gap-8">
          <div class="flex-1">
            <h4 class="text-xs font-bold text-gray-800 uppercase tracking-wider mb-2">Sobre el producto</h4>
            <p class="text-sm text-gray-600 leading-relaxed">Este producto está experimentando un pico de viralidad sostenida en las últimas 3 semanas debido a campañas generadas por usuarios orgánicos en TikTok. Altamente recomendado para iniciar en modalidad Dropshipping.</p>
          </div>
          <div class="flex gap-8 bg-gray-50 p-6 rounded-3xl border border-gray-100">
            <div>
              <div class="text-[10px] text-gray-400 font-mono uppercase mb-1">TrendScore</div>
              <div id="pmScore" class="text-4xl font-black text-gray-900">0</div>
            </div>
            <div>
              <div class="text-[10px] text-gray-400 font-mono uppercase mb-1">Margen ROI</div>
              <div id="pmMargin" class="text-2xl font-bold text-green-600">0%</div>
            </div>
            <div>
              <div class="text-[10px] text-gray-400 font-mono uppercase mb-1">Competencia</div>
              <div id="pmComp" class="text-sm font-bold text-gray-800 mt-2 px-3 py-1 bg-white border border-gray-200 rounded-lg inline-block saas-shadow-sm">Baja</div>
            </div>
          </div>
        </div>
        <div class="flex gap-4 pt-4">
          <button id="pmSaveBtn" onclick="toggleSaveFromModal()" class="flex-1 py-3 border border-gray-200 bg-white hover:bg-gray-50 text-gray-900 text-xs font-extrabold uppercase tracking-wider rounded-xl transition saas-shadow-sm flex items-center justify-center gap-2"><i data-lucide="bookmark" class="w-4 h-4"></i> Guardar</button>
          <button onclick="showSection('sec-analisis', null); closeModalDirect();" class="flex-1 py-3 bg-gray-100 hover:bg-gray-200 text-gray-900 text-xs font-extrabold uppercase tracking-wider rounded-xl transition saas-shadow-sm">Analizar Mercado</button>
          <button onclick="showAddProductModal(undefined); closeModalDirect();" class="flex-1 py-3 bg-green-500 hover:bg-green-600 text-white text-xs font-extrabold uppercase tracking-wider rounded-xl transition saas-shadow flex items-center justify-center gap-2"><i data-lucide="dollar-sign" class="w-4 h-4"></i> Marcar Venta</button>
        </div>
      </div>

      <!-- Tab Content: HISTORY -->
      <div id="mtab-history" class="p-8 hidden">
        <div class="bg-gray-50 p-6 rounded-3xl border border-gray-100">
          <h4 class="text-xs font-bold text-gray-800 uppercase tracking-wider mb-4">Evolución del Score</h4>
          <div class="h-64 w-full relative">
            <canvas id="modalChart"></canvas>
          </div>
        </div>
      </div>

      <!-- Tab Content: SUPPLIERS -->
      <div id="mtab-suppliers" class="p-8 hidden space-y-4">
        <h4 class="text-xs font-bold text-gray-800 uppercase tracking-wider">Proveedores Globales</h4>
        <div id="pmSuppliers" class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <!-- Injected via JS -->
        </div>
      </div>

      <!-- Tab Content: MARKETING -->
      <div id="mtab-marketing" class="p-8 hidden space-y-6">
        <div class="bg-gradient-to-r from-yellow-50 to-orange-50 border border-yellow-100 rounded-3xl p-6 relative overflow-hidden">
          <div class="relative z-10 flex flex-col sm:flex-row gap-6 items-start sm:items-center justify-between">
            <div>
              <h3 class="text-lg font-bold text-gray-900 flex items-center gap-2"><i data-lucide="sparkles" class="w-5 h-5 text-yellow-600"></i> Generador de Copys IA</h3>
              <p class="text-sm text-gray-600 mt-1 max-w-md">Crea textos persuasivos para tus anuncios en TikTok e Instagram basados en el ángulo ganador del producto.</p>
            </div>
            <button id="mktGenerateBtn" onclick="generateMarketingCopy()" class="inline-flex items-center gap-2 px-6 py-3 bg-black text-white text-xs font-extrabold uppercase tracking-wider rounded-xl hover:-translate-y-0.5 transition saas-shadow whitespace-nowrap">
              Generar Copys <i data-lucide="zap" class="w-4 h-4"></i>
            </button>
          </div>
        </div>

        <div id="mktLoading" class="hidden py-12 flex flex-col items-center justify-center gap-4">
          <div class="w-8 h-8 border-4 border-gray-200 border-t-black rounded-full animate-spin"></div>
          <p class="text-sm font-mono text-gray-500 animate-pulse">Analizando ángulos ganadores...</p>
        </div>

        <div id="mktContent" class="hidden space-y-6">
          <div class="flex justify-end">
            <button onclick="clearMarketingCache()" class="text-xs text-gray-400 hover:text-gray-900 transition font-bold"><i data-lucide="refresh-cw" class="w-3 h-3 inline"></i> Regenerar</button>
          </div>
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- TikTok -->
            <div class="bg-gray-50 border border-gray-200 rounded-2xl p-6 saas-shadow-sm">
              <div class="flex justify-between items-center mb-4">
                <h4 class="font-bold text-gray-900 flex items-center gap-2"><i data-lucide="music" class="w-4 h-4 text-gray-500"></i> TikTok Ads</h4>
                <button onclick="copyMktField('mkt-tiktok')" class="text-[10px] font-bold text-gray-500 hover:text-black uppercase bg-white px-2 py-1 rounded border border-gray-200">Copiar</button>
              </div>
              <p id="mkt-tiktok" class="text-sm text-gray-700 whitespace-pre-line leading-relaxed"></p>
            </div>
            <!-- Instagram -->
            <div class="bg-gray-50 border border-gray-200 rounded-2xl p-6 saas-shadow-sm">
              <div class="flex justify-between items-center mb-4">
                <h4 class="font-bold text-gray-900 flex items-center gap-2"><i data-lucide="instagram" class="w-4 h-4 text-gray-500"></i> Instagram Reels</h4>
                <button onclick="copyMktField('mkt-instagram')" class="text-[10px] font-bold text-gray-500 hover:text-black uppercase bg-white px-2 py-1 rounded border border-gray-200">Copiar</button>
              </div>
              <p id="mkt-instagram" class="text-sm text-gray-700 whitespace-pre-line leading-relaxed"></p>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>"""

html = re.sub(modal_pattern, full_modal_html, html, flags=re.DOTALL)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)


# 3. APPEND FILTERS & MODAL JS TO APP.JS
with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# We need to replace the static renderTable with one that uses filters
render_table_pattern = r'window\.renderTable = function\(\) \{.*?(?=window\.nextPage = function\(\) \{)'
new_render_table = """window.filterParams = { cat: '', plt: '', region: '', sort: 'score', text: '' };

  window.filterCatChange = function(v) { window.filterParams.cat = v; window.currentPage = 1; window.renderTable(); }
  window.filterPltChange = function(v) { window.filterParams.plt = v; window.currentPage = 1; window.renderTable(); }
  window.filterRegionChange = function(v) { window.filterParams.region = v; window.currentPage = 1; window.renderTable(); }
  window.filterSortChange = function(v) { window.filterParams.sort = v; window.currentPage = 1; window.renderTable(); }
  window.filterText = function() { window.filterParams.text = document.getElementById('filterSearch').value.toLowerCase(); window.currentPage = 1; window.renderTable(); }

  window.renderTable = function() {
    const tbody = document.getElementById('tableBody');
    if(!tbody) return;
    
    let filtered = products.filter(p => {
      if(window.filterParams.cat && p.cat !== window.filterParams.cat) return false;
      if(window.filterParams.plt && !p.plts.includes(window.filterParams.plt)) return false;
      if(window.filterParams.region && !p.regions.includes(window.filterParams.region)) return false;
      if(window.filterParams.text && !p.name.toLowerCase().includes(window.filterParams.text)) return false;
      return true;
    });

    if(window.filterParams.sort === 'score') filtered.sort((a,b) => b.score - a.score);
    if(window.filterParams.sort === 'change') filtered.sort((a,b) => parseFloat(b.change) - parseFloat(a.change));
    if(window.filterParams.sort === 'margin') filtered.sort((a,b) => b.margin - a.margin);

    const start = (currentPage - 1) * PAGE_SIZE;
    const list = filtered.slice(start, start + PAGE_SIZE);
    
    const savedIds = getSavedProducts().map(s => s.name);

    tbody.innerHTML = list.map((p, i) => {
      const idx = products.indexOf(p);
      const isHot = p.score >= 90;
      const badgeStyle = isHot ? 'bg-red-50 text-red-600 border border-red-100' : 'bg-gray-100 text-gray-600';
      const pltsHtml = p.plts.map(plt => `<span class="bg-gray-100 text-gray-500 text-[10px] uppercase font-bold px-2 py-1 rounded mr-1">${plt}</span>`).join('');
      const isSaved = savedIds.includes(p.name);
      
      return `
        <tr class="border-b border-gray-100 hover:bg-gray-50/50 transition">
          <td class="p-4 pl-6">
            <div class="flex items-center gap-4">
              <div class="w-10 h-10 rounded-xl bg-gray-100 border border-gray-200 flex items-center justify-center flex-shrink-0">
                <i data-lucide="image" class="w-4 h-4 text-gray-400"></i>
              </div>
              <div class="font-bold text-gray-900 leading-tight max-w-[200px] truncate" title="${p.name}">${p.name}</div>
            </div>
          </td>
          <td class="p-4 font-mono text-gray-500">${p.cat}</td>
          <td class="p-4">${pltsHtml}</td>
          <td class="p-4 font-mono font-bold text-gray-700">${p.price_str}</td>
          <td class="p-4">
            <span class="px-2 py-1 rounded-lg text-xs font-bold ${badgeStyle}">${p.score}</span>
          </td>
          <td class="p-4 pr-6 text-right flex items-center justify-end gap-3 h-[73px]">
            <button onclick="toggleSave(${idx})" class="${isSaved ? 'text-black' : 'text-gray-400'} hover:text-black transition flex items-center justify-center h-full"><i data-lucide="bookmark" class="w-5 h-5 ${isSaved ? 'fill-current' : ''}"></i></button>
            <button onclick="openProduct(${idx})" class="bg-black hover:-translate-y-0.5 text-white text-xs font-extrabold px-5 py-2.5 rounded-xl transition saas-shadow">Ver Detalle</button>
          </td>
        </tr>
      `;
    }).join('');
    
    document.getElementById('pageInfo').textContent = `Mostrando ${start + 1}-${Math.min(start + PAGE_SIZE, filtered.length)} de ${filtered.length}`;
    lucide.createIcons();
  }
  
  """
app_js = re.sub(render_table_pattern, new_render_table, app_js, flags=re.DOTALL)

# Also append Toggle Save & Marketing & Tabs logic
additional_js = """
// --- SAVED PRODUCTS LOGIC ---
window.toggleSave = function(idx) {
  const p = window.MOCK_DATA.products[idx];
  if(!p) return;
  let saved = getSavedProducts();
  const exists = saved.findIndex(s => s.name === p.name);
  if(exists >= 0) {
    saved.splice(exists, 1);
  } else {
    saved.push(p);
  }
  localStorage.setItem('tb_saved', JSON.stringify(saved));
  window.renderTable();
  if(window.renderSaved) window.renderSaved();
};

window.toggleSaveFromModal = function() {
  if(window.currentProdIndex !== null) {
    window.toggleSave(window.currentProdIndex);
    const saved = getSavedProducts().find(s => s.name === window.MOCK_DATA.products[window.currentProdIndex].name);
    document.getElementById('pmSaveBtn').innerHTML = saved 
      ? `<i data-lucide="bookmark" class="w-4 h-4 fill-current"></i> Guardado`
      : `<i data-lucide="bookmark" class="w-4 h-4"></i> Guardar`;
    lucide.createIcons();
  }
};

// --- MODAL TABS & MARKETING ---
window.switchModalTab = function(tabId, btn) {
  document.querySelectorAll('.modal-tab').forEach(b => {
    b.classList.remove('text-black', 'border-b-2', 'border-black');
    b.classList.add('text-gray-400');
  });
  btn.classList.remove('text-gray-400');
  btn.classList.add('text-black', 'border-b-2', 'border-black');
  
  ['mtab-info', 'mtab-history', 'mtab-suppliers', 'mtab-marketing'].forEach(id => {
    document.getElementById(id).classList.add('hidden');
  });
  document.getElementById('mtab-' + tabId).classList.remove('hidden');
};

const marketingCache = {};

window.generateMarketingCopy = function() {
  const p = window.MOCK_DATA.products[window.currentProdIndex];
  if(!p) return;
  
  if(marketingCache[p.name]) {
    showMarketingResult(marketingCache[p.name]);
    return;
  }
  
  document.getElementById('mktLoading').classList.remove('hidden');
  document.getElementById('mktContent').classList.add('hidden');
  
  setTimeout(() => {
    const copy = {
      tiktok: `¿Cansado de [Problema]? 😩\\n\\nCon ${p.name} puedes [Beneficio Principal] en segundos. ✨\\n\\n🔥 Consigue el tuyo con 50% OFF solo por hoy (Link en bio)\\n\\n#${p.cat} #Viral #TikTokMadeMeBuyIt`,
      instagram: `Transforma tu rutina con ${p.name} ✨\\n\\nBeneficios:\\n✅ [Beneficio 1]\\n✅ [Beneficio 2]\\n\\n💬 Comenta "QUIERO" y te envío el link por DM.\\n\\n#${p.cat} #Tendencia #Oferta`
    };
    marketingCache[p.name] = copy;
    showMarketingResult(copy);
  }, 2000);
};

function showMarketingResult(copy) {
  document.getElementById('mktLoading').classList.add('hidden');
  document.getElementById('mktContent').classList.remove('hidden');
  document.getElementById('mkt-tiktok').textContent = copy.tiktok;
  document.getElementById('mkt-instagram').textContent = copy.instagram;
}

window.clearMarketingCache = function() {
  const p = window.MOCK_DATA.products[window.currentProdIndex];
  if(p && marketingCache[p.name]) {
    delete marketingCache[p.name];
    window.generateMarketingCopy();
  }
};

window.copyMktField = function(id) {
  const text = document.getElementById(id).innerText;
  navigator.clipboard.writeText(text);
  alert('Copiado al portapapeles');
};

window.exportDataCSV = function() {
  alert('Iniciando descarga de CSV...');
};
"""

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js + '\n' + additional_js)
