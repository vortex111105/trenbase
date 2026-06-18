import re

# --- DASHBOARD.HTML ---
with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Mi Negocio
old_negocio_start = '<section id="sec-negocio"'
old_negocio_end = '</section>'

# Find the sec-negocio block
match_neg = re.search(r'(<section id="sec-negocio".*?</section>)', html, re.DOTALL)
if match_neg:
    old_neg_content = match_neg.group(1)
    new_neg_content = """<section id="sec-negocio" class="dash-section space-y-6">
      <div class="flex justify-between items-center mb-6">
        <div>
          <h2 class="text-3xl font-extrabold text-white tracking-tight">Dashboard Financiero de Ventas</h2>
          <p class="text-xs text-gray-400 mt-1">Estadísticas reales de facturación e inversión publicitaria</p>
        </div>
        <button class="bg-champagne text-black px-6 py-2.5 rounded-full text-xs font-bold tracking-wider hover:bg-yellow-500 transition">+ CARGAR PRODUCTO</button>
      </div>

      <div class="bg-[#1E1E26] rounded-3xl p-6 border border-gray-800">
        <div class="mb-4">
          <h3 class="font-bold text-white">Mi Tienda Online</h3>
          <p class="text-xs text-gray-400">Conecta tu tienda para sincronizar ventas y stock automáticamente.</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="bg-[#15151B] border border-gray-800 rounded-2xl p-4 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-[#2A2A35] rounded-xl flex items-center justify-center">
                <div class="w-5 h-5 bg-green-500 rounded-sm"></div>
              </div>
              <div>
                <h4 class="font-bold text-sm text-white">Shopify</h4>
                <p class="text-[10px] text-gray-500">Desconectado</p>
              </div>
            </div>
            <button class="bg-[#2A2A35] text-white px-4 py-2 rounded-xl text-xs font-bold hover:bg-gray-700 transition">Conectar</button>
          </div>
          <div class="bg-[#15151B] border border-gray-800 rounded-2xl p-4 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-[#2A2A35] rounded-xl flex items-center justify-center">
                <div class="w-5 h-5 bg-blue-600 rounded-sm"></div>
              </div>
              <div>
                <h4 class="font-bold text-sm text-white">TiendaNube</h4>
                <p class="text-[10px] text-gray-500">Desconectado</p>
              </div>
            </div>
            <button onclick="alert('Vinculación automática en progreso...')" class="bg-[#2A2A35] text-white px-4 py-2 rounded-xl text-xs font-bold hover:bg-gray-700 transition">Conectar</button>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-[#1E1E26] rounded-3xl p-6 border border-gray-800 flex flex-col justify-center">
          <span class="text-[10px] text-gray-400 font-bold uppercase tracking-wider mb-2">Ingresos Totales</span>
          <span class="text-2xl font-black text-green-400">$0 ARS</span>
          <span class="text-[10px] text-gray-500 mt-1">0 unidades vendidas</span>
        </div>
        <div class="bg-[#1E1E26] rounded-3xl p-6 border border-gray-800 flex flex-col justify-center">
          <span class="text-[10px] text-gray-400 font-bold uppercase tracking-wider mb-2">Ganancia Neta</span>
          <span class="text-2xl font-black text-green-400">$0 ARS</span>
          <span class="text-[10px] text-gray-500 mt-1">ROI: 0%</span>
        </div>
        <div class="bg-[#1E1E26] rounded-3xl p-6 border border-gray-800 flex flex-col justify-center">
          <span class="text-[10px] text-gray-400 font-bold uppercase tracking-wider mb-2">Inversión Stock</span>
          <span class="text-2xl font-black text-white">$0 ARS</span>
          <span class="text-[10px] text-gray-500 mt-1">Stock + Publicidad</span>
        </div>
        <div class="bg-[#1E1E26] rounded-3xl p-6 border border-gray-800 flex flex-col justify-center">
          <span class="text-[10px] text-gray-400 font-bold uppercase tracking-wider mb-2">Valor en Stock</span>
          <span class="text-2xl font-black text-white">$0 ARS</span>
          <span class="text-[10px] text-gray-500 mt-1">0 unidades disponibles</span>
        </div>
      </div>

      <div class="bg-[#1E1E26] rounded-3xl p-6 border border-gray-800">
        <h3 class="text-xs text-champagne font-bold tracking-widest uppercase mb-4">Mis Productos de Venta</h3>
        <div class="w-full h-32 flex items-center justify-center border border-dashed border-gray-700 rounded-xl">
          <p class="text-gray-500 text-sm">Aún no hay productos cargados en tu tienda.</p>
        </div>
      </div>
    </section>"""
    html = html.replace(old_neg_content, new_neg_content)

