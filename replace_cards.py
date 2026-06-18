import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_cards = """    <!-- Top Cards Grid (Skillset Style) -->
    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
      
      <!-- Black Card (Hero) -->
      <div class="bg-[#1C1C1E] rounded-3xl p-6 relative overflow-hidden saas-shadow shadow-black/20 saas-card-hover flex flex-col justify-between h-40 cursor-pointer" onclick="openProduct(0)">
        <div class="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent opacity-50"></div>
        <div class="relative z-10">
          <div class="text-[13px] text-white/60 font-medium mb-1" id="heroCat">Oportunidad #1</div>
          <div class="text-3xl font-bold text-white tracking-tight leading-tight truncate" id="heroTitle">Cargando...</div>
        </div>
        <div class="relative z-10 mt-auto flex items-center text-[11px] font-bold text-green-400">
          <i data-lucide="trending-up" class="w-3 h-3 mr-1"></i> <span id="heroScore">0</span> TrendScore
        </div>
      </div>

      <!-- White Card 1 -->
      <div class="bg-white rounded-3xl p-6 flex flex-col justify-between saas-shadow saas-card-hover h-40">
        <div>
          <div class="text-[13px] text-gray-500 font-medium mb-1">Productos Trackeados</div>
          <div class="text-3xl font-bold text-gray-900 tracking-tight leading-tight" id="kpiTotal">0+</div>
        </div>
        <div class="mt-auto flex items-center text-[11px] font-bold text-green-500">
          <i data-lucide="trending-up" class="w-3 h-3 mr-1"></i> +12% vs mes anterior
        </div>
      </div>

      <!-- White Card 2 -->
      <div class="bg-white rounded-3xl p-6 flex flex-col justify-between saas-shadow saas-card-hover h-40">
        <div>
          <div class="text-[13px] text-gray-500 font-medium mb-1">Promedio ROI</div>
          <div class="text-3xl font-bold text-gray-900 tracking-tight leading-tight">68%</div>
        </div>
        <div class="mt-auto flex items-center text-[11px] font-bold text-green-500">
          <i data-lucide="trending-up" class="w-3 h-3 mr-1"></i> +4.2% vs mes anterior
        </div>
      </div>

      <!-- White Card 3 -->
      <div class="bg-white rounded-3xl p-6 flex flex-col justify-between saas-shadow saas-card-hover h-40">
        <div>
          <div class="text-[13px] text-gray-500 font-medium mb-1">Tendencias Nuevas</div>
          <div class="text-3xl font-bold text-gray-900 tracking-tight leading-tight">142</div>
        </div>
        <div class="mt-auto flex items-center text-[11px] font-bold text-red-500">
          <i data-lucide="trending-down" class="w-3 h-3 mr-1"></i> -2.9% vs mes anterior
        </div>
      </div>

    </div>"""

# Find the start and end of Top Cards Grid
start_marker = "<!-- Top Cards Grid -->"
end_marker = "<!-- Charts Section -->"

start_idx = html.find(start_marker)
end_idx = html.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_html = html[:start_idx] + new_cards + "\n\n    " + html[end_idx:]
    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Replaced cards successfully.")
else:
    print("Could not find markers.")
