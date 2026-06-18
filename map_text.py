def inject_real_content():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. LANDING PAGE REPLACEMENTS
    html = html.replace('TrendBase Overview', 'TrendBase')
    html = html.replace('Domina el E-Commerce con precisión absoluta.', 'Inteligencia Artificial para E-commerce & Dropshipping.')
    html = html.replace('Descubre productos virales antes de que saturen, conéctalos a tu tienda y visualiza tus ganancias en un solo workspace increíblemente hermoso.', 'Encuentra productos virales, espía los anuncios de tu competencia, conecta tu tienda y calcula el ROI de tus campañas antes de invertir un solo dólar.')
    html = html.replace('Detección Virales', 'Detección Temprana')
    html = html.replace('24/7', '24/7')
    html = html.replace('Escaneo de patrones de crecimiento antes de la competencia.', 'Escaneo de patrones de crecimiento en TikTok, Instagram y AliExpress.')
    html = html.replace('Control Financiero', 'Calculadora ROI')
    html = html.replace('Mide tu retorno exacto cruzando ventas reales con gastos.', 'Calcula el margen de ganancia, CPA máximo y punto de equilibrio.')
    
    # Let's map the Dashboard Sidebar items to have the IDs the JS needs!
    # The original JS looks for: onclick="goSection('tendencias')", etc.
    # We will replace the showView('dashboard') with the real JS calls.
    
    # The original sidebar had:
    # id="btn-resumen" onclick="goSection('resumen')"
    # id="btn-tendencias" onclick="goSection('tendencias')"
    # id="btn-analisis" onclick="goSection('analisis')"
    # id="btn-alertas" onclick="goSection('alertas')"
    # id="btn-guardados" onclick="goSection('guardados')"
    # id="btn-perfil" onclick="goSection('perfil')"
    
    html = html.replace('<button onclick="showView(\'dashboard\')" id="nav-dash" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl sidebar-item active">', '<button onclick="goSection(\'tendencias\')" id="btn-tendencias" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl sidebar-item active">')
    html = html.replace('<button onclick="showView(\'products\')" id="nav-tendencias" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl sidebar-item">', '<button onclick="goSection(\'analisis\')" id="btn-analisis" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl sidebar-item">')
    
    # Dashboard Overview Header mapping
    html = html.replace('Dashboard Overview', 'Monitoreo de Productos Virales')
    html = html.replace('<span class="text-[--text-dark] font-medium tracking-tight hidden md:block">Monday, Oct 23, 10:09 AM</span>', '<p class="text-xs text-[--text-muted] mt-1" id="freshness">Actualizado hace instantes</p>')

    # Ensure the dashboard has the right ID for the JS to target
    html = html.replace('<main id="view-dashboard" class="flex-1 p-8 md:p-10 overflow-y-auto block relative z-10">', '<main id="sec-tendencias" class="dash-section flex-1 p-8 md:p-10 overflow-y-auto block relative z-10">')
    
    # We need to insert the productGrid div into the dashboard so JS can populate it!
    # The dashboard in TrendBase_Vision.html has a 3-card layout, let's keep it as the TOP metrics, and then put the product grid below it!
    
    grid_injection = """
            <!-- Búsqueda y Filtros Reales -->
            <div class="flex flex-col md:flex-row items-center gap-4 mb-6 mt-8">
              <div class="flex items-center bg-[rgba(255,255,255,0.4)] rounded-xl border border-white/50 p-1 shadow-sm backdrop-blur-md">
                <button onclick="setBusinessMode('dropshipping')" id="mode-drop" class="px-4 py-2 rounded-lg text-xs font-bold transition bg-white text-[--text-dark] shadow-sm">Dropshipping</button>
                <button onclick="setBusinessMode('ecommerce')" id="mode-ecom" class="px-4 py-2 rounded-lg text-xs font-bold transition text-[--text-muted] hover:text-[--text-dark]">Marca Propia</button>
              </div>

              <div class="relative flex-1 md:flex-none">
                <i data-lucide="search" class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[--text-muted]"></i>
                <input id="productSearch" type="text" placeholder="Buscar producto..." oninput="searchProducts(this.value)" class="w-full md:w-64 bg-[rgba(255,255,255,0.4)] border border-white/50 rounded-xl pl-10 pr-4 py-2.5 text-sm font-medium text-[--text-dark] placeholder-[--text-muted] outline-none focus:border-[rgba(0,0,0,0.2)] transition shadow-sm backdrop-blur-md">
              </div>
            </div>

            <!-- GRILLA DE PRODUCTOS REAL -->
            <div id="productGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"></div>
"""

    # We inject the grid exactly after the 4 fake cards in the desktop file
    # The 4 fake cards end before the "TENDENCIAS GLOBALES" section or before the closing of main.
    
    # We will just append the grid inside the <main id="sec-tendencias">
    html = html.replace('<!-- ========================================== -->\n        <!-- DASHBOARD VIEW (EXACT IMAGE REPLICA)       -->', '<!-- ========================================== -->\n        <!-- DASHBOARD VIEW (REAL JS INTEGRATED)        -->')
    
    # Find the end of the top 4 cards grid. The div is `<div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8 relative z-10">`
    # Let's just append the productGrid after `<div class="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-6">` ... wait, let's inject it into `TrendBase_Vision.html`
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    inject_real_content()
