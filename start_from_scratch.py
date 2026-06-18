def create_pure_vision_prototype():
    html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrendBase Vision Prototype</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style id="premium-apple-vision-theme">
        :root {
            --bg-wall: #E6DCD1;
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
        
        ::-webkit-scrollbar { display: none; }
        * { -ms-overflow-style: none; scrollbar-width: none; }

        .environment-bg {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -2;
            background-color: #E6DCD1;
            background-image: url('https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?q=80&w=2000&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
        }
        
        .environment-bg::after {
            content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(230, 220, 209, 0.4);
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.08'/%3E%3C/svg%3E");
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

        .font-heading { letter-spacing: -0.04em !important; font-weight: 700 !important; color: var(--text-dark) !important; }
        .text-muted { color: var(--text-muted) !important; font-weight: 500 !important; }
        .text-accent-green { color: var(--soft-green) !important; font-weight: 700 !important; }

        .btn-solid {
            background: #2E2B2A !important; color: #FDFBFA !important; border-radius: 999px !important;
            font-weight: 600 !important; box-shadow: 0 4px 10px rgba(0,0,0,0.15), inset 0 1px 1px rgba(255,255,255,0.15) !important;
            transition: all 0.3s ease !important;
            letter-spacing: -0.01em;
        }
        
        .pill-gray {
            background: #EAE6E1 !important; color: var(--text-dark) !important; border-radius: 999px !important;
            font-weight: 600 !important; padding: 4px 12px !important; font-size: 0.8rem !important;
            box-shadow: inset 0 1px 2px rgba(255,255,255,1) !important;
        }
    </style>
</head>
<body class="antialiased min-h-screen p-4 md:p-8 flex items-center justify-center">

    <div class="environment-bg"></div>

    <div class="w-full max-w-[1400px] mx-auto glass-app-container flex flex-col md:flex-row h-[90vh]">
        
        <!-- SIDEBAR -->
        <aside class="w-full md:w-[240px] py-8 px-6 flex md:flex-col items-start gap-8 border-b md:border-b-0 md:border-r border-[rgba(200,190,180,0.2)]">
            <div class="flex items-center gap-3 w-full mb-4">
                <div class="w-10 h-10 rounded-xl bg-[#3E3C3A] shadow-[0_4px_10px_rgba(0,0,0,0.2),inset_0_2px_2px_rgba(255,255,255,0.2)] flex items-center justify-center">
                    <div class="w-4 h-4 rounded-md bg-[--bg-wall] shadow-inner"></div>
                </div>
                <span class="font-heading text-lg tracking-tight">TrendBase</span>
            </div>
            
            <nav class="flex md:flex-col gap-2 w-full">
                <button class="w-full flex items-center gap-3 px-4 py-3 rounded-xl" style="background: rgba(255,255,255,0.8); box-shadow: inset 0 2px 4px rgba(255,255,255,1), 0 4px 8px rgba(0,0,0,0.05);">
                    <i data-lucide="layout-grid" class="w-5 h-5"></i>
                    <span class="font-bold text-sm">Resumen</span>
                </button>
                <button class="w-full flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-white/50 transition">
                    <i data-lucide="flame" class="w-5 h-5 text-muted"></i>
                    <span class="font-bold text-sm text-muted">Tendencias</span>
                </button>
                <button class="w-full flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-white/50 transition">
                    <i data-lucide="bar-chart-2" class="w-5 h-5 text-muted"></i>
                    <span class="font-bold text-sm text-muted">Análisis</span>
                </button>
                <button class="w-full flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-white/50 transition">
                    <i data-lucide="bell" class="w-5 h-5 text-muted"></i>
                    <span class="font-bold text-sm text-muted">Alertas</span>
                    <span class="ml-auto bg-red-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full">3</span>
                </button>
                <button class="w-full flex justify-between items-center px-4 py-3 rounded-xl hover:bg-white/50 transition">
                    <div class="flex items-center gap-3">
                        <i data-lucide="bookmark" class="w-5 h-5 text-muted"></i>
                        <span class="font-bold text-sm text-muted">Guardados</span>
                    </div>
                </button>
            </nav>
        </aside>

        <!-- MAIN CONTENT AREA -->
        <main class="flex-1 p-8 md:p-12 overflow-y-auto">
            
            <!-- HEADER -->
            <header class="flex justify-between items-center mb-12">
                <h1 class="text-3xl font-heading">TrendBase Overview</h1>
                <button class="btn-solid px-6 py-2.5 text-sm font-bold tracking-widest uppercase">Ingresar</button>
            </header>

            <!-- HERO SECTION -->
            <section class="mb-16">
                <div class="matte-card p-10 md:p-16 mb-8 flex flex-col items-center text-center">
                    <div class="pill-gray flex items-center gap-2 mb-6 uppercase tracking-widest text-[10px] font-bold">
                        <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                        Monitoreo en tiempo real
                    </div>
                    <h2 class="text-5xl md:text-7xl font-heading max-w-4xl leading-[1.05] mb-6 tracking-tighter">
                        Domina el E-Commerce con precisión absoluta.
                    </h2>
                    <p class="text-lg md:text-xl text-[--text-muted] max-w-2xl mb-10">
                        Descubre productos virales antes de que saturen, conéctalos a tu tienda y visualiza tus ganancias.
                    </p>
                    <div class="flex gap-4">
                        <button class="btn-solid px-8 py-4 text-sm uppercase tracking-widest font-bold">Comenzar Gratis</button>
                    </div>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="matte-card p-8">
                        <div class="flex justify-between items-start mb-6">
                            <h3 class="font-heading text-lg font-medium">Detección Virales</h3>
                            <i data-lucide="more-horizontal" class="text-muted w-5 h-5"></i>
                        </div>
                        <div class="text-4xl font-bold mb-2 tracking-tighter">24/7</div>
                        <p class="text-muted text-sm">Escaneo de redes sociales continuo.</p>
                    </div>
                    <div class="matte-card p-8">
                        <div class="flex justify-between items-start mb-6">
                            <h3 class="font-heading text-lg font-medium">Océano Azul</h3>
                            <i data-lucide="more-horizontal" class="text-muted w-5 h-5"></i>
                        </div>
                        <div class="text-4xl font-bold mb-2 tracking-tighter">Score</div>
                        <p class="text-muted text-sm">Alto margen comprobado</p>
                    </div>
                    <div class="matte-card p-8">
                        <div class="flex justify-between items-start mb-6">
                            <h3 class="font-heading text-lg font-medium">Finanzas</h3>
                            <i data-lucide="more-horizontal" class="text-muted w-5 h-5"></i>
                        </div>
                        <div class="text-4xl text-accent-green font-bold mb-2 flex items-center gap-2 tracking-tighter">ROI <i data-lucide="arrow-up-right" class="w-6 h-6"></i></div>
                        <p class="text-muted text-sm">Mide tu retorno cruzando ventas y Ads.</p>
                    </div>
                </div>
            </section>
            
        </main>
    </div>
    
    <script>
        lucide.createIcons();
    </script>
</body>
</html>"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("Pure original prototype created successfully.")

if __name__ == "__main__":
    create_pure_vision_prototype()
