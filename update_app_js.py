import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Make calcROI available globally
calc_roi_func = """
  window.calcROI = function() {
    const cost = parseFloat(document.getElementById('calcCost').value) || 0;
    const price = parseFloat(document.getElementById('calcPrice').value) || 0;
    const ads = parseFloat(document.getElementById('calcAds').value) || 0;
    const sales = parseInt(document.getElementById('calcSales').value) || 0;
    const el = document.getElementById('calcResult');
    if(!el) return;
    
    if(!cost || !price) {
      el.innerHTML = '<p class="text-xs text-gray-500 text-center py-2">Completa los campos.</p>';
      return;
    }
    
    const netPerSale = price - cost - ads;
    const monthlyProfit = netPerSale * sales;
    const margin = Math.round((netPerSale / price) * 100);
    const roi = cost > 0 ? Math.round((netPerSale / cost) * 100) : 0;
    const breakeven = netPerSale > 0 ? Math.ceil(cost / netPerSale) : 0;
    
    const profitColor = netPerSale > 0 ? 'text-green-600' : 'text-red-500';
    const bgBreakeven = netPerSale > 0 ? 'bg-green-50' : 'bg-red-50';
    
    el.innerHTML = `
      <div class="grid grid-cols-2 gap-2">
        <div class="bg-white p-2 rounded-lg border border-gray-100 text-center shadow-sm">
          <div class="text-[10px] text-gray-400 font-bold uppercase tracking-wider">Ganancia/u</div>
          <div class="text-sm font-extrabold ${profitColor}">$${netPerSale.toFixed(2)}</div>
        </div>
        <div class="bg-white p-2 rounded-lg border border-gray-100 text-center shadow-sm">
          <div class="text-[10px] text-gray-400 font-bold uppercase tracking-wider">Margen</div>
          <div class="text-sm font-extrabold text-gray-900">${margin}%</div>
        </div>
        <div class="bg-white p-2 rounded-lg border border-gray-100 text-center shadow-sm">
          <div class="text-[10px] text-gray-400 font-bold uppercase tracking-wider">Ganancia/mes</div>
          <div class="text-sm font-extrabold ${profitColor}">$${monthlyProfit.toFixed(0)}</div>
        </div>
        <div class="${bgBreakeven} p-2 rounded-lg border border-gray-100 text-center shadow-sm flex flex-col justify-center">
          <div class="text-[10px] text-gray-500 font-bold uppercase tracking-wider">Break-even</div>
          <div class="text-sm font-extrabold text-gray-900">${breakeven} ventas</div>
        </div>
      </div>
    `;
  }
"""

# Render Opportunities function
render_opps_func = """
  function renderOpportunities() {
    const el = document.getElementById('oppList');
    if(!el) return;
    
    // Sort by low competition and high score
    const sorted = [...products].sort((a,b) => {
      const aComp = a.comp === 'Baja' ? 3 : (a.comp === 'Media' ? 2 : 1);
      const bComp = b.comp === 'Baja' ? 3 : (b.comp === 'Media' ? 2 : 1);
      const aScore = a.score * a.margin * aComp;
      const bScore = b.score * b.margin * bComp;
      return bScore - aScore;
    }).slice(0, 4);
    
    el.innerHTML = sorted.map((p, i) => {
      const isLow = p.comp === 'Baja';
      const badgeBg = isLow ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700';
      const originalIdx = products.indexOf(p);
      return `
        <div class="flex items-center justify-between p-3 border border-gray-100 rounded-xl hover:border-gray-200 hover:bg-gray-50 transition cursor-pointer" onclick="openProduct(${originalIdx})">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center font-bold text-gray-400 text-xs">${i+1}</div>
            <div>
              <div class="font-bold text-sm text-gray-900 truncate max-w-[120px]">${p.name}</div>
              <div class="text-[10px] text-gray-400 font-mono mt-0.5">${p.cat}</div>
            </div>
          </div>
          <div class="text-right flex flex-col items-end">
            <div class="text-sm font-extrabold text-green-500">${p.margin}% ROI</div>
            <div class="text-[9px] font-bold px-1.5 py-0.5 rounded mt-1 ${badgeBg} uppercase tracking-wider">Comp ${p.comp}</div>
          </div>
        </div>
      `;
    }).join('');
  }
"""

if 'window.calcROI =' not in js:
    # Insert functions before window.renderTable
    js = js.replace('window.renderTable = function()', calc_roi_func + '\n' + render_opps_func + '\n  window.renderTable = function()')
    
    # Call them inside initDashboard
    js = js.replace('renderTable();', 'renderTable();\n    renderOpportunities();\n    window.calcROI();')

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
