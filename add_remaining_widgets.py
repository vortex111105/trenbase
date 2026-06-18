import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. REMOVE SIDEBAR CATEGORIES AND PLATFORMS
html = re.sub(r'<div class="px-4 pt-6 border-t border-white/10 mt-2">.*?<span[^>]*>Categorías</span>.*?</div>\s*</div>', '', html, flags=re.DOTALL)
html = re.sub(r'<div class="px-4 pt-6 border-t border-white/10 mt-4">.*?<span[^>]*>Plataformas</span>.*?</div>\s*</div>', '', html, flags=re.DOTALL)

# 2. ADD CATEGORIES AND PLATFORMS SELECTORS TO TENDENCIAS TOP BAR
tendencias_filters_pattern = r'(<select class="bg-white border border-gray-200 rounded-xl px-4 py-2 text-xs font-bold text-gray-700 outline-none focus:border-gray-400 saas-shadow-sm">\s*<option value="score">TrendScore</option>\s*<option value="change">Crecimiento</option>\s*<option value="margin">Margen</option>\s*</select>\s*</div>)'

cat_plat_selectors = """
          <select class="bg-white border border-gray-200 rounded-xl px-4 py-2 text-xs font-bold text-gray-700 outline-none focus:border-gray-400 saas-shadow-sm">
            <option value="">Categorías (Todas)</option>
            <option value="tech">💻 Tecnología</option>
            <option value="beauty">✨ Belleza</option>
            <option value="home">🏠 Hogar</option>
          </select>
          <select class="bg-white border border-gray-200 rounded-xl px-4 py-2 text-xs font-bold text-gray-700 outline-none focus:border-gray-400 saas-shadow-sm">
            <option value="">Plataformas (Todas)</option>
            <option value="tt">📱 TikTok</option>
            <option value="ig">📸 Instagram</option>
            <option value="amz">🛒 Amazon</option>
          </select>
"""
if 'Categorías (Todas)' not in html:
    html = re.sub(tendencias_filters_pattern, cat_plat_selectors + r'\1', html)

# 3. ADD MISSING WIDGETS TO ANALYSIS SECTION
# Find the end of the Analysis section (before section alertas)
analisis_end_pattern = r'(</section>\s*<!-- ALERTAS SECTION -->)'

