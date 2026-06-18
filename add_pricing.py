import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pricing_section = """  <!-- Pricing Section (Dark Glassmorphism) -->
  <section id="pricing" class="bg-[#0A0A0C] w-full py-32 relative overflow-hidden flex flex-col items-center">
    <!-- Huge blurred background text -->
    <div class="absolute inset-0 flex items-center justify-center overflow-hidden pointer-events-none z-0">
      <h2 class="text-[12rem] md:text-[20rem] font-black text-white opacity-[0.03] select-none blur-[2px] whitespace-nowrap">Pricing</h2>
    </div>

    <div class="relative z-10 w-full max-w-7xl mx-auto px-6">
      
      <!-- Toggle -->
      <div class="flex items-center justify-center mb-16">
        <div class="flex items-center gap-4">
          <span class="text-white/50 text-sm font-medium">Billed Monthly</span>
          <div class="w-14 h-7 bg-white/10 rounded-full p-1 cursor-pointer flex items-center shadow-inner relative border border-white/5">
            <div class="w-5 h-5 bg-white rounded-full absolute right-1 shadow-md"></div>
          </div>
          <span class="text-white text-sm font-bold">Billed Yearly</span>
        </div>
      </div>

      <!-- Pricing Cards Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-center">
        
        <!-- Free Plan -->
        <div class="bg-[#18181B]/60 backdrop-blur-3xl rounded-[2rem] p-10 border border-white/5 flex flex-col h-[500px] transition-all hover:-translate-y-2 saas-shadow">
          <div class="text-sm text-white/40 mb-1 font-medium">Plan Básico</div>
          <div class="text-4xl font-bold text-white mb-10">Gratis</div>
          
          <ul class="space-y-5 flex-1">
            <li class="flex items-center gap-3 text-sm text-white/60"><div class="w-5 h-5 rounded-full bg-white/5 flex items-center justify-center"><i data-lucide="check" class="w-3 h-3 text-white/60"></i></div> 10 Búsquedas mensuales</li>
            <li class="flex items-center gap-3 text-sm text-white/60"><div class="w-5 h-5 rounded-full bg-white/5 flex items-center justify-center"><i data-lucide="check" class="w-3 h-3 text-white/60"></i></div> Historial básico de 30 días</li>
            <li class="flex items-center gap-3 text-sm text-white/60"><div class="w-5 h-5 rounded-full bg-white/5 flex items-center justify-center"><i data-lucide="check" class="w-3 h-3 text-white/60"></i></div> Soporte por email</li>
          </ul>
          
          <button class="mt-8 w-full py-4 rounded-2xl bg-white/5 text-white font-bold border border-white/10 hover:bg-white/10 transition">Empezar Gratis</button>
        </div>

        <!-- Standard Plan (Highlighted) -->
        <div class="bg-[#1F1F22]/80 backdrop-blur-3xl rounded-[2.5rem] p-12 border border-white/20 flex flex-col h-[560px] relative z-20 shadow-2xl shadow-black/50 lg:scale-105">
          <!-- Subtle top glow -->
          <div class="absolute -top-20 inset-x-0 h-40 bg-white/10 blur-[50px] rounded-full pointer-events-none"></div>
          
          <div class="text-sm text-white/60 mb-1 font-medium">Plan Pro</div>
          <div class="text-5xl font-bold text-white mb-10">$9.99<span class="text-xl text-white/40 font-normal">/m</span></div>
          
          <ul class="space-y-5 flex-1 relative z-10">
            <li class="flex items-center gap-3 text-sm text-white/90"><div class="w-5 h-5 rounded-full bg-white/20 flex items-center justify-center"><i data-lucide="check" class="w-3 h-3 text-white"></i></div> Búsquedas ilimitadas</li>
            <li class="flex items-center gap-3 text-sm text-white/90"><div class="w-5 h-5 rounded-full bg-white/20 flex items-center justify-center"><i data-lucide="check" class="w-3 h-3 text-white"></i></div> Historial completo de 1 año</li>
            <li class="flex items-center gap-3 text-sm text-white/90"><div class="w-5 h-5 rounded-full bg-white/20 flex items-center justify-center"><i data-lucide="check" class="w-3 h-3 text-white"></i></div> Exportación en CSV / Excel</li>
            <li class="flex items-center gap-3 text-sm text-white/90"><div class="w-5 h-5 rounded-full bg-white/20 flex items-center justify-center"><i data-lucide="check" class="w-3 h-3 text-white"></i></div> Alertas en tiempo real</li>
            <li class="flex items-center gap-3 text-sm text-white/90"><div class="w-5 h-5 rounded-full bg-white/20 flex items-center justify-center"><i data-lucide="check" class="w-3 h-3 text-white"></i></div> Proveedores exclusivos</li>
          </ul>
          
          <button class="mt-8 w-full py-4 rounded-2xl bg-white text-black font-extrabold hover:scale-105 transition shadow-[0_0_30px_rgba(255,255,255,0.2)] relative z-10">Obtener Pro</button>
        </div>

        <!-- Pro Plan -->
        <div class="bg-[#18181B]/60 backdrop-blur-3xl rounded-[2rem] p-10 border border-white/5 flex flex-col h-[500px] transition-all hover:-translate-y-2 saas-shadow">
          <div class="text-sm text-white/40 mb-1 font-medium">Plan Élite</div>
          <div class="text-4xl font-bold text-white mb-10">$19.99<span class="text-lg text-white/40 font-normal">/m</span></div>
          
          <ul class="space-y-5 flex-1">
            <li class="flex items-center gap-3 text-sm text-white/60"><div class="w-5 h-5 rounded-full bg-white/5 flex items-center justify-center"><i data-lucide="check" class="w-3 h-3 text-white/60"></i></div> Todo lo del Plan Pro</li>
            <li class="flex items-center gap-3 text-sm text-white/60"><div class="w-5 h-5 rounded-full bg-white/5 flex items-center justify-center"><i data-lucide="check" class="w-3 h-3 text-white/60"></i></div> Acceso a la API nativa</li>
            <li class="flex items-center gap-3 text-sm text-white/60"><div class="w-5 h-5 rounded-full bg-white/5 flex items-center justify-center"><i data-lucide="check" class="w-3 h-3 text-white/60"></i></div> Soporte VIP 24/7</li>
            <li class="flex items-center gap-3 text-sm text-white/60"><div class="w-5 h-5 rounded-full bg-white/5 flex items-center justify-center"><i data-lucide="check" class="w-3 h-3 text-white/60"></i></div> Integración con Shopify</li>
          </ul>
          
          <button class="mt-8 w-full py-4 rounded-2xl bg-white/5 text-white font-bold border border-white/10 hover:bg-white/10 transition">Contactar Ventas</button>
        </div>

      </div>
    </div>
  </section>
"""

# Insert right after </main>
html = html.replace('</main>', '</main>\n' + pricing_section)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
