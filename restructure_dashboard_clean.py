import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make sure we don't duplicate
if '<!-- DASHBOARD SECTION -->' in html:
    print("Already transformed!")
    exit()

nav_html = """    <nav class="flex-1 px-4 space-y-2 mt-4" id="sidebarNav">
      <button onclick="showSection('sec-dash', this)" class="w-full flex items-center gap-3 px-4 py-3 bg-white/10 text-white rounded-xl font-medium transition nav-btn active-nav">
        <i data-lucide="layout-dashboard" class="w-5 h-5"></i> Dashboard
      </button>
      <button onclick="showSection('sec-tendencias', this)" class="w-full flex items-center gap-3 px-4 py-3 text-white/50 hover:text-white hover:bg-white/5 rounded-xl font-medium transition nav-btn">
        <i data-lucide="trending-up" class="w-5 h-5"></i> Tendencias
      </button>
      <button onclick="showSection('sec-analisis', this)" class="w-full flex items-center gap-3 px-4 py-3 text-white/50 hover:text-white hover:bg-white/5 rounded-xl font-medium transition nav-btn">
        <i data-lucide="bar-chart-2" class="w-5 h-5"></i> Análisis
      </button>
      <button onclick="showSection('sec-alertas', this)" class="w-full flex items-center gap-3 px-4 py-3 text-white/50 hover:text-white hover:bg-white/5 rounded-xl font-medium transition nav-btn">
        <i data-lucide="bell" class="w-5 h-5"></i> Alertas
      </button>
      <a href="index.html" class="flex items-center gap-3 px-4 py-3 text-white/50 hover:text-white hover:bg-white/5 rounded-xl font-medium transition mt-4 border-t border-white/10 pt-4">
        <i data-lucide="home" class="w-5 h-5"></i> Volver al Inicio
      </a>
    </nav>"""
html = re.sub(r'<nav class="flex-1 px-4 space-y-2 mt-4">.*?</nav>', nav_html, html, flags=re.DOTALL)

css = """
    .dash-section { display: none; }
    .dash-section.active-section { display: block; animation: fadeIn 0.3s ease-out; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
"""
if '.dash-section' not in html:
    html = html.replace('</style>', css + '</style>')

def get_block(regex):
    m = re.search(regex, html, re.DOTALL)
    return m.group(1) if m else ""

top_cards = get_block(r'(<!-- Top Cards Grid \(Skillset Style\) -->.*?</div>\s*</div>\s*</div>\s*</div>\s*</div>)')
# Safer extraction
top_cards_match = re.search(r'(<!-- Top Cards Grid \(Skillset Style\) -->\s*<div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">.*?<div class="bg-white rounded-3xl p-6 flex flex-col justify-between saas-shadow saas-card-hover h-40">.*?</div>\s*</div>\s*</div>)', html, re.DOTALL)
top_cards = top_cards_match.group(1) if top_cards_match else ""

main_chart_match = re.search(r'(<div class="lg:col-span-2 bg-white rounded-\[2rem\] p-6 saas-shadow saas-card-hover">.*?<canvas id="mainChart"></canvas>\s*</div>\s*</div>)', html, re.DOTALL)
main_chart = main_chart_match.group(1) if main_chart_match else ""

donut_chart_match = re.search(r'(<div class="lg:col-span-1 bg-white rounded-\[2rem\] p-6 saas-shadow saas-card-hover flex flex-col">.*?<canvas id="donutChart"></canvas>.*?</div>\s*</div>)', html, re.DOTALL)
donut_chart = donut_chart_match.group(1) if donut_chart_match else ""

table_match = re.search(r'(<!-- Products Table -->\s*<div class="bg-white rounded-\[2rem\] saas-shadow flex-1 flex flex-col overflow-hidden min-h-\[400px\]">.*?</div>\s*</div>\s*</div>)', html, re.DOTALL)
table = table_match.group(1) if table_match else ""
table_mod = table.replace('flex-1', 'h-[600px]') if table else ""


opps_list = """
      <!-- Oportunidades List -->
      <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover flex flex-col">
        <div class="flex justify-between items-center mb-6">
          <h3 class="font-bold text-gray-800">Top Oportunidades</h3>
          <span class="text-[10px] font-bold text-green-600 bg-green-50 px-2 py-1 rounded-md uppercase tracking-wider">Alta Rentabilidad</span>
        </div>
        <div id="oppList" class="flex flex-col gap-3 flex-1">
          <div class="text-sm text-gray-400 text-center py-4 font-medium">Cargando oportunidades...</div>
        </div>
      </div>
"""

