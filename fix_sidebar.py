import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove the "ceja negra" (border-t-8 border-t-gray-900)
html = html.replace(' border-t-8 border-t-gray-900', '')

# 2. Update Sidebar HTML
# Extract sidebar
sidebar_match = re.search(r'<!-- Sidebar -->\s*<aside class=".*?</aside>', html, flags=re.DOTALL)
if sidebar_match:
    old_sidebar = sidebar_match.group(0)
    
    new_sidebar = """<!-- Sidebar -->
  <aside class="group w-[88px] hover:w-64 transition-all duration-300 ease-in-out bg-sidebar text-white flex flex-col m-3 rounded-[2rem] shadow-2xl relative z-20 overflow-hidden">
    <a href="index.html" class="p-7 pb-6 flex items-center hover:opacity-80 transition cursor-pointer overflow-hidden whitespace-nowrap">
      <div class="w-8 h-8 flex-shrink-0 bg-white rounded-lg flex items-center justify-center">
        <i data-lucide="zap" class="w-5 h-5 text-black"></i>
      </div>
      <h1 class="text-xl font-bold tracking-tight opacity-0 w-0 group-hover:opacity-100 group-hover:w-auto transition-all duration-300 group-hover:ml-3">TrendBase</h1>
    </a>
    
    <nav class="flex-1 px-4 space-y-2 mt-4" id="sidebarNav">
      <button onclick="showSection('sec-tendencias', this)" class="w-full flex items-center px-4 py-3 bg-white/10 text-white rounded-xl font-medium transition nav-btn active-nav overflow-hidden whitespace-nowrap">
        <i data-lucide="trending-up" class="w-5 h-5 flex-shrink-0"></i> 
        <span class="opacity-0 w-0 group-hover:opacity-100 group-hover:w-auto transition-all duration-300 group-hover:ml-3">Tendencias</span>
      </button>
      <button onclick="showSection('sec-analisis', this)" class="w-full flex items-center px-4 py-3 text-white/50 hover:text-white hover:bg-white/5 rounded-xl font-medium transition nav-btn overflow-hidden whitespace-nowrap">
        <i data-lucide="bar-chart-2" class="w-5 h-5 flex-shrink-0"></i> 
        <span class="opacity-0 w-0 group-hover:opacity-100 group-hover:w-auto transition-all duration-300 group-hover:ml-3">Análisis</span>
      </button>
      <button onclick="showSection('sec-alertas', this)" class="w-full flex items-center px-4 py-3 text-white/50 hover:text-white hover:bg-white/5 rounded-xl font-medium transition nav-btn overflow-hidden whitespace-nowrap">
        <i data-lucide="bell" class="w-5 h-5 flex-shrink-0"></i>
        <div class="flex items-center justify-between opacity-0 w-0 group-hover:opacity-100 group-hover:w-full transition-all duration-300 group-hover:ml-3">
          <span>Alertas</span>
          <span class="bg-red-500 text-white text-[9px] font-mono px-2 py-0.5 rounded-full">3</span>
        </div>
      </button>
      <button onclick="showSection('sec-guardados', this)" class="w-full flex items-center px-4 py-3 text-white/50 hover:text-white hover:bg-white/5 rounded-xl font-medium transition nav-btn overflow-hidden whitespace-nowrap">
        <i data-lucide="bookmark" class="w-5 h-5 flex-shrink-0"></i>
        <div class="flex items-center justify-between opacity-0 w-0 group-hover:opacity-100 group-hover:w-full transition-all duration-300 group-hover:ml-3">
          <span>Guardados</span>
          <span class="bg-white/10 text-white text-[9px] font-mono px-2 py-0.5 rounded-full">0</span>
        </div>
      </button>
      <button onclick="showSection('sec-perfil', this)" class="w-full flex items-center px-4 py-3 text-white/50 hover:text-white hover:bg-white/5 rounded-xl font-medium transition nav-btn mt-6 border-t border-white/5 pt-4 overflow-hidden whitespace-nowrap">
        <i data-lucide="user" class="w-5 h-5 flex-shrink-0"></i> 
        <span class="opacity-0 w-0 group-hover:opacity-100 group-hover:w-auto transition-all duration-300 group-hover:ml-3">Mi Perfil</span>
      </button>
      <button onclick="showSection('sec-negocio', this)" class="w-full flex items-center px-4 py-3 text-white/50 hover:text-white hover:bg-white/5 rounded-xl font-medium transition nav-btn overflow-hidden whitespace-nowrap">
        <i data-lucide="briefcase" class="w-5 h-5 flex-shrink-0"></i> 
        <span class="opacity-0 w-0 group-hover:opacity-100 group-hover:w-auto transition-all duration-300 group-hover:ml-3">Mi Negocio</span>
      </button>
      <a href="index.html" class="flex items-center px-4 py-3 text-white/50 hover:text-white hover:bg-white/5 rounded-xl font-medium transition mt-4 border-t border-white/10 pt-4 overflow-hidden whitespace-nowrap">
        <i data-lucide="home" class="w-5 h-5 flex-shrink-0"></i> 
        <span class="opacity-0 w-0 group-hover:opacity-100 group-hover:w-auto transition-all duration-300 group-hover:ml-3">Volver al Inicio</span>
      </a>
    </nav>
    
    <!-- Upgrade Pro Banner inside sidebar -->
    <div class="p-6 mt-auto overflow-hidden whitespace-nowrap">
      <div class="bg-white/5 border border-white/10 rounded-2xl p-4 text-center transition-all duration-300">
        <div class="opacity-0 w-0 group-hover:opacity-100 group-hover:w-auto transition-all duration-300">
          <p class="text-[10px] text-white/60 mb-3 font-medium">Obtén métricas avanzadas y proveedores exclusivos.</p>
          <button class="w-full bg-white text-black py-2 rounded-xl text-xs font-bold hover:bg-gray-200 transition">Upgrade Pro</button>
        </div>
        <div class="group-hover:opacity-0 group-hover:w-0 transition-all duration-300 w-auto opacity-100 text-center">
          <i data-lucide="star" class="w-5 h-5 text-champagne mx-auto"></i>
        </div>
      </div>
    </div>
  </aside>"""
    
    html = html.replace(old_sidebar, new_sidebar)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Sidebar collapsed and eyebrow removed!")
