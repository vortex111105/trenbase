import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# We need to extract the parts we want to reuse.
def get_block(regex):
    m = re.search(regex, html, re.DOTALL)
    return m.group(1) if m else ""

top_cards = get_block(r'(<!-- Top Cards Grid \(Skillset Style\) -->\s*<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">.*?<div class="bg-white rounded-3xl p-6 flex flex-col justify-between saas-shadow saas-card-hover h-40">.*?</div>\s*</div>\s*</div>)')
main_chart = get_block(r'(<div class="lg:col-span-2 bg-white rounded-\[2rem\] p-6 saas-shadow saas-card-hover">.*?<canvas id="mainChart"></canvas>\s*</div>\s*</div>)')
donut_chart = get_block(r'(<div class="lg:col-span-1 bg-white rounded-\[2rem\] p-6 saas-shadow saas-card-hover flex flex-col">.*?<canvas id="donutChart"></canvas>.*?</div>\s*</div>)')
opps_list = get_block(r'(<!-- Oportunidades List -->.*?</div>\s*</div>)')
racha = get_block(r'(<!-- Quick Stats / Leaderboard preview -->.*?</div>\s*</div>)')
table_mod = get_block(r'(<!-- Products Table -->\s*<div class="bg-white rounded-\[2rem\] saas-shadow h-\[600px\] flex flex-col overflow-hidden min-h-\[400px\]">.*?</div>\s*</div>\s*</div>)')


# NEW ROI Calc with sliders (Matching original functionality but SaaS style)
roi_calc_sliders = """
      <!-- ROI Calculator -->
      <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover flex flex-col">
        <h3 class="font-bold text-gray-800 mb-6 flex items-center gap-2"><i data-lucide="calculator" class="w-4 h-4 text-gray-500"></i> Calculadora de Rentabilidad</h3>
        <div class="space-y-6 flex-1 flex flex-col">
          <div class="space-y-4">
            <div>
              <div class="flex justify-between text-[11px] font-bold text-gray-500 uppercase tracking-wider mb-1.5">
                <label>Costo de Envío / Base ($)</label>
                <span id="calcCostVal" class="text-gray-900 font-extrabold">$15.00</span>
              </div>
              <input type="range" id="calcCost" oninput="calcROISliders()" min="0" max="100" step="1" value="15" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-black">
            </div>
            <div>
              <div class="flex justify-between text-[11px] font-bold text-gray-500 uppercase tracking-wider mb-1.5">
                <label>CPA / Publicidad ($)</label>
                <span id="calcAdsVal" class="text-gray-900 font-extrabold">$8.00</span>
              </div>
              <input type="range" id="calcAds" oninput="calcROISliders()" min="1" max="100" step="1" value="8" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-black">
            </div>
            <div>
              <div class="flex justify-between text-[11px] font-bold text-gray-500 uppercase tracking-wider mb-1.5">
                <label>Precio de Venta ($)</label>
                <span id="calcPriceVal" class="text-gray-900 font-extrabold">$49.00</span>
              </div>
              <input type="range" id="calcPrice" oninput="calcROISliders()" min="5" max="250" step="1" value="49" class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-black">
            </div>
          </div>
          <div id="calcResult" class="mt-auto bg-gray-50 rounded-xl p-4 border border-gray-100 grid grid-cols-2 gap-2">
            <!-- Injected by JS -->
          </div>
        </div>
      </div>
"""

# NEW Suppliers section
proveedores = """
      <!-- Proveedores VIP -->
      <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover flex flex-col">
        <h3 class="font-bold text-gray-800 mb-6 flex items-center gap-2"><i data-lucide="package" class="w-4 h-4 text-gray-500"></i> Proveedores VIP</h3>
        <div class="space-y-3">
          <div class="bg-gray-50 border border-gray-100 rounded-xl p-3 flex justify-between items-center hover:border-gray-200 transition">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-[#ff4747] flex items-center justify-center text-white font-bold text-xs">Ali</div>
              <div>
                <div class="text-xs font-bold text-gray-900">AliExpress (Choice)</div>
                <div class="text-[10px] text-gray-500">Envío 7-12 días</div>
              </div>
            </div>
            <button class="text-[10px] bg-white border border-gray-200 font-bold px-3 py-1.5 rounded-lg saas-shadow hover:-translate-y-0.5 transition">Ver</button>
          </div>
          <div class="bg-gray-50 border border-gray-100 rounded-xl p-3 flex justify-between items-center hover:border-gray-200 transition">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-lg bg-orange-500 flex items-center justify-center text-white font-bold text-xs">CJ</div>
              <div>
                <div class="text-xs font-bold text-gray-900">CJDropshipping</div>
                <div class="text-[10px] text-gray-500">Agente Privado</div>
              </div>
            </div>
            <button class="text-[10px] bg-white border border-gray-200 font-bold px-3 py-1.5 rounded-lg saas-shadow hover:-translate-y-0.5 transition">Ver</button>
          </div>
        </div>
      </div>
"""