roi_calc = """
      <!-- ROI Calculator -->
      <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover flex flex-col">
        <h3 class="font-bold text-gray-800 mb-6 flex items-center gap-2"><i data-lucide="calculator" class="w-4 h-4 text-gray-500"></i> Calculadora ROI</h3>
        <div class="space-y-4 flex-1 flex flex-col">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-[11px] font-bold text-gray-500 uppercase tracking-wider mb-1.5">Costo Base ($)</label>
              <input type="number" id="calcCost" value="15" oninput="calcROI()" class="w-full bg-gray-50 border border-gray-200 rounded-xl px-3 py-2 text-sm font-bold text-gray-900 outline-none focus:border-gray-400 transition">
            </div>
            <div>
              <label class="block text-[11px] font-bold text-gray-500 uppercase tracking-wider mb-1.5">Precio Venta ($)</label>
              <input type="number" id="calcPrice" value="49" oninput="calcROI()" class="w-full bg-gray-50 border border-gray-200 rounded-xl px-3 py-2 text-sm font-bold text-gray-900 outline-none focus:border-gray-400 transition">
            </div>
            <div>
              <label class="block text-[11px] font-bold text-gray-500 uppercase tracking-wider mb-1.5">Costo Ads/venta</label>
              <input type="number" id="calcAds" value="8" oninput="calcROI()" class="w-full bg-gray-50 border border-gray-200 rounded-xl px-3 py-2 text-sm font-bold text-gray-900 outline-none focus:border-gray-400 transition">
            </div>
            <div>
              <label class="block text-[11px] font-bold text-gray-500 uppercase tracking-wider mb-1.5">Ventas/mes est.</label>
              <input type="number" id="calcSales" value="50" oninput="calcROI()" class="w-full bg-gray-50 border border-gray-200 rounded-xl px-3 py-2 text-sm font-bold text-gray-900 outline-none focus:border-gray-400 transition">
            </div>
          </div>
          <div id="calcResult" class="mt-auto bg-gray-50 rounded-xl p-4 border border-gray-100 flex flex-col gap-2"></div>
        </div>
      </div>
"""

racha = """
      <!-- Quick Stats / Leaderboard preview -->
      <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover flex flex-col">
        <h3 class="font-bold text-gray-800 mb-6 flex items-center gap-2"><i data-lucide="award" class="w-4 h-4 text-gray-500"></i> Tu Racha</h3>
        <div class="flex-1 flex flex-col items-center justify-center text-center space-y-4">
          <div class="w-20 h-20 rounded-full border-4 border-gray-100 flex items-center justify-center shadow-inner relative">
            <span class="text-3xl">🔥</span>
            <div class="absolute -bottom-2 bg-black text-white text-[10px] font-bold px-2 py-0.5 rounded-full">NIVEL 1</div>
          </div>
          <div>
            <div class="text-3xl font-extrabold text-gray-900">0 Ventas</div>
            <div class="text-xs font-medium text-gray-500 mt-1">Registradas este mes</div>
          </div>
          <div class="w-full bg-gray-100 h-2 rounded-full mt-2">
            <div class="bg-black h-full rounded-full" style="width: 10%"></div>
          </div>
          <div class="text-[10px] text-gray-400 font-bold uppercase tracking-widest mt-1">10 ventas para Nivel 2</div>
        </div>
      </div>
"""

# Remove old chunks
if top_cards: html = html.replace(top_cards, '')
if main_chart: html = html.replace(main_chart, '')
if donut_chart: html = html.replace(donut_chart, '')
if table: html = html.replace(table, '')

# Also remove the wrapper for charts section if it exists
html = re.sub(r'<!-- Charts Section -->\s*<div class="grid grid-cols-1 lg:grid-cols-3 gap-6">\s*</div>', '', html, flags=re.DOTALL)


spa_html = f"""
    <!-- DASHBOARD SECTION -->
    <section id="sec-dash" class="dash-section active-section space-y-6">
      {top_cards}
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {main_chart}
        {racha}
      </div>
    </section>

    <!-- TENDENCIAS SECTION -->
    <section id="sec-tendencias" class="dash-section space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 flex flex-col">
          {table_mod}
        </div>
        <div class="lg:col-span-1 flex flex-col">
          <div class="grid grid-cols-1 gap-6">
            {opps_list}
          </div>
        </div>
      </div>
    </section>

    <!-- ANALISIS SECTION -->
    <section id="sec-analisis" class="dash-section space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {roi_calc}
        {donut_chart}
      </div>
    </section>

    <!-- ALERTAS SECTION -->
    <section id="sec-alertas" class="dash-section space-y-6">
      <div class="bg-white rounded-[2rem] p-12 saas-shadow flex flex-col items-center justify-center text-center h-[400px]">
        <div class="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mb-4 border border-gray-100">
          <i data-lucide="bell" class="w-8 h-8 text-gray-300"></i>
        </div>
        <h3 class="text-xl font-bold text-gray-800">No tienes alertas activas</h3>
        <p class="text-gray-500 mt-2 text-sm max-w-sm">Configura notificaciones para enterarte cuando un producto de tu nicho supere los 90 TrendScore.</p>
        <button class="mt-6 bg-black text-white px-6 py-2.5 rounded-full text-xs font-bold saas-shadow hover:-translate-y-0.5 transition">Crear Nueva Alerta</button>
      </div>
    </section>
"""

# Insert spa_html inside <main> right after </header>
header_match = re.search(r'(</header>)', html)
if header_match:
    html = html[:header_match.end()] + "\n" + spa_html + html[header_match.end():]

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
