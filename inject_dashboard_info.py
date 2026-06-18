import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_sections_html = """    <!-- Info Section: Oportunidades & Calculadora ROI -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- Oportunidades List -->
      <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover flex flex-col">
        <div class="flex justify-between items-center mb-6">
          <h3 class="font-bold text-gray-800">Top Oportunidades</h3>
          <span class="text-[10px] font-bold text-green-600 bg-green-50 px-2 py-1 rounded-md uppercase tracking-wider">Alta Rentabilidad</span>
        </div>
        <div id="oppList" class="flex flex-col gap-3 flex-1">
          <!-- Injected via JS -->
          <div class="text-sm text-gray-400 text-center py-4 font-medium">Cargando oportunidades...</div>
        </div>
      </div>

      <!-- ROI Calculator -->
      <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover flex flex-col">
        <h3 class="font-bold text-gray-800 mb-6 flex items-center gap-2"><i data-lucide="calculator" class="w-4 h-4 text-gray-500"></i> Calculadora ROI</h3>
        <div class="space-y-4 flex-1 flex flex-col">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-[11px] font-bold text-gray-500 uppercase tracking-wider mb-1.5">Costo Base ($)</label>
              <input type="number" id="calcCost" value="15" oninput="calcROI()" class="w-full bg-gray-50 border border-gray-200 rounded-xl px-3 py-2 text-sm font-bold text-gray-900 outline-none focus:border-gray-400 transition">
            </div>
            <div>
              <label class="block text-[11px] font-bold text-gray-500 uppercase tracking-wider mb-1.5">Precio Venta ($)</label>
              <input type="number" id="calcPrice" value="49" oninput="calcROI()" class="w-full bg-gray-50 border border-gray-200 rounded-xl px-3 py-2 text-sm font-bold text-gray-900 outline-none focus:border-gray-400 transition">
            </div>
            <div>
              <label class="block text-[11px] font-bold text-gray-500 uppercase tracking-wider mb-1.5">Costo Ads/venta</label>
              <input type="number" id="calcAds" value="8" oninput="calcROI()" class="w-full bg-gray-50 border border-gray-200 rounded-xl px-3 py-2 text-sm font-bold text-gray-900 outline-none focus:border-gray-400 transition">
            </div>
            <div>
              <label class="block text-[11px] font-bold text-gray-500 uppercase tracking-wider mb-1.5">Ventas/mes est.</label>
              <input type="number" id="calcSales" value="50" oninput="calcROI()" class="w-full bg-gray-50 border border-gray-200 rounded-xl px-3 py-2 text-sm font-bold text-gray-900 outline-none focus:border-gray-400 transition">
            </div>
          </div>
          <div id="calcResult" class="mt-auto bg-gray-50 rounded-xl p-4 border border-gray-100 flex flex-col gap-2">
            <!-- Results via JS -->
          </div>
        </div>
      </div>

      <!-- Quick Stats / Leaderboard preview -->
      <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover flex flex-col">
        <h3 class="font-bold text-gray-800 mb-6 flex items-center gap-2"><i data-lucide="award" class="w-4 h-4 text-gray-500"></i> Tu Racha</h3>
        <div class="flex-1 flex flex-col items-center justify-center text-center space-y-4">
          <div class="w-20 h-20 rounded-full border-4 border-gray-100 flex items-center justify-center shadow-inner relative">
            <span class="text-3xl">🔥</span>
            <div class="absolute -bottom-2 bg-black text-white text-[10px] font-bold px-2 py-0.5 rounded-full">NIVEL 1</div>
          </div>
          <div>
            <div class="text-3xl font-extrabold text-gray-900">0 Ventas</div>
            <div class="text-xs font-medium text-gray-500 mt-1">Registradas este mes</div>
          </div>
          <div class="w-full bg-gray-100 h-2 rounded-full mt-2">
            <div class="bg-black h-full rounded-full" style="width: 10%"></div>
          </div>
          <div class="text-[10px] text-gray-400 font-bold uppercase tracking-widest mt-1">10 ventas para Nivel 2</div>
        </div>
      </div>

    </div>

    """

if '<!-- Info Section: Oportunidades & Calculadora ROI -->' not in html:
    html = html.replace('<!-- Products Table -->', new_sections_html + '<!-- Products Table -->')

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
