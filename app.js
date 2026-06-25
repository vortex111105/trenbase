let saved = JSON.parse(localStorage.getItem('tb_saved') || '[]');
let currentProdIndex = null;
let currentFilter = { cat: null, mode: null };

document.addEventListener('DOMContentLoaded', () => {
  lucide.createIcons();


  window.productsData = [];
  window.fxRates = { ARS: 1050, UYU: 39, CLP: 970 };

  async function loadFxRates() {
    try {
      const res = await fetch('/api/fx');
      if (!res.ok) return;
      const data = await res.json();
      if (data.rates) window.fxRates = data.rates;
    } catch(e) { /* keep defaults */ }
  }

  async function loadRealProducts() {
    try {
      const res = await fetch('/api/products');
      if (!res.ok) throw new Error('Failed to load products');
      window.productsData = await res.json();
      initDashboard();
    } catch (e) {
      console.error(e);
      if (window.MOCK_DATA && window.MOCK_DATA.products) {
          window.productsData = window.MOCK_DATA.products;
          initDashboard();
      }
    }
  }

  // Load FX rates in parallel with products
  loadFxRates();
  loadRealProducts();
  setInterval(loadRealProducts, 6 * 60 * 60 * 1000);
  setInterval(loadFxRates, 30 * 60 * 1000);

  const PAGE_SIZE = 10;
  let currentPage = 1;

  // Charts
  let mainChart = null;
  let donutChart = null;
  let modalChart = null;
  
  function initDashboard() {
    // Calculate KPIs from real data
    const products = window.productsData;
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
    renderOpportunities();
    window.calcROI();
    renderSaved();
    renderAlerts();
    renderCommunityLeaderboard();
    const heroCard = document.querySelector('#sec-analisis .cursor-pointer[onclick]');
    if(heroCard) heroCard.setAttribute('onclick', 'openProduct(0)');
    setTimeout(applyPlanGates, 300);
  }

  async function renderCommunityLeaderboard() {
    const el = document.getElementById('communityLeaderboard');
    if(!el) return;
    try {
      const res = await fetch('/api/leaderboard');
      if(!res.ok) throw new Error();
      const data = await res.json();
      const items = data.top_products || [];
      if(!items.length) {
        el.innerHTML = '<p class="text-sm text-gray-400 text-center py-4">Aún no hay ventas registradas hoy.</p>';
        return;
      }
      const max = items[0]?.count || 1;
      el.innerHTML = items.slice(0,5).map((item, i) => {
        const pct = Math.round((item.count / max) * 100);
        const medals = ['🥇','🥈','🥉','',''];
        return `
          <div class="flex items-center gap-3">
            <span class="text-base w-6 text-center">${medals[i] || ''}</span>
            <div class="flex-1 min-w-0">
              <div class="text-xs font-bold text-gray-900 truncate">${item.name}</div>
              <div class="mt-1 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                <div class="h-full bg-black rounded-full transition-all" style="width:${pct}%"></div>
              </div>
            </div>
            <span class="text-[10px] font-mono text-gray-400 flex-shrink-0">${item.count} venta${item.count !== 1 ? 's' : ''}</span>
          </div>`;
      }).join('');
    } catch(e) {
      el.innerHTML = '<p class="text-sm text-gray-400 text-center py-4">Sin datos disponibles.</p>';
    }
  }

  function renderAlerts() {
    const el = document.getElementById('alertsList');
    if(!el) return;
    const products = window.productsData;
    if(!products || !products.length) {
      el.innerHTML = '<p class="text-gray-400 text-sm text-center py-12">No hay alertas disponibles.</p>';
      return;
    }

    const alerts = [];

    // Top scoring product
    const top = [...products].sort((a,b) => (b.score||0) - (a.score||0))[0];
    if(top) alerts.push({
      icon: 'rocket', color: 'blue',
      title: `Oportunidad del día: ${top.name}`,
      body: `Score ${top.score} — margen estimado del ${top.margin}% con competencia ${top.comp}. Ideal para lanzar ahora.`,
      time: 'Ahora'
    });

    // Products with score >= 95 (peak trend)
    const peaks = products.filter(p => p.score >= 95).slice(0, 2);
    peaks.forEach(p => alerts.push({
      icon: 'trending-up', color: 'orange',
      title: `Pico de tendencia: ${p.name}`,
      body: `Score ${p.score} en categoría ${p.cat}. Alta viralidad detectada en LATAM. Competencia: ${p.comp}.`,
      time: 'Hoy'
    }));

    // Low-competition products (potential for new dropshippers)
    const lowComp = products.filter(p => p.comp === 'Baja' && p.score >= 80).slice(0, 2);
    lowComp.forEach(p => alerts.push({
      icon: 'star', color: 'green',
      title: `Nicho sin competencia: ${p.name}`,
      body: `Competencia baja con score ${p.score}. Oportunidad para diferenciarte en ${(p.regions||['LATAM']).join(', ')}.`,
      time: 'Este mes'
    }));

    // High-margin products
    const highMargin = products.filter(p => p.margin >= 55).slice(0, 1);
    highMargin.forEach(p => alerts.push({
      icon: 'dollar-sign', color: 'purple',
      title: `Alto margen detectado: ${p.name}`,
      body: `Margen del ${p.margin}% por unidad. Categoría: ${p.cat}. Ideal para escalar con publicidad pagada.`,
      time: 'Esta semana'
    }));

    const colorMap = {
      blue: { bg: 'bg-blue-50', hover: 'group-hover:bg-blue-100', icon: 'text-blue-500' },
      orange: { bg: 'bg-orange-50', hover: 'group-hover:bg-orange-100', icon: 'text-orange-500' },
      green: { bg: 'bg-emerald-50', hover: 'group-hover:bg-emerald-100', icon: 'text-emerald-500' },
      purple: { bg: 'bg-purple-50', hover: 'group-hover:bg-purple-100', icon: 'text-purple-500' },
      red: { bg: 'bg-red-50', hover: 'group-hover:bg-red-100', icon: 'text-red-500' }
    };

    el.innerHTML = alerts.slice(0, 5).map(a => {
      const c = colorMap[a.color] || colorMap.blue;
      return `
        <div class="p-6 flex items-start gap-4 hover:bg-gray-50 transition cursor-pointer group">
          <div class="w-10 h-10 rounded-full ${c.bg} flex items-center justify-center flex-shrink-0 ${c.hover} transition">
            <i data-lucide="${a.icon}" class="w-5 h-5 ${c.icon}"></i>
          </div>
          <div class="flex-1">
            <div class="text-sm font-bold text-gray-900">${a.title}</div>
            <p class="text-xs text-gray-500 mt-1 leading-relaxed">${a.body}</p>
            <span class="text-[9px] font-mono text-gray-400 uppercase mt-2 block font-bold tracking-wider">${a.time}</span>
          </div>
        </div>`;
    }).join('');
    lucide.createIcons();
  }
  
  function initCharts() {
    // Main Chart (Bar) — real score-tier distribution
    const ctxMain = document.getElementById('mainChart');
    if(ctxMain) {
      const tiers = { '<60': 0, '60–70': 0, '70–80': 0, '80–90': 0, '90–95': 0, '95+': 0 };
      window.productsData.forEach(p => {
        const s = p.score || 0;
        if (s < 60) tiers['<60']++;
        else if (s < 70) tiers['60–70']++;
        else if (s < 80) tiers['70–80']++;
        else if (s < 90) tiers['80–90']++;
        else if (s < 95) tiers['90–95']++;
        else tiers['95+']++;
      });
      mainChart = new Chart(ctxMain, {
        type: 'bar',
        data: {
          labels: Object.keys(tiers),
          datasets: [{
            label: 'Tendencias Activas',
            data: Object.values(tiers),
            backgroundColor: '#121212',
            borderRadius: 8,
            barPercentage: 0.6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { display: false }, border: { display: false } },
            y: { grid: { color: '#F3F4F6' }, border: { display: false }, ticks: { precision: 0 } }
          }
        }
      });
    }

    // Donut Chart
    const ctxDonut = document.getElementById('donutChart');
    if(ctxDonut) {
      const cats = {};
      window.productsData.forEach(p => cats[p.cat] = (cats[p.cat] || 0) + 1);
      const labels = Object.keys(cats);
      const data = Object.values(cats);
      
      donutChart = new Chart(ctxDonut, {
        type: 'doughnut',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: ['#121212', '#9CA3AF', '#D1D5DB', '#F3F4F6', '#6B7280', '#4B5563'],
            borderWidth: 0,
            cutout: '75%'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } }
        }
      });
    }
  }

    
  
  window.calcROISliders = function() {
    const cost = parseFloat(document.getElementById('calcCost').value) || 0;
    const price = parseFloat(document.getElementById('calcPrice').value) || 0;
    const ads = parseFloat(document.getElementById('calcAds').value) || 0;
    
    document.getElementById('calcCostVal').innerText = '$' + cost.toFixed(2);
    document.getElementById('calcAdsVal').innerText = '$' + ads.toFixed(2);
    document.getElementById('calcPriceVal').innerText = '$' + price.toFixed(2);
    
    const el = document.getElementById('calcResult');
    if(!el) return;
    
    const netPerSale = price - cost - ads;
    const margin = price > 0 ? Math.round((netPerSale / price) * 100) : 0;
    const breakeven = netPerSale > 0 ? Math.ceil(cost / netPerSale) : 0;
    
    const profitColor = netPerSale > 0 ? 'text-green-600' : 'text-red-500';
    
    el.innerHTML = `
        <div class="bg-white p-2 rounded-lg border border-gray-100 text-center shadow-sm">
          <div class="text-[10px] text-gray-400 font-bold uppercase tracking-wider">Ganancia Neta</div>
          <div class="text-sm font-extrabold ${profitColor}">$${netPerSale.toFixed(2)}</div>
        </div>
        <div class="bg-white p-2 rounded-lg border border-gray-100 text-center shadow-sm">
          <div class="text-[10px] text-gray-400 font-bold uppercase tracking-wider">Margen</div>
          <div class="text-sm font-extrabold text-gray-900">${margin}%</div>
        </div>
    `;
  }
  // Initialize slider values on load
  setTimeout(() => { if(window.calcROISliders) window.calcROISliders(); }, 500);

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


  function renderOpportunities() {
    const el = document.getElementById('oppList');
    if(!el) return;

    const sorted = [...window.productsData].sort((a,b) => {
      const aComp = a.comp === 'Baja' ? 3 : (a.comp === 'Media' ? 2 : 1);
      const bComp = b.comp === 'Baja' ? 3 : (b.comp === 'Media' ? 2 : 1);
      return (b.score * b.margin * bComp) - (a.score * a.margin * aComp);
    }).slice(0, 8);

    el.innerHTML = sorted.map((p, i) => {
      const isLow = p.comp === 'Baja';
      const badgeBg = isLow ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700';
      const originalIdx = window.productsData.indexOf(p);
      return `
        <div class="flex-shrink-0 w-44 p-3 border border-gray-100 rounded-xl hover:border-gray-200 hover:bg-gray-50 transition cursor-pointer" onclick="openProduct(${originalIdx})">
          <div class="text-[10px] font-mono text-gray-400 mb-1">#${i+1} · ${p.cat}</div>
          <div class="font-bold text-sm text-gray-900 leading-tight mb-3" style="display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden">${p.name}</div>
          <div class="flex justify-between items-center">
            <span class="text-sm font-extrabold text-green-500">${p.margin}% ROI</span>
            <span class="text-[9px] font-bold px-1.5 py-0.5 rounded ${badgeBg} uppercase tracking-wider">Comp ${p.comp}</span>
          </div>
        </div>
      `;
    }).join('');
  }

  
  window.showSection = function(sectionId, btn) {
    // Hide all sections
    document.querySelectorAll('.dash-section').forEach(sec => {
      sec.classList.remove('active-section');
    });
    
    // Show target section
    const target = document.getElementById(sectionId);
    if(target) {
      target.classList.add('active-section');
    }
    
    // Update active state in sidebar
    if(btn) {
      document.querySelectorAll('#sidebarNav .nav-btn').forEach(b => {
        b.classList.remove('bg-gray-100', 'text-gray-900');
        b.classList.add('text-gray-900/50');
      });
      btn.classList.remove('text-gray-900/50');
      btn.classList.add('bg-gray-100', 'text-gray-900');
    }
  }

  window.renderTable = function() {
    const tbody = document.getElementById('tableBody');
    if(!tbody) return;
    const start = (currentPage - 1) * PAGE_SIZE;
    let filtered = window.productsData;
    if(currentFilter.cat) filtered = filtered.filter(p => p.cat === currentFilter.cat);
    if(currentFilter.mode === 'marca-propia') filtered = filtered.filter(p => p.type === 'marca-propia');
    const list = filtered.slice(start, start + PAGE_SIZE);

    tbody.innerHTML = list.map((p) => {
      const originalIdx = window.productsData.indexOf(p);
      const isHot = p.score >= 90;
      const badgeStyle = isHot ? 'bg-pastel-pink text-pink-700' : 'bg-gray-100 text-gray-600';
      const pltsHtml = (p.plts || []).map(plt => `<span class="bg-gray-100 text-gray-500 text-[10px] uppercase font-bold px-2 py-1 rounded mr-1">${plt}</span>`).join('');

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
          <td class="p-4 font-mono text-gray-500">${p.cat || ''}</td>
          <td class="p-4">${pltsHtml}</td>
          <td class="p-4 font-mono font-bold text-gray-700">${p.price_str || ''}</td>
          <td class="p-4">
            <span class="px-2 py-1 rounded-lg text-xs font-bold ${badgeStyle}">${p.score}</span>
          </td>
          <td class="p-4 pr-6 text-right">
            <button onclick="openProduct(${originalIdx})" class="bg-black hover:bg-gray-800 text-white text-xs font-bold px-4 py-2 rounded-xl transition saas-shadow">Ver Detalle</button>
          </td>
        </tr>
      `;
    }).join('');

    document.getElementById('pageInfo').textContent = `Mostrando ${start + 1}-${Math.min(start + PAGE_SIZE, filtered.length)} de ${filtered.length}`;
    lucide.createIcons();
  }
  
  window.nextPage = function() {
    let filtered = window.productsData;
    if(currentFilter.cat) filtered = filtered.filter(p => p.cat === currentFilter.cat);
    if(currentFilter.mode === 'marca-propia') filtered = filtered.filter(p => p.type === 'marca-propia');
    if(currentPage * PAGE_SIZE < filtered.length) {
      currentPage++;
      renderTable();
      renderOpportunities();
      window.calcROI();
    }
  }

  window.prevPage = function() {
    if(currentPage > 1) {
      currentPage--;
      renderTable();
      renderOpportunities();
      window.calcROI();
    }
  }
  
  window.toggleSave = function(idx) {
    const pos = saved.indexOf(idx);
    if(pos === -1) saved.push(idx);
    else saved.splice(pos, 1);
    localStorage.setItem('tb_saved', JSON.stringify(saved));
    renderSaved();
  }

  function renderSaved() {
    const el = document.getElementById('savedList');
    if(!el) return;
    const items = saved.map(idx => ({ idx, p: window.productsData[idx] })).filter(o => o.p);
    if(!items.length) {
      el.innerHTML = '<p class="text-gray-400 text-sm text-center py-12">No tenés productos guardados aún.<br><span class="text-xs">Abrí un producto y tocá "Guardar".</span></p>';
      return;
    }
    el.innerHTML = items.map(({ idx, p }) => `
      <div class="p-5 flex items-center gap-4 hover:bg-gray-50 transition cursor-pointer group" onclick="openProduct(${idx})">
        <div class="w-12 h-12 rounded-2xl bg-gray-100 flex items-center justify-center flex-shrink-0">
          <i data-lucide="package" class="w-5 h-5 text-gray-400"></i>
        </div>
        <div class="flex-1 min-w-0">
          <div class="font-bold text-sm text-gray-900 truncate">${p.name}</div>
          <div class="text-xs text-gray-400 font-mono mt-0.5">${p.cat || ''} · Score ${p.score}</div>
        </div>
        <div class="text-right flex-shrink-0">
          <div class="text-sm font-extrabold text-green-500">${p.margin}% ROI</div>
          <button onclick="event.stopPropagation(); window.toggleSave(${idx})" class="text-[10px] text-gray-400 hover:text-red-500 font-bold transition mt-1 block">Quitar</button>
        </div>
      </div>
    `).join('');
    lucide.createIcons();
  }

  window.filterByCategory = function(cat) {
    currentFilter.cat = (currentFilter.cat === cat) ? null : cat;
    currentPage = 1;
    renderTable();
  }

  window.setFilter = function(mode) {
    currentFilter.mode = (currentFilter.mode === mode) ? null : mode;
    currentPage = 1;
    renderTable();
  }

  window.openProduct = function(idx) {
    const products = window.productsData;
    currentProdIndex = idx;
    const p = products[idx];
    if(!p) return;
    
    document.getElementById('pmTitle').textContent = p.name;
    document.getElementById('pmCat').textContent = p.cat;
    document.getElementById('pmScore').textContent = p.score;
    document.getElementById('pmMargin').textContent = p.margin + '%';
    document.getElementById('pmComp').textContent = p.comp;
    
    // Render suppliers (from product data as baseline)
    function buildSupHtml(items) {
      return items.map(s => `
        <div class="flex items-center justify-between p-3 border border-gray-100 bg-white rounded-2xl shadow-sm">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center">
              <i data-lucide="package" class="w-4 h-4 text-gray-600"></i>
            </div>
            <span class="font-bold text-sm text-gray-900">${s.name}</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="font-mono text-gray-500 text-sm">$${s.price}</span>
            ${s.url ? `<a href="${s.url}" target="_blank" rel="noopener" class="text-[10px] font-bold bg-orange-50 text-orange-600 border border-orange-100 px-2 py-1 rounded-lg hover:bg-orange-100 transition">Ver →</a>` : ''}
          </div>
        </div>
      `).join('');
    }
    document.getElementById('pmSuppliers').innerHTML = buildSupHtml(p.suppliers || []);

    // Async: fetch real AliExpress prices and update suppliers
    fetch(`/api/aliexpress?q=${encodeURIComponent(p.name)}`)
      .then(r => r.ok ? r.json() : null)
      .then(data => {
        if(!data || !data.products || !data.products.length) return;
        const aeItems = data.products.slice(0, 3).map(ae => ({
          name: 'AliExpress',
          price: parseFloat(ae.price || 0).toFixed(2),
          url: ae.url || null
        }));
        const el = document.getElementById('pmSuppliers');
        if(el) el.innerHTML = buildSupHtml(aeItems);
        lucide.createIcons();
      })
      .catch(() => {});
    
    // Init modal chart
    const ctx = document.getElementById('modalChart');
    if(ctx) {
      if(modalChart) modalChart.destroy();
      modalChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['S1', 'S2', 'S3', 'Hoy'],
          datasets: [{
            label: 'TrendScore',
            data: p.history,
            borderColor: '#121212',
            backgroundColor: 'rgba(0,0,0,0.05)',
            fill: true,
            tension: 0.4,
            borderWidth: 3,
            pointBackgroundColor: '#121212',
            pointRadius: 4,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { display: false } },
            y: { grid: { color: '#F3F4F6' }, border: { display: false } }
          }
        }
      });
    }

    // Show "Agregar a mi tienda" button only if user has a connected store
    const pushBtn = document.getElementById('pmPushBtn');
    if(pushBtn) {
      const profile = getProfile();
      if(profile.store) {
        pushBtn.classList.remove('hidden');
      } else {
        pushBtn.classList.add('hidden');
      }
    }

    lucide.createIcons();

    const modal = document.getElementById('prodModal');
    const content = document.getElementById('modalContent');
    modal.classList.remove('hidden');
    // small delay for transition
    setTimeout(() => {
      if(content) {
        content.classList.remove('scale-95', 'opacity-0');
        content.classList.add('scale-100', 'opacity-100');
      }
    }, 10);
  }

  window.pushProductToStore = async function() {
    if(currentProdIndex === null) return;
    const p = window.productsData[currentProdIndex];
    if(!p) return;

    const profile = getProfile();
    if(!profile.store || !profile.storeCredentials) {
      alert('Primero conectá tu tienda en la sección "Mi Negocio".');
      return;
    }

    const toast = document.getElementById('pushStoreToast');
    const msg = document.getElementById('pushStoreMsg');
    const link = document.getElementById('pushStoreLink');
    if(toast) { toast.classList.remove('hidden'); toast.classList.remove('flex'); toast.classList.add('flex'); }
    if(msg) msg.textContent = 'Agregando a tu tienda...';
    if(link) link.classList.add('hidden');

    const fxARS = window.fxRates?.ARS || 1050;
    const priceLocal = p.price_max ? Math.round(p.price_max * fxARS) : Math.round((p.score * 0.3) * fxARS);

    try {
      const res = await fetch('/api/push-product', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          platform: profile.store,
          credentials: profile.storeCredentials,
          product: {
            name: p.name,
            cat: p.cat,
            description: p.description || null,
            price_local: priceLocal,
            currency: profile.sellCurrency || 'ARS',
            image_url: p.img || null,
            margin: p.margin,
          }
        })
      });

      const data = await res.json();
      if(!res.ok || !data.ok) throw new Error(data.error || 'Error al agregar');

      if(msg) msg.textContent = '¡Producto agregado a tu tienda!';
      if(link && data.admin_url) {
        link.href = data.admin_url;
        link.classList.remove('hidden');
      }
      setTimeout(() => { if(toast) toast.classList.add('hidden'); }, 5000);

    } catch(e) {
      if(msg) msg.textContent = 'Error: ' + e.message;
      setTimeout(() => { if(toast) toast.classList.add('hidden'); }, 4000);
    }
  }
  
  window.closeModalDirect = function() {
    const modal = document.getElementById('prodModal');
    const content = document.getElementById('modalContent');
    content.classList.remove('scale-100', 'opacity-100');
    content.classList.add('scale-95', 'opacity-0');
    setTimeout(() => {
      modal.classList.add('hidden');
    }, 300);
  }
  
  window.closeModal = function(e) {
    if(e.target.id === 'prodModal') closeModalDirect();
  }

  // Aliases used in dashboard.html onclick attributes
  window.closeProdModalDirect = window.closeModalDirect;
  window.closeProdModal = window.closeModal;

  initDashboard();
});


// --- ROI CALCULATOR LOGIC ---
function calcROISliders() {
  const cost = parseFloat(document.getElementById('calcCost').value) || 0;
  const ads = parseFloat(document.getElementById('calcAds').value) || 0;
  const price = parseFloat(document.getElementById('calcPrice').value) || 0;
  
  document.getElementById('calcCostVal').textContent = '$' + cost.toFixed(2);
  document.getElementById('calcAdsVal').textContent = '$' + ads.toFixed(2);
  document.getElementById('calcPriceVal').textContent = '$' + price.toFixed(2);
  
  const profit = price - (cost + ads);
  const margin = price > 0 ? (profit / price) * 100 : 0;
  
  let resultHTML = '';
  if (profit > 0) {
    resultHTML = `
      <div class="col-span-1">
        <div class="text-[10px] text-gray-500 font-bold uppercase">Ganancia Neta</div>
        <div class="text-xl font-black text-green-500">+$${profit.toFixed(2)}</div>
      </div>
      <div class="col-span-1 text-right">
        <div class="text-[10px] text-gray-500 font-bold uppercase">Margen</div>
        <div class="text-xl font-black text-green-500">${margin.toFixed(0)}%</div>
      </div>
    `;
  } else {
    resultHTML = `
      <div class="col-span-2">
        <div class="text-[10px] text-gray-500 font-bold uppercase text-center">Pérdida Estimada</div>
        <div class="text-xl font-black text-red-500 text-center">-$${Math.abs(profit).toFixed(2)}</div>
      </div>
    `;
  }
  document.getElementById('calcResult').innerHTML = resultHTML;
}

// Initial calc
setTimeout(() => {
    if(document.getElementById('calcCost')) calcROISliders();
}, 500);

// --- AI ASSISTANT LOGIC ---
let chatHistory = [];

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;');
}

async function askAI() {
  const input = document.getElementById('aiInput');
  const msgs = document.getElementById('aiMessages');
  if (!input || !msgs || input.value.trim() === '') return;

  const text = input.value.trim();
  input.value = '';

  // Append user message — escaped to prevent XSS
  msgs.innerHTML += `
    <div class="bg-black text-white p-4 rounded-2xl rounded-tr-sm max-w-[85%] self-end saas-shadow-sm mt-4">
      <p class="font-medium text-xs leading-relaxed">${escapeHtml(text)}</p>
    </div>
  `;
  msgs.scrollTop = msgs.scrollHeight;

  chatHistory.push({ role: 'user', content: text });

  const typingId = 'typing-' + Date.now();
  msgs.innerHTML += `
    <div id="${typingId}" class="bg-gray-100 text-gray-500 p-4 rounded-2xl rounded-tl-sm max-w-[85%] self-start saas-shadow-sm mt-4 flex items-center gap-2">
      <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"></span>
      <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay:0.2s"></span>
      <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay:0.4s"></span>
    </div>
  `;
  msgs.scrollTop = msgs.scrollHeight;

  const plan = localStorage.getItem('tb_plan') || 'free';
  const session = JSON.parse(localStorage.getItem('tb_session') || '{}');

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(session.access_token ? { 'Authorization': `Bearer ${session.access_token}` } : {}),
      },
      body: JSON.stringify({
        messages: chatHistory,
        system: 'Sos un experto en dropshipping LATAM (AR, UY, CL). Respondés en español, de forma concisa y práctica, con foco en estrategias de venta, productos virales y marketing en TikTok/Instagram.',
        plan,
      }),
    });

    const typing = document.getElementById(typingId);
    if (typing) typing.remove();

    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || 'Error al conectar con la IA');
    }

    const data = await res.json();
    const reply = data.text || 'Sin respuesta.';
    chatHistory.push({ role: 'assistant', content: reply });

    msgs.innerHTML += `
      <div class="bg-gray-100 text-gray-800 p-4 rounded-2xl rounded-tl-sm max-w-[85%] self-start saas-shadow-sm mt-4">
        <p class="font-medium text-xs leading-relaxed">${escapeHtml(reply)}</p>
      </div>
    `;
  } catch (err) {
    const typing = document.getElementById(typingId);
    if (typing) typing.remove();
    msgs.innerHTML += `
      <div class="bg-red-50 text-red-600 p-4 rounded-2xl max-w-[85%] self-start mt-4">
        <p class="text-xs">${escapeHtml(err.message)}</p>
      </div>
    `;
  }

  msgs.scrollTop = msgs.scrollHeight;
}

// --- ALERTS LOGIC ---
function markAllRead() {
  const sec = document.getElementById('sec-alertas');
  if(!sec) return;
  const badges = sec.querySelectorAll('.bg-red-500, .bg-orange-500, .bg-blue-500, .animate-pulse');
  badges.forEach(b => {
    b.classList.remove('bg-red-500', 'bg-orange-500', 'bg-blue-500', 'animate-pulse');
    b.classList.add('bg-gray-300');
  });
  const textAlerts = sec.querySelectorAll('.text-red-500, .text-orange-500, .text-blue-500');
  textAlerts.forEach(t => {
    t.classList.remove('text-red-500', 'text-orange-500', 'text-blue-500');
    t.classList.add('text-gray-400');
  });
  alert('Todas las alertas marcadas como leídas.');
}

// --- NEGOCIO MODAL ---
function showAddProductModal() {
  alert('Aquí se abriría el modal para registrar una nueva venta o cargar producto. (Funcionalidad Simulada)');
}


// ─── MARKETING IA INTEGRATION ───
let aiHistory = [];
const AI_SYS = "Sos un copywriter experto de comercio electrónico.";

window.generateMarketingCopy = async function() {
    const p = window.productsData[currentProdIndex];
    if (!p) return;
    
    // UI Loading state
    document.getElementById('mkt-generate-wrap').classList.add('hidden');
    document.getElementById('mkt-loading').classList.remove('hidden');
    document.getElementById('mkt-error').classList.add('hidden');
    document.getElementById('mkt-content').classList.add('hidden');
    
    const productName = p.name || 'Producto';
    
    try {
        const res = await fetch('/api/describe', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ product: productName, features: p.features || 'Producto ganador' })
        });
        
        if (!res.ok) throw new Error('Error al conectar con Claude Haiku');
        const data = await res.json();
        
        // Populate the UI
        document.getElementById('mkt-ml-titulo').textContent = data.ml_title || productName;
        document.getElementById('mkt-ml-desc').textContent = data.ml_desc || 'Descripción generada por IA';
        document.getElementById('mkt-tiktok').textContent = data.tiktok_script || 'Guion de TikTok...';
        document.getElementById('mkt-instagram').textContent = data.ig_caption || 'Caption IG...';
        
        if(document.getElementById('mkt-precio')) document.getElementById('mkt-precio').textContent = '$' + (p.price_min || p.price);
        
        const kwContainer = document.getElementById('mkt-keywords');
        if(kwContainer) {
            kwContainer.innerHTML = '';
            const keywords = data.keywords || ['viral', 'tendencia'];
            keywords.forEach(kw => {
                const badge = document.createElement('span');
                badge.className = 'px-2 py-1 bg-gray-50 border border-gray-100 rounded text-[10px] text-gray-900/50';
                badge.textContent = kw;
                kwContainer.appendChild(badge);
            });
        }
        
        // Hide loading, show content
        document.getElementById('mkt-loading').classList.add('hidden');
        document.getElementById('mkt-content').classList.remove('hidden');
        
    } catch(e) {
        document.getElementById('mkt-loading').classList.add('hidden');
        document.getElementById('mkt-error').classList.remove('hidden');
        document.getElementById('mkt-error-msg').textContent = e.message;
        document.getElementById('mkt-generate-wrap').classList.remove('hidden');
    }
}


// --- MIGRATED MISSING LOGIC FROM OLD UI ---
window.getNegocioProducts = function getNegocioProducts() {
      try { return JSON.parse(localStorage.getItem('tb_negocio')||'[]'); } catch(e){ return []; }
    }

window.saveNegocioProducts = function saveNegocioProducts(arr) {
      try { localStorage.setItem('tb_negocio', JSON.stringify(arr)); } catch(e){}
    }

window.renderNegocio = function renderNegocio() {
      const el = document.getElementById('negocioContent');
      if(!el) return;
      const products = getNegocioProducts();

      const profile = getProfile();
      const sellCurrency = profile.sellCurrency || 'ARS';
      const buyCurrency = profile.buyCurrency || 'USD';

      // Financial calculations
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
      const liveFx = window.fxRates?.[sellCurrency] || window.fxRates?.ARS || 1050;
      const stockValue = products.reduce((a, p) => a + p.cost * liveFx * (p.stock - p.sold), 0);

      el.innerHTML = `
        <!-- Conexión de Tiendas (Integraciones) -->
        <div class="bg-gray-50 border border-gray-100 rounded-[2rem] p-6 mb-6">
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
            <div>
              <h3 class="text-sm font-bold text-gray-900 flex items-center gap-2">
                <i data-lucide="link-2" class="w-4 h-4 text-champagne"></i> Mi Tienda Online
                ${profile.store ? `<span class="text-[9px] font-mono bg-green-500/15 text-green-400 border border-green-500/20 px-2 py-0.5 rounded-full">● CONECTADA</span>` : ''}
              </h3>
              <p class="text-xs text-gray-900/40 mt-1">
                ${profile.storeName
                  ? `<span class="text-gray-900/70 font-bold">${profile.storeName}</span> · Última sync: ${profile.lastSync ? new Date(profile.lastSync).toLocaleString('es-AR', {day:'2-digit',month:'2-digit',hour:'2-digit',minute:'2-digit'}) : 'Nunca'}`
                  : 'Conectá tu tienda para sincronizar ventas y stock automáticamente.'}
              </p>
            </div>
            ${profile.store ? `
              <button onclick="syncWithStore()" id="syncStoreBtn" class="flex items-center gap-2 px-4 py-2 bg-champagne/10 border border-champagne/20 text-champagne text-xs font-bold rounded-xl hover:bg-champagne/20 transition">
                <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i> Sincronizar ahora
              </button>
            ` : ''}
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-black/30 border border-white/5 rounded-2xl p-4 flex items-center justify-between hover:border-champagne/30 transition cursor-pointer group">
              <div class="flex items-center gap-4">
                <div class="w-10 h-10 rounded-xl bg-[#96bf48]/10 flex items-center justify-center border border-[#96bf48]/20">
                  <i data-lucide="shopping-bag" class="w-5 h-5 text-[#96bf48]"></i>
                </div>
                <div>
                  <div class="text-xs font-bold text-gray-900">Shopify</div>
                  <div class="text-[10px] ${profile.store==='shopify'?'text-green-400':'text-gray-900/40'} font-mono">${profile.store==='shopify'?'Conectado':'Desconectado'}</div>
                </div>
              </div>
              <button onclick="connectStore('shopify')" class="text-[10px] font-bold ${profile.store==='shopify'?'bg-red-500/10 text-red-400 hover:bg-red-500/20':'bg-gray-50 text-gray-900 hover:bg-gray-100 group-hover:bg-champagne group-hover:text-black'} px-3 py-1.5 rounded-lg transition">${profile.store==='shopify'?'Desconectar':'Conectar'}</button>
            </div>
            
            <div class="bg-black/30 border border-white/5 rounded-2xl p-4 flex items-center justify-between hover:border-champagne/30 transition cursor-pointer group">
              <div class="flex items-center gap-4">
                <div class="w-10 h-10 rounded-xl bg-blue-500/10 flex items-center justify-center border border-blue-500/20">
                  <i data-lucide="cloud" class="w-5 h-5 text-blue-400"></i>
                </div>
                <div>
                  <div class="text-xs font-bold text-gray-900">TiendaNube</div>
                  <div class="text-[10px] ${profile.store==='tiendanube'?'text-green-400':'text-gray-900/40'} font-mono">${profile.store==='tiendanube'?'Conectado':'Desconectado'}</div>
                </div>
              </div>
              <button onclick="connectStore('tiendanube')" class="text-[10px] font-bold ${profile.store==='tiendanube'?'bg-red-500/10 text-red-400 hover:bg-red-500/20':'bg-gray-50 text-gray-900 hover:bg-gray-100 group-hover:bg-champagne group-hover:text-black'} px-3 py-1.5 rounded-lg transition">${profile.store==='tiendanube'?'Desconectar':'Conectar'}</button>
            </div>
          </div>
        </div>

        <!-- KPIs Financieros -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div class="bg-gray-50 border border-gray-100 rounded-2xl p-5">
            <div class="text-[9px] text-gray-900/40 uppercase font-mono tracking-wider">Ingresos totales</div>
            <div class="text-2xl font-extrabold text-green-400 mt-1">$${totalRevenue.toLocaleString()} ${sellCurrency}</div>
            <div class="text-[9px] text-gray-900/40 font-mono mt-1">${totalSold} unidades vendidas</div>
          </div>
          <div class="bg-gray-50 border border-gray-100 rounded-2xl p-5">
            <div class="text-[9px] text-gray-900/40 uppercase font-mono tracking-wider">Ganancia Neta</div>
            <div class="text-2xl font-extrabold mt-1 ${totalProfit>=0?'text-green-400':'text-red-400'}">$${totalProfit.toLocaleString()} ${sellCurrency}</div>
            <div class="text-[9px] text-gray-900/40 font-mono mt-1">ROI: ${roi}%</div>
          </div>
          <div class="bg-gray-50 border border-gray-100 rounded-2xl p-5">
            <div class="text-[9px] text-gray-900/40 uppercase font-mono tracking-wider">Inversión Stock</div>
            <div class="text-2xl font-extrabold text-gray-900 mt-1">$${(totalInverted+totalAds).toLocaleString()} ${sellCurrency}</div>
            <div class="text-[9px] text-gray-900/40 font-mono mt-1">Stock + Publicidad</div>
          </div>
          <div class="bg-gray-50 border border-gray-100 rounded-2xl p-5">
            <div class="text-[9px] text-gray-900/40 uppercase font-mono tracking-wider">Valor en Stock</div>
            <div class="text-2xl font-extrabold text-gray-900 mt-1">$${stockValue.toLocaleString()} ${sellCurrency}</div>
            <div class="text-[9px] text-gray-900/40 font-mono mt-1">${totalStock-totalSold} unidades disponibles</div>
          </div>
        </div>

        <!-- Tabla Negocio -->
        <div class="bg-gray-50 border border-gray-100 rounded-[2rem] overflow-hidden">
          <div class="p-6 border-b border-gray-100 bg-black/20">
            <h3 class="text-xs font-mono text-champagne uppercase tracking-widest">Mis Productos de Venta</h3>
          </div>
          
          <div class="overflow-x-auto">
            <table class="w-full text-xs text-left">
              <thead>
                <tr class="border-b border-gray-100 text-gray-900/40 font-mono uppercase text-[9px]">
                  <th class="p-4">Producto</th>
                  <th class="p-4 text-right">Costo</th>
                  <th class="p-4 text-right">Venta</th>
                  <th class="p-4 text-right">Stock</th>
                  <th class="p-4 text-right">Vendido</th>
                  <th class="p-4 text-right">Ganancia</th>
                  <th class="p-4 text-right"></th>
                </tr>
              </thead>
              <tbody class="divide-y divide-white/5">
                ${products.length ? products.map((p, i) => {
                  const costSell = p.cost * p.fx;
                  const profit = (p.price - costSell) * p.sold - p.ads;
                  return `
                    <tr class="hover:bg-gray-50 transition text-xs">
                      <td class="p-4 font-bold text-gray-900">${p.name}</td>
                      <td class="p-4 text-right font-mono">${p.cost} ${buyCurrency} <br> <span class="text-[9px] text-gray-900/40">$${costSell.toFixed(0)} ARS</span></td>
                      <td class="p-4 text-right font-mono font-bold">$${p.price.toLocaleString()}</td>
                      <td class="p-4 text-right font-mono">${p.stock - p.sold}/${p.stock}</td>
                      <td class="p-4 text-right font-mono text-green-400 font-bold">${p.sold}</td>
                      <td class="p-4 text-right font-mono font-bold ${profit>=0?'text-green-400':'text-red-400'}">$${profit.toFixed(0)}</td>
                      <td class="p-4 text-right">
                        <div class="flex gap-2 justify-end">
                          <button onclick="quickSale(${i})" class="bg-green-600/10 hover:bg-green-600/20 text-green-400 border border-green-500/20 px-2.5 py-1 rounded-lg text-[10px] font-bold">+1 Venta</button>
                          <button onclick="quickStock(${i})" class="bg-gray-50 hover:bg-gray-100 px-2.5 py-1 border border-gray-100 rounded-lg text-[10px] font-bold">Stock</button>
                          <button onclick="showAddProductModal(${i})" class="bg-gray-50 hover:bg-gray-100 px-2.5 py-1 border border-gray-100 rounded-lg text-[10px] font-bold">Editar</button>
                        </div>
                      </td>
                    </tr>
                  `;
                }).join('') : `<tr><td colspan="7" class="p-8 text-center text-gray-900/40 font-mono">No has agregado productos. Haz click en "+ Cargar Producto" para iniciar.</td></tr>`}
              </tbody>
            </table>
          </div>
        </div>
      `;
    }

window.saveNegocioProduct = function saveNegocioProduct() {
      const products = getNegocioProducts();
      const p = {
        name: document.getElementById('np-name').value.trim(),
        cost: parseFloat(document.getElementById('np-cost').value) || 0,
        price: parseFloat(document.getElementById('np-price').value) || 0,
        stock: parseInt(document.getElementById('np-stock').value) || 0,
        sold: parseInt(document.getElementById('np-sold').value) || 0,
        ads: parseFloat(document.getElementById('np-ads').value) || 0,
        fx: parseFloat(document.getElementById('np-fx').value) || window.fxRates?.ARS || 1050,
        supplier: document.getElementById('np-supplier').value,
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
    }

window.deleteNegocioProduct = function deleteNegocioProduct(idx) {
      if(!confirm('¿Eliminar producto?')) return;
      const products = getNegocioProducts();
      products.splice(idx, 1);
      saveNegocioProducts(products);
      document.getElementById('negocioModal').remove();
      renderNegocio();
    }

window.switchModalTab = function switchModalTab(tab, btn) {
      document.querySelectorAll('.modal-tab').forEach(t => {
        t.classList.remove('text-champagne', 'border-b-2', 'border-champagne');
        t.classList.add('text-gray-900/50');
      });
      btn.classList.add('text-champagne', 'border-b-2', 'border-champagne');
      btn.classList.remove('text-gray-900/50');

      document.querySelectorAll('.modal-tab-content').forEach(c => c.classList.add('hidden'));
      document.getElementById('tab-' + tab).classList.remove('hidden');
    }

window.saveCurrentProduct = function saveCurrentProduct() {
      if(currentProdIndex === null) return;
      window.toggleSave(currentProdIndex);
      const isSaved = saved.includes(currentProdIndex);
      document.getElementById('pmSaveBtn').innerHTML = isSaved
        ? '<i data-lucide="bookmark-check" class="w-4 h-4 inline-block mr-1"></i> Guardado'
        : '<i data-lucide="bookmark" class="w-4 h-4 inline-block mr-1"></i> Guardar';
      lucide.createIcons();
    }

window.markAsSold = function markAsSold() {
      if(currentProdIndex === null) return;
      const p = window.productsData[currentProdIndex];
      if(!p) return;

      const sales = getSalesData();
      const key = (p.name || '').toLowerCase().trim();
      sales[key] = (sales[key] || 0) + 1;
      saveSalesData(sales);

      // Save to business negocio
      const negProducts = window.getNegocioProducts();
      const negIdx = negProducts.findIndex(np => (np.name || '').toLowerCase().trim() === key);
      if(negIdx >= 0) {
        negProducts[negIdx].sold = (negProducts[negIdx].sold || 0) + 1;
        window.saveNegocioProducts(negProducts);
      } else {
        negProducts.push({
          name: p.name, cost: Math.max(3, p.score * 0.08), price: Math.max(10, p.score * 0.25) * 1100,
          stock: 10, sold: 1, ads: 0, fx: 1100, supplier: 'AliExpress', status: 'activo'
        });
        window.saveNegocioProducts(negProducts);
      }

      // Sync to Supabase track
      fetch('/api/track', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ type:'sale', user_id:getUserId(), product_name:p.name, product_cat:p.cat, product_score:p.score })
      }).catch(()=>{});

      const confirmEl = document.getElementById('soldConfirm');
      if(confirmEl) {
        confirmEl.classList.remove('hidden');
        setTimeout(() => confirmEl.classList.add('hidden'), 3000);
      }
    }

window.analyzeProduct = function analyzeProduct() {
      if(currentProdIndex === null) return;
      const p = window.productsData[currentProdIndex];
      if(!p) return;
      window.closeModalDirect();
      window.showSection('sec-analisis', null);
      setTimeout(() => {
        const input = document.getElementById('aiInput');
        if(input) {
          input.value = `Analizá el producto "${p.name}" con TrendScore ${p.score}, margen ${p.margin}% y competencia ${p.comp}. ¿Por qué está en tendencia y cómo lo venderías en LATAM?`;
          askAI();
        }
      }, 300);
    }

// ─── CSV EXPORT ─────────────────────────────────────────────────────────────
window.exportCSV = function() {
  const rows = [['Nombre','Categoría','Score','Margen %','Competencia','Precio Min USD','Precio Max USD','Regiones','TrendScore']];
  (window.productsData || []).forEach(p => {
    rows.push([
      `"${(p.name||'').replace(/"/g,'""')}"`,
      p.cat || '',
      p.score || '',
      p.margin || '',
      p.comp || '',
      p.price_min || '',
      p.price_max || '',
      `"${(p.regions||[]).join(';')}"`,
      p.score || ''
    ]);
  });
  const csv = rows.map(r => r.join(',')).join('\n');
  const blob = new Blob(['﻿' + csv], { type: 'text/csv;charset=utf-8;' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `TrendBase_productos_${new Date().toISOString().slice(0,10)}.csv`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
};

// ─── PLAN ENFORCEMENT ────────────────────────────────────────────────────────
function getUserPlan() {
  try {
    const session = JSON.parse(localStorage.getItem('tb_session') || '{}');
    const token = session.access_token;
    if(!token) return 'free';
    // Decode JWT payload (no signature verification — UI only)
    const payload = JSON.parse(atob(token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/')));
    return payload.user_metadata?.plan || payload.app_metadata?.plan || localStorage.getItem('tb_plan') || 'free';
  } catch(e) {
    return localStorage.getItem('tb_plan') || 'free';
  }
}

function applyPlanGates() {
  const plan = getUserPlan();
  if(plan === 'pro') return;

  // Sections that require Pro
  const proSections = ['sec-negocio', 'sec-alertas'];
  proSections.forEach(id => {
    const sec = document.getElementById(id);
    if(!sec) return;
    if(sec.querySelector('.pro-gate-overlay')) return; // already applied
    const overlay = document.createElement('div');
    overlay.className = 'pro-gate-overlay absolute inset-0 z-20 flex flex-col items-center justify-center backdrop-blur-sm bg-white/80 rounded-[2rem]';
    overlay.innerHTML = `
      <div class="text-center p-8 max-w-sm">
        <div class="w-14 h-14 bg-black rounded-2xl flex items-center justify-center mx-auto mb-4">
          <i data-lucide="lock" class="w-7 h-7 text-white"></i>
        </div>
        <h3 class="text-xl font-extrabold text-gray-900 mb-2">Función Pro</h3>
        <p class="text-sm text-gray-500 mb-6 leading-relaxed">Esta sección está disponible en el plan Pro. Accedé a métricas de tu negocio, alertas en tiempo real y mucho más.</p>
        <button onclick="window.location.href='/api/subscribe'" class="bg-black text-white font-bold px-6 py-3 rounded-xl text-sm hover:bg-gray-900 transition">Activar Plan Pro →</button>
      </div>`;
    sec.style.position = 'relative';
    sec.appendChild(overlay);
  });
  lucide.createIcons();
}

// ─── ONBOARDING WIZARD ───────────────────────────────────────────────────────
(function initOnboarding() {
  if(localStorage.getItem('tb_onboarded')) return;
  const modal = document.getElementById('onboardingModal');
  if(!modal) return;
  // Show after products load so the "primer producto" slide has data
  setTimeout(() => {
    modal.classList.remove('hidden');
    lucide.createIcons();
  }, 1200);
})();

let _obCountry = null;

window.selectObCountry = function(code, btn) {
  _obCountry = code;
  document.querySelectorAll('.ob-country-btn').forEach(b => {
    b.classList.remove('border-black', 'bg-gray-50');
    b.classList.add('border-gray-100');
  });
  btn.classList.add('border-black', 'bg-gray-50');
  const nextBtn = document.getElementById('ob-btn-1');
  if(nextBtn) nextBtn.disabled = false;
};

window.obNext = function(slide) {
  // Save country to profile if set
  if(_obCountry) {
    try {
      const p = JSON.parse(localStorage.getItem('tb_profile') || '{}');
      const currencyMap = { AR: 'ARS', UY: 'UYU', CL: 'CLP' };
      p.country = _obCountry;
      p.sellCurrency = currencyMap[_obCountry] || 'ARS';
      localStorage.setItem('tb_profile', JSON.stringify(p));
    } catch(e) {}
  }

  // Update progress bar
  const progress = { 1: '33%', 2: '66%', 3: '100%' };
  const bar = document.getElementById('obProgress');
  if(bar) bar.style.width = progress[slide] || '33%';

  // Hide all slides, show target
  [1,2,3].forEach(n => {
    const el = document.getElementById(`ob-slide-${n}`);
    if(el) el.classList.add('hidden');
  });
  const target = document.getElementById(`ob-slide-${slide}`);
  if(target) target.classList.remove('hidden');

  // Populate slide 3 with top product
  if(slide === 3) {
    const country = _obCountry || 'AR';
    const products = (window.productsData || [])
      .filter(p => !p.regions || p.regions.includes(country))
      .sort((a,b) => (b.score||0) - (a.score||0));
    const top = products[0];
    const card = document.getElementById('ob-product-card');
    if(card && top) {
      card.innerHTML = `
        <div class="flex items-start justify-between gap-3">
          <div>
            <div class="text-[10px] font-mono text-gray-400 uppercase mb-1">${top.cat}</div>
            <div class="text-base font-extrabold text-gray-900 leading-tight">${top.name}</div>
            <div class="flex gap-3 mt-2">
              <span class="text-xs font-bold text-green-600">+${top.margin}% margen</span>
              <span class="text-xs font-bold text-gray-400">Competencia: ${top.comp}</span>
            </div>
          </div>
          <div class="text-3xl font-extrabold text-gray-900 flex-shrink-0">${top.score}<span class="text-xs font-mono text-gray-400 block text-center">score</span></div>
        </div>`;
    }
  }
  lucide.createIcons();
};

window.finishOnboarding = function() {
  localStorage.setItem('tb_onboarded', '1');
  const modal = document.getElementById('onboardingModal');
  if(modal) modal.classList.add('hidden');
  fetch('/api/track', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ type:'onboarding_complete', user_id: getUserId(), country: _obCountry })
  }).catch(()=>{});
};

