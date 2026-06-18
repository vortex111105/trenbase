import re

def rebuild_home():
    with open('index.html', 'r') as f:
        content = f.read()

    custom_css = """
  <style id="premium-apple-theme">
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    :root {
      --aw-bg: #EAE5DF;
      --aw-card: rgba(247, 245, 242, 0.7);
      --aw-text-main: #2C2A29;
      --aw-text-muted: #827E7A;
      --aw-green: #3D7A50;
      --aw-red: #A64444;
      --aw-shadow: 0 24px 48px rgba(140, 130, 120, 0.15), 0 2px 6px rgba(140, 130, 120, 0.08), inset 0 1px 2px rgba(255, 255, 255, 0.9);
      --aw-shadow-hover: 0 32px 64px rgba(140, 130, 120, 0.25), 0 4px 12px rgba(140, 130, 120, 0.12), inset 0 1px 2px rgba(255, 255, 255, 1);
      --aw-btn-primary: linear-gradient(180deg, #3A3A3C 0%, #1C1C1E 100%);
      --aw-btn-primary-text: #F5F5F7;
    }
    
    body {
      background-color: var(--aw-bg) !important;
      color: var(--aw-text-main) !important;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
      letter-spacing: -0.015em;
    }
    
    .aw-card {
      background-color: var(--aw-card) !important;
      border-radius: 40px !important;
      box-shadow: var(--aw-shadow) !important;
      border: 1px solid rgba(255, 255, 255, 0.6) !important;
      backdrop-filter: blur(40px) !important;
      -webkit-backdrop-filter: blur(40px) !important;
      transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
      color: var(--aw-text-main) !important;
      overflow: hidden;
    }
    
    .aw-card:hover {
      box-shadow: var(--aw-shadow-hover) !important;
      transform: translateY(-4px) !important;
    }
    
    .aw-btn-primary {
      background: var(--aw-btn-primary) !important;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15), inset 0 1px 1px rgba(255,255,255,0.2) !important;
      color: var(--aw-btn-primary-text) !important;
      border-radius: 999px !important;
      font-weight: 600 !important;
      transition: all 0.3s ease !important;
      border: 1px solid rgba(0,0,0,0.8);
    }
    .aw-btn-primary:hover {
      transform: scale(1.02) !important;
      box-shadow: 0 8px 24px rgba(0,0,0,0.25), inset 0 1px 1px rgba(255,255,255,0.3) !important;
    }
    
    .text-title { color: var(--aw-text-main); letter-spacing: -0.04em; font-weight: 800; }
    .text-subtitle { color: var(--aw-text-muted); letter-spacing: -0.01em; font-weight: 500; }
    .aw-text-green { color: var(--aw-green) !important; }
    .aw-text-red { color: var(--aw-red) !important; }
    .aw-badge-green { background: rgba(61, 122, 80, 0.1); color: var(--aw-green); padding: 4px 12px; border-radius: 999px; font-weight: 700; font-size: 0.75rem; border: 1px solid rgba(61, 122, 80, 0.2); }
    
    .bg-glow-1 {
      position: absolute; top: -20%; left: 50%; transform: translateX(-50%);
      width: 120vw; height: 120vw; background: radial-gradient(circle, rgba(255,255,255,0.9) 0%, rgba(255,255,255,0) 60%);
      z-index: -1; pointer-events: none;
    }
    .bg-glow-2 {
      position: absolute; bottom: -10%; right: -10%;
      width: 80vw; height: 80vw; background: radial-gradient(circle, rgba(255,255,255,0.7) 0%, rgba(255,255,255,0) 60%);
      z-index: -1; pointer-events: none;
    }
  </style>
"""

    if 'premium-apple-theme' not in content:
        content = content.replace('</head>', custom_css + '\n</head>')

    content = re.sub(r'<body class="[^"]*">', '<body class="bg-[#EAE5DF] text-[#2C2A29] antialiased overflow-x-hidden font-sans">', content)

    new_landing = """
  <!-- ─── APP VIEW: LANDING ────────────────────────────────────────────────── -->
  <div id="view-landing" class="app-view active-view relative w-full min-h-screen">
    
    <div class="bg-glow-1"></div>
    <div class="bg-glow-2"></div>

    <!-- Floating Navbar -->
    <nav class="fixed top-6 left-1/2 -translate-x-1/2 w-[95%] max-w-6xl z-50">
      <div class="aw-card px-8 py-4 flex items-center justify-between !rounded-full !bg-[rgba(247,245,242,0.85)]">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-full bg-gradient-to-br from-stone-200 to-stone-400 flex items-center justify-center shadow-inner">
            <i data-lucide="zap" class="w-4 h-4 text-white"></i>
          </div>
          <span class="font-extrabold tracking-tight text-lg">TrendBase</span>
        </div>
        <div class="hidden md:flex items-center gap-8 text-sm font-semibold text-[#827E7A]">
          <a href="#protocol" class="hover:text-[#2C2A29] transition">El Protocolo</a>
          <a href="#leaderboard" class="hover:text-[#2C2A29] transition">Top Productos</a>
          <a href="#founder" class="hover:text-[#2C2A29] transition">Nosotros</a>
          <a href="#pricing" class="hover:text-[#2C2A29] transition">Precios</a>
        </div>
        <div class="flex items-center gap-4">
          <button onclick="openAuth('login')" class="text-sm font-semibold text-[#2C2A29] hover:opacity-70 transition">Ingresar</button>
          <button onclick="openAuth('signup')" class="aw-btn-primary px-6 py-2.5 text-sm">Comenzar Gratis</button>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="pt-48 pb-24 px-6 flex flex-col items-center justify-center text-center relative z-10">
      <div class="aw-badge-green mb-8 inline-flex items-center gap-2">
        <span class="relative flex h-2 w-2">
          <span class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75" style="background-color: var(--aw-green)"></span>
          <span class="relative inline-flex rounded-full h-2 w-2" style="background-color: var(--aw-green)"></span>
        </span>
        La V2.0 ya está disponible
      </div>
      
      <h1 class="text-title text-6xl md:text-8xl max-w-5xl mx-auto leading-[0.95] mb-8">
        Domina el E-Commerce <br/><span class="text-transparent bg-clip-text bg-gradient-to-r from-[#2C2A29] to-[#827E7A]">con precisión absoluta.</span>
      </h1>
      
      <p class="text-subtitle text-xl md:text-2xl max-w-3xl mx-auto mb-12 leading-relaxed">
        Descubre productos virales antes de que saturen, conéctalos a tu tienda y visualiza todas tus ganancias en un solo workspace increíblemente hermoso.
      </p>
      
      <div class="flex flex-col sm:flex-row items-center gap-4 mb-20">
        <button onclick="openAuth('signup')" class="aw-btn-primary px-8 py-4 text-lg w-full sm:w-auto">Crear cuenta gratis</button>
        <button onclick="document.getElementById('demo-video').scrollIntoView({behavior:'smooth'})" class="aw-card !rounded-full px-8 py-4 text-lg font-semibold flex items-center justify-center gap-2 w-full sm:w-auto hover:bg-white/80">
          <i data-lucide="play-circle" class="w-5 h-5"></i> Ver Demo
        </button>
      </div>

      <!-- Bento Box Hero Showcase (Reemplazo visual del video aburrido) -->
      <div id="demo-video" class="w-full max-w-6xl mx-auto aw-card p-4 md:p-8 relative">
        <!-- Barra superior del "Navegador Mac" -->
        <div class="flex items-center gap-2 mb-6 px-4">
          <div class="w-3 h-3 rounded-full bg-red-400"></div>
          <div class="w-3 h-3 rounded-full bg-yellow-400"></div>
          <div class="w-3 h-3 rounded-full bg-green-400"></div>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 h-auto">
          <div class="aw-card !bg-white/40 !shadow-none p-8 col-span-2 flex flex-col justify-center">
            <h3 class="text-3xl font-extrabold tracking-tight mb-2">Ingresos Totales</h3>
            <div class="text-6xl font-extrabold tracking-tighter mb-4">$87,450 <span class="text-xl text-[#827E7A]">USD</span></div>
            <div class="w-full h-32 bg-gradient-to-t from-stone-200/50 to-transparent rounded-2xl relative overflow-hidden">
               <!-- Curva suave simulada -->
               <svg viewBox="0 0 100 40" class="absolute bottom-0 w-full h-full preserve-3d" preserveAspectRatio="none">
                 <path d="M0,40 L0,30 Q25,10 50,25 T100,5 L100,40 Z" fill="rgba(44,42,41,0.1)"></path>
                 <path d="M0,30 Q25,10 50,25 T100,5" fill="none" stroke="#2C2A29" stroke-width="2"></path>
                 <circle cx="100" cy="5" r="2" fill="#2C2A29"></circle>
               </svg>
            </div>
          </div>
          <div class="aw-card !bg-white/40 !shadow-none p-8 flex flex-col gap-6">
            <div>
              <h4 class="text-sm font-bold text-[#827E7A] uppercase tracking-widest mb-1">Margen Promedio</h4>
              <div class="text-4xl font-extrabold tracking-tight">65%</div>
            </div>
            <div>
              <h4 class="text-sm font-bold text-[#827E7A] uppercase tracking-widest mb-1">Salud del Negocio</h4>
              <div class="text-2xl font-bold aw-text-green flex items-center gap-2"><i data-lucide="check-circle" class="w-6 h-6"></i> Óptimo</div>
            </div>
            <div class="mt-auto">
               <button class="w-full bg-[#2C2A29] text-white py-3 rounded-xl font-bold text-sm">Sincronizar Shopify</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- El Protocolo (Features) -->
    <section id="protocol" class="py-32 px-6 max-w-6xl mx-auto relative z-10">
      <div class="text-center mb-20">
        <h2 class="text-title text-4xl md:text-6xl mb-6">El Protocolo TrendBase.</h2>
        <p class="text-subtitle text-xl max-w-2xl mx-auto">No es magia. Es un sistema estructurado de 3 pasos para minimizar el riesgo y maximizar tus ganancias en el e-commerce.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- Paso 1 -->
        <div class="aw-card p-10 flex flex-col items-start relative group">
          <div class="text-8xl font-extrabold text-black/5 absolute -top-4 -right-2">1</div>
          <div class="w-16 h-16 rounded-2xl bg-white shadow-sm flex items-center justify-center mb-8 relative z-10">
            <i data-lucide="radar" class="w-8 h-8 text-[#2C2A29]"></i>
          </div>
          <h3 class="text-2xl font-bold mb-4 relative z-10">Detección de Virales</h3>
          <p class="text-[#827E7A] leading-relaxed relative z-10">Nuestros algoritmos escanean TikTok e Instagram 24/7 buscando patrones de crecimiento antes de que la competencia los vea.</p>
        </div>

        <!-- Paso 2 -->
        <div class="aw-card p-10 flex flex-col items-start relative group">
          <div class="text-8xl font-extrabold text-black/5 absolute -top-4 -right-2">2</div>
          <div class="w-16 h-16 rounded-2xl bg-white shadow-sm flex items-center justify-center mb-8 relative z-10">
            <i data-lucide="line-chart" class="w-8 h-8 text-[#2C2A29]"></i>
          </div>
          <h3 class="text-2xl font-bold mb-4 relative z-10">Análisis de Océano Azul</h3>
          <p class="text-[#827E7A] leading-relaxed relative z-10">Filtramos la basura. Solo te mostramos productos con alto margen comprobado de proveedores reales y baja saturación en el mercado.</p>
        </div>

        <!-- Paso 3 -->
        <div class="aw-card p-10 flex flex-col items-start relative group">
          <div class="text-8xl font-extrabold text-black/5 absolute -top-4 -right-2">3</div>
          <div class="w-16 h-16 rounded-2xl bg-white shadow-sm flex items-center justify-center mb-8 relative z-10">
            <i data-lucide="briefcase" class="w-8 h-8 text-[#2C2A29]"></i>
          </div>
          <h3 class="text-2xl font-bold mb-4 relative z-10">Control Financiero</h3>
          <p class="text-[#827E7A] leading-relaxed relative z-10">Conecta tu tienda y ve el dinero real. Mide tu ROI exacto en automático cruzando ventas reales con gastos de Ads.</p>
        </div>
      </div>
    </section>

    <!-- Leaderboard -->
    <section id="leaderboard" class="py-32 px-6 max-w-6xl mx-auto relative z-10">
      <div class="flex flex-col md:flex-row gap-16 items-center">
        <div class="md:w-1/2">
          <h2 class="text-title text-4xl md:text-5xl mb-6">Productos que están imprimiendo dinero.</h2>
          <p class="text-subtitle text-lg mb-8 leading-relaxed">No operamos con suposiciones. El Leaderboard muestra lo que está funcionando EXACTAMENTE hoy, en tu país.</p>
          <ul class="space-y-4">
            <li class="flex items-center gap-4"><i data-lucide="check" class="aw-text-green w-5 h-5"></i> <span class="font-medium">Métricas de competencia en vivo</span></li>
            <li class="flex items-center gap-4"><i data-lucide="check" class="aw-text-green w-5 h-5"></i> <span class="font-medium">Calculadora de márgenes exactos</span></li>
            <li class="flex items-center gap-4"><i data-lucide="check" class="aw-text-green w-5 h-5"></i> <span class="font-medium">Proveedores verificados</span></li>
          </ul>
        </div>
        <div class="md:w-1/2 w-full">
          <div class="aw-card p-6">
            <div class="space-y-3">
              <div class="flex items-center justify-between p-4 bg-white/50 rounded-2xl">
                <div class="flex items-center gap-4">
                  <span class="text-2xl font-extrabold text-stone-300">1</span>
                  <div>
                    <div class="font-bold">Suplemento Ashwagandha</div>
                    <div class="text-xs text-[#827E7A]">Score: 98/100</div>
                  </div>
                </div>
                <div class="aw-badge-green">+15%</div>
              </div>
              <div class="flex items-center justify-between p-4 bg-white/50 rounded-2xl">
                <div class="flex items-center gap-4">
                  <span class="text-2xl font-extrabold text-stone-300">2</span>
                  <div>
                    <div class="font-bold">Set Skincare Hialurónico</div>
                    <div class="text-xs text-[#827E7A]">Score: 95/100</div>
                  </div>
                </div>
                <div class="aw-badge-green">+12%</div>
              </div>
              <div class="flex items-center justify-between p-4 bg-white/50 rounded-2xl">
                <div class="flex items-center gap-4">
                  <span class="text-2xl font-extrabold text-stone-300">3</span>
                  <div>
                    <div class="font-bold">Ropa Seamless B2B</div>
                    <div class="text-xs text-[#827E7A]">Score: 92/100</div>
                  </div>
                </div>
                <div class="aw-badge-green">+8%</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing Section -->
    <section id="pricing" class="py-32 px-6 max-w-6xl mx-auto relative z-10 text-center">
      <h2 class="text-title text-4xl md:text-5xl mb-6">Inversión transparente.</h2>
      <p class="text-subtitle text-lg mb-16">Recuperas la suscripción mensual con tu primera venta del mes.</p>
      
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-left">
        <!-- Free -->
        <div class="aw-card p-8 flex flex-col">
          <h3 class="text-xl font-bold mb-2">Básico</h3>
          <p class="text-[#827E7A] text-sm mb-6">Para empezar y entender el sistema.</p>
          <div class="text-5xl font-extrabold tracking-tight mb-8">Gratis</div>
          <ul class="space-y-4 mb-8 flex-1">
            <li class="flex items-center gap-3 text-sm"><i data-lucide="check" class="w-4 h-4 aw-text-green"></i> 20 productos analizados</li>
            <li class="flex items-center gap-3 text-sm"><i data-lucide="check" class="w-4 h-4 aw-text-green"></i> Historial 7 días</li>
            <li class="flex items-center gap-3 text-sm opacity-50"><i data-lucide="x" class="w-4 h-4"></i> Asistente IA</li>
            <li class="flex items-center gap-3 text-sm opacity-50"><i data-lucide="x" class="w-4 h-4"></i> Filtros Avanzados</li>
          </ul>
          <button onclick="openAuth('signup')" class="w-full bg-white/50 hover:bg-white text-[#2C2A29] py-3 rounded-xl font-bold transition border border-white/80">Comenzar Gratis</button>
        </div>

        <!-- Starter -->
        <div class="aw-card p-8 flex flex-col relative transform md:-translate-y-4 shadow-2xl !bg-[rgba(247,245,242,0.95)] !border-stone-300">
          <div class="absolute -top-4 left-1/2 -translate-x-1/2 aw-badge-green !bg-[#3D7A50] !text-white !border-none px-4 py-1">Más Popular</div>
          <h3 class="text-xl font-bold mb-2">Starter</h3>
          <p class="text-[#827E7A] text-sm mb-6">Para el emprendedor que ya vende.</p>
          <div class="text-5xl font-extrabold tracking-tight mb-8">$19<span class="text-lg text-[#827E7A] font-medium">/mes</span></div>
          <ul class="space-y-4 mb-8 flex-1">
            <li class="flex items-center gap-3 text-sm"><i data-lucide="check" class="w-4 h-4 aw-text-green"></i> 150 productos analizados</li>
            <li class="flex items-center gap-3 text-sm"><i data-lucide="check" class="w-4 h-4 aw-text-green"></i> Historial 90 días</li>
            <li class="flex items-center gap-3 text-sm"><i data-lucide="check" class="w-4 h-4 aw-text-green"></i> Filtros Avanzados</li>
            <li class="flex items-center gap-3 text-sm"><i data-lucide="check" class="w-4 h-4 aw-text-green"></i> Análisis IA (10 msg)</li>
          </ul>
          <button onclick="subscribe('starter')" class="aw-btn-primary w-full py-3 rounded-xl font-bold">Suscribirme</button>
        </div>

        <!-- Pro -->
        <div class="aw-card p-8 flex flex-col">
          <h3 class="text-xl font-bold mb-2">Pro</h3>
          <p class="text-[#827E7A] text-sm mb-6">Para agencias y tiendas escalando.</p>
          <div class="text-5xl font-extrabold tracking-tight mb-8">$49<span class="text-lg text-[#827E7A] font-medium">/mes</span></div>
          <ul class="space-y-4 mb-8 flex-1">
            <li class="flex items-center gap-3 text-sm"><i data-lucide="check" class="w-4 h-4 aw-text-green"></i> Productos Ilimitados</li>
            <li class="flex items-center gap-3 text-sm"><i data-lucide="check" class="w-4 h-4 aw-text-green"></i> Historial Completo</li>
            <li class="flex items-center gap-3 text-sm"><i data-lucide="check" class="w-4 h-4 aw-text-green"></i> Comparador de nichos</li>
            <li class="flex items-center gap-3 text-sm"><i data-lucide="check" class="w-4 h-4 aw-text-green"></i> Asistente IA Ilimitado</li>
          </ul>
          <button onclick="subscribe('pro')" class="w-full bg-white/50 hover:bg-white text-[#2C2A29] py-3 rounded-xl font-bold transition border border-white/80">Suscribirme</button>
        </div>
      </div>
    </section>

    <!-- Founder Note -->
    <section id="founder" class="py-32 px-6 max-w-4xl mx-auto relative z-10">
      <div class="aw-card p-12 md:p-16">
        <div class="w-16 h-16 rounded-full bg-stone-300 mb-8 border-4 border-white shadow-lg overflow-hidden">
          <img src="https://ui-avatars.com/api/?name=N+F&background=2C2A29&color=fff" alt="Founder" class="w-full h-full object-cover">
        </div>
        <h3 class="text-3xl font-extrabold mb-8 tracking-tight">Construí TrendBase porque estaba cansado de perder dinero probando productos a ciegas.</h3>
        <div class="space-y-6 text-[#6B6661] text-lg leading-relaxed font-serif">
          <p>Hace dos años, quemé $2,000 en Facebook Ads probando un producto que pensé que sería un éxito. Resulta que estaba llegando 4 meses tarde a la tendencia.</p>
          <p>El e-commerce no se trata de "tener suerte". Se trata de datos. Se trata de encontrar la curva ascendente antes de que el mercado se sature. Construí este sistema para mi propia agencia, y los resultados fueron tan ridículamente buenos que decidí abrirlo al público.</p>
          <p>No te prometo que te harás millonario de la noche a la mañana. Pero te prometo que nunca más volverás a probar productos a ciegas.</p>
        </div>
        <div class="mt-10 font-bold text-[#2C2A29]">
          Ignacio Fraga<br/>
          <span class="text-sm font-normal text-[#827E7A]">Fundador de TrendBase</span>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="py-12 border-t border-white/50 mt-20 relative z-10 text-center md:text-left">
      <div class="max-w-6xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
        <div class="flex items-center gap-2">
          <div class="w-6 h-6 rounded-full bg-gradient-to-br from-stone-200 to-stone-400 flex items-center justify-center shadow-inner">
            <i data-lucide="zap" class="w-3 h-3 text-white"></i>
          </div>
          <span class="font-extrabold tracking-tight text-[#2C2A29]">TrendBase</span>
        </div>
        <p class="text-sm text-[#827E7A]">© 2026 TrendBase Inc. Todos los derechos reservados.</p>
        <div class="flex gap-4 justify-center">
          <a href="#" class="text-[#827E7A] hover:text-[#2C2A29] transition"><i data-lucide="twitter" class="w-5 h-5"></i></a>
          <a href="#" class="text-[#827E7A] hover:text-[#2C2A29] transition"><i data-lucide="instagram" class="w-5 h-5"></i></a>
        </div>
      </div>
    </footer>
  </div>
"""

    start_str = "  <!-- ─── APP VIEW: LANDING ────────────────────────────────────────────────── -->"
    end_str = "  <!-- ─── APP VIEW: DASHBOARD ─────────────────────────────────────────────── -->"
    
    start_idx = content.find(start_str)
    end_idx = content.find(end_str)
    
    if start_idx != -1 and end_idx != -1:
        new_content = content[:start_idx] + new_landing + "\n" + content[end_idx:]
        
        with open('index.html', 'w') as f:
            f.write(new_content)
        print("Landing page completely rebuilt with ALL content!")
    else:
        print("Could not find boundaries for Landing Page.")

rebuild_home()
