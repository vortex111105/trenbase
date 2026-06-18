import re

# 1. READ FRESH dashboard.html
with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 2. RESTORE SEC-ANALISIS
with open('original_index.html', 'r', encoding='utf-8') as f:
    orig = f.read()

match = re.search(r'<!-- SECTION: ANÁLISIS -->(.*?)</section>', orig, flags=re.DOTALL)
if match:
    sec_analisis_html = match.group(0)
    # Colors and borders
    migrated_html = sec_analisis_html.replace('bg-white/5', 'bg-white')
    migrated_html = migrated_html.replace('bg-black/30', 'bg-gray-50')
    migrated_html = migrated_html.replace('bg-black/20', 'bg-gray-50')
    migrated_html = migrated_html.replace('bg-black/10', 'bg-gray-50')
    migrated_html = migrated_html.replace('bg-obsidian', 'bg-white')
    migrated_html = migrated_html.replace('border-white/10', 'border-gray-100')
    migrated_html = migrated_html.replace('border-white/5', 'border-gray-100')
    migrated_html = migrated_html.replace('border-b border-white/5', 'border-b border-gray-100')
    migrated_html = migrated_html.replace('border-t border-white/10', 'border-t border-gray-100')
    migrated_html = migrated_html.replace('border-t border-white/5', 'border-t border-gray-100')
    
    # Text colors
    migrated_html = migrated_html.replace('text-white/70', 'text-gray-700')
    migrated_html = migrated_html.replace('text-white/60', 'text-gray-600')
    migrated_html = migrated_html.replace('text-white/50', 'text-gray-500')
    migrated_html = migrated_html.replace('text-white/40', 'text-gray-400')
    migrated_html = migrated_html.replace('text-white/30', 'text-gray-400')
    migrated_html = migrated_html.replace('text-white', 'text-gray-900')
    migrated_html = migrated_html.replace('text-champagne', 'text-gray-900')
    
    # Specific elements
    migrated_html = migrated_html.replace('bg-champagne text-obsidian', 'bg-black text-white saas-shadow')
    migrated_html = migrated_html.replace('bg-white/10 text-white', 'bg-black text-white saas-shadow')
    migrated_html = migrated_html.replace('text-green-400', 'text-green-500')
    migrated_html = migrated_html.replace('text-blue-400', 'text-blue-500')
    migrated_html = migrated_html.replace('shadow-[0_0_10px_rgba(255,255,255,0.8)]', 'shadow-md')
    migrated_html = migrated_html.replace('bg-green-500/10', 'bg-green-100')
    migrated_html = migrated_html.replace('bg-yellow-500/10', 'bg-yellow-100')
    migrated_html = migrated_html.replace('bg-red-500/10', 'bg-red-100')
    
    # Add saas-shadow to cards
    migrated_html = migrated_html.replace('rounded-[2rem]', 'rounded-[2rem] saas-shadow saas-card-hover')
    migrated_html = migrated_html.replace('rounded-[2.5rem]', 'rounded-[2.5rem] saas-shadow saas-card-hover')

    html = re.sub(r'<!-- ANALISIS SECTION -->.*?</section>', '<!-- ANALISIS SECTION -->\n' + migrated_html, html, flags=re.DOTALL)


# 3. FIX TABLE HEADERS (10 columns)
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

html = html.replace(old_thead, new_thead)

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

html = html.replace(old_pagination, new_pagination)


# 4. APPLY AESTHETICS (Stitch-Level)
google_fonts = """
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  
  <style>
    /* Premium Typography */
    body { font-family: 'Outfit', sans-serif; }
    
    /* Scrollbar minimalista */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.1); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(0,0,0,0.2); }

    /* Micro-animations */
    .saas-card-hover {
      transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .saas-card-hover:hover {
      transform: translateY(-4px);
      box-shadow: 0 20px 40px -10px rgba(0,0,0,0.08), 0 0 0 1px rgba(0,0,0,0.03);
    }

    /* Glassmorphism Sidebar */
    .sidebar-glass {
      background: rgba(17, 17, 17, 0.95);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* Animated Background Orbs */
    .bg-orb {
      position: absolute;
      border-radius: 50%;
      filter: blur(80px);
      z-index: 0;
      animation: floatOrb 20s infinite ease-in-out alternate;
      pointer-events: none;
    }
    .orb-1 { width: 400px; height: 400px; background: rgba(255, 215, 0, 0.15); top: -10%; left: -10%; animation-delay: 0s; }
    .orb-2 { width: 300px; height: 300px; background: rgba(0, 200, 255, 0.1); bottom: 10%; right: -5%; animation-delay: -5s; }
    .orb-3 { width: 350px; height: 350px; background: rgba(255, 100, 150, 0.1); top: 40%; left: 30%; animation-delay: -10s; }

    @keyframes floatOrb {
      0% { transform: translate(0, 0) scale(1); }
      50% { transform: translate(50px, 30px) scale(1.1); }
      100% { transform: translate(-30px, 50px) scale(0.9); }
    }
    
    /* Table hover glow */
    tbody tr { transition: all 0.2s ease; }
    tbody tr:hover { background-color: rgba(255,255,255,0.8); box-shadow: inset 0 0 0 1px rgba(0,0,0,0.05); transform: scale(1.002); z-index: 10; position: relative; }
  </style>
</head>
"""

html = html.replace('</head>', google_fonts)

# Add Background Orbs inside main content area (SAFELY THIS TIME)
orbs_html = """
    <!-- Animated Orbs -->
    <div class="fixed inset-0 pointer-events-none overflow-hidden z-0">
      <div class="bg-orb orb-1"></div>
      <div class="bg-orb orb-2"></div>
      <div class="bg-orb orb-3"></div>
    </div>
"""

# Replace `<main...>` safely
html = re.sub(r'(<main[^>]*>)', r'\g<1>\n' + orbs_html, html, count=1)

# Upgrade Sidebar
sidebar_old = '<aside class="w-64 bg-black text-white p-6 flex flex-col m-4 rounded-[2.5rem] shadow-2xl z-20">'
sidebar_new = '<aside class="w-64 sidebar-glass text-white p-6 flex flex-col m-4 rounded-[2.5rem] shadow-2xl z-20 shadow-black/20 relative">'
html = html.replace(sidebar_old, sidebar_new)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Dashboard HTML perfectly restored and upgraded!")
