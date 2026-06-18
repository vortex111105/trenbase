def map_vision_os():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Landing Page Texts
    html = html.replace('Domina el E-Commerce <br/>', 'Inteligencia Artificial para <br/>')
    html = html.replace('<span class="text-transparent bg-clip-text bg-gradient-to-r from-[--text-primary] to-[--text-secondary]">con precisión absoluta.</span>', '<span class="text-transparent bg-clip-text bg-gradient-to-r from-[--text-primary] to-[--text-secondary]">E-Commerce & Dropshipping.</span>')
    html = html.replace('Descubre productos virales antes de que saturen, conéctalos a tu tienda y visualiza todas tus ganancias en un solo workspace increíblemente hermoso.', 'Encuentra productos virales, espía los anuncios de tu competencia, conecta tu tienda y calcula el ROI de tus campañas antes de invertir un solo dólar.')
    
    html = html.replace('Detección de Virales', 'Detección Temprana')
    html = html.replace('Nuestros algoritmos escanean redes 24/7 buscando patrones de crecimiento antes de la competencia los vea.', 'Escaneo de patrones de crecimiento en TikTok, Instagram y AliExpress antes de la competencia.')
    
    html = html.replace('Control Financiero', 'Calculadora ROI')
    html = html.replace('Conecta tu tienda. Mide tu ROI exacto en automático cruzando ventas reales con gastos de publicidad.', 'Calcula el margen de ganancia real de un producto, CPA máximo y punto de equilibrio.')
    
    # 2. Append Javascript Engine
    with open('original_index.html', 'r', encoding='utf-8') as f:
        orig = f.read()
    
    js_start = orig.find('<!-- MODALES DE LA APLICACIÓN -->')
    if js_start == -1:
        js_start = orig.find('<script>')
        
    js_content = orig[js_start:]
    
    # Add an ID to the Main tag so we can hide/show the landing page
    html = html.replace('<main class="relative z-10 pt-48 pb-20 px-6">', '<main id="sec-landing" class="dash-section block relative z-10 pt-48 pb-20 px-6">')
    
    # Let's insert the Dashboard sections before the end of the <main> block... 
    # Actually, the original JS toggles "dash-section" classes. So we need multiple <main> or <section> blocks at the same level.
    # The current structure is <main> ... </main> <footer> ... </footer>
    
    dashboard_html = """
    <!-- DASHBOARD VIEW -->
    <main id="sec-tendencias" class="dash-section hidden relative z-10 pt-32 pb-20 px-6 max-w-6xl mx-auto">
        <!-- Búsqueda y Filtros Reales -->
        <div class="flex flex-col md:flex-row items-center gap-4 mb-8">
            <div class="flex items-center glass-panel p-1">
            <button onclick="setBusinessMode('dropshipping')" id="mode-drop" class="px-4 py-2 rounded-lg text-sm font-bold transition bg-[--text-primary] text-white shadow-sm">Dropshipping</button>
            <button onclick="setBusinessMode('ecommerce')" id="mode-ecom" class="px-4 py-2 rounded-lg text-sm font-bold transition text-[--text-secondary] hover:text-[--text-primary]">Marca Propia</button>
            </div>

            <div class="relative flex-1 md:flex-none">
            <i data-lucide="search" class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-[--text-secondary]"></i>
            <input id="productSearch" type="text" placeholder="Buscar producto..." oninput="searchProducts(this.value)" class="w-full md:w-64 glass-panel border border-[--glass-border] pl-10 pr-4 py-3 text-sm font-medium text-[--text-primary] placeholder-[--text-secondary] outline-none focus:border-[rgba(0,0,0,0.2)] transition">
            </div>
        </div>

        <!-- Product Table -->
        <div class="glass-panel overflow-hidden">
            <div class="p-6 border-b border-[--glass-border] flex justify-between items-center bg-[rgba(255,255,255,0.4)]">
            <h3 id="tableTitle" class="text-sm font-bold uppercase tracking-widest text-[--text-primary]">Top Productos en Tendencia</h3>
            <span id="tableProductCount" class="text-xs text-[--text-secondary] font-bold">0 productos</span>
            </div>
            
            <div class="overflow-x-auto">
            <table class="w-full text-sm text-left">
                <thead>
                <tr class="border-b border-[--glass-border] text-[--text-secondary] font-bold uppercase text-[10px]">
                    <th class="p-4 w-10 text-center"><input type="checkbox" id="masterCheckbox" onclick="toggleAllSelection(event)" class="accent-[--text-primary] w-3 h-3 rounded bg-transparent"></th>
                    <th class="p-4 w-12 text-center">#</th>
                    <th class="p-4">Producto</th>
                    <th class="p-4">TrendScore</th>
                    <th class="p-4">Cambio</th>
                    <th class="p-4" id="th-margen">Margen</th>
                    <th class="p-4">Competencia</th>
                    <th class="p-4" id="th-venta">Venta Est.</th>
                    <th class="p-4" id="th-costo">Costo Est.</th>
                    <th class="p-4 w-12"></th>
                </tr>
                </thead>
                <tbody id="productsTbody" class="divide-y divide-[rgba(200,190,180,0.15)]">
                <!-- Dynamically populated table list rows -->
                </tbody>
            </table>
            </div>

            <!-- Table Pagination -->
            <div id="pagination" class="p-4 flex items-center justify-center gap-2 border-t border-[--glass-border] bg-[rgba(255,255,255,0.4)]"></div>
        </div>
    </main>
    
    <!-- Dummy sections for the JS to not break -->
    <main id="sec-analisis" class="dash-section hidden"></main>
    <main id="sec-alertas" class="dash-section hidden"></main>
    <main id="sec-guardados" class="dash-section hidden"></main>
    <main id="sec-perfil" class="dash-section hidden"></main>
    <main id="sec-negocio" class="dash-section hidden"></main>
    """
    
    # Find the end of <main id="sec-landing"> and append dashboard HTML
    html = html.replace('</main>\n\n    <!-- Footer -->', '</main>\n\n' + dashboard_html + '\n    <!-- Footer -->')
    
    # Update Navbar navigation
    html = html.replace('<button class="text-sm font-semibold text-[--text-primary] hover:opacity-70 transition">Ingresar</button>', '<button onclick="goSection(\'tendencias\')" class="text-sm font-semibold text-[--text-primary] hover:opacity-70 transition">Ingresar</button>')
    html = html.replace('<button class="btn-solid px-6 py-2.5 text-sm">Comenzar Gratis</button>', '<button onclick="goSection(\'tendencias\')" class="btn-solid px-6 py-2.5 text-sm">Comenzar Gratis</button>')
    html = html.replace('<button class="btn-solid px-8 py-4 text-lg w-full sm:w-auto">Crear cuenta gratis</button>', '<button onclick="goSection(\'tendencias\')" class="btn-solid px-8 py-4 text-lg w-full sm:w-auto">Crear cuenta gratis</button>')
    
    # 3. Add the JS engine
    # Fix the JS `renderProducts` to use the Vision OS styling for the table rows
    old_comp = "const compClass = p.comp === 'Baja' ? 'text-green-400 bg-green-500/10 border-green-500/20' : p.comp === 'Alta' ? 'text-red-400 bg-red-500/10 border-red-500/20' : 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20';"
    new_comp = "const compClass = p.comp === 'Baja' ? 'badge-green' : p.comp === 'Alta' ? 'text-[#FF3B30] bg-[#FF3B30]/10 px-3 py-1 rounded-full text-xs font-bold' : 'text-[#FF9F0A] bg-[#FF9F0A]/10 px-3 py-1 rounded-full text-xs font-bold';"
    js_content = js_content.replace(old_comp, new_comp)
    
    js_content = js_content.replace('<tr onclick="openProduct(${idx})" class="hover:bg-white/5 transition cursor-pointer text-xs">', '<tr onclick="openProduct(${idx})" class="hover:bg-[rgba(255,255,255,0.6)] transition cursor-pointer text-xs text-[--text-primary]">')
    js_content = js_content.replace('class="accent-champagne w-3 h-3 rounded bg-transparent border-white/20"', 'class="accent-[--text-primary] w-3 h-3 rounded bg-transparent"')
    js_content = js_content.replace('<td class="p-4 text-center font-mono text-white/40">${start + i + 1}</td>', '<td class="p-4 text-center font-bold text-[--text-secondary]">${start + i + 1}</td>')
    js_content = js_content.replace('class="w-8 h-8 rounded border border-white/10 bg-black/20 object-cover"', 'class="w-8 h-8 rounded border border-[rgba(0,0,0,0.1)] bg-white object-cover"')
    js_content = js_content.replace('<span class="font-bold text-white">${p.name}</span>', '<span class="font-bold text-[--text-primary]">${p.name}</span>')
    js_content = js_content.replace('<td class="p-4 font-mono text-champagne">${p.score}</td>', '<td class="p-4 font-bold text-[--text-primary]">${p.score}</td>')
    js_content = js_content.replace('<td class="p-4 font-mono text-green-400">${p.change}</td>', '<td class="p-4 font-bold text-[#34C759]">${p.change}</td>')
    js_content = js_content.replace('<td class="p-4 font-mono text-green-400">${p.marginStr}</td>', '<td class="p-4 font-bold text-[#34C759]">${p.marginStr}</td>')
    js_content = js_content.replace('<td class="p-4 font-mono text-white/70">${p.priceStr}</td>', '<td class="p-4 font-bold text-[--text-secondary]">${p.priceStr}</td>')
    js_content = js_content.replace('<td class="p-4 font-mono text-white/40">${p.suppliers && p.suppliers[0] ? p.suppliers[0].price : \'—\'}</td>', '<td class="p-4 font-bold text-[--text-secondary]">${p.suppliers && p.suppliers[0] ? p.suppliers[0].price : \'—\'}</td>')
    js_content = js_content.replace('<button onclick="event.stopPropagation(); toggleSave(${idx})" class="text-white/40 hover:text-champagne transition">', '<button onclick="event.stopPropagation(); toggleSave(${idx})" class="text-[--text-secondary] hover:text-[--text-primary] transition">')
    
    # 4. Modify goSection so it toggles the blocks correctly
    # Find the goSection function
    go_section_replacement = """
    function goSection(sectionId) {
      document.querySelectorAll('.dash-section').forEach(s => {
        s.classList.add('hidden');
        s.classList.remove('block');
      });
      const target = document.getElementById('sec-' + sectionId);
      if(target) {
        target.classList.remove('hidden');
        target.classList.add('block');
      }
      
      // Update nav style
      if(sectionId !== 'landing') {
         document.getElementById('nav-dash-buttons')?.classList.remove('hidden');
      }
    }
    """
    
    # We don't want to break the original function too much if we don't have to, let's just use CSS.
    # The original JS has function goSection(sectionId)
    # We append the modals and js_content
    
    html = html.replace('</body>\n</html>', js_content + '\n</body>\n</html>')
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    map_vision_os()
