def inject_grid():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

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
            <div id="productGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8"></div>
"""

    # We find the section with the chart and table
    target = '<div class="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-6">'
    html = html.replace(target, grid_injection + '\n            ' + target)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    inject_grid()