# Reconstruct Sidebar
nav_html = """    <nav class="flex-1 px-4 space-y-2 mt-4" id="sidebarNav">
      <button onclick="showSection('sec-tendencias', this)" class="w-full flex items-center gap-3 px-4 py-3 bg-white/10 text-white rounded-xl font-medium transition nav-btn active-nav">
        <i data-lucide="trending-up" class="w-5 h-5"></i> Tendencias
      </button>
      <button onclick="showSection('sec-analisis', this)" class="w-full flex items-center gap-3 px-4 py-3 text-white/50 hover:text-white hover:bg-white/5 rounded-xl font-medium transition nav-btn">
        <i data-lucide="bar-chart-2" class="w-5 h-5"></i> Análisis
      </button>
      <button onclick="showSection('sec-alertas', this)" class="w-full flex items-center justify-between px-4 py-3 text-white/50 hover:text-white hover:bg-white/5 rounded-xl font-medium transition nav-btn">
        <span class="flex items-center gap-3"><i data-lucide="bell" class="w-5 h-5"></i> Alertas</span>
        <span class="bg-red-500 text-white text-[9px] font-mono px-2 py-0.5 rounded-full">3</span>
      </button>
      <button onclick="showSection('sec-guardados', this)" class="w-full flex items-center justify-between px-4 py-3 text-white/50 hover:text-white hover:bg-white/5 rounded-xl font-medium transition nav-btn">
        <span class="flex items-center gap-3"><i data-lucide="bookmark" class="w-5 h-5"></i> Guardados</span>
        <span class="bg-white/10 text-white text-[9px] font-mono px-2 py-0.5 rounded-full">0</span>
      </button>
      <button onclick="showSection('sec-perfil', this)" class="w-full flex items-center gap-3 px-4 py-3 text-white/50 hover:text-white hover:bg-white/5 rounded-xl font-medium transition nav-btn mt-6 border-t border-white/5 pt-4">
        <i data-lucide="user" class="w-5 h-5"></i> Mi Perfil
      </button>
      <button onclick="showSection('sec-negocio', this)" class="w-full flex items-center gap-3 px-4 py-3 text-white/50 hover:text-white hover:bg-white/5 rounded-xl font-medium transition nav-btn">
        <i data-lucide="briefcase" class="w-5 h-5"></i> Mi Negocio
      </button>
      <a href="index.html" class="flex items-center gap-3 px-4 py-3 text-white/50 hover:text-white hover:bg-white/5 rounded-xl font-medium transition mt-4 border-t border-white/10 pt-4">
        <i data-lucide="home" class="w-5 h-5"></i> Volver al Inicio
      </a>
    </nav>"""

