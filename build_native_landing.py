import re

def extract_section(content, start_marker, end_marker):
    start = content.find(start_marker)
    end = content.find(end_marker, start)
    if start != -1 and end != -1:
        return content[start:end]
    return ""

def rebuild_flawless():
    with open('/Users/nachofrag/Desktop/TrendBase_Vision.html', 'r', encoding='utf-8') as f:
        vision = f.read()

    with open('index_backup_broken_ui.html', 'r', encoding='utf-8') as f:
        idx = f.read()

    js_start = idx.find('<!-- ─── JAVASCRIPT APP ENGINE ───────────────────────────────────────────── -->')
    js_content = idx[js_start:idx.rfind('</body>')]

    modals = extract_section(idx, '<!-- Toast Notification Container -->', '<!-- ─── APP VIEW: LANDING ────────────────────────────────────────────────── -->')
    
    # Extract Real Dashboard Content
    dash_content = extract_section(idx, '<!-- Dashboard Content View Area -->', '<!-- Mobile Navigation Bar -->')
    # Strip any bg-obsidian, bg-black from dash_content so it doesn't break Apple Vision
    dash_content = re.sub(r'bg-obsidian|bg-black|bg-ivory|text-slate|border-slate/[0-9]+', '', dash_content)
    
    head_start = idx.find('<head>') + 6
    head_end = idx.find('<!-- Tailwind CSS CDN -->')
    idx_head = idx[head_start:head_end]

    native_landing = """
        <!-- HEADER -->
        <header class="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-4">
            <h1 class="text-3xl font-heading text-[--text-dark]">TrendBase</h1>
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
                    <div class="absolute -top-3 left-1/2 -translate-x-1/2 pill-active text-accent-green text-[10px] uppercase tracking-widest font-bold">Más Popular</div>
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
    """

    vision_landing_start = vision.find('<main id="view-landing"')
    vision_landing_end = vision.find('</main>', vision_landing_start) + 7
    
    new_landing = f"""
        <main id="view-landing" class="dash-section active-section flex-1 p-8 md:p-12 overflow-y-auto w-full">
            {native_landing}
        </main>
    """
    vision = vision[:vision_landing_start] + new_landing + vision[vision_landing_end:]

    # Strip the mockup dashboard views from vision
    dash_start = vision.find('<!-- ========================================== -->\n        <!-- DASHBOARD VIEW')
    dash_end = vision.find('</main>', vision.find('id="view-products"')) + 7
    
    new_dashboard = f"""
        <main id="view-dash" class="flex-1 overflow-y-auto hidden relative z-10 w-full flex-col">
            {dash_content}
        </main>
    """
    vision = vision[:dash_start] + new_dashboard + vision[dash_end:]
    
    # We don't need to replace the sidebar because in index.html the JS handles "goSection('inicio')" and the sidebar is ALREADY inside `view-dash` in index.html!
    # Wait, the prototype has a beautiful global sidebar. 
    # Let's keep the global sidebar!
    
    sidebar_target = """        <!-- SIDEBAR (Matches the original app sections with Apple aesthetic) -->
        <aside class="w-full md:w-[240px] py-8 px-6 flex md:flex-col items-start gap-8 border-b md:border-b-0 md:border-r border-[rgba(200,190,180,0.1)] relative z-10 sidebar-panel">"""
    sidebar_end = vision.find('</aside>', vision.find(sidebar_target)) + 8
    
    new_sidebar = """        <!-- SIDEBAR -->
        <aside class="w-full md:w-[240px] py-8 px-6 flex md:flex-col items-start gap-8 border-b md:border-b-0 md:border-r border-[rgba(200,190,180,0.1)] relative z-10 sidebar-panel">
            <div class="flex items-center gap-3 w-full mb-4 cursor-pointer hover:opacity-80 transition" onclick="goSection('view-landing')">
                <div class="w-10 h-10 rounded-xl bg-[#3E3C3A] shadow-[0_4px_10px_rgba(0,0,0,0.2),inset_0_2px_2px_rgba(255,255,255,0.2)] flex items-center justify-center">
                    <div class="w-4 h-4 rounded-md bg-[--bg-wall] shadow-inner"></div>
                </div>
                <span class="font-heading text-lg tracking-tight text-[--text-dark]">TrendBase</span>
            </div>
            
            <nav class="flex md:flex-col gap-2 w-full">
                <button onclick="goSection('inicio')" id="nav-inicio" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl sidebar-item">
                    <i data-lucide="layout-grid" class="w-5 h-5"></i>
                    <span class="font-bold text-sm">Resumen</span>
                </button>
                <button onclick="goSection('tendencias')" id="nav-tendencias" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl sidebar-item">
                    <i data-lucide="flame" class="w-5 h-5"></i>
                    <span class="font-bold text-sm">Tendencias</span>
                </button>
                <button onclick="goSection('analisis')" id="nav-analisis" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl sidebar-item">
                    <i data-lucide="bar-chart-2" class="w-5 h-5"></i>
                    <span class="font-bold text-sm">Análisis</span>
                </button>
                <button onclick="goSection('guardados')" id="nav-guardados" class="w-full flex justify-between items-center px-4 py-3 rounded-xl sidebar-item">
                    <div class="flex items-center gap-3">
                        <i data-lucide="bookmark" class="w-5 h-5"></i>
                        <span class="font-bold text-sm">Guardados</span>
                    </div>
                </button>
            </nav>
        </aside>"""
        
    vision = vision[:vision.find(sidebar_target)] + new_sidebar + vision[sidebar_end:]

    vision_js_start = vision.find('<script>')
    vision_js_end = vision.rfind('</body>')
    
    container_start = vision.find('<!-- MAIN APP CONTAINER -->')
    vision = vision[:container_start] + modals + vision[container_start:]
    vision = vision[:vision.rfind('<script>')] + js_content + "\n" + vision[vision_js_end:]
    
    vision_style_start = vision.find('<style>')
    vision_style_end = vision.find('</style>') + 8
    vision_style = vision[vision_style_start:vision_style_end]
    
    new_head = f"""<head>
    {idx_head}
    {vision_style}
    <style>
        .dash-section {{ display: none; }}
        .active-section {{ display: block; }}
        .sidebar-item.active {{ background: rgba(255,255,255,0.8); color: var(--text-dark); box-shadow: inset 0 2px 4px rgba(255,255,255,1), 0 4px 8px rgba(0,0,0,0.05); }}
    </style>
    </head>"""
    
    vision = vision[:vision.find('<head>')] + new_head + vision[vision.find('</head>') + 7:]
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(vision)
        
    print("Flawless native rebuild complete!")

rebuild_flawless()
