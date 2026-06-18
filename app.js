document.addEventListener('DOMContentLoaded', () => {
  lucide.createIcons();
  
  
  window.productsData = [];
  
  async function loadRealProducts() {
    try {
      const res = await fetch('/api/products');
      if (!res.ok) throw new Error('Failed to load products');
      window.productsData = await res.json();
      
      // Transform keys to match what the UI expects if necessary
      // Supabase format usually matches, but let's be sure.
      
      initDashboard();
    } catch (e) {
      console.error(e);
      // Fallback to MOCK_DATA if API fails in dev mode
      if (window.MOCK_DATA && window.MOCK_DATA.products) {
          window.productsData = window.MOCK_DATA.products;
          initDashboard();
      }
    }
  }
  
  loadRealProducts();

  const PAGE_SIZE = 10;
  let currentPage = 1;
  let currentProdIndex = null;
  
  // Charts
  let mainChart = null;
  let donutChart = null;
  let modalChart = null;
  
  const WEEKS = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'];

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
  }
  
  function initCharts() {
    // Main Chart (Bar)
    const ctxMain = document.getElementById('mainChart');
    if(ctxMain) {
      mainChart = new Chart(ctxMain, {
        type: 'bar',
        data: {
          labels: WEEKS,
          datasets: [{
            label: 'Tendencias Activas',
            data: [25, 42, 38, 55, 48, 85],
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
            y: { grid: { color: '#F3F4F6' }, border: { display: false } }
          }
        }
      });
    }

    // Donut Chart
    const ctxDonut = document.getElementById('donutChart');
    if(ctxDonut) {
      const cats = {};
      products.forEach(p => cats[p.cat] = (cats[p.cat] || 0) + 1);
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
            <button onclick="openProduct(${idx})" class="bg-black hover:bg-gray-800 text-gray-900 text-xs font-bold px-4 py-2 rounded-xl transition saas-shadow">Ver Detalle</button>
          </td>
        </tr>
      `;
    }).join('');
    
    document.getElementById('pageInfo').textContent = `Mostrando ${start + 1}-${Math.min(start + PAGE_SIZE, products.length)} de ${products.length}`;
    lucide.createIcons();
  }
  
  window.nextPage = function() {
    if(currentPage * PAGE_SIZE < products.length) {
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
    
    // Render suppliers
    const supHTML = p.suppliers.map(s => `
      <div class="flex items-center justify-between p-3 border border-gray-100 bg-white rounded-2xl shadow-sm">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center">
            <i data-lucide="package" class="w-4 h-4 text-gray-600"></i>
          </div>
          <span class="font-bold text-sm text-gray-900">${s.name}</span>
        </div>
        <span class="font-mono text-gray-500 text-sm">$${s.price}</span>
      </div>
    `).join('');
    document.getElementById('pmSuppliers').innerHTML = supHTML;
    
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

    lucide.createIcons();
    
    const modal = document.getElementById('prodModal');
    const content = document.getElementById('modalContent');
    modal.classList.remove('hidden');
    // small delay for transition
    setTimeout(() => {
      content.classList.remove('scale-95', 'opacity-0');
      content.classList.add('scale-100', 'opacity-100');
    }, 10);
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
function askAI() {
  const input = document.getElementById('aiInput');
  const msgs = document.getElementById('aiMessages');
  if(!input || !msgs || input.value.trim() === '') return;
  
  const text = input.value.trim();
  
  // User message
  msgs.innerHTML += `
    <div class="bg-black text-gray-900 p-4 rounded-2xl rounded-tr-sm max-w-[85%] self-end saas-shadow-sm mt-4">
      <p class="font-medium text-xs leading-relaxed">${text}</p>
    </div>
  `;
  
  input.value = '';
  msgs.scrollTop = msgs.scrollHeight;
  
  // Fake typing
  const typingId = 'typing-' + Date.now();
  msgs.innerHTML += `
    <div id="${typingId}" class="bg-gray-100 text-gray-500 p-4 rounded-2xl rounded-tl-sm max-w-[85%] self-start saas-shadow-sm mt-4 flex items-center gap-2">
      <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"></span>
      <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></span>
      <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></span>
    </div>
  `;
  msgs.scrollTop = msgs.scrollHeight;
  
  setTimeout(() => {
    document.getElementById(typingId).remove();
    msgs.innerHTML += `
      <div class="bg-gray-100 text-gray-800 p-4 rounded-2xl rounded-tl-sm max-w-[85%] self-start saas-shadow-sm mt-4">
        <p class="font-medium text-xs leading-relaxed">Según mis datos, ese producto tiene una alta estacionalidad. Te recomendaría preparar creativos enfocados en el ángulo de "regalo ideal" y apuntar a audiencias de 25-34 años en TikTok Ads. El CPA estimado rondará los $4.50.</p>
      </div>
    `;
    msgs.scrollTop = msgs.scrollHeight;
  }, 2000);
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
      const stockValue = products.reduce((a, p) => a + p.cost * (p.fx || 1100) * (p.stock - p.sold), 0);

      const profile = getProfile();
      const sellCurrency = profile.sellCurrency || 'ARS';
      const buyCurrency = profile.buyCurrency || 'USD';

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
        fx: parseFloat(document.getElementById('np-fx').value) || 1100,
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

      if(tab === 'history' && currentProd !== null) {
        renderHistoryChart();
      }
    }

window.saveCurrentProduct = function saveCurrentProduct() {
      if(currentProd === null) return;
      toggleSave(currentProd);
      document.getElementById('pmSaveBtn').innerHTML = saved.includes(currentProd) ? '<i data-lucide="bookmark-check" class="w-4 h-4 inline-block mr-1"></i> Guardado' : '<i data-lucide="bookmark" class="w-4 h-4 inline-block mr-1"></i> Guardar';
      lucide.createIcons();
    }

window.markAsSold = function markAsSold() {
      if(currentProd === null) return;
      const p = PRODUCTS[currentProd];
      if(!p) return;
      
      const sales = getSalesData();
      const key = (p.name || '').toLowerCase().trim();
      sales[key] = (sales[key] || 0) + 1;
      saveSalesData(sales);

      // Save to business negocio
      const negProducts = getNegocioProducts();
      const negIdx = negProducts.findIndex(np => (np.name || '').toLowerCase().trim() === key);
      if(negIdx >= 0) {
        negProducts[negIdx].sold = (negProducts[negIdx].sold || 0) + 1;
        saveNegocioProducts(negProducts);
      } else {
        negProducts.push({
          name: p.name, cost: Math.max(3, p.score * 0.08), price: Math.max(10, p.score * 0.25) * 1100,
          stock: 10, sold: 1, ads: 0, fx: 1100, supplier: 'AliExpress', status: 'activo'
        });
        saveNegocioProducts(negProducts);
      }

      // Sync to Supabase track
      fetch('/api/track', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ type:'sale', user_id:getUserId(), product_name:p.name, product_cat:p.cat, product_score:p.score })
      }).catch(()=>{});

      const confirm = document.getElementById('soldConfirm');
      if(confirm) {
        confirm.classList.remove('hidden');
        setTimeout(() => confirm.classList.add('hidden'), 3000);
      }
      
      renderPublicLeaderboard();
    }

window.analyzeProduct = function analyzeProduct() {
      if(currentProd === null) return;
      const p = PRODUCTS[currentProd];
      closeProdModalDirect();
      enterDash();
      setTimeout(() => {
        goSection('analisis');
        askAI(`Analizá el producto "${p.name}" con TrendScore ${p.score}, margen ${p.marginStr} y competencia ${p.comp}. ¿Por qué está en tendencia y cómo lo venderías en LATAM?`);
      }, 300);
    }

