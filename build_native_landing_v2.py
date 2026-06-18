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

    # 1. JAVASCRIPT
    js_start = idx.find('<!-- ─── JAVASCRIPT APP ENGINE ───────────────────────────────────────────── -->')
    js_content = idx[js_start:idx.rfind('</body>')]

    # 2. MODALS (Exclude the old Navbar!)
    # We want Toasts, Auth Modal, Product Modal, Onboarding Modal
    toast_start = idx.find('<!-- Toast Notification Container -->')
    toast_end = idx.find('<!-- A. NAVBAR — "The Floating Island" -->')
    toasts = extract_section(idx, '<!-- Toast Notification Container -->', '<!-- A. NAVBAR — "The Floating Island" -->')
    
    modals_start = idx.find('<!-- AUTHENTICATION MODAL -->')
    modals_end = idx.find('<!-- ─── APP VIEW: LANDING ────────────────────────────────────────────────── -->')
    actual_modals = extract_section(idx, '<!-- AUTHENTICATION MODAL -->', '<!-- ─── APP VIEW: LANDING ────────────────────────────────────────────────── -->')
    
    modals = toasts + "\n" + actual_modals

    # 3. REAL DASHBOARD CONTENT (Strip bad Tailwind classes)
    dash_content = extract_section(idx, '<!-- Dashboard Content View Area -->', '<!-- Mobile Navigation Bar -->')
    dash_content = re.sub(r'bg-obsidian|bg-black|bg-ivory|text-slate-\d+|border-slate/\d+', '', dash_content)

    # 4. FULL HEAD (Include Tailwind!)
    head_start = idx.find('<head>') + 6
    head_end = idx.find('</head>')
    idx_head = idx[head_start:head_end]
    
    # Wait, idx_head already has the Tailwind CDN, Google Fonts, etc.
    # But we want to ensure Vision CSS variables are present.

    # 5. PURE HTML LANDING PAGE
    native_landing = """
        <!-- HERO SECTION -->
        <section class="mb-16 mt-8">
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
                    <button onclick="goSection('inicio')" class="btn-solid px-8 py-4 text-sm uppercase tracking-widest font-bold">Comenzar Gratis</button>
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

    # 6. INJECT INTO VISION
    # Remove Demo Buttons
    demo_start = vision.find('<!-- View Switcher (For Demo Purposes) -->')
    if demo_start != -1:
        demo_end = vision.find('</div>', demo_start) + 6
        vision = vision[:demo_start] + vision[demo_end:]

    vision_landing_start = vision.find('<main id="view-landing"')
    vision_landing_end = vision.find('</main>', vision_landing_start) + 7
    
    new_landing = f"""
        <main id="view-landing" class="dash-section active-section flex-1 p-8 md:p-12 overflow-y-auto w-full">
            {native_landing}
        </main>
    """
    vision = vision[:vision_landing_start] + new_landing + vision[vision_landing_end:]

    dash_start = vision.find('<!-- ========================================== -->\n        <!-- DASHBOARD VIEW')
    if dash_start == -1:
        dash_start = vision.find('<main id="view-dash"')
    dash_end = vision.find('</main>', vision.find('id="view-products"') if vision.find('id="view-products"') != -1 else dash_start) + 7
    
    new_dashboard = f"""
        <main id="view-dash" class="flex-1 overflow-y-auto hidden relative z-10 w-full flex-col">
            {dash_content}
        </main>
    """
    vision = vision[:dash_start] + new_dashboard + vision[dash_end:]
    
    # Custom Sidebar with Auth/User Profile at the bottom
    sidebar_target = """        <!-- SIDEBAR (Matches the original app sections with Apple aesthetic) -->"""
    if sidebar_target not in vision:
        sidebar_target = """        <!-- SIDEBAR -->"""
    
    sidebar_start = vision.find(sidebar_target)
    sidebar_end = vision.find('</aside>', sidebar_start) + 8
    
    new_sidebar = """        <!-- SIDEBAR -->
        <aside class="w-full md:w-[240px] py-8 px-6 flex md:flex-col items-start justify-between gap-8 border-b md:border-b-0 md:border-r border-[rgba(200,190,180,0.1)] relative z-10 sidebar-panel shrink-0">
            <div class="w-full flex flex-col gap-8">
                <!-- LOGO -->
                <div class="flex items-center gap-3 w-full cursor-pointer hover:opacity-80 transition" onclick="goSection('view-landing')">
                    <div class="w-10 h-10 rounded-xl bg-[#3E3C3A] shadow-[0_4px_10px_rgba(0,0,0,0.2),inset_0_2px_2px_rgba(255,255,255,0.2)] flex items-center justify-center">
                        <div class="w-4 h-4 rounded-md bg-[--bg-wall] shadow-inner"></div>
                    </div>
                    <span class="font-heading text-lg tracking-tight text-[--text-dark]">TrendBase</span>
                </div>
                
                <!-- NAV MENU -->
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
            </div>
            
            <!-- AUTH / USER PROFILE -->
            <div class="w-full pt-6 border-t border-[rgba(200,190,180,0.1)]">
                <!-- Logged Out State -->
                <div id="navLoggedOut" class="flex flex-col gap-2 w-full">
                    <button onclick="openAuth('login')" class="w-full btn-solid px-4 py-3 text-sm font-bold uppercase tracking-widest text-center">Ingresar</button>
                </div>
                <!-- Logged In State (Hidden by default) -->
                <div id="navLoggedIn" class="hidden flex-col gap-3 w-full">
                    <div class="flex items-center gap-3 px-2">
                        <div id="navUserInitial" class="w-8 h-8 rounded-full bg-[--text-dark] text-white flex items-center justify-center font-bold text-sm shadow-inner">U</div>
                        <div class="flex flex-col">
                            <span id="navUserEmail" class="text-xs font-bold text-[--text-dark] truncate w-24">usuario@email</span>
                            <span id="navUserPlan" class="text-[10px] text-[--text-muted] uppercase tracking-widest font-bold">Free</span>
                        </div>
                    </div>
                    <button onclick="logout()" class="w-full flex items-center gap-3 px-4 py-2 rounded-xl text-sm font-bold text-[--text-muted] hover:bg-[rgba(0,0,0,0.02)] transition">
                        <i data-lucide="log-out" class="w-4 h-4"></i> Salir
                    </button>
                </div>
            </div>
        </aside>"""
        
    vision = vision[:sidebar_start] + new_sidebar + vision[sidebar_end:]

    vision_js_start = vision.find('<script>')
    vision_js_end = vision.rfind('</body>')
    
    container_start = vision.find('<!-- MAIN APP CONTAINER -->')
    vision = vision[:container_start] + modals + vision[container_start:]
    vision = vision[:vision.rfind('<script>')] + js_content + "\n" + vision[vision_js_end:]
    
    vision_style_start = vision.find('<style>')
    vision_style_end = vision.find('</style>', vision_style_start) + 8
    vision_style = vision[vision_style_start:vision_style_end]
    
    # Restore full head from index_backup_broken_ui.html, which has Tailwind CDN and fonts
    # And append the vision_style to it.
    new_head = idx_head + "\n" + vision_style + """
    <style>
        .dash-section { display: none; }
        .active-section { display: block; }
        .sidebar-item.active { background: rgba(255,255,255,0.8); color: var(--text-dark); box-shadow: inset 0 2px 4px rgba(255,255,255,1), 0 4px 8px rgba(0,0,0,0.05); }
    </style>
    </head>
    """
    
    vision = vision[:vision.find('<head>')] + "<head>\n" + new_head + vision[vision.find('</head>') + 7:]
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(vision)
        
    print("Flawless native rebuild complete (Tailwind Restored)!")

rebuild_flawless()