new_analysis_widgets = """
      <!-- NUEVOS WIDGETS COMPETITIVOS -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
        <!-- Índice de Saturación -->
        <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover space-y-4 relative overflow-hidden flex flex-col">
          <h3 class="font-bold text-gray-800 border-b border-gray-100 pb-2 flex items-center gap-2"><i data-lucide="thermometer" class="w-4 h-4 text-gray-500"></i> Índice de Saturación</h3>
          <div class="flex flex-col items-center justify-center pt-4 pb-2 flex-1">
            <div class="relative w-40 h-20 overflow-hidden mb-2">
              <div class="absolute inset-0 bg-gradient-to-r from-green-400 via-yellow-400 to-red-500 rounded-t-full opacity-80"></div>
              <div class="absolute bottom-0 left-[12%] right-[12%] top-[24%] bg-white rounded-t-full"></div>
              <div class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-2 h-14 origin-bottom rotate-[-50deg] z-10 transition-transform duration-1000">
                <div class="w-1 h-full bg-black mx-auto rounded-t-full"></div>
                <div class="w-3 h-3 rounded-full bg-black absolute bottom-0 left-1/2 transform -translate-x-1/2"></div>
              </div>
            </div>
            <div class="text-3xl font-extrabold text-green-500">24%</div>
            <div class="text-xs font-bold text-green-500 uppercase tracking-widest mt-1">Oportunidad Temprana</div>
          </div>
          <div class="text-[10px] text-gray-500 text-center leading-relaxed mt-auto">
            El volumen de búsquedas es dinámico, y actualmente hay <strong class="text-gray-900">12 tiendas</strong> escalándolo en LATAM.
          </div>
        </div>

        <!-- Perfil de Audiencia Objetivo -->
        <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover space-y-4 flex flex-col">
          <h3 class="font-bold text-gray-800 border-b border-gray-100 pb-2 flex items-center gap-2"><i data-lucide="users" class="w-4 h-4 text-gray-500"></i> Audiencia Objetivo (Ads)</h3>
          <div class="space-y-4 pt-2 flex-1">
            <div>
              <div class="flex justify-between text-[10px] text-gray-500 font-bold mb-1">
                <span>Mujeres (75%)</span>
                <span>Hombres (25%)</span>
              </div>
              <div class="w-full h-2 bg-gray-100 rounded-full overflow-hidden flex">
                <div class="h-full bg-pink-400 w-[75%]"></div>
                <div class="h-full bg-blue-400 w-[25%]"></div>
              </div>
            </div>
            <div>
              <div class="text-xs text-gray-800 mb-1 font-bold">Edades de mayor conversión:</div>
              <div class="flex gap-2">
                <span class="px-2 py-1 bg-gray-100 rounded-md text-[10px] font-mono text-gray-600">18-24</span>
                <span class="px-2 py-1 bg-black rounded-md text-[10px] font-mono text-white font-bold saas-shadow-sm">25-34 (Top)</span>
                <span class="px-2 py-1 bg-gray-100 rounded-md text-[10px] font-mono text-gray-600">35-44</span>
              </div>
            </div>
            <div>
              <div class="text-xs text-gray-800 mb-1 font-bold">Intereses sugeridos:</div>
              <div class="flex flex-wrap gap-1.5">
                <span class="px-2 py-1 text-[9px] uppercase bg-gray-50 border border-gray-200 rounded-full text-gray-500 font-bold">Cuidado de la piel</span>
                <span class="px-2 py-1 text-[9px] uppercase bg-gray-50 border border-gray-200 rounded-full text-gray-500 font-bold">Spa en casa</span>
                <span class="px-2 py-1 text-[9px] uppercase bg-gray-50 border border-gray-200 rounded-full text-gray-500 font-bold">Belleza coreana</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Espía de Anuncios (Ads Spy) -->
        <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover space-y-4 flex flex-col">
          <h3 class="font-bold text-gray-800 border-b border-gray-100 pb-2 flex items-center gap-2"><i data-lucide="video" class="w-4 h-4 text-gray-500"></i> Creativos Ganadores</h3>
          <p class="text-[10px] text-gray-500 font-bold">Top videos escalando en TikTok Ads</p>
          <div class="grid grid-cols-2 gap-3 flex-1">
            <div class="relative aspect-[9/16] bg-gray-900 rounded-xl overflow-hidden group cursor-pointer border border-gray-100 saas-shadow-sm">
              <img src="https://images.unsplash.com/photo-1611162617474-5b21e879e113?q=80&w=200&auto=format&fit=crop" class="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition group-hover:scale-105 duration-500">
              <div class="absolute inset-0 flex items-center justify-center">
                <div class="w-8 h-8 rounded-full bg-white/80 backdrop-blur-sm flex items-center justify-center shadow-md">
                  <i data-lucide="play" class="w-4 h-4 text-black fill-current"></i>
                </div>
              </div>
              <div class="absolute bottom-2 left-2 text-[8px] font-bold text-gray-900 bg-white/90 px-1.5 py-0.5 rounded shadow-sm">1.2M Vistas</div>
            </div>
            <div class="relative aspect-[9/16] bg-gray-900 rounded-xl overflow-hidden group cursor-pointer border border-gray-100 saas-shadow-sm">
              <img src="https://images.unsplash.com/photo-1522337660859-02fbefca4702?q=80&w=200&auto=format&fit=crop" class="w-full h-full object-cover opacity-80 group-hover:opacity-100 transition group-hover:scale-105 duration-500">
              <div class="absolute inset-0 flex items-center justify-center">
                <div class="w-8 h-8 rounded-full bg-white/80 backdrop-blur-sm flex items-center justify-center shadow-md">
                  <i data-lucide="play" class="w-4 h-4 text-black fill-current"></i>
                </div>
              </div>
              <div class="absolute bottom-2 left-2 text-[8px] font-bold text-gray-900 bg-white/90 px-1.5 py-0.5 rounded shadow-sm">850K Vistas</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Asistente de IA -->
      <div class="bg-white rounded-[2rem] saas-shadow overflow-hidden flex flex-col mt-6 border border-gray-100">
        <div class="px-6 py-4 border-b border-gray-100 bg-gray-50 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-green-500 animate-pulse"></span>
            <span class="text-sm font-extrabold text-gray-900">Asistente IA TrendBase</span>
          </div>
          <span class="text-[9px] font-mono text-gray-400 uppercase font-bold tracking-widest bg-gray-200 px-2 py-1 rounded-md">Anthropic Claude Engine</span>
        </div>
        
        <div class="p-6 h-64 overflow-y-auto space-y-4 flex flex-col text-sm bg-white">
          <div class="bg-gray-100 text-gray-800 p-4 rounded-2xl rounded-tl-sm max-w-[85%] self-start saas-shadow-sm">
            <p class="font-medium text-xs leading-relaxed">¡Hola! Soy tu asistente de tendencias de TrendBase. ¿Sobre qué producto te gustaría que analicemos su estrategia, estimación de márgenes o canales de reventa en LATAM?</p>
          </div>
        </div>

        <div class="px-6 py-4 border-t border-gray-100 flex gap-3 items-center bg-gray-50">
          <input type="text" placeholder="Pregúntame sobre estrategias de venta..." class="flex-1 bg-white border border-gray-200 rounded-xl px-4 py-3 text-sm text-gray-900 placeholder-gray-400 outline-none focus:border-gray-400 transition saas-shadow-sm">
          <button class="bg-black text-white px-6 py-3 rounded-xl text-xs font-extrabold uppercase tracking-wider saas-shadow hover:-translate-y-0.5 transition flex items-center gap-2">Enviar <i data-lucide="send" class="w-4 h-4"></i></button>
        </div>
      </div>
"""
if 'Creativos Ganadores' not in html:
    html = re.sub(analisis_end_pattern, new_analysis_widgets + r'\n    \1', html)

