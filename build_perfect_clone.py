def build_perfect_clone():
    html_content = """<!DOCTYPE html>
<html lang="es" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrendBase - Dominio del E-Commerce</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <!-- Inter Font -->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        :root {
            /* Exact Colors Extracted from Image */
            --bg-wall: #E6DCD1; /* The warm beige wall color */
            --bg-desk: #D5C8B8;
            
            --glass-container: rgba(245, 240, 230, 0.65); /* The massive glass app container */
            
            --matte-card: #FDFBFA; /* The inner opaque ceramic cards */
            
            --text-dark: #2E2B2A; /* Deep warm charcoal */
            --text-muted: #807A75;
            
            --soft-green: #599B62; /* The organic green for +12.4% */
            --soft-red: #C76B6B;
            
            /* Shadows from the image */
            /* 1. The shadow cast by the whole glass app onto the "desk" */
            --app-shadow: 0 40px 80px rgba(140, 120, 100, 0.25), 0 10px 30px rgba(140, 120, 100, 0.1);
            
            /* 2. The shadow of the inner matte cards */
            --card-shadow: 0 12px 30px rgba(170, 150, 130, 0.15), 0 4px 10px rgba(170, 150, 130, 0.05);
            
            /* 3. The inner bevel highlight that gives the 3D ceramic look */
            --card-bevel: inset 0 2px 4px rgba(255, 255, 255, 1), inset 0 0 0 1px rgba(255, 255, 255, 0.8);
            
            /* The inner highlight for the glass */
            --glass-bevel: inset 0 1px 1px rgba(255,255,255,0.7), inset 1px 0 1px rgba(255,255,255,0.4);
        }

        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--bg-wall);
            color: var(--text-dark);
            overflow-x: hidden;
            letter-spacing: -0.015em;
        }

        /* 
         * Background Simulation
         * Simulating the 3D studio lighting and desk gradient from the image 
         */
        .environment-bg {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            z-index: -2;
            background: 
                /* A soft spotlight on the wall */
                radial-gradient(circle at 30% 20%, #F5EEE6 0%, transparent 60%),
                /* The desk horizon line simulated via gradient */
                linear-gradient(to bottom, transparent 65%, #DBCDC0 65%, #C2B3A3 100%);
        }

        /* 
         * The Main Glass Container 
         * (Like the entire app window in the image)
         */
        .glass-app-container {
            background: var(--glass-container);
            backdrop-filter: blur(50px) saturate(120%);
            -webkit-backdrop-filter: blur(50px) saturate(120%);
            border-radius: 32px;
            box-shadow: var(--app-shadow), var(--glass-bevel);
            border: 1px solid rgba(255,255,255,0.3);
            overflow: hidden;
            position: relative;
        }
        
        /* The slightly more yellow/opaque sidebar area effect from the image */
        .glass-app-container::before {
            content: "";
            position: absolute;
            top: 0; left: 0; bottom: 0; width: 80px;
            background: linear-gradient(to right, rgba(240, 230, 215, 0.5), transparent);
            z-index: -1;
        }

        /* 
         * The Inner Matte Cards (Performance Summary, Key Metrics, etc.)
         * These are opaque, white/cream, with soft shadows and inner bevels.
         */
        .matte-card {
            background: var(--matte-card);
            border-radius: 24px;
            box-shadow: var(--card-shadow), var(--card-bevel);
            /* Notice: NO border, the border effect is created entirely by the inset shadow bevel */
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
            color: var(--text-dark);
            position: relative;
        }
        
        .matte-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 16px 40px rgba(170, 150, 130, 0.2), 0 6px 15px rgba(170, 150, 130, 0.08), var(--card-bevel);
        }

        /* Typography matching the image */
        h1, h2, h3, h4, .font-heading {
            letter-spacing: -0.04em;
            color: var(--text-dark);
            font-weight: 700;
        }
        
        .text-data {
            font-size: 2.5rem;
            font-weight: 600;
            letter-spacing: -0.03em;
            line-height: 1;
        }
        
        p, .text-muted {
            color: var(--text-muted);
            font-weight: 500;
        }

        /* Accent Colors */
        .text-accent-green { color: var(--soft-green); }
        .text-accent-red { color: var(--soft-red); }

        /* Buttons */
        .btn-solid {
            background: #2E2B2A;
            color: #FDFBFA;
            border-radius: 999px;
            font-weight: 600;
            box-shadow: 0 4px 10px rgba(0,0,0,0.15), inset 0 1px 1px rgba(255,255,255,0.15);
            transition: all 0.3s ease;
            letter-spacing: -0.01em;
        }
        .btn-solid:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 20px rgba(0,0,0,0.2), inset 0 1px 1px rgba(255,255,255,0.2);
        }

        /* Badges / Small Pills */
        .pill-gray {
            background: #EAE6E1;
            color: var(--text-dark);
            border-radius: 999px;
            font-weight: 600;
            padding: 4px 12px;
            font-size: 0.8rem;
            box-shadow: inset 0 1px 2px rgba(255,255,255,1);
        }
    </style>
</head>
<body class="antialiased min-h-screen py-12 px-4 md:px-12">

    <!-- The 3D Environment Background -->
    <div class="environment-bg"></div>

    <!-- The Entire Website wrapped in the Massive Glass App Container -->
    <div class="max-w-[1400px] mx-auto glass-app-container min-h-[90vh] flex flex-col md:flex-row">
        
        <!-- Left Sidebar (Mimicking the image's layout structure slightly) -->
        <aside class="w-full md:w-24 p-6 flex md:flex-col items-center gap-8 border-b md:border-b-0 md:border-r border-[rgba(200,190,180,0.2)]">
            <!-- App Icon -->
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-stone-600 to-stone-800 shadow-[0_4px_10px_rgba(0,0,0,0.2),inset_0_1px_1px_rgba(255,255,255,0.3)] flex items-center justify-center">
                <i data-lucide="zap" class="w-5 h-5 text-white"></i>
            </div>
            
            <!-- Nav Icons (like the reference) -->
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
        <main class="flex-1 p-8 md:p-12 overflow-y-auto overflow-x-hidden">
            
            <!-- Header (Dashboard Overview style) -->
            <header class="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-4">
                <h1 class="text-3xl font-heading">TrendBase Overview</h1>
                <div class="flex items-center gap-4">
                    <span class="text-sm font-medium text-[--text-muted]">V2.0 Active</span>
                    <div class="pill-gray flex items-center gap-2">ES <i data-lucide="chevron-down" class="w-4 h-4"></i></div>
                    <button class="btn-solid px-6 py-2.5 text-sm ml-4">Crear cuenta</button>
                </div>
            </header>

            <!-- Hero Section mimicking the Grid Layout -->
            <section id="hero" class="mb-16">
                <!-- Big Hero Card -->
                <div class="matte-card p-10 md:p-16 mb-8 flex flex-col items-center text-center">
                    <h2 class="text-5xl md:text-7xl font-heading max-w-4xl leading-[1.1] mb-6">
                        Domina el E-Commerce con precisión absoluta.
                    </h2>
                    <p class="text-lg md:text-xl text-[--text-muted] max-w-2xl mb-10">
                        Descubre productos virales, conéctalos a tu tienda y visualiza todas tus ganancias en un solo workspace.
                    </p>
                    <div class="video-container w-full max-w-4xl rounded-2xl overflow-hidden shadow-inner bg-black relative" style="padding-bottom: 45%;">
                        <!-- Simulated Video Player -->
                        <div class="absolute inset-0 flex items-center justify-center bg-stone-800 bg-opacity-40 group cursor-pointer">
                            <div class="w-20 h-20 rounded-full bg-white/20 backdrop-blur-md border border-white/40 flex items-center justify-center group-hover:scale-105 transition">
                                <i data-lucide="play" class="w-8 h-8 text-white ml-2"></i>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 3 Feature Cards (Mimicking Performance Summary, Key Metrics, Recent Activity) -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6" id="protocol">
                    <!-- Card 1 -->
                    <div class="matte-card p-8">
                        <div class="flex justify-between items-start mb-6">
                            <h3 class="font-heading text-lg">Detección de Virales</h3>
                            <i data-lucide="more-horizontal" class="text-[--text-muted] w-5 h-5"></i>
                        </div>
                        <div class="text-data mb-2">24/7</div>
                        <p class="text-[--text-muted] text-sm">Escaneo de patrones de crecimiento antes de la competencia.</p>
                    </div>

                    <!-- Card 2 -->
                    <div class="matte-card p-8">
                        <div class="flex justify-between items-start mb-6">
                            <h3 class="font-heading text-lg">Océano Azul</h3>
                            <i data-lucide="more-horizontal" class="text-[--text-muted] w-5 h-5"></i>
                        </div>
                        <div class="text-data mb-2">Score</div>
                        <!-- Progress bar simulation like in the image -->
                        <div class="flex gap-2 w-full h-3 mb-2">
                            <div class="w-1/3 bg-[--text-muted] rounded-full"></div>
                            <div class="w-1/3 bg-[--text-muted] rounded-full opacity-60"></div>
                            <div class="w-1/3 bg-[--text-muted] rounded-full opacity-30"></div>
                        </div>
                        <p class="text-[--text-muted] text-sm flex justify-between">Alto margen <span class="font-bold text-[--text-dark]">Comprobado</span></p>
                    </div>

                    <!-- Card 3 -->
                    <div class="matte-card p-8">
                        <div class="flex justify-between items-start mb-6">
                            <h3 class="font-heading text-lg">Control Financiero</h3>
                            <i data-lucide="more-horizontal" class="text-[--text-muted] w-5 h-5"></i>
                        </div>
                        <div class="text-data mb-2 text-accent-green flex items-center gap-2">ROI <i data-lucide="arrow-up-right" class="w-6 h-6"></i></div>
                        <p class="text-[--text-muted] text-sm">Mide tu retorno exacto cruzando ventas y Ads.</p>
                    </div>
                </div>
            </section>

            <!-- Leaderboard Section (Mimicking Team Overview list) -->
            <section id="leaderboard" class="mb-16">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <!-- Text Side -->
                    <div class="p-4 flex flex-col justify-center">
                        <h2 class="text-4xl font-heading mb-4">Productos que imprimen dinero.</h2>
                        <p class="text-[--text-muted] mb-8">El Leaderboard muestra lo que está funcionando EXACTAMENTE hoy.</p>
                        <ul class="space-y-4">
                            <li class="flex items-center gap-3 text-sm font-medium"><i data-lucide="check" class="text-accent-green w-5 h-5"></i> Competencia en vivo</li>
                            <li class="flex items-center gap-3 text-sm font-medium"><i data-lucide="check" class="text-accent-green w-5 h-5"></i> Calculadora de márgenes</li>
                            <li class="flex items-center gap-3 text-sm font-medium"><i data-lucide="check" class="text-accent-green w-5 h-5"></i> Proveedores verificados</li>
                        </ul>
                    </div>
                    
                    <!-- List Side -->
                    <div class="matte-card p-8">
                        <div class="flex justify-between items-start mb-6">
                            <h3 class="font-heading text-lg">Top Ranking Diario</h3>
                            <i data-lucide="more-horizontal" class="text-[--text-muted] w-5 h-5"></i>
                        </div>
                        <div class="space-y-6">
                            <!-- Item -->
                            <div class="flex items-center justify-between">
                                <div class="flex items-center gap-4">
                                    <div class="w-10 h-10 rounded-full bg-[--bg-wall] flex items-center justify-center font-bold shadow-inner">1</div>
                                    <div>
                                        <div class="font-bold text-sm">Ashwagandha</div>
                                        <div class="text-xs text-[--text-muted]">Suplemento</div>
                                    </div>
                                </div>
                                <div class="text-sm font-bold text-accent-green flex items-center">↗ 15%</div>
                            </div>
                            <!-- Item -->
                            <div class="flex items-center justify-between">
                                <div class="flex items-center gap-4">
                                    <div class="w-10 h-10 rounded-full bg-[--bg-wall] flex items-center justify-center font-bold shadow-inner">2</div>
                                    <div>
                                        <div class="font-bold text-sm">Skincare Hialurónico</div>
                                        <div class="text-xs text-[--text-muted]">Cosmética</div>
                                    </div>
                                </div>
                                <div class="text-sm font-bold text-accent-green flex items-center">↗ 12%</div>
                            </div>
                            <!-- Item -->
                            <div class="flex items-center justify-between">
                                <div class="flex items-center gap-4">
                                    <div class="w-10 h-10 rounded-full bg-[--bg-wall] flex items-center justify-center font-bold shadow-inner">3</div>
                                    <div>
                                        <div class="font-bold text-sm">Ropa Seamless</div>
                                        <div class="text-xs text-[--text-muted]">Fitness</div>
                                    </div>
                                </div>
                                <div class="text-sm font-bold text-accent-green flex items-center">↗ 8%</div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Pricing (Mimicking a large multi-column widget) -->
            <section id="pricing" class="mb-16">
                <div class="matte-card p-10 flex flex-col items-center">
                    <h2 class="text-4xl font-heading mb-2 text-center">Inversión transparente.</h2>
                    <p class="text-[--text-muted] mb-12 text-center">Recuperas la suscripción con tu primera venta.</p>
                    
                    <div class="grid grid-cols-1 md:grid-cols-3 w-full gap-8">
                        <!-- Free -->
                        <div class="flex flex-col p-4 border-r border-[rgba(200,190,180,0.3)]">
                            <h3 class="font-heading text-lg mb-1">Básico</h3>
                            <div class="text-4xl font-bold mb-6">Gratis</div>
                            <ul class="space-y-3 mb-8 text-sm text-[--text-muted]">
                                <li>20 productos/mes</li>
                                <li>Historial 7 días</li>
                            </ul>
                            <button class="pill-gray w-full py-3 mt-auto border border-transparent hover:border-[--text-muted] transition">Elegir</button>
                        </div>
                        <!-- Starter -->
                        <div class="flex flex-col p-6 -m-2 bg-white rounded-2xl shadow-[0_10px_30px_rgba(140,120,100,0.1),inset_0_2px_4px_white] relative z-10">
                            <div class="absolute -top-3 left-1/2 -translate-x-1/2 bg-[--soft-green] text-white text-[10px] uppercase font-bold tracking-wider px-3 py-1 rounded-full">Popular</div>
                            <h3 class="font-heading text-lg mb-1">Starter</h3>
                            <div class="text-4xl font-bold mb-6">$19<span class="text-base text-[--text-muted] font-normal">/mo</span></div>
                            <ul class="space-y-3 mb-8 text-sm text-[--text-muted] font-medium">
                                <li class="text-[--text-dark]">150 productos</li>
                                <li class="text-[--text-dark]">Historial 90 días</li>
                                <li class="text-[--text-dark]">Análisis IA</li>
                            </ul>
                            <button class="btn-solid w-full py-3 mt-auto">Suscribirse</button>
                        </div>
                        <!-- Pro -->
                        <div class="flex flex-col p-4 md:pl-8">
                            <h3 class="font-heading text-lg mb-1">Pro</h3>
                            <div class="text-4xl font-bold mb-6">$49<span class="text-base text-[--text-muted] font-normal">/mo</span></div>
                            <ul class="space-y-3 mb-8 text-sm text-[--text-muted]">
                                <li>Ilimitados productos</li>
                                <li>Historial completo</li>
                                <li>IA Ilimitada</li>
                            </ul>
                            <button class="pill-gray w-full py-3 mt-auto border border-transparent hover:border-[--text-muted] transition">Elegir</button>
                        </div>
                    </div>
                </div>
            </section>
            
            <footer class="pt-8 pb-4 border-t border-[rgba(200,190,180,0.3)] flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-[--text-muted]">
                <div class="font-bold text-[--text-dark]">TrendBase © 2026</div>
                <div class="flex gap-4">
                    <a href="#" class="hover:text-[--text-dark] transition">Términos</a>
                    <a href="#" class="hover:text-[--text-dark] transition">Privacidad</a>
                </div>
            </footer>

        </main>
    </div>

    <script>
        lucide.createIcons();
    </script>
</body>
</html>"""

    with open('/Users/nachofrag/Desktop/TrendBase_Vision.html', 'w') as f:
        f.write(html_content)
    
    print("TrendBase Vision OS Built flawlessly.")

build_perfect_clone()
