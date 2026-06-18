import re

def rebuild_surgical():
    with open('index_backup_broken_ui.html', 'r', encoding='utf-8') as f:
        idx = f.read()

    with open('/Users/nachofrag/Desktop/TrendBase_Vision.html', 'r', encoding='utf-8') as f:
        vision = f.read()

    # 1. EXTRACT APPLE VISION CSS
    vision_style_start = vision.find('<style>')
    vision_style_end = vision.find('</style>', vision_style_start) + 8
    vision_style = vision[vision_style_start:vision_style_end]

    # Add environment-bg to body if missing
    idx = idx.replace('<body class="', '<body class="environment-bg ')

    # 2. INJECT VISION CSS INTO HEAD
    idx = idx.replace('</head>', f'{vision_style}\n</head>')

    # 3. REMOVE OLD NAVBAR (Lines 302-396)
    # The navbar starts with <!-- A. NAVBAR — "The Floating Island" -->
    # and ends before <!-- AUTHENTICATION MODAL -->
    nav_start = idx.find('<!-- A. NAVBAR — "The Floating Island" -->')
    nav_end = idx.find('<!-- AUTHENTICATION MODAL -->')
    if nav_start != -1 and nav_end != -1:
        idx = idx[:nav_start] + idx[nav_end:]

    # 4. REPLACE LANDING PAGE
    landing_start = idx.find('<!-- ─── APP VIEW: LANDING ────────────────────────────────────────────────── -->')
    landing_end = idx.find('<!-- ─── APP VIEW: DASHBOARD ─────────────────────────────────────────────── -->')

    native_landing = """
  <!-- ─── APP VIEW: LANDING ────────────────────────────────────────────────── -->
  <div id="view-landing" class="app-view active-view">
    <div class="w-full max-w-[1280px] mx-auto glass-app-container min-h-[85vh] shadow-2xl relative mt-8 p-8 md:p-12 overflow-y-auto mb-20">
        <!-- HEADER -->
        <header class="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-4">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-[#3E3C3A] shadow-[0_4px_10px_rgba(0,0,0,0.2),inset_0_2px_2px_rgba(255,255,255,0.2)] flex items-center justify-center">
                    <div class="w-4 h-4 rounded-md bg-[--bg-wall] shadow-inner"></div>
                </div>
                <h1 class="text-3xl font-heading tracking-tight text-[--text-dark]">TrendBase</h1>
            </div>
            <div class="flex items-center gap-4">
                <button onclick="enterDash()" class="btn-solid px-6 py-2.5 text-sm font-bold tracking-widest uppercase">Ingresar</button>
            </div>
        </header>

        <!-- HERO SECTION -->
        <section class="mb-16">
            <div class="matte-card p-10 md:p-16 mb-8 flex flex-col items-center text-center">
                <div class="pill-gray flex items-center gap-2 mb-6 uppercase tracking-widest text-[10px] font-bold">
                    <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                    Monitoreo en tiempo real · latam
                </div>
                <h1 class="text-5xl md:text-7xl font-heading max-w-4xl leading-[1.05] mb-6 tracking-tight text-[--text-dark]">
                    Inteligencia Artificial para <br>
                    <span class="font-normal italic text-[--text-muted]">E-commerce & Dropshipping.</span>
                </h1>
                <p class="text-lg md:text-xl text-[--text-muted] max-w-2xl mb-10 font-medium">
                    Encuentra productos virales, espía los anuncios de tu competencia y gestiona tus finanzas en un solo lugar. Ya sea que operes sin stock o tengas tu propia marca.
                </p>
                <div class="flex gap-4">
                    <button onclick="enterDash()" class="btn-solid px-8 py-4 text-sm uppercase tracking-widest font-bold">Comenzar Gratis</button>
                </div>
            </div>
        </section>

        <!-- FEATURES SECTION -->
        <section class="mb-16">
            <div class="text-center mb-8">
                <span class="pill-gray uppercase tracking-widest text-[10px] mb-3 inline-block font-bold">Métrica y Precisión</span>
                <h2 class="text-3xl md:text-5xl font-heading tracking-tight text-[--text-dark]">Todo para vender en tendencia</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="matte-card p-8 flex flex-col justify-between">
                    <div class="flex justify-between items-start mb-6">
                        <h3 class="font-heading text-lg font-medium text-[--text-dark]">Detección Viral</h3>
                        <i data-lucide="flame" class="text-[--text-muted] w-5 h-5"></i>
                    </div>
                    <div class="text-data mb-2 tracking-tight text-[--text-dark]">24/7</div>
                    <p class="text-[--text-muted] text-sm">Monitoreo continuo de 47k+ productos en 9 plataformas líderes.</p>
                </div>
                <div class="matte-card p-8 flex flex-col justify-between">
                    <div class="flex justify-between items-start mb-6">
                        <h3 class="font-heading text-lg font-medium text-[--text-dark]">Telemetría Local</h3>
                        <i data-lucide="globe" class="text-[--text-muted] w-5 h-5"></i>
                    </div>
                    <div class="text-data mb-2 tracking-tight text-[--text-dark]">LATAM</div>
                    <p class="text-[--text-muted] text-sm">Métricas precisas en ARS, UYU y CLP para evitar riesgos.</p>
                </div>
                <div class="matte-card p-8 flex flex-col justify-between">
                    <div class="flex justify-between items-start mb-6">
                        <h3 class="font-heading text-lg font-medium text-[--text-dark]">Rentabilidad</h3>
                        <i data-lucide="calculator" class="text-[--text-muted] w-5 h-5"></i>
                    </div>
                    <div class="text-data mb-2 text-accent-green flex items-center gap-2 tracking-tight">ROI <i data-lucide="arrow-up-right" class="w-6 h-6"></i></div>
                    <p class="text-[--text-muted] text-sm">Cálculo de márgenes reales cruzando ventas con gastos de envío.</p>
                </div>
            </div>
        </section>

        <!-- LEADERBOARD SECTION -->
        <section class="mb-16">
            <div class="text-center mb-8">
                <span class="pill-gray uppercase tracking-widest text-[10px] mb-3 inline-block font-bold">Comunidad</span>
                <h2 class="text-3xl md:text-5xl font-heading tracking-tight text-[--text-dark]">Productos que están volando</h2>
                <p class="text-[--text-muted] text-sm mt-3 font-medium">Ventas reales registradas por dropshippers activos.</p>
            </div>
            <!-- KPI Row -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div class="matte-card p-6 text-center">
                    <div id="cStatSales" class="text-3xl font-heading tracking-tight text-[--text-dark]">—</div>
                    <div class="text-[10px] text-[--text-muted] uppercase font-bold tracking-widest mt-1">Ventas Registradas</div>
                </div>
                <div class="matte-card p-6 text-center">
                    <div id="cStatUsers" class="text-3xl font-heading tracking-tight text-[--text-dark]">—</div>
                    <div class="text-[10px] text-[--text-muted] uppercase font-bold tracking-widest mt-1">Vendedores Activos</div>
                </div>
                <div class="matte-card p-6 text-center">
                    <div id="cStatTop" class="text-lg font-heading tracking-tight text-[--text-dark] truncate mt-2">—</div>
                    <div class="text-[10px] text-[--text-muted] uppercase font-bold tracking-widest mt-2">Producto Estrella</div>
                </div>
            </div>
            <!-- Populated by JS -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12" id="publicLeaderboard"></div>
            <div id="landingProducts" class="grid grid-cols-1 md:grid-cols-3 gap-6"></div>
        </section>

        <!-- PHILOSOPHY SECTION -->
        <section class="mb-16">
            <div class="matte-card p-10 md:p-16 flex flex-col items-center text-center">
                <span class="pill-gray uppercase tracking-widest text-[10px] mb-6 inline-block font-bold">El Manifiesto</span>
                <p class="text-[--text-muted] text-sm md:text-base font-medium max-w-lg mb-8 leading-relaxed">
                    La mayoría de los dropshippers buscan productos a ciegas, perdiendo tiempo y dinero en campañas que no convierten.
                </p>
                <h2 class="text-3xl md:text-5xl font-heading tracking-tight text-[--text-dark] leading-[1.1]">
                    Nosotros nos enfocamos en el <br>
                    <span class="italic font-normal text-[--text-muted]">Monitoreo Científico de Tendencias.</span>
                </h2>
            </div>
        </section>

        <!-- PRICING SECTION -->
        <section class="mb-16" id="pricing">
            <div class="text-center mb-8">
                <span class="pill-gray uppercase tracking-widest text-[10px] mb-3 inline-block font-bold">Membresía</span>
                <h2 class="text-3xl md:text-5xl font-heading tracking-tight text-[--text-dark]">Precios sin sorpresas</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- Free -->
                <div class="matte-card p-8 flex flex-col justify-between h-full">
                    <div>
                        <span class="pill-gray uppercase tracking-widest text-[10px] mb-4 inline-block font-bold">Básico</span>
                        <h3 class="text-2xl font-heading text-[--text-dark] mb-2">Free</h3>
                        <div class="mb-6"><span class="text-5xl font-heading tracking-tight text-[--text-dark]">$0</span><span class="text-[--text-muted] text-xs ml-1">/mes</span></div>
                        <div class="space-y-3 mb-8">
                            <div class="flex gap-2 text-sm text-[--text-dark] font-medium"><i data-lucide="check" class="w-4 h-4 text-accent-green"></i> 3 Búsquedas diarias</div>
                            <div class="flex gap-2 text-sm text-[--text-dark] font-medium"><i data-lucide="check" class="w-4 h-4 text-accent-green"></i> Análisis básico (1 país)</div>
                        </div>
                    </div>
                    <button onclick="openAuth('signup')" class="w-full btn-solid px-4 py-3 text-sm font-bold uppercase tracking-widest mt-8">Empezar Gratis</button>
                </div>
                <!-- Startup -->
                <div class="matte-card p-8 flex flex-col justify-between h-full relative" style="border: 2px solid var(--soft-green);">
                    <div class="absolute -top-3 left-1/2 -translate-x-1/2 pill-active text-accent-green text-[10px] uppercase tracking-widest font-bold bg-white px-2 py-0.5 rounded-full shadow-sm">Más Popular</div>
                    <div>
                        <span class="pill-gray uppercase tracking-widest text-[10px] mb-4 inline-block font-bold">Profesional</span>
                        <h3 class="text-2xl font-heading text-[--text-dark] mb-2">Startup</h3>
                        <div class="mb-6"><span class="text-5xl font-heading tracking-tight text-[--text-dark]">$29</span><span class="text-[--text-muted] text-xs ml-1">/mes</span></div>
                        <div class="space-y-3 mb-8">
                            <div class="flex gap-2 text-sm text-[--text-dark] font-medium"><i data-lucide="check" class="w-4 h-4 text-accent-green"></i> Búsquedas Ilimitadas</div>
                            <div class="flex gap-2 text-sm text-[--text-dark] font-medium"><i data-lucide="check" class="w-4 h-4 text-accent-green"></i> Análisis full (3 países)</div>
                            <div class="flex gap-2 text-sm text-[--text-dark] font-medium"><i data-lucide="check" class="w-4 h-4 text-accent-green"></i> Competidores en vivo</div>
                        </div>
                    </div>
                    <button onclick="openAuth('signup')" class="w-full btn-solid px-4 py-3 text-sm font-bold uppercase tracking-widest mt-8">Elegir Startup</button>
                </div>
                <!-- Pro -->
                <div class="matte-card p-8 flex flex-col justify-between h-full">
                    <div>
                        <span class="pill-gray uppercase tracking-widest text-[10px] mb-4 inline-block font-bold">Escala</span>
                        <h3 class="text-2xl font-heading text-[--text-dark] mb-2">Pro</h3>
                        <div class="mb-6"><span class="text-5xl font-heading tracking-tight text-[--text-dark]">$79</span><span class="text-[--text-muted] text-xs ml-1">/mes</span></div>
                        <div class="space-y-3 mb-8">
                            <div class="flex gap-2 text-sm text-[--text-dark] font-medium"><i data-lucide="check" class="w-4 h-4 text-accent-green"></i> Todo lo de Startup</div>
                            <div class="flex gap-2 text-sm text-[--text-dark] font-medium"><i data-lucide="check" class="w-4 h-4 text-accent-green"></i> Acceso API</div>
                            <div class="flex gap-2 text-sm text-[--text-dark] font-medium"><i data-lucide="check" class="w-4 h-4 text-accent-green"></i> Soporte 24/7</div>
                        </div>
                    </div>
                    <button onclick="openAuth('signup')" class="w-full btn-solid px-4 py-3 text-sm font-bold uppercase tracking-widest mt-8">Elegir Pro</button>
                </div>
            </div>
        </section>
        
        <!-- FOOTER -->
        <footer class="matte-card py-16 rounded-[3rem] mt-16 text-center">
            <span class="text-[var(--text-dark)] font-extrabold text-xl"><span class="text-[--text-muted] font-heading">Trend</span>Base</span>
            <p class="text-[var(--text-muted)] text-xs mt-4">Inteligencia competitiva para dropshippers en Latinoamérica.</p>
        </footer>
    </div>
  </div>
"""

    idx = idx[:landing_start] + native_landing + "\n  " + idx[landing_end:]

    # Write output
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(idx)

    print("Surgical patch complete!")

rebuild_surgical()
