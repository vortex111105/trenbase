import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add Marquee animation to style tag
style_addition = """
    @keyframes marquee {
      0% { transform: translateX(0%); }
      100% { transform: translateX(-50%); }
    }
    .animate-marquee {
      animation: marquee 25s linear infinite;
    }
"""
html = html.replace('</style>', style_addition + '\n  </style>')

# 2. Build the new sections
demo_video = """
    <!-- Demo Video Section (SaaS Style) -->
    <div class="mt-20 relative max-w-5xl w-full" id="demo">
      <span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest block mb-4">Conoce TrendBase por dentro</span>
      <div class="relative w-full aspect-video rounded-[2.5rem] overflow-hidden border-8 border-white bg-gray-50 saas-shadow group cursor-pointer">
        <div class="absolute inset-0 flex flex-col items-center justify-center bg-black/10 backdrop-blur-[2px] z-10 transition-opacity duration-300 group-hover:bg-black/20">
          <div class="w-20 h-20 bg-white text-black rounded-full flex items-center justify-center shadow-2xl transform group-hover:scale-110 transition-all duration-300">
            <i data-lucide="play" class="w-8 h-8 ml-1"></i>
          </div>
        </div>
        <!-- Native HTML5 Video -->
        <video class="w-full h-full object-cover grayscale opacity-80" poster="https://images.unsplash.com/photo-1460925895917-afdab827c52f?ixlib=rb-4.0.3&auto=format&fit=crop&w=2000&q=80"></video>
      </div>
    </div>
"""

integrations_and_stats = """
  <!-- Trust Element: Integration Banner -->
  <section class="py-12 bg-white border-y border-gray-100 overflow-hidden relative z-20">
    <div class="absolute inset-y-0 left-0 w-32 bg-gradient-to-r from-white to-transparent z-10 pointer-events-none"></div>
    <div class="absolute inset-y-0 right-0 w-32 bg-gradient-to-l from-white to-transparent z-10 pointer-events-none"></div>
    
    <div class="max-w-7xl mx-auto px-6 mb-6 text-center">
      <span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">TrendBase escanea el ecosistema de</span>
    </div>
    
    <div class="flex w-[200%] animate-marquee">
      <!-- Group 1 -->
      <div class="flex w-1/2 justify-around items-center gap-12 px-6">
        <div class="flex items-center gap-3 text-gray-400 font-bold text-xl hover:text-gray-900 transition duration-300"><i data-lucide="shopping-bag" class="w-6 h-6"></i> Shopify</div>
        <div class="flex items-center gap-3 text-gray-400 font-bold text-xl hover:text-gray-900 transition duration-300"><i data-lucide="shopping-cart" class="w-6 h-6"></i> Tiendanube</div>
        <div class="flex items-center gap-3 text-gray-400 font-bold text-xl hover:text-gray-900 transition duration-300"><i data-lucide="package" class="w-6 h-6"></i> Mercado Libre</div>
        <div class="flex items-center gap-3 text-gray-400 font-bold text-xl hover:text-gray-900 transition duration-300"><i data-lucide="box" class="w-6 h-6"></i> Amazon</div>
        <div class="flex items-center gap-3 text-gray-400 font-bold text-xl hover:text-gray-900 transition duration-300"><i data-lucide="instagram" class="w-6 h-6"></i> TikTok</div>
      </div>
      <!-- Group 2 (Duplicate) -->
      <div class="flex w-1/2 justify-around items-center gap-12 px-6">
        <div class="flex items-center gap-3 text-gray-400 font-bold text-xl hover:text-gray-900 transition duration-300"><i data-lucide="shopping-bag" class="w-6 h-6"></i> Shopify</div>
        <div class="flex items-center gap-3 text-gray-400 font-bold text-xl hover:text-gray-900 transition duration-300"><i data-lucide="shopping-cart" class="w-6 h-6"></i> Tiendanube</div>
        <div class="flex items-center gap-3 text-gray-400 font-bold text-xl hover:text-gray-900 transition duration-300"><i data-lucide="package" class="w-6 h-6"></i> Mercado Libre</div>
        <div class="flex items-center gap-3 text-gray-400 font-bold text-xl hover:text-gray-900 transition duration-300"><i data-lucide="box" class="w-6 h-6"></i> Amazon</div>
        <div class="flex items-center gap-3 text-gray-400 font-bold text-xl hover:text-gray-900 transition duration-300"><i data-lucide="instagram" class="w-6 h-6"></i> TikTok</div>
      </div>
    </div>
  </section>

  <!-- Stats Bar -->
  <section class="py-16 bg-bgmain relative z-20">
    <div class="max-w-6xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
      <div class="bg-white rounded-3xl p-8 saas-shadow border border-gray-100 hover:-translate-y-1 transition-transform">
        <div class="text-4xl font-extrabold text-gray-900">47K+</div>
        <div class="text-[10px] text-gray-500 uppercase font-bold tracking-wider mt-2">Productos Analizados</div>
      </div>
      <div class="bg-white rounded-3xl p-8 saas-shadow border border-gray-100 hover:-translate-y-1 transition-transform">
        <div class="text-4xl font-extrabold text-gray-900">9</div>
        <div class="text-[10px] text-gray-500 uppercase font-bold tracking-wider mt-2">Plataformas</div>
      </div>
      <div class="bg-white rounded-3xl p-8 saas-shadow border border-gray-100 hover:-translate-y-1 transition-transform">
        <div class="text-4xl font-extrabold text-gray-900">3</div>
        <div class="text-[10px] text-gray-500 uppercase font-bold tracking-wider mt-2">Países LATAM</div>
      </div>
      <div class="bg-white rounded-3xl p-8 saas-shadow border border-gray-100 hover:-translate-y-1 transition-transform">
        <div class="text-4xl font-extrabold text-green-500 font-mono">100%</div>
        <div class="text-[10px] text-gray-500 uppercase font-bold tracking-wider mt-2">Uptime Garantizado</div>
      </div>
    </div>
  </section>
"""

# Replace the Mockup with Demo Video
mockup_start = html.find('<!-- Floating UI Mockup to give context -->')
main_end = html.find('</main>', mockup_start)
html = html[:mockup_start] + demo_video + html[main_end:]

# Insert Integrations and Stats right after </main>
html = html.replace('</main>', '</main>\n' + integrations_and_stats)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
