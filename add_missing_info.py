import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

def get_block(regex):
    m = re.search(regex, html, re.DOTALL)
    return m.group(1) if m else ""

# 1. ADD SIDEBAR CATEGORIES & PLATFORMS
sidebar_nav_pattern = r'(<nav class="flex-1 px-4 space-y-2 mt-4" id="sidebarNav">.*?</nav>)'
sidebar_extra = """
    <div class="px-4 pt-6 border-t border-white/10 mt-2">
      <button onclick="toggleSidebarMenu('cat-list', 'cat-icon')" class="w-full flex justify-between items-center text-[10px] font-bold text-white/50 hover:text-white uppercase tracking-widest px-3 mb-2 transition">
        <span>Categorías</span>
        <i id="cat-icon" data-lucide="chevron-down" class="w-3 h-3 transition-transform duration-300"></i>
      </button>
      <div id="cat-list" class="space-y-1">
        <button class="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium text-white/60 hover:text-white hover:bg-white/5 transition"><i data-lucide="grid" class="w-3.5 h-3.5"></i> Todas</button>
        <button class="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium text-white/60 hover:text-white hover:bg-white/5 transition"><i data-lucide="laptop" class="w-3.5 h-3.5"></i> Tecnología</button>
        <button class="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium text-white/60 hover:text-white hover:bg-white/5 transition"><i data-lucide="sparkles" class="w-3.5 h-3.5"></i> Belleza</button>
        <button class="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium text-white/60 hover:text-white hover:bg-white/5 transition"><i data-lucide="home" class="w-3.5 h-3.5"></i> Hogar</button>
      </div>
    </div>

    <div class="px-4 pt-6 border-t border-white/10 mt-4">
      <button onclick="toggleSidebarMenu('plat-list', 'plat-icon')" class="w-full flex justify-between items-center text-[10px] font-bold text-white/50 hover:text-white uppercase tracking-widest px-3 mb-2 transition">
        <span>Plataformas</span>
        <i id="plat-icon" data-lucide="chevron-down" class="w-3 h-3 transition-transform duration-300"></i>
      </button>
      <div id="plat-list" class="space-y-1 hidden">
        <button class="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium text-white/60 hover:text-white hover:bg-white/5 transition"><i data-lucide="video" class="w-3.5 h-3.5"></i> TikTok</button>
        <button class="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium text-white/60 hover:text-white hover:bg-white/5 transition"><i data-lucide="camera" class="w-3.5 h-3.5"></i> Instagram</button>
        <button class="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium text-white/60 hover:text-white hover:bg-white/5 transition"><i data-lucide="shopping-cart" class="w-3.5 h-3.5"></i> Amazon</button>
      </div>
    </div>
"""

if 'Categorías' not in get_block(sidebar_nav_pattern) and 'Categorías' not in html:
    html = re.sub(sidebar_nav_pattern, r'\1\n' + sidebar_extra, html, flags=re.DOTALL)


# 2. ADD TENDENCIAS FILTERS
tendencias_header_pattern = r'(<h2 class="text-2xl font-extrabold text-gray-900 tracking-tight">Monitoreo de Productos Virales</h2>\s*<p class="text-xs text-gray-500 mt-1">Actualizado hace instantes</p>\s*</div>)'
tendencias_filters = """
        <div class="flex items-center gap-2 flex-wrap mt-4 xl:mt-0">
          <div class="flex items-center bg-gray-100 rounded-xl border border-gray-200 p-1">
            <button class="px-3 py-1.5 rounded-lg text-[10px] font-bold transition bg-white text-gray-900 saas-shadow">Dropshipping</button>
            <button class="px-3 py-1.5 rounded-lg text-[10px] font-bold transition text-gray-500 hover:text-gray-900">Marca Propia</button>
          </div>
          <div class="relative">
            <i data-lucide="search" class="absolute left-3 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-gray-400 pointer-events-none"></i>
            <input type="text" placeholder="Buscar producto..." class="bg-white border border-gray-200 rounded-xl pl-8 pr-4 py-2 text-xs font-medium text-gray-900 placeholder-gray-400 outline-none focus:border-gray-400 transition w-44 saas-shadow-sm">
          </div>
          <select class="bg-white border border-gray-200 rounded-xl px-4 py-2 text-xs font-bold text-gray-700 outline-none focus:border-gray-400 saas-shadow-sm">
            <option value="">Región (Todas)</option>
            <option value="AR">🇦🇷 Argentina</option>
            <option value="UY">🇺🇾 Uruguay</option>
            <option value="CL">🇨🇱 Chile</option>
          </select>
          <select class="bg-white border border-gray-200 rounded-xl px-4 py-2 text-xs font-bold text-gray-700 outline-none focus:border-gray-400 saas-shadow-sm">
            <option value="score">TrendScore</option>
            <option value="change">Crecimiento</option>
            <option value="margin">Margen</option>
          </select>
        </div>
"""
if 'Región (Todas)' not in html:
    html = re.sub(tendencias_header_pattern, r'\1\n' + tendencias_filters, html)

