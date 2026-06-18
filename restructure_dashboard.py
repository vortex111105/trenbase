import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update the sidebar navigation to use onclick events instead of href="#"
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

# Add custom CSS for sections
css = """
    .dash-section { display: none; }
    .dash-section.active-section { display: block; animation: fadeIn 0.3s ease-out; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
"""
if '.dash-section' not in html:
    html = html.replace('</style>', css + '</style>')

# Extract blocks
top_cards_match = re.search(r'(<!-- Top Cards Grid.*?</div>\s*</div>)', html, re.DOTALL)
top_cards = top_cards_match.group(1) if top_cards_match else ""

charts_match = re.search(r'(<!-- Charts Section -->.*?</div>\s*</div>\s*</div>)', html, re.DOTALL)
charts_section = charts_match.group(1) if charts_match else ""

# Extract individual charts
volumen_chart = re.search(r'(<div class="lg:col-span-2 bg-white rounded-\[2rem\] p-6 saas-shadow saas-card-hover">.*?<canvas id="mainChart"></canvas>\s*</div>\s*</div>)', charts_section, re.DOTALL)
donut_chart = re.search(r'(<div class="lg:col-span-1 bg-white rounded-\[2rem\] p-6 saas-shadow saas-card-hover flex flex-col">.*?<canvas id="donutChart"></canvas>.*?</div>\s*</div>)', charts_section, re.DOTALL)

info_match = re.search(r'(<!-- Info Section: Oportunidades & Calculadora ROI -->.*?</div>\s*</div>\s*</div>)', html, re.DOTALL)
info_section = info_match.group(1) if info_match else ""

opps_list = re.search(r'(<!-- Oportunidades List -->.*?</div>\s*</div>)', info_section, re.DOTALL)
roi_calc = re.search(r'(<!-- ROI Calculator -->.*?</div>\s*</div>)', info_section, re.DOTALL)
racha_card = re.search(r'(<!-- Quick Stats / Leaderboard preview -->.*?</div>\s*</div>)', info_section, re.DOTALL)

table_match = re.search(r'(<!-- Products Table -->.*?</div>\s*</div>\s*</div>)', html, re.DOTALL)
table_section = table_match.group(1) if table_match else ""


# Remove original blocks from main
html = html.replace(top_cards, '')
html = html.replace(charts_section, '')
html = html.replace(info_section, '')
html = html.replace(table_section, '')

# Reconstruct Main
new_main_content = f"""
    <!-- DASHBOARD SECTION -->
    <section id="sec-dash" class="dash-section active-section space-y-6">
      {top_cards}
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {volumen_chart.group(1) if volumen_chart else ''}
        {racha_card.group(1) if racha_card else ''}
      </div>
    </section>

    <!-- TENDENCIAS SECTION -->
    <section id="sec-tendencias" class="dash-section space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-2 flex flex-col">
          {table_section.replace('flex-1', 'h-[600px]')} 
        </div>
        <div class="lg:col-span-1 flex flex-col">
          {opps_list.group(1) if opps_list else ''}
        </div>
      </div>
    </section>

    <!-- ANALISIS SECTION -->
    <section id="sec-analisis" class="dash-section space-y-6">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {roi_calc.group(1) if roi_calc else ''}
        {donut_chart.group(1) if donut_chart else ''}
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

# Inject into main after header
header_match = re.search(r'(</header>)', html)
if header_match:
    html = html[:header_match.end()] + new_main_content + html[header_match.end():]

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