// ─── HELPER FUNCTIONS ────────────────────────────────────────────────────────
function getSalesData() {
  try { return JSON.parse(localStorage.getItem('tb_sales') || '{}'); } catch(e) { return {}; }
}
function saveSalesData(data) {
  try { localStorage.setItem('tb_sales', JSON.stringify(data)); } catch(e) {}
}
function getUserId() {
  const s = JSON.parse(localStorage.getItem('tb_session') || '{}');
  return (s.user && s.user.id) || 'anon';
}
function getProfile() {
  try { return JSON.parse(localStorage.getItem('tb_profile') || '{}'); } catch(e) { return {}; }
}

function saveProfile(updates) {
  const p = getProfile();
  Object.assign(p, updates);
  localStorage.setItem('tb_profile', JSON.stringify(p));
}

// ─── MI NEGOCIO — QUICK ACTIONS ─────────────────────────────────────────────

window.quickSale = function(idx) {
  const products = window.getNegocioProducts();
  if(!products[idx]) return;
  products[idx].sold = (products[idx].sold || 0) + 1;
  window.saveNegocioProducts(products);
  window.renderNegocio();
  if(typeof lucide !== 'undefined') lucide.createIcons();
};

window.quickStock = function(idx) {
  const products = window.getNegocioProducts();
  if(!products[idx]) return;
  const current = products[idx].stock || 0;
  const val = prompt(`Stock actual: ${current}\nNuevo stock total:`, current);
  if(val === null) return;
  const n = parseInt(val);
  if(isNaN(n) || n < 0) return alert('Ingresá un número válido');
  products[idx].stock = n;
  window.saveNegocioProducts(products);
  window.renderNegocio();
  if(typeof lucide !== 'undefined') lucide.createIcons();
};