# 3. ADD ANALISIS FILTERS
analisis_header_pattern = r'(<h2 class="text-2xl font-extrabold text-gray-900 tracking-tight">Estadísticas y Análisis de Nichos</h2>\s*<p class="text-xs text-gray-500 mt-1">Inteligencia de mercado consolidada</p>\s*</div>)'
analisis_filters = """
        <div class="flex flex-col sm:flex-row items-end sm:items-center gap-3 mt-4 lg:mt-0">
          <button class="flex items-center gap-2 bg-black text-white px-3 py-1.5 rounded-xl text-[10px] font-bold uppercase transition saas-shadow hover:-translate-y-0.5">
            <i data-lucide="download" class="w-3.5 h-3.5"></i> Exportar
          </button>
          <div class="flex items-center border border-gray-200 rounded-xl bg-gray-100 p-1">
            <button class="px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase transition text-gray-500 hover:text-gray-900">7 Días</button>
            <button class="px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase transition bg-white text-gray-900 saas-shadow">30 Días</button>
            <button class="px-3 py-1.5 rounded-lg text-[10px] font-bold uppercase transition text-gray-500 hover:text-gray-900">90 Días</button>
          </div>
        </div>
"""
if 'Exportar' not in html:
    html = re.sub(analisis_header_pattern, r'\1\n' + analisis_filters, html)

# 4. ADD VOLUMEN DE TENDENCIAS HISTORY TABLE AND SELECTOR
volumen_pattern = r'(<h3 class="font-bold text-gray-800">Volumen de Tendencias \(Últimos 6 meses\)</h3>\s*<select class="bg-gray-50 border border-gray-200 rounded-lg px-3 py-1.5 text-xs font-medium text-gray-600 outline-none">\s*<option>Todas las categorías</option>\s*</select>\s*</div>\s*<div class="h-64 w-full">\s*<canvas id="mainChart"></canvas>\s*</div>)'
volumen_extra = """
          <div class="overflow-x-auto rounded-xl border border-gray-100 mt-6">
            <table class="w-full text-xs font-mono text-gray-500 text-left">
              <thead>
                <tr class="bg-gray-50 border-b border-gray-100 text-gray-400">
                  <th class="p-3 uppercase font-bold">Semana</th>
                  <th class="p-3 uppercase font-bold">Score</th>
                  <th class="p-3 uppercase font-bold">Cambio</th>
                  <th class="p-3 uppercase font-bold">País líder</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100 bg-white">
                <tr><td class="p-3 font-bold text-gray-900">Esta Semana</td><td class="p-3">94</td><td class="p-3 text-green-500">+12%</td><td class="p-3">🇺🇾 UY</td></tr>
                <tr><td class="p-3 font-bold text-gray-900">Semana Pasada</td><td class="p-3">82</td><td class="p-3 text-green-500">+5%</td><td class="p-3">🇦🇷 AR</td></tr>
                <tr><td class="p-3 font-bold text-gray-900">Hace 2 Semanas</td><td class="p-3">77</td><td class="p-3 text-gray-400">0%</td><td class="p-3">🇨🇱 CL</td></tr>
              </tbody>
            </table>
          </div>
"""
if 'Esta Semana' not in html:
    html = re.sub(volumen_pattern, r'\1' + volumen_extra, html)


# 5. MOBILE NAV BAR
mobile_nav = """
    <!-- Mobile Navigation Bar -->
    <div id="mobileNav" class="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-white/90 backdrop-blur-md border-t border-gray-100 flex items-center justify-around py-3 px-2 saas-shadow-up">
      <button onclick="showSection('sec-tendencias', null)" class="flex flex-col items-center gap-1 text-[10px] font-bold text-black"><i data-lucide="flame" class="w-5 h-5"></i>Inicio</button>
      <button onclick="showSection('sec-analisis', null)" class="flex flex-col items-center gap-1 text-[10px] font-bold text-gray-400 hover:text-black transition"><i data-lucide="bar-chart-2" class="w-5 h-5"></i>Análisis</button>
      <button onclick="showSection('sec-guardados', null)" class="flex flex-col items-center gap-1 text-[10px] font-bold text-gray-400 hover:text-black transition"><i data-lucide="bookmark" class="w-5 h-5"></i>Guardados</button>
      <button onclick="showSection('sec-perfil', null)" class="flex flex-col items-center gap-1 text-[10px] font-bold text-gray-400 hover:text-black transition"><i data-lucide="user" class="w-5 h-5"></i>Perfil</button>
      <button onclick="showSection('sec-negocio', null)" class="flex flex-col items-center gap-1 text-[10px] font-bold text-gray-400 hover:text-black transition"><i data-lucide="briefcase" class="w-5 h-5"></i>Negocio</button>
    </div>
"""
if 'mobileNav' not in html:
    html = html.replace('</main>', '</main>\n' + mobile_nav)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