# 2. Update Guardados
match_gua = re.search(r'(<section id="sec-guardados".*?</section>)', html, re.DOTALL)
if match_gua:
    old_gua_content = match_gua.group(1)
    new_gua_content = """<section id="sec-guardados" class="dash-section space-y-6">
      <div class="flex justify-between items-center mb-6">
        <div>
          <h2 class="text-3xl font-extrabold text-white tracking-tight">Mis Productos Guardados</h2>
          <p class="text-xs text-gray-400 mt-1">Lista de productos seleccionados para seguimiento</p>
        </div>
      </div>

      <!-- Filtros tipo Kanban / Pipeline -->
      <div class="flex gap-4 overflow-x-auto pb-4 hide-scrollbar">
        <button class="px-6 py-3 bg-[#1E1E26] border border-gray-700 text-gray-300 text-sm font-bold rounded-xl whitespace-nowrap hover:bg-[#2A2A35] transition flex items-center gap-2">
          📌 Por Testear <span class="bg-gray-800 text-xs px-2 py-0.5 rounded-full">0</span>
        </button>
        <button class="px-6 py-3 bg-[#1E1E26] border border-gray-700 text-gray-300 text-sm font-bold rounded-xl whitespace-nowrap hover:bg-[#2A2A35] transition flex items-center gap-2">
          🧪 Testeando <span class="bg-gray-800 text-xs px-2 py-0.5 rounded-full">1</span>
        </button>
        <button class="px-6 py-3 bg-[#1E1E26] border border-gray-700 text-gray-300 text-sm font-bold rounded-xl whitespace-nowrap hover:bg-[#2A2A35] transition flex items-center gap-2">
          🔥 Ganador (Escalando) <span class="bg-gray-800 text-xs px-2 py-0.5 rounded-full">0</span>
        </button>
        <button class="px-6 py-3 bg-[#1E1E26] border border-gray-700 text-gray-300 text-sm font-bold rounded-xl whitespace-nowrap hover:bg-[#2A2A35] transition flex items-center gap-2">
          🗑️ Descartado
        </button>
      </div>

      <!-- Product Grid (Mock Testeando) -->
      <div id="savedGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div class="bg-[#1E1E26] rounded-2xl overflow-hidden border border-gray-800 hover:border-gray-600 transition group relative">
          <div class="h-48 bg-gray-800 relative">
            <img src="https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&q=80&w=800" class="w-full h-full object-cover opacity-80" alt="Zapatillas">
            <div class="absolute top-2 left-2 bg-champagne text-black text-[9px] font-bold px-2 py-0.5 rounded-sm uppercase">MODA</div>
          </div>
          <div class="p-4">
            <h3 class="font-bold text-white text-sm leading-tight mb-4">Zapatillas Transpirables Multifunción 69</h3>
            <div class="flex justify-between items-center text-xs">
              <span class="text-gray-400">Margen: <span class="text-green-400 font-bold">59% ROI</span></span>
              <span class="text-gray-400">Comp: <span class="text-white">Baja</span></span>
            </div>
          </div>
        </div>
      </div>
    </section>"""
    html = html.replace(old_gua_content, new_gua_content)

# We must ensure the dashboard text colors adapt to the Midnight Luxe theme if they are white.
# Actually, the user's dashboard is dark in the screenshots! Our UI was light mode.
# I will enforce dark mode classes for these specific sections to match the screenshots.

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)


# --- APP.JS (Product Modal) ---
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace innerHTML of productModal
old_modal_content_start = 'const modal = `'
old_modal_content_end = "document.body.insertAdjacentHTML('beforeend', modal);"

