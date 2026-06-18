document.addEventListener('DOMContentLoaded', () => {
  lucide.createIcons();
  
  if (!window.MOCK_DATA || !window.MOCK_DATA.products) {
    console.error("No MOCK_DATA found!");
    return;
  }
  
  const products = window.MOCK_DATA.products;
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
            <button onclick="openProduct(${idx})" class="bg-black hover:bg-gray-800 text-white text-xs font-bold px-4 py-2 rounded-xl transition saas-shadow">Ver Detalle</button>
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
    }
  }
  
  window.prevPage = function() {
    if(currentPage > 1) {
      currentPage--;
      renderTable();
    }
  }
  
  window.openProduct = function(idx) {
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
