def fix_dashboard():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Replace the productGrid with the actual table structure
    bad_grid = '<!-- GRILLA DE PRODUCTOS REAL -->\n            <div id="productGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 mb-8"></div>'
    
    good_table = """<!-- Product Table List -->
            <div class="matte-card overflow-hidden mt-8">
              <div class="p-6 border-b border-[rgba(200,190,180,0.2)] flex justify-between items-center bg-[rgba(255,255,255,0.4)]">
                <h3 id="tableTitle" class="text-sm font-heading font-bold uppercase tracking-widest text-[--text-dark]">Top Productos en Tendencia</h3>
                <span id="tableProductCount" class="text-xs text-muted font-bold">0 productos</span>
              </div>
              
              <div class="overflow-x-auto">
                <table class="w-full text-xs text-left">
                  <thead>
                    <tr class="border-b border-[rgba(200,190,180,0.2)] text-[--text-muted] font-bold uppercase text-[10px]">
                      <th class="p-4 w-10 text-center"><input type="checkbox" id="masterCheckbox" onclick="toggleAllSelection(event)" class="accent-[--text-dark] w-3 h-3 rounded bg-transparent"></th>
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
              <div id="pagination" class="p-4 flex items-center justify-center gap-2 border-t border-[rgba(200,190,180,0.2)] bg-[rgba(255,255,255,0.4)]"></div>
            </div>"""
            
    html = html.replace(bad_grid, good_table)

    # 2. Modify `renderProducts` in the Javascript to generate Light Mode rows
    # Original template has: <tr onclick="openProduct(${idx})" class="hover:bg-white/5 transition cursor-pointer text-xs">
    # We want: <tr onclick="openProduct(${idx})" class="hover:bg-[rgba(255,255,255,0.6)] transition cursor-pointer text-xs text-[--text-dark]">
    
    html = html.replace('<tr onclick="openProduct(${idx})" class="hover:bg-white/5 transition cursor-pointer text-xs">', '<tr onclick="openProduct(${idx})" class="hover:bg-[rgba(255,255,255,0.6)] transition cursor-pointer text-xs text-[--text-dark]">')
    
    # Checkbox
    html = html.replace('class="accent-champagne w-3 h-3 rounded bg-transparent border-white/20"', 'class="accent-[--text-dark] w-3 h-3 rounded bg-transparent"')
    
    # ID / Number
    html = html.replace('<td class="p-4 text-center font-mono text-white/40">${start + i + 1}</td>', '<td class="p-4 text-center font-bold text-muted">${start + i + 1}</td>')
    
    # Product Name & Image
    html = html.replace('class="w-8 h-8 rounded border border-white/10 bg-black/20 object-cover"', 'class="w-8 h-8 rounded border border-[rgba(0,0,0,0.1)] bg-[--bg-wall] object-cover"')
    html = html.replace('<span class="font-bold text-white">${p.name}</span>', '<span class="font-bold text-[--text-dark]">${p.name}</span>')
    
    # TrendScore
    html = html.replace('<td class="p-4 font-mono text-champagne">${p.score}</td>', '<td class="p-4 font-bold text-[--text-dark]">${p.score}</td>')
    
    # Competencia tags:
    # Original: const compClass = p.comp === 'Baja' ? 'text-green-400 bg-green-500/10 border-green-500/20' : p.comp === 'Alta' ? 'text-red-400 bg-red-500/10 border-red-500/20' : 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20';
    old_comp = "const compClass = p.comp === 'Baja' ? 'text-green-400 bg-green-500/10 border-green-500/20' : p.comp === 'Alta' ? 'text-red-400 bg-red-500/10 border-red-500/20' : 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20';"
    new_comp = "const compClass = p.comp === 'Baja' ? 'text-[--soft-green] bg-[#E8F3EA] border border-[#599B62]/20' : p.comp === 'Alta' ? 'text-[--soft-red] bg-[#F9EAEB] border border-[#C76B6B]/20' : 'text-[#D97706] bg-[#FEF3C7] border border-[#D97706]/20';"
    html = html.replace(old_comp, new_comp)

    # Empty text/dashes
    html = html.replace('<td class="p-4 font-mono text-white/70">${p.priceStr}</td>', '<td class="p-4 font-bold text-muted">${p.priceStr}</td>')
    html = html.replace('<td class="p-4 font-mono text-white/40">${p.suppliers && p.suppliers[0] ? p.suppliers[0].price : \'—\'}</td>', '<td class="p-4 font-bold text-muted">${p.suppliers && p.suppliers[0] ? p.suppliers[0].price : \'—\'}</td>')
    html = html.replace('<button onclick="event.stopPropagation(); toggleSave(${idx})" class="text-white/40 hover:text-champagne transition">', '<button onclick="event.stopPropagation(); toggleSave(${idx})" class="text-muted hover:text-[--text-dark] transition">')

    # Now, we also need to append the missing sections! original_index.html had <section id="sec-analisis">, etc.
    # The javascript expects them. Let's just append dummy sections at the end of `#sec-tendencias`
    
    sections = """
        <!-- SECTION: ANÁLISIS -->
        <main id="sec-analisis" class="dash-section hidden flex-1 p-8 md:p-10 overflow-y-auto relative z-10">
          <div class="matte-card p-10 flex flex-col items-center justify-center text-center h-full">
            <h2 class="text-2xl font-heading text-[--text-dark]">Análisis</h2>
            <p class="text-muted">Próximamente</p>
          </div>
        </main>
        
        <!-- SECTION: ALERTAS -->
        <main id="sec-alertas" class="dash-section hidden flex-1 p-8 md:p-10 overflow-y-auto relative z-10">
          <div class="matte-card p-10 flex flex-col items-center justify-center text-center h-full">
            <h2 class="text-2xl font-heading text-[--text-dark]">Alertas</h2>
            <p class="text-muted">Próximamente</p>
          </div>
        </main>

        <!-- SECTION: GUARDADOS -->
        <main id="sec-guardados" class="dash-section hidden flex-1 p-8 md:p-10 overflow-y-auto relative z-10">
          <div class="matte-card p-10 flex flex-col items-center justify-center text-center h-full">
            <h2 class="text-2xl font-heading text-[--text-dark]">Productos Guardados</h2>
            <div id="savedContent" class="w-full mt-8"></div>
          </div>
        </main>

        <!-- SECTION: MI PERFIL -->
        <main id="sec-perfil" class="dash-section hidden flex-1 p-8 md:p-10 overflow-y-auto relative z-10">
          <div class="matte-card p-10 flex flex-col items-center justify-center text-center h-full">
            <h2 class="text-2xl font-heading text-[--text-dark]">Mi Perfil</h2>
            <div id="perfilContent" class="w-full mt-8"></div>
          </div>
        </main>

        <!-- SECTION: MI NEGOCIO -->
        <main id="sec-negocio" class="dash-section hidden flex-1 p-8 md:p-10 overflow-y-auto relative z-10">
          <div class="matte-card p-10 flex flex-col items-center justify-center text-center h-full">
            <h2 class="text-2xl font-heading text-[--text-dark]">Mi Negocio</h2>
            <div id="negocioContent" class="w-full mt-8"></div>
          </div>
        </main>
"""
    
    # insert the extra sections after the end of sec-tendencias
    html = html.replace('        </main>\n    </div>\n\n    <!-- MODALES DE LA APLICACIÓN -->', '        </main>\n' + sections + '    </div>\n\n    <!-- MODALES DE LA APLICACIÓN -->')
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    fix_dashboard()