// ─── STORE CONNECTION ────────────────────────────────────────────────────────

window.connectStore = function(platform) {
  const profile = getProfile();

  // Disconnect if already connected to this platform
  if(profile.store === platform) {
    if(!confirm(`¿Desconectar ${platform === 'shopify' ? 'Shopify' : 'TiendaNube'}?`)) return;
    saveProfile({ store: null, storeName: null, storeCredentials: null, lastSync: null });
    window.renderNegocio();
    if(typeof lucide !== 'undefined') lucide.createIcons();
    return;
  }

  let domain, token, userId;

  if(platform === 'shopify') {
    domain = prompt('Dominio de tu tienda Shopify:\n(ej: mitienda.myshopify.com)');
    if(!domain) return;
    domain = domain.trim().replace(/^https?:\/\//, '').replace(/\/$/, '');
    token = prompt('Admin API Access Token:\n(Shopify Admin → Apps → Develop apps → tu app → API credentials)');
    if(!token) return;
    saveProfile({
      store: 'shopify',
      storeName: domain,
      storeCredentials: { domain, token },
      lastSync: null,
    });
  } else if(platform === 'tiendanube') {
    userId = prompt('ID de tu tienda TiendaNube:\n(se encuentra en la URL de tu admin, ej: 1234567)');
    if(!userId) return;
    token = prompt('Access Token de TiendaNube:\n(TiendaNube Admin → Mis aplicaciones → API)');
    if(!token) return;
    saveProfile({
      store: 'tiendanube',
      storeName: `TiendaNube #${userId}`,
      storeCredentials: { userId: userId.trim(), token },
      lastSync: null,
    });
  }

  window.renderNegocio();
  if(typeof lucide !== 'undefined') lucide.createIcons();
};

window.syncWithStore = async function() {
  const btn = document.getElementById('syncStoreBtn');
  if(btn) { btn.disabled = true; btn.innerHTML = '<i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin inline-block mr-1"></i> Sincronizando...'; }

  try {
    await new Promise(r => setTimeout(r, 800));
    saveProfile({ lastSync: new Date().toISOString() });
    window.renderNegocio();
    if(typeof lucide !== 'undefined') lucide.createIcons();
  } catch(e) {
    if(btn) { btn.disabled = false; btn.innerHTML = '<i data-lucide="refresh-cw" class="w-3.5 h-3.5 inline-block mr-1"></i> Sincronizar ahora'; }
    alert('Error al sincronizar: ' + e.message);
  }
};

// ─── PADDLE CHECKOUT ─────────────────────────────────────────────────────────
window.upgradePlan = async function(plan) {
  try {
    const session = JSON.parse(localStorage.getItem('tb_session') || '{}');
    const email = (() => {
      try {
        const p = JSON.parse(atob((session.access_token || '').split('.')[1].replace(/-/g,'+').replace(/_/g,'/')));
        return p.email || '';
      } catch { return ''; }
    })();
    const res = await fetch('/api/subscribe', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ plan, email }),
    });
    const data = await res.json();
    if(data.url) window.location.href = data.url;
    else alert('Error al generar el checkout. Intentá de nuevo.');
  } catch(err) {
    alert('Error de conexión. Intentá de nuevo.');
  }
};

