import re

# 1. Read dashboard.html
with open('dashboard.html', 'r', encoding='utf-8') as f:
    dash = f.read()

# Replace table headers
old_thead = """          <thead>
            <tr class="bg-gray-50 text-gray-400 text-xs font-medium uppercase tracking-wider">
              <th class="p-4 pl-6 font-mono font-medium">Producto</th>
              <th class="p-4 font-mono font-medium">Categoría</th>
              <th class="p-4 font-mono font-medium">Plataformas</th>
              <th class="p-4 font-mono font-medium">Precio Venta</th>
              <th class="p-4 font-mono font-medium">TrendScore</th>
              <th class="p-4 pr-6"></th>
            </tr>
          </thead>"""

new_thead = """          <thead>
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
          </thead>"""

dash = dash.replace(old_thead, new_thead)

# Replace pagination footer
old_pagination = """      <!-- Pagination -->
      <div class="p-4 border-t border-gray-100 flex justify-between items-center bg-gray-50/50 mt-auto">
        <span class="text-xs text-gray-500 font-medium" id="pageInfo">Mostrando 1-10 de 500</span>
        <div class="flex gap-2">
          <button onclick="prevPage()" class="w-8 h-8 rounded-lg bg-white border border-gray-200 flex items-center justify-center hover:bg-gray-50 transition shadow-sm"><i data-lucide="chevron-left" class="w-4 h-4"></i></button>
          <button onclick="nextPage()" class="w-8 h-8 rounded-lg bg-white border border-gray-200 flex items-center justify-center hover:bg-gray-50 transition shadow-sm"><i data-lucide="chevron-right" class="w-4 h-4"></i></button>
        </div>
      </div>"""

new_pagination = """      <!-- Table Pagination -->
      <div id="pagination" class="p-4 flex items-center justify-center gap-2 border-t border-gray-100 bg-gray-50/50 mt-auto"></div>"""

dash = dash.replace(old_pagination, new_pagination)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dash)

# 2. Extract renderTable from original_index.html's <script> block and insert it into app.js
with open('original_index.html', 'r', encoding='utf-8') as f:
    orig = f.read()

render_table_match = re.search(r'function renderTable\(\) \{.*?(?=function renderPagination)', orig, flags=re.DOTALL)
if render_table_match:
    render_table_js = render_table_match.group(0)
    
    # We need to adapt the classes in the generated HTML from the original renderTable
    # The original generated <tr> with 'border-b border-white/5 hover:bg-white/5' etc.
    render_table_js = render_table_js.replace('border-b border-white/5 hover:bg-white/5', 'border-b border-gray-100 hover:bg-gray-50/50 transition')
    render_table_js = render_table_js.replace('accent-champagne', 'accent-black')
    render_table_js = render_table_js.replace('border-white/20', 'border-gray-200')
    render_table_js = render_table_js.replace('w-3 h-3 rounded', 'w-3 h-3 rounded bg-white')
    render_table_js = render_table_js.replace('w-8 h-8 rounded bg-white/5', 'w-8 h-8 rounded-xl bg-gray-100 border border-gray-200')
    render_table_js = render_table_js.replace('text-white', 'text-gray-900')
    render_table_js = render_table_js.replace('text-white/50', 'text-gray-500')
    render_table_js = render_table_js.replace('tag-hot', 'bg-red-50 text-red-600 border border-red-100')
    render_table_js = render_table_js.replace('tag-rising', 'bg-blue-50 text-blue-600 border border-blue-100')
    render_table_js = render_table_js.replace('bg-white/10 text-white/70', 'bg-gray-100 text-gray-600')
    render_table_js = render_table_js.replace('text-green-400', 'text-green-500')
    render_table_js = render_table_js.replace('text-champagne', 'text-black')
    
    # The bookmark button
    render_table_js = render_table_js.replace('text-champagne fill-champagne', 'text-black fill-current')
    render_table_js = render_table_js.replace('text-white/20 hover:text-champagne', 'text-gray-400 hover:text-black')
    
    # We need to append the new renderTable to app.js, overriding the old one.
    with open('app.js', 'a', encoding='utf-8') as f:
        f.write('\\n// --- RESTORED RENDERTABLE FROM ORIGINAL ---\\n')
        f.write(render_table_js)

# Also grab the pagination functions
pagination_match = re.search(r'function renderPagination\(\) \{.*?(?=function exportDataCSV)', orig, flags=re.DOTALL)
if pagination_match:
    pagination_js = pagination_match.group(0)
    pagination_js = pagination_js.replace('bg-white/10 text-white', 'bg-black text-white')
    pagination_js = pagination_js.replace('text-white/50 hover:bg-white/5 hover:text-white', 'bg-white border border-gray-200 text-gray-500 hover:bg-gray-50 hover:text-gray-900')
    
    with open('app.js', 'a', encoding='utf-8') as f:
        f.write('\\n' + pagination_js)
        f.write('\\nwindow.renderTable = renderTable;')
        f.write('\\nwindow.renderPagination = renderPagination;')
        f.write('\\nwindow.goToPage = goToPage;')
