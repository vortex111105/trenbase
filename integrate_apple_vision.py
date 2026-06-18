import re

def execute_integration():
    with open('index.html', 'r') as f:
        content = f.read()

    # 1. NEW CSS SYSTEM
    custom_css = """
  <!-- ─── APPLE LIQUID GLASS SYSTEM ─── -->
  <style id="premium-apple-vision-theme">
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    :root {
        --bg-wall: #E6DCD1;
        --bg-desk: #D5C8B8;
        --glass-container: rgba(245, 240, 230, 0.65);
        --matte-card: #FDFBFA;
        --text-dark: #2E2B2A;
        --text-muted: #807A75;
        --soft-green: #599B62;
        --soft-red: #C76B6B;
        
        --app-shadow: 0 40px 80px rgba(140, 120, 100, 0.25), 0 10px 30px rgba(140, 120, 100, 0.1);
        --card-shadow: 0 12px 30px rgba(170, 150, 130, 0.15), 0 4px 10px rgba(170, 150, 130, 0.05);
        --card-bevel: inset 0 2px 4px rgba(255, 255, 255, 1), inset 0 0 0 1px rgba(255, 255, 255, 0.8);
        --glass-bevel: inset 0 1px 1px rgba(255,255,255,0.7), inset 1px 0 1px rgba(255,255,255,0.4);
    }

    body {
        font-family: 'Inter', -apple-system, sans-serif !important;
        background-color: var(--bg-wall) !important;
        color: var(--text-dark) !important;
        letter-spacing: -0.015em;
        overflow-x: hidden;
    }
    
    /* Hide scrollbars for absolute purity */
    ::-webkit-scrollbar { display: none; }
    * { -ms-overflow-style: none; scrollbar-width: none; }

    .environment-bg {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -2;
        background: radial-gradient(circle at 30% 20%, #F5EEE6 0%, transparent 60%), linear-gradient(to bottom, transparent 65%, #DBCDC0 65%, #C2B3A3 100%);
        pointer-events: none;
    }

    .glass-app-container {
        background: var(--glass-container) !important;
        backdrop-filter: blur(50px) saturate(120%) !important;
        -webkit-backdrop-filter: blur(50px) saturate(120%) !important;
        border-radius: 32px !important;
        box-shadow: var(--app-shadow), var(--glass-bevel) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        position: relative;
    }

    .matte-card {
        background: var(--matte-card) !important;
        border-radius: 24px !important;
        box-shadow: var(--card-shadow), var(--card-bevel) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        color: var(--text-dark) !important;
    }
    .matte-card:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 16px 40px rgba(170, 150, 130, 0.2), 0 6px 15px rgba(170, 150, 130, 0.08), var(--card-bevel) !important;
    }

    .font-heading { letter-spacing: -0.04em !important; font-weight: 700 !important; color: var(--text-dark) !important; }
    .text-data { font-size: 2.5rem !important; font-weight: 700 !important; letter-spacing: -0.03em !important; line-height: 1 !important; color: var(--text-dark) !important; }
    .text-muted { color: var(--text-muted) !important; font-weight: 500 !important; }
    .text-accent-green { color: var(--soft-green) !important; font-weight: 700 !important; }
    .text-accent-red { color: var(--soft-red) !important; font-weight: 700 !important; }

    .btn-solid {
        background: #2E2B2A !important; color: #FDFBFA !important; border-radius: 999px !important;
        font-weight: 600 !important; box-shadow: 0 4px 10px rgba(0,0,0,0.15), inset 0 1px 1px rgba(255,255,255,0.15) !important;
        transition: all 0.3s ease !important;
        letter-spacing: -0.01em;
    }
    .btn-solid:hover { transform: scale(1.02) !important; box-shadow: 0 8px 20px rgba(0,0,0,0.2), inset 0 1px 1px rgba(255,255,255,0.2) !important; }
    
    .pill-gray {
        background: #EAE6E1 !important; color: var(--text-dark) !important; border-radius: 999px !important;
        font-weight: 600 !important; padding: 4px 12px !important; font-size: 0.8rem !important;
        box-shadow: inset 0 1px 2px rgba(255,255,255,1) !important;
    }

    /* ─── DASHBOARD & MODAL OVERRIDES ─── */
    /* Target exactly the dashboard elements to flip them from dark mode to Apple Liquid Glass */
    
    #view-dash .bg-\\[\\#0A0A0A\\] { background: transparent !important; }
    #view-dash .bg-black\\/40 { background: rgba(245, 238, 230, 0.4) !important; }
    
    #view-dash .bg-white\\/5, #view-dash .bg-white\\/10, .product-card, .notification-item, .chat-message {
        background: var(--matte-card) !important;
        border-radius: 20px !important;
        box-shadow: var(--card-shadow), var(--card-bevel) !important;
        border: none !important;
        color: var(--text-dark) !important;
    }
    
    #view-dash .border-white\\/10 { border-color: rgba(200,190,180,0.2) !important; }
    #view-dash .text-white { color: var(--text-dark) !important; }
    #view-dash .text-white\\/70, #view-dash .text-white\\/60, #view-dash .text-white\\/50 { color: var(--text-muted) !important; font-weight: 500 !important; }
    
    /* Highlight states for sidebar */
    #view-dash .hover\\:bg-white\\/5:hover { background: rgba(255,255,255,0.5) !important; color: var(--text-dark) !important; transform: translateX(2px) !important; }
    .active-sidebar-item { background: rgba(255,255,255,0.8) !important; box-shadow: inset 0 1px 1px white !important; color: var(--text-dark) !important; }

    /* Forms & Inputs in Dashboard */
    #view-dash input, #view-dash select, #view-dash textarea {
        background: rgba(255,255,255,0.5) !important; border: 1px solid rgba(255,255,255,0.8) !important;
        color: var(--text-dark) !important; border-radius: 12px !important; box-shadow: inset 0 1px 2px rgba(0,0,0,0.02) !important;
    }
    #view-dash input::placeholder { color: var(--text-muted) !important; }

    /* Modals (Auth, Product View, AI Chat) */
    .fixed.inset-0.z-50 > .absolute.inset-0 { background: rgba(245, 240, 230, 0.6) !important; backdrop-filter: blur(10px) !important; }
    .fixed.inset-0.z-50 > div:not(.absolute) {
        background: var(--glass-container) !important;
        backdrop-filter: blur(50px) saturate(120%) !important;
        border-radius: 32px !important;
        box-shadow: var(--app-shadow), var(--glass-bevel) !important;
        border: 1px solid rgba(255,255,255,0.5) !important;
    }
    .fixed.inset-0.z-50 .text-white { color: var(--text-dark) !important; }
    .fixed.inset-0.z-50 .text-white\\/60 { color: var(--text-muted) !important; }
    .fixed.inset-0.z-50 .bg-white\\/5 { background: rgba(255,255,255,0.5) !important; border: 1px solid rgba(255,255,255,0.8) !important; color: var(--text-dark) !important; }
    .fixed.inset-0.z-50 button[type="submit"], .fixed.inset-0.z-50 button.bg-white { background: #2E2B2A !important; color: #FDFBFA !important; border: none !important; }

    /* Mobile Bottom Nav */
    #mobile-bottom-nav { background: rgba(245, 240, 230, 0.8) !important; backdrop-filter: blur(20px) !important; border-top: 1px solid rgba(255,255,255,0.5) !important; }
    #mobile-bottom-nav button { color: var(--text-muted) !important; }
    #mobile-bottom-nav .text-white { color: var(--text-dark) !important; }
  </style>
"""

    if 'premium-apple-vision-theme' not in content:
        content = content.replace('</head>', custom_css + '\n</head>')

    # 2. Inject environment bg into body
    content = re.sub(r'<body class="[^"]*">', '<body class="antialiased min-h-screen bg-[#E6DCD1] text-[#2E2B2A]">\n<div class="environment-bg"></div>', content)

    # 3. REWRITE LANDING PAGE EXACTLY
    new_landing = """
  <!-- ─── APP VIEW: LANDING ────────────────────────────────────────────────── -->
  <div id="view-landing" class="app-view active-view relative w-full h-full flex flex-col p-4 md:p-8">
    <!-- The Entire Website wrapped in the Massive Glass App Container -->
    <div class="w-full max-w-[1400px] mx-auto glass-app-container min-h-[90vh] flex flex-col md:flex-row">
        
        <!-- Left Sidebar (mimicking the aesthetic reference) -->
        <aside class="w-full md:w-24 p-6 flex md:flex-col items-center gap-8 border-b md:border-b-0 md:border-r border-[rgba(200,190,180,0.2)]">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-stone-600 to-stone-800 shadow-[0_4px_10px_rgba(0,0,0,0.2),inset_0_1px_1px_rgba(255,255,255,0.3)] flex items-center justify-center">
                <i data-lucide="zap" class="w-5 h-5 text-white"></i>
            </div>
            <nav class="flex md:flex-col gap-6 w-full justify-center">
                <a href="#hero" class="w-10 h-10 rounded-xl bg-[rgba(255,255,255,0.5)] shadow-[inset_0_1px_1px_white] flex items-center justify-center text-[--text-dark]"><i data-lucide="layout-dashboard" class="w-5 h-5"></i></a>
                <a href="#protocol" class="w-10 h-10 rounded-xl flex items-center justify-center text-[--text-muted] hover:text-[--text-dark] transition"><i data-lucide="radar" class="w-5 h-5"></i></a>
                <a href="#leaderboard" class="w-10 h-10 rounded-xl flex items-center justify-center text-[--text-muted] hover:text-[--text-dark] transition"><i data-lucide="line-chart" class="w-5 h-5"></i></a>
                <a href="#pricing" class="w-10 h-10 rounded-xl flex items-center justify-center text-[--text-muted] hover:text-[--text-dark] transition"><i data-lucide="credit-card" class="w-5 h-5"></i></a>
            </nav>
            <div class="mt-auto hidden md:flex">
                <a href="#founder" class="w-10 h-10 rounded-xl flex items-center justify-center text-[--text-muted] hover:text-[--text-dark] transition"><i data-lucide="settings" class="w-5 h-5"></i></a>
            </div>
        </aside>

        <!-- Main Content Area -->
        <main class="flex-1 p-8 md:p-12 overflow-y-auto">
            
            <!-- Header -->
            <header class="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-4">
                <h1 class="text-3xl font-heading">TrendBase Overview</h1>
                <div class="flex items-center gap-4">
                    <span class="text-sm font-medium text-[--text-muted]">V2.0 Active</span>
                    <button onclick="openAuth('login')" class="font-bold text-[--text-dark] text-sm hover:opacity-70 transition">Ingresar</button>
                    <button onclick="openAuth('signup')" class="btn-solid px-6 py-2.5 text-sm ml-4">Crear cuenta</button>
                </div>
            </header>

            <!-- Hero Section -->
            <section id="hero" class="mb-16">
                <div class="matte-card p-10 md:p-16 mb-8 flex flex-col items-center text-center">
                    <h2 class="text-5xl md:text-7xl font-heading max-w-4xl leading-[1.05] mb-6 tracking-tighter">
                        Domina el E-Commerce con precisión absoluta.
                    </h2>
                    <p class="text-lg md:text-xl text-[--text-muted] max-w-2xl mb-10">
                        Descubre productos virales antes de que saturen, conéctalos a tu tienda y visualiza tus ganancias.
                    </p>
                    <div class="video-container w-full max-w-4xl rounded-2xl overflow-hidden shadow-inner bg-black relative" style="padding-bottom: 45%;">
                        <div class="absolute inset-0 flex items-center justify-center bg-stone-800 bg-opacity-40 group cursor-pointer" onclick="document.getElementById('yt-iframe').src='https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=1'">
                            <div class="w-20 h-20 rounded-full bg-white/20 backdrop-blur-md border border-white/40 flex items-center justify-center group-hover:scale-105 transition">
                                <i data-lucide="play" class="w-8 h-8 text-white ml-2"></i>
                            </div>
                        </div>
                        <iframe id="yt-iframe" class="absolute inset-0 w-full h-full" src="" frameborder="0" allowfullscreen></iframe>
                    </div>
                </div>

                <!-- 3 Feature Cards (Matte Ceramic) -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6" id="protocol">
                    <div class="matte-card p-8">
                        <div class="flex justify-between items-start mb-6">
                            <h3 class="font-heading text-lg font-medium">Detección Virales</h3>
                            <i data-lucide="more-horizontal" class="text-muted w-5 h-5"></i>
                        </div>
                        <div class="text-data mb-2 tracking-tighter">24/7</div>
                        <p class="text-muted text-sm">Escaneo de redes sociales continuo.</p>
                    </div>
                    <div class="matte-card p-8">
                        <div class="flex justify-between items-start mb-6">
                            <h3 class="font-heading text-lg font-medium">Océano Azul</h3>
                            <i data-lucide="more-horizontal" class="text-muted w-5 h-5"></i>
                        </div>
                        <div class="text-data mb-2 tracking-tighter">Score</div>
                        <div class="flex gap-2 w-full h-3 mb-2">
                            <div class="w-1/3 bg-[#807A75] rounded-full"></div>
                            <div class="w-1/3 bg-[#807A75] rounded-full opacity-60"></div>
                            <div class="w-1/3 bg-[#807A75] rounded-full opacity-30"></div>
                        </div>
                        <p class="text-muted text-sm">Alto margen <span class="font-bold text-[--text-dark]">Comprobado</span></p>
                    </div>
                    <div class="matte-card p-8">
                        <div class="flex justify-between items-start mb-6">
                            <h3 class="font-heading text-lg font-medium">Finanzas</h3>
                            <i data-lucide="more-horizontal" class="text-muted w-5 h-5"></i>
                        </div>
                        <div class="text-data mb-2 text-accent-green flex items-center gap-2 tracking-tighter">ROI <i data-lucide="arrow-up-right" class="w-6 h-6"></i></div>
                        <p class="text-muted text-sm">Mide tu retorno cruzando ventas y Ads.</p>
                    </div>
                </div>
            </section>

            <!-- Leaderboard -->
            <section id="leaderboard" class="mb-16 grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="p-4 flex flex-col justify-center">
                    <h2 class="text-4xl font-heading mb-4">Productos que imprimen dinero.</h2>
                    <p class="text-muted mb-8">El Leaderboard muestra lo que está funcionando EXACTAMENTE hoy.</p>
                    <ul class="space-y-4">
                        <li class="flex items-center gap-3 text-sm font-medium"><i data-lucide="check" class="text-accent-green w-5 h-5"></i> Competencia en vivo</li>
                        <li class="flex items-center gap-3 text-sm font-medium"><i data-lucide="check" class="text-accent-green w-5 h-5"></i> Calculadora de márgenes</li>
                    </ul>
                </div>
                <div class="matte-card p-8">
                    <div class="flex justify-between items-start mb-6">
                        <h3 class="font-heading text-lg font-medium">Top Ranking Diario</h3>
                        <i data-lucide="more-horizontal" class="text-muted w-5 h-5"></i>
                    </div>
                    <div class="space-y-6">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-4">
                                <div class="w-10 h-10 rounded-full bg-[--bg-wall] flex items-center justify-center font-bold shadow-inner">1</div>
                                <div><div class="font-bold text-sm">Ashwagandha</div><div class="text-xs text-muted">Suplemento</div></div>
                            </div>
                            <div class="text-sm text-accent-green tracking-tighter font-bold">↗ 15%</div>
                        </div>
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-4">
                                <div class="w-10 h-10 rounded-full bg-[--bg-wall] flex items-center justify-center font-bold shadow-inner">2</div>
                                <div><div class="font-bold text-sm">Skincare Hialurónico</div><div class="text-xs text-muted">Cosmética</div></div>
                            </div>
                            <div class="text-sm text-accent-green tracking-tighter font-bold">↗ 12%</div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Pricing -->
            <section id="pricing" class="mb-16 matte-card p-10 flex flex-col items-center">
                <h2 class="text-4xl font-heading mb-2 text-center">Inversión transparente.</h2>
                <p class="text-muted mb-12 text-center">Recuperas la suscripción con tu primera venta.</p>
                <div class="grid grid-cols-1 md:grid-cols-3 w-full gap-8">
                    <div class="flex flex-col p-4 border-r border-[rgba(200,190,180,0.3)]">
                        <h3 class="font-heading text-lg mb-1 font-medium">Básico</h3>
                        <div class="text-4xl font-bold mb-6 tracking-tighter">Gratis</div>
                        <ul class="space-y-3 mb-8 text-sm text-muted"><li>20 productos/mes</li><li>Historial 7 días</li></ul>
                        <button onclick="openAuth('signup')" class="pill-gray w-full py-3 mt-auto border border-transparent hover:border-[--text-muted] transition">Elegir</button>
                    </div>
                    <div class="flex flex-col p-6 -m-2 bg-white rounded-2xl shadow-[0_10px_30px_rgba(140,120,100,0.1),inset_0_2px_4px_white] relative z-10">
                        <div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-[#599B62] text-white text-[10px] uppercase font-bold tracking-wider px-3 py-1 rounded-full">Popular</div>
                        <h3 class="font-heading text-lg mb-1 font-medium">Starter</h3>
                        <div class="text-4xl font-bold mb-6 tracking-tighter">$19<span class="text-base text-muted font-normal">/mo</span></div>
                        <ul class="space-y-3 mb-8 text-sm text-[--text-dark] font-medium"><li>150 productos</li><li>Historial 90 días</li><li>Análisis IA</li></ul>
                        <button onclick="openAuth('signup')" class="btn-solid w-full py-3 mt-auto">Suscribirse</button>
                    </div>
                    <div class="flex flex-col p-4 md:pl-8">
                        <h3 class="font-heading text-lg mb-1 font-medium">Pro</h3>
                        <div class="text-4xl font-bold mb-6 tracking-tighter">$49<span class="text-base text-muted font-normal">/mo</span></div>
                        <ul class="space-y-3 mb-8 text-sm text-muted"><li>Ilimitados productos</li><li>Historial completo</li><li>IA Ilimitada</li></ul>
                        <button onclick="openAuth('signup')" class="pill-gray w-full py-3 mt-auto border border-transparent hover:border-[--text-muted] transition">Elegir</button>
                    </div>
                </div>
            </section>

            <footer class="pt-8 pb-4 border-t border-[rgba(200,190,180,0.3)] flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-muted">
                <div class="font-bold text-[--text-dark]">TrendBase © 2026</div>
                <div class="flex gap-4"><a href="#" class="hover:text-[--text-dark] transition">Privacidad</a></div>
            </footer>
        </main>
    </div>
  </div>
"""

    start_landing = "  <!-- ─── APP VIEW: LANDING ────────────────────────────────────────────────── -->"
    end_landing = "  <!-- ─── APP VIEW: DASHBOARD ─────────────────────────────────────────────── -->"
    
    idx_landing_start = content.find(start_landing)
    idx_landing_end = content.find(end_landing)
    
    if idx_landing_start != -1 and idx_landing_end != -1:
        # Wrap the dashboard in the new glass container visually via classes, but keep HTML logic intact!
        dashboard_content = content[idx_landing_end:]
        dashboard_content = dashboard_content.replace('class="min-h-screen grid grid-cols-1 md:grid-cols-[240px_1fr] pt-24 pb-20 md:pb-0"', 'class="w-full max-w-[1400px] mx-auto glass-app-container min-h-[90vh] grid grid-cols-1 md:grid-cols-[240px_1fr] md:my-6 md:p-0 p-4 mb-20"')
        
        new_content = content[:idx_landing_start] + new_landing + "\n" + dashboard_content
        with open('index.html', 'w') as f:
            f.write(new_content)
        print("Integration successful!")
    else:
        print("Could not find delimiters.")

execute_integration()
