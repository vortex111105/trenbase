import re

def build_masterpiece():
    # Read the original logic
    with open('index.html', 'r', encoding='utf-8') as f:
        idx = f.read()
        
    # Read the perfect aesthetic prototype
    with open('/Users/nachofrag/Desktop/TrendBase_Vision.html', 'r', encoding='utf-8') as f:
        vision = f.read()

    # 1. EXTRACT REAL PUBLIC INFO FROM ORIGINAL
    
    toast_start = idx.find('<!-- Toast Notification Container -->')
    toast_end = idx.find('<!-- A. NAVBAR — "The Floating Island" -->')
    toasts = idx[toast_start:toast_end] if toast_start != -1 else ""
    
    auth_start = idx.find('<!-- AUTHENTICATION MODAL -->')
    auth_end = idx.find('<!-- ─── APP VIEW: LANDING ────────────────────────────────────────────────── -->')
    actual_modals = idx[auth_start:auth_end] if auth_start != -1 else ""
    
    modals = toasts + "\n" + actual_modals

    dash_start = idx.find('<section id="sec-tendencias"')
    dash_end = idx.find('</section>', idx.find('<section id="sec-negocio"')) + 10
    dash_content = idx[dash_start:dash_end]

    js_start = idx.find('<!-- ─── JAVASCRIPT APP ENGINE ───────────────────────────────────────────── -->')
    js_content = idx[js_start:idx.rfind('</body>')]

    # 2. CLEAN UP COLORS (Smooth Apple Vision style)
    def clean_colors(text):
        # Remove dark background blocks
        text = re.sub(r'bg-obsidian|bg-black\b', '', text)
        text = re.sub(r'bg-black/(\d+)', r'bg-[rgba(200,190,180,0.1)]', text)
        # Convert cards to matte-card
        text = re.sub(r'bg-white/5|bg-white/10|bg-white/20', 'matte-card', text)
        # Convert text colors to balanced vision variables
        text = re.sub(r'text-white/(\d+)|text-slate-\d+', 'text-[var(--text-muted)]', text)
        text = re.sub(r'text-white\b|text-ivory\b', 'text-[var(--text-dark)]', text)
        text = re.sub(r'text-obsidian\b', 'text-[var(--text-dark)]', text)
        # Convert borders
        text = re.sub(r'border-white/10|border-white/5|border-slate-800', 'border-[rgba(200,190,180,0.3)]', text)
        text = re.sub(r'placeholder-white/\d+', 'placeholder-[var(--text-muted)]', text)
        text = text.replace('max-w-7xl mx-auto', 'w-full')
        return text

    modals = clean_colors(modals)
    dash_content = clean_colors(dash_content)

    # 3. BUILD THE PERFECT LANDING PAGE
    native_landing = """
        <div id="view-landing" class="app-view active-view dash-section w-full p-8 md:p-12 overflow-y-auto relative z-10">
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
                    <div class="flex flex-wrap justify-center gap-4 items-center">
                        <button onclick="openAuth('signup')" class="btn-solid px-8 py-4 text-sm font-extrabold uppercase tracking-widest">
                            Comenzar gratis (Probar 7 días gratis)
                        </button>
                        <button onclick="enterDash()" class="px-8 py-4 text-sm uppercase tracking-widest font-bold rounded-full text-[--text-dark] hover:bg-[rgba(0,0,0,0.05)] transition border border-[rgba(200,190,180,0.5)]">
                            Ingresar al Dashboard →
                        </button>
                    </div>
                </div>
            </section>

            <!-- DEMO VIDEO SECTION -->
            <section class="mb-16">
                <div class="text-center mb-8">
                    <span class="pill-gray uppercase tracking-widest text-[10px] mb-3 inline-block font-bold">¿Cómo funciona?</span>
                    <h2 class="text-3xl md:text-5xl font-heading tracking-tight text-[--text-dark]">Conoce TrendBase por dentro</h2>
                </div>
                <div class="relative w-full aspect-video rounded-3xl overflow-hidden border border-[rgba(200,190,180,0.3)] matte-card backdrop-blur-xl group">
                    <div class="absolute inset-0 flex flex-col items-center justify-center z-10 pointer-events-none">
                        <div class="w-20 h-20 rounded-full bg-white/20 backdrop-blur flex items-center justify-center mb-4 group-hover:scale-110 transition duration-300">
                            <div class="w-0 h-0 border-t-8 border-b-8 border-l-[14px] border-transparent border-l-[--text-dark] ml-1"></div>
                        </div>
                        <span class="text-sm font-bold tracking-widest text-[--text-dark] uppercase">Ver Demo de 2 minutos</span>
                    </div>
                    <img src="https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=1600" alt="Dashboard Demo" class="w-full h-full object-cover opacity-30 group-hover:opacity-40 transition duration-500">
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
                        <div class="text-[--text-dark] font-bold text-3xl mb-2 tracking-tight">24/7</div>
                        <p class="text-[--text-muted] text-sm">Monitoreo continuo de 47k+ productos en 9 plataformas líderes.</p>
                    </div>
                    <div class="matte-card p-8 flex flex-col justify-between">
                        <div class="flex justify-between items-start mb-6">
                            <h3 class="font-heading text-lg font-medium text-[--text-dark]">Telemetría Local</h3>
                            <i data-lucide="globe" class="text-[--text-muted] w-5 h-5"></i>
                        </div>
                        <div class="text-[--text-dark] font-bold text-3xl mb-2 tracking-tight">LATAM</div>
                        <p class="text-[--text-muted] text-sm">Métricas precisas en ARS, UYU y CLP para evitar riesgos.</p>
                    </div>
                    <div class="matte-card p-8 flex flex-col justify-between">
                        <div class="flex justify-between items-start mb-6">
                            <h3 class="font-heading text-lg font-medium text-[--text-dark]">Rentabilidad</h3>
                            <i data-lucide="calculator" class="text-[--text-muted] w-5 h-5"></i>
                        </div>
                        <div class="text-accent-green font-bold text-3xl mb-2 flex items-center gap-2 tracking-tight">ROI <i data-lucide="arrow-up-right" class="w-6 h-6"></i></div>
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
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12" id="publicLeaderboard"></div>
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
                            </div>
                        </div>
                        <button onclick="openAuth('signup')" class="w-full btn-solid px-4 py-3 text-sm font-bold uppercase tracking-widest mt-8">Empezar Gratis</button>
                    </div>
                    <!-- Startup -->
                    <div class="matte-card p-8 flex flex-col justify-between h-full relative" style="border: 2px solid var(--soft-green);">
                        <div class="absolute -top-3 left-1/2 -translate-x-1/2 pill-active text-[--text-dark] text-[10px] uppercase tracking-widest font-bold bg-[#D3E8D6] px-2 py-0.5 rounded-full shadow-sm">Más Popular</div>
                        <div>
                            <span class="pill-gray uppercase tracking-widest text-[10px] mb-4 inline-block font-bold">Profesional</span>
                            <h3 class="text-2xl font-heading text-[--text-dark] mb-2">Startup</h3>
                            <div class="mb-6"><span class="text-5xl font-heading tracking-tight text-[--text-dark]">$29</span><span class="text-[--text-muted] text-xs ml-1">/mes</span></div>
                            <div class="space-y-3 mb-8">
                                <div class="flex gap-2 text-sm text-[--text-dark] font-medium"><i data-lucide="check" class="w-4 h-4 text-accent-green"></i> Búsquedas Ilimitadas</div>
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
                                <div class="flex gap-2 text-sm text-[--text-dark] font-medium"><i data-lucide="check" class="w-4 h-4 text-accent-green"></i> Soporte 24/7</div>
                            </div>
                        </div>
                        <button onclick="openAuth('signup')" class="w-full btn-solid px-4 py-3 text-sm font-bold uppercase tracking-widest mt-8">Elegir Pro</button>
                    </div>
                </div>
            </section>
        </div>
    """

    # 4. FIX AESTHETICS IN VISION PROTOTYPE
    # Replace background image with elegant dark abstract silver/grey/black fluid
    # Unsplash: 1550684848-fac1c5b4e853 is an elegant dark glass abstract that produces beautiful greys and whites when blurred
    vision = vision.replace(
        "background-image: url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1600');",
        "background-image: url('https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=1600');"
    )
    
    # Flatten the "Old Apple" 3D bevel on matte-card to a modern soft ceramic flat look
    vision = vision.replace(
        'box-shadow: var(--card-shadow), inset 0 2px 4px rgba(255,255,255,1), inset 0 0 0 1px rgba(255,255,255,0.8);',
        'box-shadow: 0 8px 24px rgba(170, 150, 130, 0.1), inset 0 1px 1px rgba(255,255,255,0.8); border: 1px solid rgba(255,255,255,0.4);'
    )
    vision = vision.replace(
        'box-shadow: inset 0 2px 4px rgba(255,255,255,1), 0 4px 8px rgba(0,0,0,0.05);',
        'box-shadow: 0 4px 12px rgba(170, 150, 130, 0.1), inset 0 1px 1px rgba(255,255,255,0.5); border: 1px solid rgba(255,255,255,0.2);'
    )

    # 5. INJECT EVERYTHING INTO VISION PROTOTYPE
    
    demo_start = vision.find('<!-- View Switcher (For Demo Purposes) -->')
    if demo_start != -1:
        demo_end = vision.find('</div>', demo_start) + 6
        vision = vision[:demo_start] + vision[demo_end:]
        
    v_landing_start = vision.find('<main id="view-landing"')
    v_landing_end = vision.find('</main>', v_landing_start) + 7
    vision = vision[:v_landing_start] + native_landing + vision[v_landing_end:]

    v_dash_start = vision.find('<!-- ========================================== -->\n        <!-- DASHBOARD VIEW')
    if v_dash_start == -1:
        v_dash_start = vision.find('<main id="view-dash"')
    v_products_end = vision.find('</main>', vision.find('<main id="view-products"')) + 7
    
    new_dash = f"""
        <!-- DASHBOARD VIEW -->
        <main id="view-dash" class="app-view flex-1 overflow-y-auto relative z-10 w-full flex-col p-6 md:p-10 space-y-8">
            {dash_content}
        </main>
    """
    vision = vision[:v_dash_start] + new_dash + vision[v_products_end:]

    sidebar_start = vision.find('<!-- SIDEBAR -->')
    sidebar_end = vision.find('</aside>', sidebar_start) + 8
    
    new_sidebar = """        <!-- SIDEBAR -->
        <aside class="w-full md:w-[240px] py-8 px-6 flex md:flex-col items-start justify-between gap-8 border-b md:border-b-0 md:border-r border-[rgba(200,190,180,0.1)] relative z-10 sidebar-panel shrink-0">
            <div class="w-full flex flex-col gap-8">
                <div class="flex items-center gap-3 w-full cursor-pointer hover:opacity-80 transition" onclick="goSection('inicio')">
                    <div class="w-10 h-10 rounded-xl bg-[#3E3C3A] shadow-[0_4px_10px_rgba(0,0,0,0.2),inset_0_2px_2px_rgba(255,255,255,0.2)] flex items-center justify-center">
                        <div class="w-4 h-4 rounded-md bg-[--bg-wall] shadow-inner"></div>
                    </div>
                    <span class="font-heading text-lg tracking-tight text-[--text-dark]">TrendBase</span>
                </div>
                
                <nav class="flex md:flex-col gap-2 w-full">
                    <button onclick="goSection('inicio')" id="nav-inicio" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl sidebar-item active">
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
                    <button onclick="goSection('alertas')" id="nav-alertas" class="w-full flex items-center justify-between px-4 py-3 rounded-xl sidebar-item">
                        <div class="flex items-center gap-3">
                            <i data-lucide="bell" class="w-5 h-5"></i>
                            <span class="font-bold text-sm">Alertas</span>
                        </div>
                        <span id="alertBadge" class="hidden bg-red-500 text-white text-[9px] font-mono px-2 py-0.5 rounded-full shadow-sm">3</span>
                    </button>
                    <button onclick="goSection('guardados')" id="nav-guardados" class="w-full flex justify-between items-center px-4 py-3 rounded-xl sidebar-item">
                        <div class="flex items-center gap-3">
                            <i data-lucide="bookmark" class="w-5 h-5"></i>
                            <span class="font-bold text-sm">Guardados</span>
                        </div>
                        <span id="savedCountSidebar" class="bg-[#EAE6E1] text-[--text-dark] text-[9px] font-bold px-2 py-0.5 rounded-full shadow-inner">0</span>
                    </button>
                    <button onclick="goSection('perfil')" id="nav-perfil" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl sidebar-item">
                        <i data-lucide="user" class="w-5 h-5"></i>
                        <span class="font-bold text-sm">Mi perfil</span>
                    </button>
                    <button onclick="goSection('negocio')" id="nav-negocio" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl sidebar-item">
                        <i data-lucide="briefcase" class="w-5 h-5"></i>
                        <span class="font-bold text-sm">Mi negocio</span>
                    </button>
                </nav>
            </div>
            
            <div class="w-full pt-6 border-t border-[rgba(200,190,180,0.1)]">
                <div id="navLoggedOut" class="flex flex-col gap-2 w-full">
                    <button onclick="openAuth('login')" class="w-full btn-solid px-4 py-3 text-sm font-bold uppercase tracking-widest text-center">Ingresar</button>
                </div>
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

    container_end = vision.find('<!-- MAIN APP CONTAINER -->')
    vision = vision[:container_end] + modals + "\n" + vision[container_end:]

    vision_js_start = vision.find('<script>')
    vision_js_end = vision.rfind('</body>')
    vision = vision[:vision_js_start] + js_content + "\n" + vision[vision_js_end:]

    style_inject = """
    <style>
        .dash-section { display: none; }
        .active-section { display: block; }
        .app-view { display: none; }
        .app-view.active-view { display: block; }
    </style>
    """
    vision = vision.replace('</head>', style_inject + '\n</head>')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(vision)

    print("Masterpiece Compiled Successfully!")

if __name__ == "__main__":
    build_masterpiece()
