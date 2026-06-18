import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# HTML to insert
features_and_protocol = """
  <!-- Features Section -->
  <section id="features" class="py-24 bg-white relative z-20">
    <div class="max-w-7xl mx-auto px-6 md:px-12">
      <div class="mb-16 text-center">
        <span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest block mb-4">Métrica y Precisión</span>
        <h2 class="text-3xl md:text-5xl font-black text-gray-900 tracking-tight">Todo para vender en tendencia</h2>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        <!-- Feature 1 -->
        <div class="bg-gray-50 rounded-[2.5rem] p-10 flex flex-col justify-between hover:-translate-y-2 transition-transform duration-300 border border-gray-100 saas-shadow">
          <div>
            <div class="w-14 h-14 rounded-2xl bg-white saas-shadow flex items-center justify-center mb-8">
              <i data-lucide="flame" class="w-6 h-6 text-black"></i>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-4">Monitoreo en tiempo real</h3>
            <p class="text-gray-500 leading-relaxed font-medium">
              Rastreo continuo de 47k+ productos en plataformas líderes como TikTok, Amazon y Mercado Libre para que encuentres tendencias antes de que se saturen.
            </p>
          </div>
        </div>

        <!-- Feature 2 -->
        <div class="bg-gray-50 rounded-[2.5rem] p-10 flex flex-col justify-between hover:-translate-y-2 transition-transform duration-300 border border-gray-100 saas-shadow">
          <div>
            <div class="w-14 h-14 rounded-2xl bg-white saas-shadow flex items-center justify-center mb-8">
              <i data-lucide="globe" class="w-6 h-6 text-black"></i>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-4">Precios localizados</h3>
            <p class="text-gray-500 leading-relaxed font-medium">
              Obtén datos específicos para LATAM en ARS, UYU y CLP. Evalúa el historial de tendencia de 90 días para mitigar riesgos antes de invertir un solo centavo.
            </p>
          </div>
        </div>

        <!-- Feature 3 -->
        <div class="bg-gray-50 rounded-[2.5rem] p-10 flex flex-col justify-between hover:-translate-y-2 transition-transform duration-300 border border-gray-100 saas-shadow">
          <div>
            <div class="w-14 h-14 rounded-2xl bg-white saas-shadow flex items-center justify-center mb-8">
              <i data-lucide="calculator" class="w-6 h-6 text-black"></i>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-4">Filtros de rentabilidad</h3>
            <p class="text-gray-500 leading-relaxed font-medium">
              Cálculo automático de margen de ganancia estimado, nivel de competencia del nicho y estimación de retorno de inversión por producto.
            </p>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- Protocol Section -->
  <section id="protocol" class="py-24 bg-bgmain border-y border-gray-100 relative z-20">
    <div class="max-w-5xl mx-auto px-6 md:px-12">
      <div class="mb-20 text-center">
        <span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest block mb-4">Cómo Funciona</span>
        <h2 class="text-3xl md:text-5xl font-black text-gray-900 tracking-tight">El Protocolo TrendBase</h2>
      </div>

      <div class="space-y-12 relative">
        <!-- Connecting Line -->
        <div class="absolute left-8 top-10 bottom-10 w-0.5 bg-gray-200 hidden md:block z-0"></div>

        <!-- Step 1 -->
        <div class="relative z-10 flex flex-col md:flex-row gap-8 items-start">
          <div class="w-16 h-16 rounded-full bg-white border border-gray-200 saas-shadow flex items-center justify-center flex-shrink-0 relative">
            <span class="font-black text-xl text-gray-900">01</span>
          </div>
          <div class="bg-white rounded-[2rem] p-8 saas-shadow border border-gray-100 flex-1 hover:-translate-y-1 transition-transform">
            <h3 class="text-2xl font-bold text-gray-900 mb-3">Extracción Multiplataforma</h3>
            <p class="text-gray-500 font-medium leading-relaxed">
              Nuestros motores analizan millones de señales de comportamiento de usuario en TikTok, Amazon, Instagram y Mercado Libre cada hora. Almacenamos métricas de volumen y viralidad crudas listas para su evaluación estadística.
            </p>
          </div>
        </div>

        <!-- Step 2 -->
        <div class="relative z-10 flex flex-col md:flex-row gap-8 items-start">
          <div class="w-16 h-16 rounded-full bg-black border-4 border-gray-100 shadow-xl flex items-center justify-center flex-shrink-0 relative">
            <span class="font-black text-xl text-white">02</span>
          </div>
          <div class="bg-white rounded-[2rem] p-8 saas-shadow border border-gray-100 flex-1 hover:-translate-y-1 transition-transform transform md:scale-105 z-20 shadow-xl">
            <h3 class="text-2xl font-bold text-gray-900 mb-3">Algoritmo de Tendencia</h3>
            <p class="text-gray-500 font-medium leading-relaxed">
              Combinamos datos de volumen de búsqueda, tasa de interacción (engagement) en redes sociales, nivel de competencia publicitaria y volumen de ventas históricas para generar un <strong class="text-black">TrendScore</strong> exacto que define el potencial de rentabilidad de cada producto.
            </p>
          </div>
        </div>

        <!-- Step 3 -->
        <div class="relative z-10 flex flex-col md:flex-row gap-8 items-start">
          <div class="w-16 h-16 rounded-full bg-white border border-gray-200 saas-shadow flex items-center justify-center flex-shrink-0 relative">
            <span class="font-black text-xl text-gray-900">03</span>
          </div>
          <div class="bg-white rounded-[2rem] p-8 saas-shadow border border-gray-100 flex-1 hover:-translate-y-1 transition-transform">
            <h3 class="text-2xl font-bold text-gray-900 mb-3">Validación y Localización</h3>
            <p class="text-gray-500 font-medium leading-relaxed">
              Convertimos todas las métricas al ecosistema LATAM. Te brindamos enlaces directos de proveedores validados (Dropshipping, Mayoristas o AliExpress) para que puedas importar el producto a tu tienda en 1 clic.
            </p>
          </div>
        </div>

      </div>
    </div>
  </section>
"""

# Insert right before the Pricing section
pricing_start = html.find('<!-- Pricing Section (Dark Glassmorphism) -->')
html = html[:pricing_start] + features_and_protocol + "\n  " + html[pricing_start:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