match_modal = re.search(r'const modal = `(.*?)`;\s*document\.body\.insertAdjacentHTML', js, re.DOTALL)
if match_modal:
    old_modal_content = match_modal.group(1)
    new_modal_content = """
    <div id="productModal" class="fixed inset-0 z-50 bg-[#0D0D12]/90 backdrop-blur-md flex items-center justify-center p-4 sm:p-6 opacity-0 transition-opacity duration-300">
      <div class="bg-[#1E1E26] w-full max-w-4xl rounded-3xl saas-shadow-2xl relative flex flex-col md:flex-row overflow-hidden border border-gray-800 transform scale-95 transition-transform duration-300" id="productModalContent">
        
        <button onclick="closeProductModal()" class="absolute top-4 right-4 bg-gray-800 text-gray-400 hover:text-white p-2 rounded-full z-10 transition"><i data-lucide="x" class="w-4 h-4"></i></button>

        <div class="w-full md:w-2/5 h-64 md:h-auto bg-gray-900 relative">
          <img src="${product.image}" class="w-full h-full object-cover opacity-80" alt="${product.name}">
          <div class="absolute inset-0 bg-gradient-to-t from-[#1E1E26] to-transparent"></div>
        </div>
        
        <div class="w-full md:w-3/5 p-8 flex flex-col h-[600px] overflow-y-auto custom-scrollbar">
          
          <!-- Header -->
          <h2 class="text-2xl font-extrabold text-white mb-6 leading-tight">${product.name}</h2>
          
          <div class="flex items-end gap-3 mb-8">
            <span class="text-5xl font-black text-white">${product.score}</span>
            <div class="pb-1 flex items-center gap-2">
              <span class="text-xs text-gray-400 font-bold tracking-widest uppercase">Trendscore</span>
              <span class="bg-champagne text-black text-[10px] font-black px-2 py-0.5 rounded-sm uppercase tracking-wider">HOT</span>
            </div>
          </div>

          <!-- Tabs -->
          <div class="flex gap-6 border-b border-gray-800 mb-6">
            <button class="pb-2 text-sm font-bold text-champagne border-b-2 border-champagne">Información</button>
            <button class="pb-2 text-sm font-bold text-gray-500 hover:text-gray-300">Historial 90 días</button>
            <button class="pb-2 text-sm font-bold text-gray-500 hover:text-gray-300">Proveedores</button>
            <button class="pb-2 text-sm font-bold text-gray-500 hover:text-gray-300 flex items-center gap-1"><i data-lucide="sparkles" class="w-3 h-3"></i> Marketing IA</button>
          </div>

          <!-- 5 Data Blocks -->
          <div class="grid grid-cols-2 lg:grid-cols-3 gap-3 mb-8">
            <div class="bg-[#15151B] border border-gray-800 rounded-2xl p-4 flex flex-col items-center justify-center text-center">
              <span class="text-champagne text-lg font-bold">up</span>
              <span class="text-[9px] text-gray-500 uppercase tracking-widest font-bold mt-1">Cambio 24hs</span>
            </div>
            <div class="bg-[#15151B] border border-gray-800 rounded-2xl p-4 flex flex-col items-center justify-center text-center">
              <span class="text-green-400 text-lg font-bold">${product.roi}% ROI</span>
              <span class="text-[9px] text-gray-500 uppercase tracking-widest font-bold mt-1">Margen Est.</span>
            </div>
            <div class="bg-[#15151B] border border-gray-800 rounded-2xl p-4 flex flex-col items-center justify-center text-center">
              <span class="text-white text-base font-bold">${product.category || 'Hogar'}</span>
              <span class="text-[9px] text-gray-500 uppercase tracking-widest font-bold mt-1">Categoría</span>
            </div>
            <div class="bg-[#15151B] border border-gray-800 rounded-2xl p-4 flex flex-col items-center justify-center text-center col-span-2 lg:col-span-1">
              <span class="text-white text-lg font-bold">$61 - $83</span>
              <span class="text-[9px] text-gray-500 uppercase tracking-widest font-bold mt-1">Precio Venta Est.</span>
            </div>
            <div class="bg-[#15151B] border border-gray-800 rounded-2xl p-4 flex flex-col items-center justify-center text-center col-span-2">
              <span class="text-champagne border border-champagne px-3 py-1 rounded-sm text-xs font-bold uppercase">Muy Alta</span>
              <span class="text-[9px] text-gray-500 uppercase tracking-widest font-bold mt-2">Competencia</span>
            </div>
          </div>

          <!-- Badges -->
          <div class="space-y-6 flex-1">
            <div>
              <span class="text-[10px] text-gray-500 font-bold uppercase tracking-widest mb-3 block">Plataformas donde es tendencia</span>
              <span class="bg-[#2A2A35] text-white text-xs px-3 py-1.5 rounded-md">Facebook</span>
            </div>
            <div>
              <span class="text-[10px] text-gray-500 font-bold uppercase tracking-widest mb-3 block">Regiones Activas</span>
              <div class="flex gap-2">
                <span class="bg-[#2A2A35] border border-gray-700 text-white text-xs px-3 py-1.5 rounded-md flex items-center gap-2">🇨🇱 CL</span>
                <span class="bg-[#2A2A35] border border-gray-700 text-white text-xs px-3 py-1.5 rounded-md flex items-center gap-2">🇨🇱 CL</span>
              </div>
            </div>
            <div>
              <span class="text-[10px] text-champagne font-bold uppercase tracking-widest mb-3 flex items-center gap-2"><i data-lucide="shopping-bag" class="w-3 h-3"></i> Recomendado vender en:</span>
              <div class="flex gap-2 flex-wrap">
                <span class="text-white text-[11px] font-bold">Shopify</span>
                <span class="text-blue-400 text-[11px] font-bold">TiendaNube</span>
                <span class="text-yellow-400 text-[11px] font-bold">Mercado Libre</span>
                <span class="text-green-400 text-[11px] font-bold">Falabella</span>
              </div>
            </div>
          </div>

          <div class="mt-8 pt-6 border-t border-gray-800 grid grid-cols-2 gap-3">
            <button onclick="alert('Comparador Abierto')" class="w-full bg-[#2A2A35] hover:bg-gray-700 text-white font-extrabold text-sm py-4 rounded-xl transition flex items-center justify-center gap-2">
              <i data-lucide="git-compare" class="w-5 h-5"></i> Comparar
            </button>
            <button onclick="window.startImportWorkflow(${idx})" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-sm py-4 rounded-xl saas-shadow transition hover:-translate-y-0.5 flex items-center justify-center gap-2">
              <i data-lucide="cloud-lightning" class="w-5 h-5"></i> Importar
            </button>
          </div>

        </div>
      </div>
    </div>
"""
    js = js.replace(old_modal_content, new_modal_content)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Data density and complex views restored!")