# NEW SPA SECTIONS
spa_html = f"""
    <!-- TENDENCIAS SECTION (HOME) -->
    <section id="sec-tendencias" class="dash-section active-section space-y-6">
      <div class="flex justify-between items-center mb-2">
        <div>
          <h2 class="text-2xl font-extrabold text-gray-900 tracking-tight">Monitoreo de Productos Virales</h2>
          <p class="text-xs text-gray-500 mt-1">Actualizado hace instantes</p>
        </div>
      </div>
      
      <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
        <div class="xl:col-span-2 flex flex-col">
          {table_mod}
        </div>
        <div class="xl:col-span-1 flex flex-col">
          {opps_list}
        </div>
      </div>
    </section>

    <!-- ANALISIS SECTION -->
    <section id="sec-analisis" class="dash-section space-y-6">
      <div class="flex justify-between items-center mb-2">
        <div>
          <h2 class="text-2xl font-extrabold text-gray-900 tracking-tight">Estadísticas y Análisis de Nichos</h2>
          <p class="text-xs text-gray-500 mt-1">Inteligencia de mercado consolidada</p>
        </div>
      </div>
      {top_cards}
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
        {main_chart}
        <div class="flex flex-col gap-6">
          {roi_calc_sliders}
          {proveedores}
        </div>
      </div>
    </section>

    <!-- ALERTAS SECTION -->
    <section id="sec-alertas" class="dash-section space-y-6">
      <div class="flex justify-between items-center mb-2">
        <div>
          <h2 class="text-2xl font-extrabold text-gray-900 tracking-tight">Centro de Alertas</h2>
          <p class="text-xs text-gray-500 mt-1">Monitorea tus nichos</p>
        </div>
      </div>
      <div class="bg-white rounded-[2rem] p-12 saas-shadow flex flex-col items-center justify-center text-center h-[400px]">
        <div class="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mb-4 border border-gray-100">
          <i data-lucide="bell" class="w-8 h-8 text-gray-300"></i>
        </div>
        <h3 class="text-xl font-bold text-gray-800">No tienes alertas activas</h3>
        <p class="text-gray-500 mt-2 text-sm max-w-sm">Configura notificaciones para enterarte cuando un producto de tu nicho supere los 90 TrendScore.</p>
        <button class="mt-6 bg-black text-white px-6 py-2.5 rounded-full text-xs font-bold saas-shadow hover:-translate-y-0.5 transition">Crear Nueva Alerta</button>
      </div>
    </section>

    <!-- GUARDADOS SECTION -->
    <section id="sec-guardados" class="dash-section space-y-6">
      <div class="flex justify-between items-center mb-2">
        <div>
          <h2 class="text-2xl font-extrabold text-gray-900 tracking-tight">Productos Guardados</h2>
          <p class="text-xs text-gray-500 mt-1">Tus favoritos listos para testear</p>
        </div>
      </div>
      <div class="bg-white rounded-[2rem] p-12 saas-shadow flex flex-col items-center justify-center text-center h-[400px]">
        <div class="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mb-4 border border-gray-100">
          <i data-lucide="bookmark" class="w-8 h-8 text-gray-300"></i>
        </div>
        <h3 class="text-xl font-bold text-gray-800">Lista vacía</h3>
        <p class="text-gray-500 mt-2 text-sm max-w-sm">Explora Tendencias y guarda los productos que te llamen la atención.</p>
        <button onclick="showSection('sec-tendencias', document.querySelector('#sidebarNav button:nth-child(1)'))" class="mt-6 bg-black text-white px-6 py-2.5 rounded-full text-xs font-bold saas-shadow hover:-translate-y-0.5 transition">Explorar Tendencias</button>
      </div>
    </section>

    <!-- PERFIL SECTION -->
    <section id="sec-perfil" class="dash-section space-y-6">
      <div class="flex justify-between items-center mb-2">
        <div>
          <h2 class="text-2xl font-extrabold text-gray-900 tracking-tight">Mi Perfil</h2>
          <p class="text-xs text-gray-500 mt-1">Ajustes de cuenta</p>
        </div>
      </div>
      <div class="bg-white rounded-[2rem] p-8 saas-shadow max-w-3xl">
        <div class="flex items-center gap-6 mb-8 border-b border-gray-100 pb-8">
          <div class="w-20 h-20 bg-gray-900 rounded-full flex items-center justify-center text-white text-3xl font-bold">N</div>
          <div>
            <h3 class="text-xl font-bold text-gray-900">Nacho Frag</h3>
            <p class="text-sm text-gray-500">nachofrag@trendbase.com</p>
            <div class="mt-2 inline-block bg-black text-white text-[10px] font-bold px-2 py-1 rounded-md uppercase tracking-wider">Plan Pro</div>
          </div>
        </div>
        <div class="space-y-6">
          <button class="w-full bg-gray-50 hover:bg-gray-100 text-left px-6 py-4 rounded-xl border border-gray-200 font-bold text-gray-800 transition flex justify-between items-center">
            Facturación y Suscripción <i data-lucide="chevron-right" class="w-4 h-4 text-gray-400"></i>
          </button>
          <button class="w-full bg-gray-50 hover:bg-gray-100 text-left px-6 py-4 rounded-xl border border-gray-200 font-bold text-gray-800 transition flex justify-between items-center">
            Cambiar Contraseña <i data-lucide="chevron-right" class="w-4 h-4 text-gray-400"></i>
          </button>
        </div>
      </div>
    </section>

    <!-- NEGOCIO SECTION -->
    <section id="sec-negocio" class="dash-section space-y-6">
      <div class="flex justify-between items-center mb-2">
        <div>
          <h2 class="text-2xl font-extrabold text-gray-900 tracking-tight">Mi Negocio</h2>
          <p class="text-xs text-gray-500 mt-1">Registra tus ventas y sube de nivel</p>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        {racha}
        <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover flex flex-col justify-center items-center text-center">
          <div class="w-16 h-16 bg-green-50 rounded-full flex items-center justify-center mb-4 border border-green-100">
            <i data-lucide="plus" class="w-8 h-8 text-green-500"></i>
          </div>
          <h3 class="font-bold text-gray-800">Registrar Venta</h3>
          <p class="text-[11px] text-gray-500 mt-2 max-w-[200px]">Añade tus resultados para llevar un control preciso de tus ganancias.</p>
          <button class="mt-4 bg-green-500 text-white px-6 py-2.5 rounded-full text-xs font-bold saas-shadow hover:-translate-y-0.5 transition">Nueva Venta</button>
        </div>
      </div>
    </section>
"""

# Replace navigation
html = re.sub(r'<nav class="flex-1 px-4 space-y-2 mt-4" id="sidebarNav">.*?</nav>', nav_html, html, flags=re.DOTALL)

# Clear old main content
html = re.sub(r'(<!-- DASHBOARD SECTION -->.*?</section>)', '', html, flags=re.DOTALL)
html = re.sub(r'(<!-- TENDENCIAS SECTION -->.*?</section>)', '', html, flags=re.DOTALL)
html = re.sub(r'(<!-- ANALISIS SECTION -->.*?</section>)', '', html, flags=re.DOTALL)
html = re.sub(r'(<!-- ALERTAS SECTION -->.*?</section>)', '', html, flags=re.DOTALL)

# Inject new SPA HTML right after the <header> tag
header_match = re.search(r'(</header>)', html)
if header_match:
    html = html[:header_match.end()] + "\n" + spa_html + html[header_match.end():]

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Now update app.js for slider functionality
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

calc_sliders_js = """
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
"""

if 'window.calcROISliders =' not in js:
    js = js.replace('window.calcROI = function()', calc_sliders_js + '\n  window.calcROI = function()')

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
