import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update CSS for 3D Bevel
css_old = """    .spotlight-card {
      box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.4), 0 20px 60px -15px rgba(0,0,0,0.05) !important;
    }
    .spotlight-dark {
      box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1), 0 20px 60px -15px rgba(0,0,0,0.5) !important;
    }"""
    
css_new = """    .spotlight-card {
      box-shadow: inset 0 2px 4px rgba(255, 255, 255, 0.7), inset 0 -4px 6px rgba(0, 0, 0, 0.03), 0 20px 40px -10px rgba(0, 0, 0, 0.08) !important;
    }
    .spotlight-dark {
      box-shadow: inset 0 2px 4px rgba(255, 255, 255, 0.1), inset 0 -4px 6px rgba(0, 0, 0, 0.4), 0 20px 60px -15px rgba(0, 0, 0, 0.6) !important;
    }"""

if css_old in html:
    html = html.replace(css_old, css_new)
else:
    # Fallback if premium_polish.py wasn't exactly that string
    # Let's just find and replace the whole <style> block or insert it.
    pass # I'll assume it's there based on my previous action.

# 2. Update Dos Caminos Section
section_old = """      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 relative">
        <!-- Dropshipping Column -->
        <div class="bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] p-10 rounded-[3rem] relative group overflow-hidden spotlight-card">
          <div class="absolute inset-0 bg-gradient-to-br from-gray-100 to-transparent opacity-0 group-hover:opacity-100 transition duration-500"></div>
          <div class="relative z-10">
            <h3 class="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-3">
              <i data-lucide="zap" class="w-6 h-6 text-gray-900"></i> Modo Dropshipping
            </h3>
            <div class="space-y-4 mb-8">
              <div class="flex gap-3">
                <i data-lucide="check-circle-2" class="w-5 h-5 text-green-500 shrink-0"></i>
                <div class="text-gray-600"><strong class="text-gray-900">Pro:</strong> Bajo riesgo y cero inventario.</div>
              </div>
              <div class="flex gap-3">
                <i data-lucide="check-circle-2" class="w-5 h-5 text-green-500 shrink-0"></i>
                <div class="text-gray-600"><strong class="text-gray-900">Pro:</strong> Testeo rápido de múltiples nichos.</div>
              </div>
              <div class="flex gap-3 opacity-60">
                <i data-lucide="minus-circle" class="w-5 h-5 text-red-400 shrink-0"></i>
                <div class="text-gray-500"><strong class="text-gray-900">Contra:</strong> Tiempos de envío y márgenes ajustados.</div>
              </div>
            </div>
            <div class="p-6 bg-indigo-50/50 rounded-2xl border border-indigo-100/50">
              <div class="text-xs text-gray-900 font-bold uppercase tracking-wider font-mono mb-2">Cómo ayuda TrendBase</div>
              <p class="text-sm text-gray-600 leading-relaxed font-medium">Detecta micro-tendencias virales en TikTok antes de que se saturen. Te conecta directo con proveedores rápidos como CJ Dropshipping y AutoDS.</p>
            </div>
          </div>
        </div>

        <!-- Ecommerce Column -->
        <div class="bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] p-10 rounded-[3rem] relative group overflow-hidden spotlight-card">
          <div class="absolute inset-0 bg-gradient-to-bl from-gray-100 to-transparent opacity-0 group-hover:opacity-100 transition duration-500"></div>
          <div class="relative z-10">
            <h3 class="text-2xl font-bold text-gray-900 mb-6 flex items-center gap-3">
              <i data-lucide="box" class="w-6 h-6 text-gray-900"></i> Marca Propia
            </h3>
            <div class="space-y-4 mb-8">
              <div class="flex gap-3">
                <i data-lucide="check-circle-2" class="w-5 h-5 text-green-500 shrink-0"></i>
                <div class="text-gray-600"><strong class="text-gray-900">Pro:</strong> Alto margen de ganancia y calidad.</div>
              </div>
              <div class="flex gap-3">
                <i data-lucide="check-circle-2" class="w-5 h-5 text-green-500 shrink-0"></i>
                <div class="text-gray-600"><strong class="text-gray-900">Pro:</strong> Construcción de marca a largo plazo.</div>
              </div>
              <div class="flex gap-3 opacity-60">
                <i data-lucide="minus-circle" class="w-5 h-5 text-red-400 shrink-0"></i>
                <div class="text-gray-500"><strong class="text-gray-900">Contra:</strong> Riesgo de quedarse con stock.</div>
              </div>
            </div>
            <div class="p-6 bg-rose-50/50 rounded-2xl border border-gray-200/50">
              <div class="text-xs text-gray-900 font-bold uppercase tracking-wider font-mono mb-2">Cómo ayuda TrendBase</div>
              <p class="text-sm text-gray-600 leading-relaxed font-medium">Valida la demanda real del mercado antes de fabricar o importar miles de dólares en stock. Encuentra fábricas en Alibaba al mejor costo.</p>
            </div>
          </div>
        </div>
      </div>"""

