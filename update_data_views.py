import re

# 1. Update dashboard.html table headers
with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_thead = """          <thead>
            <tr class="bg-gray-50 text-gray-400 text-xs font-medium uppercase tracking-wider">
              <th class="p-4 pl-6 font-mono font-medium">Producto</th>
              <th class="p-4 font-mono font-medium">Categoría</th>
              <th class="p-4 font-mono font-medium">TrendScore</th>
              <th class="p-4 font-mono font-medium">Margen ROI</th>
              <th class="p-4 font-mono font-medium">Estado</th>
              <th class="p-4 pr-6"></th>
            </tr>
          </thead>"""

new_thead = """          <thead>
            <tr class="bg-gray-50 text-gray-400 text-xs font-medium uppercase tracking-wider">
              <th class="p-4 pl-6 font-mono font-medium">Producto</th>
              <th class="p-4 font-mono font-medium">Categoría</th>
              <th class="p-4 font-mono font-medium">Plataformas</th>
              <th class="p-4 font-mono font-medium">Precio Venta</th>
              <th class="p-4 font-mono font-medium">TrendScore</th>
              <th class="p-4 pr-6"></th>
            </tr>
          </thead>"""

html = html.replace(old_thead, new_thead)
with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)


# 2. Update app.js
with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

new_init = """  function initDashboard() {
    // Calculate KPIs from real data
    const total = products.length;
    let avgMargin = 0;
    let totalHot = 0;
    let allRegions = new Set();
    
    products.forEach(p => {
        avgMargin += p.margin;
        if (p.score >= 90) totalHot++;
        if (p.regions) p.regions.forEach(r => allRegions.add(r));
    });
    avgMargin = Math.round(avgMargin / total);

    document.getElementById('kpiTotal').textContent = total + '+';
    // The second card in dashboard is Promedio ROI
    const roiEl = document.querySelector('div.grid > div:nth-child(3) > div > div.text-3xl');
    if(roiEl) roiEl.textContent = avgMargin + '%';
    
    // The third card is Tendencias Nuevas
    const tendEl = document.querySelector('div.grid > div:nth-child(4) > div > div.text-3xl');
    if(tendEl) tendEl.textContent = totalHot;

    // Hero Card (Top #1 Product)
    if(products.length > 0) {
      const p1 = products[0];
      const titleEl = document.getElementById('heroTitle');
      if(titleEl) {
          titleEl.textContent = p1.name;
          document.getElementById('heroCat').textContent = p1.cat;
          document.getElementById('heroScore').textContent = p1.score;
      }
    }
    
    initCharts();
    renderTable();
  }"""

new_render = """  window.renderTable = function() {
    const tbody = document.getElementById('tableBody');
    const start = (currentPage - 1) * PAGE_SIZE;
    const list = products.slice(start, start + PAGE_SIZE);
    
    tbody.innerHTML = list.map((p, i) => {
      const idx = start + i;
      const isHot = p.score >= 90;
      const badgeStyle = isHot ? 'bg-pastel-pink text-pink-700' : 'bg-gray-100 text-gray-600';
      
      const pltsHtml = p.plts.map(plt => `<span class="bg-gray-100 text-gray-500 text-[10px] uppercase font-bold px-2 py-1 rounded mr-1">${plt}</span>`).join('');

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
          <td class="p-4 pr-6 text-right">
            <button onclick="openProduct(${idx})" class="bg-black hover:bg-gray-800 text-white text-xs font-bold px-4 py-2 rounded-xl transition saas-shadow">Ver Detalle</button>
          </td>
        </tr>
      `;
    }).join('');
    
    document.getElementById('pageInfo').textContent = `Mostrando ${start + 1}-${Math.min(start + PAGE_SIZE, products.length)} de ${products.length}`;
    lucide.createIcons();
  }"""

# Use regex to replace the functions
app_js = re.sub(r'function initDashboard\(\) \{.*?\n  \}', new_init, app_js, flags=re.DOTALL)
app_js = re.sub(r'window\.renderTable = function\(\) \{.*?\n  \}', new_render, app_js, flags=re.DOTALL)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)
