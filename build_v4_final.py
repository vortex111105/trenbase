import re

def build():
    # Load original working logic (The pure original with real info)
    with open('index.html', 'r', encoding='utf-8') as f:
        idx = f.read()
        
    # Load perfect aesthetic prototype
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

    landing_start = idx.find('<div id="view-landing"')
    landing_end = idx.find('<!-- ─── APP VIEW: DASHBOARD')
    landing_content = idx[landing_start:landing_end]

    dash_start = idx.find('<section id="sec-tendencias"')
    dash_end = idx.find('</section>', idx.find('<section id="sec-negocio"')) + 10
    dash_content = idx[dash_start:dash_end]

    js_start = idx.find('<!-- ─── JAVASCRIPT APP ENGINE ───────────────────────────────────────────── -->')
    js_content = idx[js_start:idx.rfind('</body>')]

    # 2. CLEAN UP COLORS (Smooth Apple Vision style, no harsh blacks/whites)
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
        # Remove any floating island classes that break layout
        text = text.replace('max-w-7xl mx-auto', 'w-full')
        return text

    modals = clean_colors(modals)
    landing_content = clean_colors(landing_content)
    dash_content = clean_colors(dash_content)


    # 3. FIX AESTHETICS IN VISION PROTOTYPE
    
    # Replace background image with elegant abstract grey/glass (No furniture)
    vision = vision.replace(
        "background-image: url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1600');",
        "background-image: url('https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=1600');"
    )
    
    # Flatten the "Old Apple" 3D bevel on matte-card to a modern flat soft glass look
    vision = vision.replace(
        'box-shadow: var(--card-shadow), inset 0 2px 4px rgba(255,255,255,1), inset 0 0 0 1px rgba(255,255,255,0.8);',
        'box-shadow: 0 8px 24px rgba(170, 150, 130, 0.1), inset 0 1px 1px rgba(255,255,255,0.8); border: 1px solid rgba(255,255,255,0.4);'
    )
    vision = vision.replace(
        'box-shadow: inset 0 2px 4px rgba(255,255,255,1), 0 4px 8px rgba(0,0,0,0.05);',
        'box-shadow: 0 4px 12px rgba(170, 150, 130, 0.1), inset 0 1px 1px rgba(255,255,255,0.5);'
    )

    # 4. INJECT EVERYTHING INTO VISION PROTOTYPE
    
    # Replace Demo Buttons
    demo_start = vision.find('<!-- View Switcher (For Demo Purposes) -->')
    if demo_start != -1:
        demo_end = vision.find('</div>', demo_start) + 6
        vision = vision[:demo_start] + vision[demo_end:]
        
    # Replace Landing Page
    v_landing_start = vision.find('<main id="view-landing"')
    v_landing_end = vision.find('</main>', v_landing_start) + 7
    # Make sure landing has app-view
    landing_content = landing_content.replace('id="view-landing" class="app-view active-view"', 'id="view-landing" class="app-view active-view dash-section w-full p-8 md:p-12 overflow-y-auto relative z-10"')
    vision = vision[:v_landing_start] + landing_content + vision[v_landing_end:]

    # Replace Dash View
    v_dash_start = vision.find('<!-- ========================================== -->\n        <!-- DASHBOARD VIEW')
    if v_dash_start == -1:
        v_dash_start = vision.find('<main id="view-dash"')
    v_products_end = vision.find('</main>', vision.find('<main id="view-products"')) + 7
    
    # Notice we give it 'app-view' and NO 'hidden' class! This fixes the missing info.
    new_dash = f"""
        <!-- DASHBOARD VIEW -->
        <main id="view-dash" class="app-view flex-1 overflow-y-auto relative z-10 w-full flex-col p-6 md:p-10 space-y-8">
            {dash_content}
        </main>
    """
    vision = vision[:v_dash_start] + new_dash + vision[v_products_end:]

    # Update Sidebar logic
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

    # Inject Modals
    container_end = vision.find('<!-- MAIN APP CONTAINER -->')
    vision = vision[:container_end] + modals + "\n" + vision[container_end:]

    # Inject JS Engine
    vision_js_start = vision.find('<script>')
    vision_js_end = vision.rfind('</body>')
    vision = vision[:vision_js_start] + js_content + "\n" + vision[vision_js_end:]

    # Add missing CSS hooks
    style_inject = """
    <style>
        .dash-section { display: none; }
        .active-section { display: block; }
        .app-view { display: none; }
        .app-view.active-view { display: block; }
        #view-landing { display: none; }
        #view-landing.active-view { display: block; }
    </style>
    """
    vision = vision.replace('</head>', style_inject + '\n</head>')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(vision)

    print("Final Version Compiled Successfully!")

if __name__ == "__main__":
    build()
