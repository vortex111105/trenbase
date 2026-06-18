import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

def get_section(start_marker, end_marker):
    start = html.find(start_marker)
    end = html.find(end_marker, start) if end_marker else len(html)
    if start == -1 or end == -1:
        return ""
    return html[start:end]

pricing = get_section('<!-- Pricing Section (Dark Glassmorphism) -->', '<!-- Footer Section -->')

if pricing:
    new_pricing = """<!-- Pricing Section (Dark Glassmorphism) -->
  <section id="pricing" class="bg-[#0A0A0C] w-full py-40 relative overflow-hidden flex flex-col items-center justify-center min-h-screen border-t border-white/5">
    
    <!-- Subtle Grid -->
    <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSA0MCAwIEwgMCAwIDAgNDAiIGZpbGw9Im5vbmUiIHN0cm9rZT0icmdiYSgyNTUsIDI1NSwgMjU1LCAwLjAzKSIgc3Ryb2tlLXdpZHRoPSIxIi8+PC9wYXR0ZXJuPjwvZGVmcz48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSJ1cmwoI2dyaWQpIi8+PC9zdmc+')] z-0 pointer-events-none [mask-image:linear-gradient(to_bottom,transparent,black,transparent)]"></div>
    
    <!-- Huge blurred background text -->
    <div class="absolute inset-0 flex items-center justify-center overflow-hidden pointer-events-none z-0">
      <h2 class="text-[12rem] md:text-[22rem] font-black text-white opacity-[0.02] select-none blur-[2px] whitespace-nowrap tracking-tighter">pricing</h2>
    </div>

    <div class="relative z-10 w-full max-w-6xl mx-auto px-6 grid grid-cols-1 md:grid-cols-2 gap-8 items-stretch">
      
      <!-- Left Column: Stacked Cards -->
      <div class="flex flex-col gap-8">
        
        <!-- Free Plan -->
        <div class="bg-[#18181B]/80 backdrop-blur-3xl rounded-[2.5rem] p-10 border border-white/5 flex flex-col transition-all hover:-translate-y-2 saas-shadow spotlight-card spotlight-dark">
          <div class="text-xs text-white/40 mb-2 font-medium tracking-wide">Plan Básico</div>
          <div class="text-4xl font-bold text-white mb-8">Gratis</div>
          
          <ul class="space-y-4 flex-1 mb-8">
            <li class="flex items-center gap-3 text-sm text-white/60"><i data-lucide="check" class="w-4 h-4 text-white/40"></i> 10 Búsquedas mensuales</li>
            <li class="flex items-center gap-3 text-sm text-white/60"><i data-lucide="check" class="w-4 h-4 text-white/40"></i> Historial básico de 30 días</li>
            <li class="flex items-center gap-3 text-sm text-white/60"><i data-lucide="check" class="w-4 h-4 text-white/40"></i> Soporte por email</li>
          </ul>
          
          <button class="w-full py-4 rounded-2xl bg-white/5 text-white text-sm font-bold border border-white/10 hover:bg-white/10 transition">Empezar Gratis</button>
        </div>

        <!-- Elite Plan -->
        <div class="bg-[#18181B]/80 backdrop-blur-3xl rounded-[2.5rem] p-10 border border-white/5 flex flex-col transition-all hover:-translate-y-2 saas-shadow spotlight-card spotlight-dark">
          <div class="text-xs text-white/40 mb-2 font-medium tracking-wide">Plan Élite</div>
          <div class="text-4xl font-bold text-white mb-8">$19.99<span class="text-lg text-white/40 font-normal">/m</span></div>
          
          <ul class="space-y-4 flex-1 mb-8">
            <li class="flex items-center gap-3 text-sm text-white/60"><i data-lucide="check" class="w-4 h-4 text-white/40"></i> Todo lo del Plan Pro</li>
            <li class="flex items-center gap-3 text-sm text-white/60"><i data-lucide="check" class="w-4 h-4 text-white/40"></i> Acceso a la API nativa</li>
            <li class="flex items-center gap-3 text-sm text-white/60"><i data-lucide="check" class="w-4 h-4 text-white/40"></i> Integración con Shopify</li>
          </ul>
          
          <button class="w-full py-4 rounded-2xl bg-white/5 text-white text-sm font-bold border border-white/10 hover:bg-white/10 transition">Contactar Ventas</button>
        </div>

      </div>

      <!-- Right Column: Pro Plan -->
      <div class="h-full flex relative">
        <div class="absolute -inset-0.5 bg-gradient-to-b from-white/10 to-transparent rounded-[3rem] blur opacity-50 z-0"></div>
        <div class="bg-[#1F1F22] rounded-[2.5rem] p-12 border border-white/10 flex flex-col relative z-20 shadow-2xl shadow-black/50 w-full spotlight-card spotlight-dark">
          <!-- Subtle top glow -->
          <div class="absolute -top-10 inset-x-0 h-32 bg-white/10 blur-[50px] rounded-full pointer-events-none"></div>
          
          <div class="text-xs text-white/60 mb-2 font-medium tracking-wide">Plan Pro</div>
          <div class="text-6xl font-bold text-white mb-12">$9.99<span class="text-xl text-white/40 font-normal">/m</span></div>
          
          <ul class="space-y-6 flex-1 relative z-10 mb-12">
            <li class="flex items-center gap-4 text-sm text-white/90"><div class="w-6 h-6 rounded-full bg-white/10 flex items-center justify-center"><i data-lucide="check" class="w-3 h-3 text-white"></i></div> Búsquedas ilimitadas</li>
            <li class="flex items-center gap-4 text-sm text-white/90"><div class="w-6 h-6 rounded-full bg-white/10 flex items-center justify-center"><i data-lucide="check" class="w-3 h-3 text-white"></i></div> Historial completo de 1 año</li>
            <li class="flex items-center gap-4 text-sm text-white/90"><div class="w-6 h-6 rounded-full bg-white/10 flex items-center justify-center"><i data-lucide="check" class="w-3 h-3 text-white"></i></div> Exportación en CSV / Excel</li>
            <li class="flex items-center gap-4 text-sm text-white/90"><div class="w-6 h-6 rounded-full bg-white/10 flex items-center justify-center"><i data-lucide="check" class="w-3 h-3 text-white"></i></div> Alertas en tiempo real</li>
            <li class="flex items-center gap-4 text-sm text-white/90"><div class="w-6 h-6 rounded-full bg-white/10 flex items-center justify-center"><i data-lucide="check" class="w-3 h-3 text-white"></i></div> Proveedores exclusivos</li>
          </ul>
          
          <button class="w-full py-4 rounded-2xl bg-white text-black font-extrabold hover:scale-105 transition shadow-[0_0_30px_rgba(255,255,255,0.2)] relative z-10">Obtener Pro</button>
        </div>
      </div>

    </div>
  </section>
"""
    
    html = html.replace(pricing, new_pricing)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Pricing updated!")
else:
    print("Could not find pricing section")