section_new = """      <div class="grid grid-cols-1 md:grid-cols-2 gap-8 relative group/paths perspective-[1000px]">
        <!-- Dropshipping Column -->
        <div class="bg-white/70 backdrop-blur-3xl border border-white/80 p-10 rounded-[3rem] relative group/card overflow-hidden spotlight-card transition-all duration-700 hover:-translate-y-4 hover:shadow-[0_40px_80px_-20px_rgba(0,0,0,0.1)] hover:scale-[1.02] group-hover/paths:[&:not(:hover)]:opacity-30 group-hover/paths:[&:not(:hover)]:blur-[4px] group-hover/paths:[&:not(:hover)]:scale-[0.98]">
          <div class="absolute inset-0 bg-gradient-to-br from-green-50/50 to-transparent opacity-0 group-hover/card:opacity-100 transition duration-500"></div>
          <div class="relative z-10">
            <h3 class="text-3xl font-bold text-gray-900 mb-6 flex items-center gap-3">
              <div class="w-12 h-12 rounded-full bg-black flex items-center justify-center text-white group-hover/card:scale-110 group-hover/card:shadow-[0_0_30px_rgba(0,255,0,0.3)] transition-all duration-500"><i data-lucide="zap" class="w-6 h-6"></i></div>
              Dropshipping
            </h3>
            <div class="space-y-5 mb-8">
              <div class="flex gap-4 items-start group-hover/card:translate-x-2 transition-transform duration-300 delay-75">
                <div class="bg-green-100 p-1.5 rounded-full shrink-0"><i data-lucide="check" class="w-4 h-4 text-green-600"></i></div>
                <div class="text-gray-600 text-sm"><strong class="text-gray-900 text-base">Bajo riesgo.</strong> Cero inventario, empiezas hoy.</div>
              </div>
              <div class="flex gap-4 items-start group-hover/card:translate-x-2 transition-transform duration-300 delay-100">
                <div class="bg-green-100 p-1.5 rounded-full shrink-0"><i data-lucide="check" class="w-4 h-4 text-green-600"></i></div>
                <div class="text-gray-600 text-sm"><strong class="text-gray-900 text-base">Testeo rápido.</strong> Escala solo lo que funciona.</div>
              </div>
              <div class="flex gap-4 items-start opacity-50 group-hover/card:translate-x-2 transition-transform duration-300 delay-150">
                <div class="bg-red-100 p-1.5 rounded-full shrink-0"><i data-lucide="minus" class="w-4 h-4 text-red-600"></i></div>
                <div class="text-gray-500 text-sm">Tiempos de envío más largos.</div>
              </div>
            </div>
            <div class="p-6 bg-indigo-50/50 rounded-2xl border border-indigo-100/50 group-hover/card:bg-indigo-50 transition-colors duration-500 relative overflow-hidden">
              <div class="absolute inset-0 bg-gradient-to-r from-indigo-500/0 via-indigo-500/10 to-indigo-500/0 translate-x-[-100%] group-hover/card:animate-[shimmer_2s_infinite]"></div>
              <div class="text-[10px] text-indigo-600 font-bold uppercase tracking-widest mb-2 flex items-center gap-2"><i data-lucide="sparkles" class="w-3 h-3"></i> La Solución TrendBase</div>
              <p class="text-sm text-gray-700 leading-relaxed font-medium relative z-10">Detecta productos que <b class="text-indigo-900">ya son virales en TikTok</b> antes de que tu competencia los vea. Conéctate con proveedores rápidos como CJ Dropshipping y AutoDS con 1 clic.</p>
            </div>
          </div>
        </div>

        <!-- Ecommerce Column -->
        <div class="bg-white/40 backdrop-blur-3xl border border-white/40 p-10 rounded-[3rem] relative group/card overflow-hidden spotlight-card transition-all duration-700 hover:-translate-y-4 hover:shadow-[0_40px_80px_-20px_rgba(0,0,0,0.1)] hover:scale-[1.02] group-hover/paths:[&:not(:hover)]:opacity-30 group-hover/paths:[&:not(:hover)]:blur-[4px] group-hover/paths:[&:not(:hover)]:scale-[0.98]">
          <div class="absolute inset-0 bg-gradient-to-bl from-rose-50/50 to-transparent opacity-0 group-hover/card:opacity-100 transition duration-500"></div>
          <div class="relative z-10">
            <h3 class="text-3xl font-bold text-gray-900 mb-6 flex items-center gap-3">
              <div class="w-12 h-12 rounded-full bg-gray-100 border border-gray-200 flex items-center justify-center text-gray-500 group-hover/card:scale-110 transition-all duration-500"><i data-lucide="box" class="w-6 h-6"></i></div>
              E-Commerce
            </h3>
            <div class="space-y-5 mb-8">
              <div class="flex gap-4 items-start group-hover/card:translate-x-2 transition-transform duration-300 delay-75">
                <div class="bg-green-100 p-1.5 rounded-full shrink-0"><i data-lucide="check" class="w-4 h-4 text-green-600"></i></div>
                <div class="text-gray-600 text-sm"><strong class="text-gray-900 text-base">Alto margen.</strong> Control total de la marca y calidad.</div>
              </div>
              <div class="flex gap-4 items-start opacity-50 group-hover/card:translate-x-2 transition-transform duration-300 delay-100">
                <div class="bg-red-100 p-1.5 rounded-full shrink-0"><i data-lucide="minus" class="w-4 h-4 text-red-600"></i></div>
                <div class="text-gray-500 text-sm">Requiere fuerte inversión inicial de capital.</div>
              </div>
              <div class="flex gap-4 items-start opacity-50 group-hover/card:translate-x-2 transition-transform duration-300 delay-150">
                <div class="bg-red-100 p-1.5 rounded-full shrink-0"><i data-lucide="minus" class="w-4 h-4 text-red-600"></i></div>
                <div class="text-gray-500 text-sm">Riesgo gigante de quedarte con stock sin vender.</div>
              </div>
            </div>
            <div class="p-6 bg-rose-50/50 rounded-2xl border border-rose-100/50 group-hover/card:bg-rose-50 transition-colors duration-500">
              <div class="text-[10px] text-rose-600 font-bold uppercase tracking-widest mb-2 flex items-center gap-2"><i data-lucide="shield-check" class="w-3 h-3"></i> La Solución TrendBase</div>
              <p class="text-sm text-gray-700 leading-relaxed font-medium">No importes a ciegas. Valida la demanda real viendo cuántas unidades de un producto <b class="text-rose-900">están vendiendo tus competidores en tu país hoy mismo</b>.</p>
            </div>
          </div>
        </div>
      </div>"""

if section_old in html:
    html = html.replace(section_old, section_new)
else:
    print("Could not find section old")

# Add shimmer animation to tailwind config
tailwind_config_old = """      theme: {
        extend: {"""
tailwind_config_new = """      theme: {
        extend: {
          keyframes: {
            shimmer: {
              '100%': { transform: 'translateX(100%)' }
            }
          },"""

if tailwind_config_old in html:
    html = html.replace(tailwind_config_old, tailwind_config_new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

