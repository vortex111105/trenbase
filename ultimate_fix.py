import re
import os

def build_ultimate():
    # Load pure original index.html
    os.system('git checkout index.html')
    with open('index.html', 'r', encoding='utf-8') as f:
        idx = f.read()

    # EXTRACT ORIGINAL SECTIONS
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

    # CLEAN COLORS
    def clean_colors(text):
        text = re.sub(r'bg-obsidian|bg-black\b', '', text)
        text = re.sub(r'bg-black/(\d+)', r'bg-[rgba(200,190,180,0.1)]', text)
        text = re.sub(r'bg-white/5|bg-white/10|bg-white/20', 'matte-card', text)
        text = re.sub(r'text-white/(\d+)|text-slate-\d+', 'text-[var(--text-muted)]', text)
        text = re.sub(r'text-white\b|text-ivory\b', 'text-[var(--text-dark)]', text)
        text = re.sub(r'text-obsidian\b', 'text-[var(--text-dark)]', text)
        text = re.sub(r'border-white/10|border-white/5|border-slate-800', 'border-[rgba(200,190,180,0.3)]', text)
        text = re.sub(r'placeholder-white/\d+', 'placeholder-[var(--text-muted)]', text)
        text = text.replace('max-w-7xl mx-auto', 'w-full')
        return text

    modals = clean_colors(modals)
    dash_content = clean_colors(dash_content)

    # ASSEMBLE ULTIMATE PERFECT HTML
    final_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrendBase — Encontrá los productos virales antes que todos</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
      tailwind.config = {{
        theme: {{
          extend: {{
            colors: {{
              obsidian: '#0D0D12',
              champagne: '#C9A84C',
              ivory: '#FAF8F5',
              slate: '#2A2A35',
            }},
            fontFamily: {{
              sans: ['Inter', 'sans-serif'],
              drama: ['Playfair Display', 'serif'],
              mono: ['JetBrains Mono', 'monospace'],
            }}
          }}
        }}
      }}
    </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-wall: #E6DCD1;
            --glass-container: rgba(245, 240, 230, 0.65);
            --matte-card: #FDFBFA;
            --text-dark: #2E2B2A;
            --text-muted: #807A75;
            --soft-green: #599B62;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--bg-wall);
            color: var(--text-dark);
            overflow-x: hidden;
            letter-spacing: -0.02em;
        }}
        
        ::-webkit-scrollbar {{ display: none; }}
        * {{ -ms-overflow-style: none; scrollbar-width: none; }}

        /* The beautiful abstract background */
        .environment-bg {{
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -2;
            background-image: url('https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=1600');
            background-size: cover;
            background-position: center;
        }}
        
        .environment-bg::after {{
            content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(230, 220, 209, 0.4);
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.08'/%3E%3C/svg%3E");
            pointer-events: none;
        }}

        .glass-app-container {{
            background: var(--glass-container);
            backdrop-filter: blur(60px) saturate(140%);
            -webkit-backdrop-filter: blur(60px) saturate(140%);
            border-radius: 40px;
            box-shadow: 0 40px 80px rgba(140, 120, 100, 0.25), inset 0 1px 1px rgba(255,255,255,0.7);
            border: 1px solid rgba(255,255,255,0.4);
            overflow: hidden;
        }}

        .sidebar-panel {{
            background: linear-gradient(180deg, rgba(255,255,255,0.4) 0%, rgba(255,255,255,0.1) 100%);
            backdrop-filter: blur(20px);
        }}

        .matte-card {{
            background: var(--matte-card);
            border-radius: 24px;
            box-shadow: 0 8px 24px rgba(170, 150, 130, 0.1), inset 0 1px 1px rgba(255,255,255,0.8);
            border: 1px solid rgba(255,255,255,0.4);
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .btn-solid {{
            background: linear-gradient(180deg, #3A3A3C 0%, #1C1C1E 100%);
            color: #FDFBFA;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15), inset 0 1px 1px rgba(255,255,255,0.25);
            border-radius: 999px;
            border: 1px solid rgba(0,0,0,0.8);
        }}

        .pill-gray {{
            background: rgba(0,0,0,0.05);
            border: 1px solid rgba(0,0,0,0.1);
            color: var(--text-dark);
            padding: 4px 12px;
            border-radius: 999px;
        }}
        
        .dash-section {{ display: none; }}
        .active-section {{ display: block; }}
        .app-view {{ display: none; }}
        .app-view.active-view {{ display: block; }}
    </style>
</head>
<body class="antialiased min-h-screen flex items-center justify-center p-4 md:p-8">

    <div class="environment-bg"></div>

    <div class="w-full max-w-[1400px] mx-auto glass-app-container flex flex-col md:flex-row h-[90vh] shadow-2xl relative">
        
        <!-- SIDEBAR -->
        <aside class="w-full md:w-[240px] py-8 px-6 flex md:flex-col items-start justify-between gap-8 border-b md:border-b-0 md:border-r border-[rgba(200,190,180,0.2)] relative z-10 sidebar-panel shrink-0">
            <div class="w-full flex flex-col gap-8">
                <div class="flex items-center gap-3 w-full cursor-pointer hover:opacity-80 transition" onclick="goSection('inicio')">
                    <div class="w-10 h-10 rounded-xl bg-[#3E3C3A] flex items-center justify-center">
                        <div class="w-4 h-4 rounded-md bg-[--bg-wall]"></div>
                    </div>
                    <span class="font-bold text-lg tracking-tight text-[--text-dark]">TrendBase</span>
                </div>
                <nav class="flex md:flex-col gap-2 w-full">
                    <button onclick="enterLanding()" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl sidebar-item active">
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
                    </button>
                    <button onclick="goSection('guardados')" id="nav-guardados" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl sidebar-item">
                        <i data-lucide="bookmark" class="w-5 h-5"></i>
                        <span class="font-bold text-sm">Guardados</span>
                    </button>
                </nav>
            </div>
            
            <div class="w-full pt-6 border-t border-[rgba(200,190,180,0.2)]">
                <button onclick="openAuth('login')" class="w-full btn-solid px-4 py-3 text-sm font-bold uppercase tracking-widest">Ingresar</button>
            </div>
        </aside>

        <!-- APP VIEWS -->
        <div class="flex-1 overflow-hidden flex flex-col relative w-full">
            
            <!-- LANDING PAGE (Clean Apple Vision Layout) -->
            <div id="view-landing" class="app-view active-view w-full p-8 md:p-12 overflow-y-auto relative z-10 h-full">
                <!-- HERO SECTION -->
                <section class="mb-16 mt-8">
                    <div class="matte-card p-10 md:p-16 mb-8 flex flex-col items-center text-center">
                        <div class="pill-gray flex items-center gap-2 mb-6 uppercase tracking-widest text-[10px] font-bold">
                            <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                            Monitoreo en tiempo real · latam
                        </div>
                        <h1 class="text-5xl md:text-7xl font-bold max-w-4xl leading-[1.05] mb-6 tracking-tight text-[--text-dark]">
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
                            <button onclick="enterDash()" class="matte-card border border-[rgba(200,190,180,0.8)] px-8 py-4 text-sm uppercase tracking-widest font-bold rounded-full text-[--text-dark] hover:bg-[rgba(0,0,0,0.05)] transition">
                                Ingresar al Dashboard →
                            </button>
                        </div>
                    </div>
                </section>

                <!-- FEATURES SECTION -->
                <section class="mb-16">
                    <div class="text-center mb-8">
                        <span class="pill-gray uppercase tracking-widest text-[10px] mb-3 inline-block font-bold">Métrica y Precisión</span>
                        <h2 class="text-3xl md:text-5xl font-bold tracking-tight text-[--text-dark]">Todo para vender en tendencia</h2>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <div class="matte-card p-8 flex flex-col justify-between">
                            <h3 class="font-bold text-lg text-[--text-dark] mb-6">Detección Viral</h3>
                            <div class="text-[--text-dark] font-bold text-3xl mb-2 tracking-tight">24/7</div>
                            <p class="text-[--text-muted] text-sm">Monitoreo continuo de 47k+ productos.</p>
                        </div>
                        <div class="matte-card p-8 flex flex-col justify-between">
                            <h3 class="font-bold text-lg text-[--text-dark] mb-6">Telemetría Local</h3>
                            <div class="text-[--text-dark] font-bold text-3xl mb-2 tracking-tight">LATAM</div>
                            <p class="text-[--text-muted] text-sm">Métricas precisas en ARS, UYU y CLP.</p>
                        </div>
                        <div class="matte-card p-8 flex flex-col justify-between">
                            <h3 class="font-bold text-lg text-[--text-dark] mb-6">Rentabilidad</h3>
                            <div class="text-[--soft-green] font-bold text-3xl mb-2 flex items-center gap-2 tracking-tight">ROI</div>
                            <p class="text-[--text-muted] text-sm">Cálculo de márgenes cruzando ventas con envío.</p>
                        </div>
                    </div>
                </section>
            </div>

            <!-- DASHBOARD VIEW -->
            <main id="view-dash" class="app-view flex-1 overflow-y-auto relative z-10 w-full flex-col p-6 md:p-10 space-y-8">
                {dash_content}
            </main>
        </div>
    </div>

    {modals}

    {js_content}

    <script>
      function enterLanding() {{
          document.getElementById('view-dash').classList.remove('active-view');
          document.getElementById('view-landing').classList.add('active-view');
          document.querySelectorAll('.dash-section').forEach(el => el.classList.remove('active-section'));
      }}
      function enterDash() {{
          document.getElementById('view-landing').classList.remove('active-view');
          document.getElementById('view-dash').classList.add('active-view');
          goSection('tendencias');
      }}
      // Overwrite the old enterDash function to ensure it toggles correctly
      window.enterDash = enterDash;
    </script>
</body>
</html>"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_html)

    print("Ultimate Fix Applied!")

if __name__ == "__main__":
    build_ultimate()