# 4. RESTORE ALERTAS LIST
alertas_empty_pattern = r'(<div class="bg-white rounded-\[2rem\] p-12 saas-shadow flex flex-col items-center justify-center text-center h-\[400px\]">.*?</div>\s*</section>)'
alertas_real = """
      <div class="flex justify-between items-center mb-6">
        <button class="text-xs text-gray-500 font-bold uppercase tracking-wider hover:text-gray-900 transition flex items-center gap-2"><i data-lucide="check-check" class="w-4 h-4"></i> Marcar todas como leídas</button>
      </div>
      <div class="bg-white rounded-[2rem] saas-shadow overflow-hidden divide-y divide-gray-100 border border-gray-100">
        <!-- Alerta 1 -->
        <div class="p-6 flex items-start gap-4 hover:bg-gray-50 transition cursor-pointer group">
          <div class="w-10 h-10 rounded-full bg-red-50 flex items-center justify-center flex-shrink-0 group-hover:bg-red-100 transition">
            <i data-lucide="alert-triangle" class="w-5 h-5 text-red-500"></i>
          </div>
          <div class="flex-1">
            <div class="text-sm font-bold text-gray-900">Alerta de Stock Bajo: Humidificador de Llama</div>
            <p class="text-xs text-gray-500 mt-1 leading-relaxed">Quedan solo 2 unidades disponibles en CJ Dropshipping a precio promocional.</p>
            <span class="text-[9px] font-mono text-gray-400 uppercase mt-2 block font-bold tracking-wider">Hace 15 minutos</span>
          </div>
        </div>
        <!-- Alerta 2 -->
        <div class="p-6 flex items-start gap-4 hover:bg-gray-50 transition cursor-pointer group">
          <div class="w-10 h-10 rounded-full bg-orange-50 flex items-center justify-center flex-shrink-0 group-hover:bg-orange-100 transition">
            <i data-lucide="trending-up" class="w-5 h-5 text-orange-500"></i>
          </div>
          <div class="flex-1">
            <div class="text-sm font-bold text-gray-900">Pico de Tendencia: Trípode Inteligente con IA</div>
            <p class="text-xs text-gray-500 mt-1 leading-relaxed">El score del producto subió +18% en las últimas 24 horas debido a alta viralidad en TikTok Chile.</p>
            <span class="text-[9px] font-mono text-gray-400 uppercase mt-2 block font-bold tracking-wider">Hace 2 horas</span>
          </div>
        </div>
        <!-- Alerta 3 -->
        <div class="p-6 flex items-start gap-4 hover:bg-gray-50 transition cursor-pointer group">
          <div class="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center flex-shrink-0 group-hover:bg-blue-100 transition">
            <i data-lucide="rocket" class="w-5 h-5 text-blue-500"></i>
          </div>
          <div class="flex-1">
            <div class="text-sm font-bold text-gray-900">Nuevo Producto Viral Detectado</div>
            <p class="text-xs text-gray-500 mt-1 leading-relaxed">Agregado al catálogo: Depiladora Láser IPL Pro con estimación de margen superior al 55%.</p>
            <span class="text-[9px] font-mono text-gray-400 uppercase mt-2 block font-bold tracking-wider">Hace 1 día</span>
          </div>
        </div>
      </div>
    </section>
"""
if 'Alerta de Stock Bajo: Humidificador de Llama' not in html:
    html = re.sub(alertas_empty_pattern, alertas_real, html, flags=re.DOTALL)

# 5. ADD + CARGAR PRODUCTO TO NEGOCIO
negocio_header_pattern = r'(<h2 class="text-2xl font-extrabold text-gray-900 tracking-tight">Mi Negocio</h2>\s*<p class="text-xs text-gray-500 mt-1">Registra tus ventas y sube de nivel</p>\s*</div>)'
negocio_button = r'\1\n        <button class="bg-black text-white px-5 py-2.5 rounded-full text-xs font-bold uppercase tracking-wider saas-shadow hover:-translate-y-0.5 transition flex items-center gap-2"><i data-lucide="plus" class="w-4 h-4"></i> Cargar Producto</button>'
if 'Cargar Producto' not in html:
    html = re.sub(negocio_header_pattern, negocio_button, html)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
