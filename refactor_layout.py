import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Current structure:
# <div class="grid grid-cols-1 xl:grid-cols-3 gap-6">
#   <div class="xl:col-span-2 flex flex-col"> (TABLE) </div>
#   <div class="xl:col-span-1 flex flex-col"> (OPPORTUNIDADES) </div>
# </div>

# Extract the Table section and the Oportunidades section
m = re.search(r'(<div class="xl:col-span-2 flex flex-col">.*?)(<div class="xl:col-span-1 flex flex-col">.*?</section>)', html, flags=re.DOTALL)
if m:
    table_col = m.group(1)
    opp_col = m.group(2)
    
    # Strip the wrappers
    table_content = re.sub(r'^<div class="xl:col-span-2 flex flex-col">', '', table_col).strip()
    table_content = re.sub(r'</div>$', '', table_content).strip()
    
    # Extract inner content of Oportunidades
    opp_match = re.search(r'<div class="bg-white rounded-\[2rem\] p-6 saas-shadow saas-card-hover flex flex-col">.*?</div>\s*</div>\s*</section>', opp_col, flags=re.DOTALL)
    
    # Actually, let's just replace the grid block directly
    
    old_grid = re.search(r'<div class="grid grid-cols-1 xl:grid-cols-3 gap-6">.*?</section>', html, flags=re.DOTALL).group(0)
    
    new_grid = """<div class="flex flex-col gap-6">
        <!-- Oportunidades List -->
        <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover flex flex-col w-full">
          <div class="flex justify-between items-center mb-6">
            <h3 class="font-bold text-gray-800">Top Oportunidades</h3>
            <span class="text-[10px] font-bold text-green-600 bg-green-50 px-2 py-1 rounded-md uppercase tracking-wider">Alta Rentabilidad</span>
          </div>
          <div id="oppList" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div class="text-sm text-gray-400 text-center py-4 font-medium col-span-full">Cargando oportunidades...</div>
          </div>
        </div>

        <!-- Products Table -->
        <div class="bg-white rounded-[2rem] saas-shadow h-[600px] flex flex-col overflow-hidden min-h-[400px] w-full">
          <div class="p-6 border-b border-gray-100 flex justify-between items-center">
            <h3 class="font-bold text-gray-800">Top Productos en Tendencia</h3>
            <div class="flex gap-2">
              <button class="bg-gray-50 hover:bg-gray-100 text-gray-600 px-4 py-2 rounded-xl text-xs font-bold transition border border-gray-200">Exportar CSV</button>
            </div>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-gray-50 text-gray-400 text-xs font-medium uppercase tracking-wider">
                  <th class="p-4 pl-6 w-10 text-center"><input type="checkbox" id="masterCheckbox" onclick="toggleAllSelection(event)" class="accent-black w-3 h-3 rounded bg-transparent border-gray-200"></th>
                  <th class="p-4 w-12 text-center font-mono">#</th>
                  <th class="p-4 font-mono">Producto</th>
                  <th class="p-4 font-mono">TrendScore</th>
                  <th class="p-4 font-mono">Cambio</th>
                  <th class="p-4 font-mono" id="th-margen">Margen</th>
                  <th class="p-4 font-mono">Competencia</th>
                  <th class="p-4 font-mono" id="th-venta">Venta Est.</th>
                  <th class="p-4 font-mono" id="th-costo">Costo Est.</th>
                  <th class="p-4 pr-6 w-12"></th>
                </tr>
              </thead>
              <tbody id="tableBody" class="text-sm">
                <!-- Rows injected by JS -->
              </tbody>
            </table>
          </div>
          
          <!-- Table Pagination -->
          <div id="pagination" class="p-4 flex items-center justify-center gap-2 border-t border-gray-100 bg-gray-50/50 mt-auto"></div>
        </div>
      </div>
    </section>"""
    
    html = html.replace(old_grid, new_grid)

# Add "Mi Negocio" new elements
old_negocio = re.search(r'<section id="sec-negocio" class="dash-section space-y-6">.*?</section>', html, flags=re.DOTALL).group(0)

new_negocio = """<section id="sec-negocio" class="dash-section space-y-6">
      <div class="flex justify-between items-center mb-2">
        <div>
          <h2 class="text-2xl font-extrabold text-gray-900 tracking-tight">Mi Negocio</h2>
          <p class="text-xs text-gray-500 mt-1">Sincroniza tus tiendas y registra tus ventas</p>
        </div>
        <button onclick="showAddProductModal()" class="bg-black text-white px-5 py-2.5 rounded-full text-xs font-bold uppercase tracking-wider saas-shadow hover:-translate-y-0.5 transition flex items-center gap-2"><i data-lucide="plus" class="w-4 h-4"></i> Cargar Venta Manual</button>
      </div>
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        <!-- Integraciones (Shopify / Tienda Nube) -->
        <div class="lg:col-span-2 bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover flex flex-col">
          <h3 class="font-bold text-gray-800 mb-6 flex items-center gap-2"><i data-lucide="link" class="w-4 h-4 text-gray-500"></i> Integraciones</h3>
          <p class="text-xs text-gray-500 mb-6">Conecta tu tienda online para sincronizar ventas y analizar rentabilidad en tiempo real.</p>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Shopify -->
            <div class="border border-gray-200 rounded-2xl p-4 flex items-center justify-between hover:border-gray-400 transition cursor-pointer">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-green-50 rounded-xl flex items-center justify-center text-green-600 font-bold">Sh</div>
                <div>
                  <h4 class="font-bold text-sm text-gray-900">Shopify</h4>
                  <p class="text-[10px] text-gray-500">Sincronización automática</p>
                </div>
              </div>
              <button class="bg-gray-100 hover:bg-gray-200 text-gray-700 px-3 py-1.5 rounded-lg text-xs font-bold transition">Conectar</button>
            </div>
            <!-- Tiendanube -->
            <div class="border border-gray-200 rounded-2xl p-4 flex items-center justify-between hover:border-gray-400 transition cursor-pointer">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-blue-50 rounded-xl flex items-center justify-center text-blue-600 font-bold">Tn</div>
                <div>
                  <h4 class="font-bold text-sm text-gray-900">Tiendanube</h4>
                  <p class="text-[10px] text-gray-500">Próximamente</p>
                </div>
              </div>
              <button class="bg-gray-50 text-gray-400 px-3 py-1.5 rounded-lg text-xs font-bold cursor-not-allowed">Pronto</button>
            </div>
          </div>
        </div>

        <!-- Quick Stats / Leaderboard preview -->
        <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover flex flex-col justify-center items-center text-center">
          <h3 class="font-bold text-gray-800 mb-4 flex items-center gap-2 w-full justify-start"><i data-lucide="award" class="w-4 h-4 text-gray-500"></i> Tu Progreso</h3>
          <div class="w-24 h-24 rounded-full border-4 border-gray-100 flex items-center justify-center shadow-inner relative mb-4">
            <span class="text-4xl">🔥</span>
            <div class="absolute -bottom-2 bg-black text-white text-[10px] font-bold px-3 py-1 rounded-full saas-shadow">NIVEL 1</div>
          </div>
          <p class="text-[11px] text-gray-500 max-w-[200px]">Conecta tu tienda o registra 5 ventas para subir al Nivel 2 y desbloquear proveedores exclusivos.</p>
        </div>

      </div>
    </section>"""

html = html.replace(old_negocio, new_negocio)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Dashboard refactored!")
