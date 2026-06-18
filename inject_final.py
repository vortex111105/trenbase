import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

leaderboard_and_manifiesto = """
  <!-- Leaderboard Section -->
  <section id="leaderboard" class="py-24 bg-white relative z-20">
    <div class="max-w-7xl mx-auto px-6 md:px-12">
      <div class="text-center mb-16">
        <span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest block mb-4">Comunidad Activa</span>
        <h2 class="text-3xl md:text-5xl font-black text-gray-900 tracking-tight">Productos que están volando</h2>
        <p class="text-gray-500 font-medium mt-4 max-w-xl mx-auto">
          Muestra en tiempo real de los productos con mayor tracción registrados por dropshippers activos hoy.
        </p>
      </div>

      <!-- Live Stats -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-16 text-center">
        <div class="bg-gray-50 border border-gray-100 rounded-3xl p-8 saas-shadow hover:-translate-y-1 transition-transform">
          <div class="text-4xl font-extrabold text-gray-900 mb-2">12,450</div>
          <div class="text-[10px] text-gray-500 uppercase font-bold tracking-wider">Ventas registradas hoy</div>
        </div>
        <div class="bg-gray-50 border border-gray-100 rounded-3xl p-8 saas-shadow hover:-translate-y-1 transition-transform">
          <div class="text-4xl font-extrabold text-gray-900 mb-2">842</div>
          <div class="text-[10px] text-gray-500 uppercase font-bold tracking-wider">Vendedores activos</div>
        </div>
        <div class="bg-gray-50 border border-gray-100 rounded-3xl p-8 saas-shadow hover:-translate-y-1 transition-transform">
          <div class="text-xl font-black text-gray-900 mt-2 mb-3">Cortador Invisible</div>
          <div class="text-[10px] text-gray-500 uppercase font-bold tracking-wider">Producto estrella (24hs)</div>
        </div>
      </div>

      <!-- Product Cards Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        
        <!-- Prod 1 -->
        <div class="bg-white border border-gray-100 rounded-3xl overflow-hidden saas-shadow hover:-translate-y-2 transition-transform duration-300">
          <div class="h-40 bg-gray-100 flex items-center justify-center relative">
            <span class="absolute top-3 right-3 bg-pink-100 text-pink-700 text-[10px] font-bold px-2 py-1 rounded-lg">Score: 99</span>
            <i data-lucide="image" class="w-8 h-8 text-gray-300"></i>
          </div>
          <div class="p-5">
            <div class="text-[10px] text-gray-400 font-bold uppercase tracking-wider mb-1">Hogar</div>
            <h4 class="font-bold text-gray-900 mb-3 truncate">Cortador de Verduras</h4>
            <div class="flex items-center justify-between">
              <span class="text-sm font-bold text-green-600">Margen: 51%</span>
              <span class="text-xs font-mono text-gray-500">$61 - $83</span>
            </div>
          </div>
        </div>

        <!-- Prod 2 -->
        <div class="bg-white border border-gray-100 rounded-3xl overflow-hidden saas-shadow hover:-translate-y-2 transition-transform duration-300">
          <div class="h-40 bg-gray-100 flex items-center justify-center relative">
            <span class="absolute top-3 right-3 bg-pink-100 text-pink-700 text-[10px] font-bold px-2 py-1 rounded-lg">Score: 99</span>
            <i data-lucide="image" class="w-8 h-8 text-gray-300"></i>
          </div>
          <div class="p-5">
            <div class="text-[10px] text-gray-400 font-bold uppercase tracking-wider mb-1">Tecnología</div>
            <h4 class="font-bold text-gray-900 mb-3 truncate">Teclado Ultra HD</h4>
            <div class="flex items-center justify-between">
              <span class="text-sm font-bold text-green-600">Margen: 48%</span>
              <span class="text-xs font-mono text-gray-500">$124 - $145</span>
            </div>
          </div>
        </div>

        <!-- Prod 3 -->
        <div class="bg-white border border-gray-100 rounded-3xl overflow-hidden saas-shadow hover:-translate-y-2 transition-transform duration-300">
          <div class="h-40 bg-gray-100 flex items-center justify-center relative">
            <span class="absolute top-3 right-3 bg-gray-100 text-gray-600 text-[10px] font-bold px-2 py-1 rounded-lg">Score: 98</span>
            <i data-lucide="image" class="w-8 h-8 text-gray-300"></i>
          </div>
          <div class="p-5">
            <div class="text-[10px] text-gray-400 font-bold uppercase tracking-wider mb-1">Tecnología</div>
            <h4 class="font-bold text-gray-900 mb-3 truncate">Organizador de Cables</h4>
            <div class="flex items-center justify-between">
              <span class="text-sm font-bold text-green-600">Margen: 79%</span>
              <span class="text-xs font-mono text-gray-500">$24 - $35</span>
            </div>
          </div>
        </div>

        <!-- Prod 4 -->
        <div class="bg-white border border-gray-100 rounded-3xl overflow-hidden saas-shadow hover:-translate-y-2 transition-transform duration-300">
          <div class="h-40 bg-gray-100 flex items-center justify-center relative">
            <span class="absolute top-3 right-3 bg-gray-100 text-gray-600 text-[10px] font-bold px-2 py-1 rounded-lg">Score: 98</span>
            <i data-lucide="image" class="w-8 h-8 text-gray-300"></i>
          </div>
          <div class="p-5">
            <div class="text-[10px] text-gray-400 font-bold uppercase tracking-wider mb-1">Deportes</div>
            <h4 class="font-bold text-gray-900 mb-3 truncate">Gorro Natación Avanzado</h4>
            <div class="flex items-center justify-between">
              <span class="text-sm font-bold text-green-600">Margen: 40%</span>
              <span class="text-xs font-mono text-gray-500">$43 - $68</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- Manifesto Section (Transition to dark) -->
  <section id="philosophy" class="py-32 bg-gray-100 relative z-20 border-b border-gray-200">
    <div class="max-w-4xl mx-auto px-6 text-center">
      <span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest block mb-8">El Manifiesto TrendBase</span>
      
      <p class="text-gray-500 text-lg font-medium tracking-wide max-w-2xl mx-auto leading-relaxed mb-6">
        La mayoría de los vendedores buscan productos a ciegas, basándose en la intuición y perdiendo tiempo y dinero en campañas que no convierten.
      </p>
      
      <h2 class="text-4xl md:text-6xl font-black text-gray-900 leading-tight tracking-tight">
        Nosotros nos enfocamos en el <br class="hidden md:block">
        <span class="text-black italic bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-500">Monitoreo Científico.</span>
      </h2>
    </div>
  </section>
"""

# Insert right before the Pricing section
pricing_start = html.find('<!-- Pricing Section (Dark Glassmorphism) -->')
html = html[:pricing_start] + leaderboard_and_manifiesto + "\n  " + html[pricing_start:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
