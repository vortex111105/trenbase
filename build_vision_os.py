def generate_vision_os():
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
            /* Vision OS Spatial Palette */
            --glass-bg: rgba(245, 240, 235, 0.45);
            --glass-border: rgba(255, 255, 255, 0.5);
            --glass-highlight: rgba(255, 255, 255, 0.8);
            
            --text-primary: #1C1C1E;
            --text-secondary: #75757A;
            
            --accent-green: #34C759;
            --accent-red: #FF3B30;
            
            /* Spatial Depth Shadows */
            --shadow-contact: 0 2px 4px rgba(100, 90, 80, 0.05);
            --shadow-diffuse: 0 12px 24px rgba(100, 90, 80, 0.1);
            --shadow-ambient: 0 40px 80px rgba(100, 90, 80, 0.15);
            
            --shadow-inner: inset 0 1px 1px var(--glass-highlight), inset 0 -1px 1px rgba(0,0,0,0.02);
        }

        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: #EFEBE6;
            color: var(--text-primary);
            overflow-x: hidden;
            letter-spacing: -0.015em;
        }

        /* 
         * Mesh Gradient & Noise Background
         * This creates the cinematic, photorealistic backdrop
         */
        .spatial-background {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            z-index: -1;
            background: 
                radial-gradient(circle at 15% 10%, rgba(255, 255, 255, 0.9) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(230, 220, 210, 0.8) 0%, transparent 50%),
                radial-gradient(circle at 50% 40%, rgba(250, 245, 240, 0.6) 0%, transparent 60%);
        }
        
        /* Photographic Grain Overlay */
        .spatial-background::after {
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.06'/%3E%3C/svg%3E");
            pointer-events: none;
        }

        /* 
         * Liquid Glass Panels
         * Deep blur, saturation, and multi-layered shadows 
         */
        .glass-panel {
            background: var(--glass-bg);
            backdrop-filter: blur(40px) saturate(160%);
            -webkit-backdrop-filter: blur(40px) saturate(160%);
            border-radius: 40px;
            border: 1px solid var(--glass-border);
            border-top: 1px solid var(--glass-highlight); /* Light bouncing off top edge */
            box-shadow: var(--shadow-contact), var(--shadow-diffuse), var(--shadow-ambient), var(--shadow-inner);
            transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        }
        
        .glass-panel:hover {
            transform: translateY(-4px);
            box-shadow: 0 4px 8px rgba(100, 90, 80, 0.05), 0 20px 40px rgba(100, 90, 80, 0.15), 0 50px 100px rgba(100, 90, 80, 0.2), var(--shadow-inner);
            background: rgba(250, 245, 240, 0.55);
        }

        /* Typography */
        h1, h2, h3, h4 {
            letter-spacing: -0.03em;
            color: var(--text-primary);
        }
        
        p {
            color: var(--text-secondary);
        }

        /* Buttons */
        .btn-solid {
            background: linear-gradient(180deg, #3A3A3C 0%, #1C1C1E 100%);
            color: #F5F5F7;
            border-radius: 999px;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15), inset 0 1px 1px rgba(255,255,255,0.2);
            transition: all 0.3s ease;
            border: 1px solid rgba(0,0,0,0.8);
        }
        
        .btn-solid:hover {
            transform: scale(1.02);
            box-shadow: 0 8px 24px rgba(0,0,0,0.25), inset 0 1px 1px rgba(255,255,255,0.3);
        }

        .btn-glass {
            background: rgba(255, 255, 255, 0.5);
            backdrop-filter: blur(20px);
            color: var(--text-primary);
            border-radius: 999px;
            font-weight: 600;
            border: 1px solid rgba(255,255,255,0.8);
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: all 0.3s ease;
        }
        
        .btn-glass:hover {
            background: rgba(255, 255, 255, 0.8);
            transform: scale(1.02);
        }

        /* Utilities */
        .badge-green {
            background: rgba(52, 199, 89, 0.1);
            color: #248A3D;
            border: 1px solid rgba(52, 199, 89, 0.2);
            padding: 4px 12px;
            border-radius: 999px;
            font-weight: 700;
            font-size: 0.75rem;
        }
        
        /* Video Container - Beautiful iframe integration */
        .video-container {
            position: relative;
            padding-bottom: 56.25%; /* 16:9 */
            height: 0;
            overflow: hidden;
            border-radius: 24px;
            background: #000;
        }
        .video-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
    </style>
</head>
<body class="antialiased">

    <!-- The 3D Environment Background -->
    <div class="spatial-background"></div>

    <!-- Navigation -->
    <nav class="fixed top-6 left-1/2 -translate-x-1/2 w-[95%] max-w-6xl z-50">
        <div class="glass-panel px-8 py-4 flex items-center justify-between !rounded-full">
            <div class="flex items-center gap-3">
                <div class="w-8 h-8 rounded-full bg-gradient-to-br from-stone-200 to-stone-400 flex items-center justify-center shadow-inner">
                    <i data-lucide="zap" class="w-4 h-4 text-white"></i>
                </div>
                <span class="font-extrabold tracking-tight text-lg">TrendBase</span>
            </div>
            <div class="hidden md:flex items-center gap-8 text-sm font-semibold text-[--text-secondary]">
                <a href="#protocol" class="hover:text-[--text-primary] transition">El Protocolo</a>
                <a href="#leaderboard" class="hover:text-[--text-primary] transition">Leaderboard</a>
                <a href="#founder" class="hover:text-[--text-primary] transition">Nosotros</a>
                <a href="#pricing" class="hover:text-[--text-primary] transition">Precios</a>
            </div>
            <div class="flex items-center gap-4">
                <button class="text-sm font-semibold text-[--text-primary] hover:opacity-70 transition">Ingresar</button>
                <button class="btn-solid px-6 py-2.5 text-sm">Comenzar Gratis</button>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="relative z-10 pt-48 pb-20 px-6">
        
        <!-- Hero Section -->
        <section class="max-w-6xl mx-auto flex flex-col items-center text-center mb-40">
            <div class="badge-green mb-8 inline-flex items-center gap-2">
                <span class="relative flex h-2 w-2">
                    <span class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 bg-green-500"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span>
                </span>
                Versión 2.0 en vivo
            </div>
            
            <h1 class="text-6xl md:text-8xl font-extrabold max-w-5xl leading-[0.95] mb-8">
                Domina el E-Commerce <br/>
                <span class="text-transparent bg-clip-text bg-gradient-to-r from-[--text-primary] to-[--text-secondary]">con precisión absoluta.</span>
            </h1>
            
            <p class="text-xl md:text-2xl max-w-3xl mb-12 leading-relaxed">
                Descubre productos virales antes de que saturen, conéctalos a tu tienda y visualiza todas tus ganancias en un solo workspace increíblemente hermoso.
            </p>
            
            <div class="flex flex-col sm:flex-row items-center gap-4 mb-20">
                <button class="btn-solid px-8 py-4 text-lg w-full sm:w-auto">Crear cuenta gratis</button>
                <a href="#demo" class="btn-glass px-8 py-4 text-lg w-full sm:w-auto flex items-center justify-center gap-2">
                    <i data-lucide="play-circle" class="w-5 h-5"></i> Ver Demo
                </a>
            </div>

            <!-- Demo Video Panel (Original Section Restored cleanly) -->
            <div id="demo" class="w-full glass-panel p-4 md:p-6">
                <!-- Mac OS Style Top Bar -->
                <div class="flex items-center gap-2 mb-4 px-2">
                    <div class="w-3 h-3 rounded-full bg-red-400 border border-black/10"></div>
                    <div class="w-3 h-3 rounded-full bg-yellow-400 border border-black/10"></div>
                    <div class="w-3 h-3 rounded-full bg-green-400 border border-black/10"></div>
                </div>
                <div class="video-container">
                    <iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ" title="TrendBase Demo" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                </div>
            </div>
        </section>

        <!-- El Protocolo (Features) -->
        <section id="protocol" class="max-w-6xl mx-auto mb-40">
            <div class="text-center mb-20">
                <h2 class="text-5xl md:text-6xl font-extrabold mb-6">El Protocolo TrendBase.</h2>
                <p class="text-xl max-w-2xl mx-auto">No es magia. Es un sistema estructurado de 3 pasos para minimizar el riesgo y maximizar tus ganancias en el e-commerce.</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <!-- Step 1 -->
                <div class="glass-panel p-10 flex flex-col relative overflow-hidden group">
                    <div class="text-[120px] font-extrabold text-black/5 absolute -top-8 -right-4 transition-transform group-hover:scale-110">1</div>
                    <div class="w-16 h-16 rounded-2xl bg-white shadow-sm flex items-center justify-center mb-8 relative z-10">
                        <i data-lucide="radar" class="w-8 h-8 text-[--text-primary]"></i>
                    </div>
                    <h3 class="text-2xl font-bold mb-4 relative z-10">Detección de Virales</h3>
                    <p class="leading-relaxed relative z-10">Nuestros algoritmos escanean redes 24/7 buscando patrones de crecimiento antes de que la competencia los vea.</p>
                </div>

                <!-- Step 2 -->
                <div class="glass-panel p-10 flex flex-col relative overflow-hidden group">
                    <div class="text-[120px] font-extrabold text-black/5 absolute -top-8 -right-4 transition-transform group-hover:scale-110">2</div>
                    <div class="w-16 h-16 rounded-2xl bg-white shadow-sm flex items-center justify-center mb-8 relative z-10">
                        <i data-lucide="line-chart" class="w-8 h-8 text-[--text-primary]"></i>
                    </div>
                    <h3 class="text-2xl font-bold mb-4 relative z-10">Océano Azul</h3>
                    <p class="leading-relaxed relative z-10">Filtramos la basura. Solo te mostramos productos con alto margen comprobado y baja saturación en el mercado.</p>
                </div>

                <!-- Step 3 -->
                <div class="glass-panel p-10 flex flex-col relative overflow-hidden group">
                    <div class="text-[120px] font-extrabold text-black/5 absolute -top-8 -right-4 transition-transform group-hover:scale-110">3</div>
                    <div class="w-16 h-16 rounded-2xl bg-white shadow-sm flex items-center justify-center mb-8 relative z-10">
                        <i data-lucide="briefcase" class="w-8 h-8 text-[--text-primary]"></i>
                    </div>
                    <h3 class="text-2xl font-bold mb-4 relative z-10">Control Financiero</h3>
                    <p class="leading-relaxed relative z-10">Conecta tu tienda. Mide tu ROI exacto en automático cruzando ventas reales con gastos de publicidad.</p>
                </div>
            </div>
        </section>

        <!-- Leaderboard -->
        <section id="leaderboard" class="max-w-6xl mx-auto mb-40">
            <div class="flex flex-col md:flex-row gap-16 items-center">
                <div class="md:w-1/2">
                    <h2 class="text-5xl font-extrabold mb-6">Productos que imprimen dinero.</h2>
                    <p class="text-lg mb-8 leading-relaxed">No operamos con suposiciones. El Leaderboard muestra lo que está funcionando EXACTAMENTE hoy.</p>
                    <ul class="space-y-4">
                        <li class="flex items-center gap-4">
                            <div class="w-8 h-8 rounded-full bg-[rgba(52,199,89,0.1)] flex items-center justify-center">
                                <i data-lucide="check" class="text-[#248A3D] w-4 h-4"></i>
                            </div>
                            <span class="font-medium">Métricas de competencia en vivo</span>
                        </li>
                        <li class="flex items-center gap-4">
                            <div class="w-8 h-8 rounded-full bg-[rgba(52,199,89,0.1)] flex items-center justify-center">
                                <i data-lucide="check" class="text-[#248A3D] w-4 h-4"></i>
                            </div>
                            <span class="font-medium">Calculadora de márgenes exactos</span>
                        </li>
                        <li class="flex items-center gap-4">
                            <div class="w-8 h-8 rounded-full bg-[rgba(52,199,89,0.1)] flex items-center justify-center">
                                <i data-lucide="check" class="text-[#248A3D] w-4 h-4"></i>
                            </div>
                            <span class="font-medium">Proveedores verificados (AliExpress/CJ)</span>
                        </li>
                    </ul>
                </div>
                <div class="md:w-1/2 w-full">
                    <div class="glass-panel p-8">
                        <div class="flex items-center justify-between mb-6">
                            <h3 class="font-bold text-sm uppercase tracking-widest text-[--text-secondary]">Top Ranking Diario</h3>
                            <i data-lucide="trending-up" class="w-5 h-5 text-[--text-secondary]"></i>
                        </div>
                        <div class="space-y-4">
                            <!-- Item 1 -->
                            <div class="flex items-center justify-between p-4 bg-white/60 rounded-2xl shadow-sm border border-white">
                                <div class="flex items-center gap-4">
                                    <span class="text-2xl font-extrabold text-stone-300">1</span>
                                    <div>
                                        <div class="font-bold">Suplemento Ashwagandha</div>
                                        <div class="text-xs text-[--text-secondary]">Score: 98/100</div>
                                    </div>
                                </div>
                                <div class="badge-green">+15% ROI</div>
                            </div>
                            <!-- Item 2 -->
                            <div class="flex items-center justify-between p-4 bg-white/60 rounded-2xl shadow-sm border border-white">
                                <div class="flex items-center gap-4">
                                    <span class="text-2xl font-extrabold text-stone-300">2</span>
                                    <div>
                                        <div class="font-bold">Set Skincare Hialurónico</div>
                                        <div class="text-xs text-[--text-secondary]">Score: 95/100</div>
                                    </div>
                                </div>
                                <div class="badge-green">+12% ROI</div>
                            </div>
                            <!-- Item 3 -->
                            <div class="flex items-center justify-between p-4 bg-white/60 rounded-2xl shadow-sm border border-white">
                                <div class="flex items-center gap-4">
                                    <span class="text-2xl font-extrabold text-stone-300">3</span>
                                    <div>
                                        <div class="font-bold">Ropa Seamless B2B</div>
                                        <div class="text-xs text-[--text-secondary]">Score: 92/100</div>
                                    </div>
                                </div>
                                <div class="badge-green">+8% ROI</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Pricing Section -->
        <section id="pricing" class="max-w-6xl mx-auto mb-40 text-center">
            <h2 class="text-5xl font-extrabold mb-6">Inversión transparente.</h2>
            <p class="text-lg mb-16 text-[--text-secondary]">Recuperas la suscripción mensual con tu primera venta.</p>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-left">
                <!-- Free -->
                <div class="glass-panel p-10 flex flex-col">
                    <h3 class="text-xl font-bold mb-2">Básico</h3>
                    <p class="text-sm mb-6 h-10">Para empezar y entender el sistema.</p>
                    <div class="text-5xl font-extrabold tracking-tight mb-8">Gratis</div>
                    <ul class="space-y-4 mb-10 flex-1">
                        <li class="flex items-center gap-3 text-sm"><i data-lucide="check" class="w-4 h-4 text-[#248A3D]"></i> 20 productos analizados</li>
                        <li class="flex items-center gap-3 text-sm"><i data-lucide="check" class="w-4 h-4 text-[#248A3D]"></i> Historial 7 días</li>
                        <li class="flex items-center gap-3 text-sm opacity-50"><i data-lucide="x" class="w-4 h-4"></i> Asistente IA</li>
                    </ul>
                    <button class="btn-glass w-full py-4 text-center">Crear cuenta</button>
                </div>

                <!-- Starter -->
                <div class="glass-panel p-10 flex flex-col relative transform md:-translate-y-4 !bg-[rgba(255,255,255,0.7)] shadow-[0_40px_80px_rgba(100,90,80,0.2)]">
                    <div class="absolute -top-4 left-1/2 -translate-x-1/2 bg-[#34C759] text-white px-4 py-1 rounded-full text-xs font-bold tracking-widest uppercase shadow-md">Más Popular</div>
                    <h3 class="text-xl font-bold mb-2">Starter</h3>
                    <p class="text-sm mb-6 h-10">Para el emprendedor que ya vende.</p>
                    <div class="text-5xl font-extrabold tracking-tight mb-8">$19<span class="text-lg text-[--text-secondary] font-medium">/mes</span></div>
                    <ul class="space-y-4 mb-10 flex-1">
                        <li class="flex items-center gap-3 text-sm"><i data-lucide="check" class="w-4 h-4 text-[#248A3D]"></i> 150 productos analizados</li>
                        <li class="flex items-center gap-3 text-sm"><i data-lucide="check" class="w-4 h-4 text-[#248A3D]"></i> Historial 90 días</li>
                        <li class="flex items-center gap-3 text-sm"><i data-lucide="check" class="w-4 h-4 text-[#248A3D]"></i> Análisis IA (10 msg)</li>
                    </ul>
                    <button class="btn-solid w-full py-4 text-center">Suscribirme</button>
                </div>

                <!-- Pro -->
                <div class="glass-panel p-10 flex flex-col">
                    <h3 class="text-xl font-bold mb-2">Pro</h3>
                    <p class="text-sm mb-6 h-10">Para agencias escalando tiendas.</p>
                    <div class="text-5xl font-extrabold tracking-tight mb-8">$49<span class="text-lg text-[--text-secondary] font-medium">/mes</span></div>
                    <ul class="space-y-4 mb-10 flex-1">
                        <li class="flex items-center gap-3 text-sm"><i data-lucide="check" class="w-4 h-4 text-[#248A3D]"></i> Ilimitados productos</li>
                        <li class="flex items-center gap-3 text-sm"><i data-lucide="check" class="w-4 h-4 text-[#248A3D]"></i> Historial Completo</li>
                        <li class="flex items-center gap-3 text-sm"><i data-lucide="check" class="w-4 h-4 text-[#248A3D]"></i> Asistente IA Ilimitado</li>
                    </ul>
                    <button class="btn-glass w-full py-4 text-center">Suscribirme</button>
                </div>
            </div>
        </section>

        <!-- Founder Note -->
        <section id="founder" class="max-w-4xl mx-auto mb-40">
            <div class="glass-panel p-12 md:p-16 relative overflow-hidden">
                <div class="absolute -top-32 -right-32 w-64 h-64 bg-white/40 blur-3xl rounded-full"></div>
                <div class="w-20 h-20 rounded-full bg-stone-300 mb-8 border-4 border-white shadow-xl overflow-hidden">
                    <img src="https://ui-avatars.com/api/?name=N+F&background=1C1C1E&color=fff" alt="Ignacio Fraga" class="w-full h-full object-cover">
                </div>
                <h3 class="text-3xl font-extrabold mb-8 tracking-tight max-w-2xl leading-tight">
                    "Construí TrendBase porque estaba cansado de perder dinero probando productos a ciegas."
                </h3>
                <div class="space-y-6 text-lg leading-relaxed font-serif text-[--text-secondary] max-w-3xl">
                    <p>Hace dos años, quemé miles de dólares en anuncios probando productos que resultaban ser tendencias muertas o sobresaturadas. El e-commerce no se trata de "tener suerte". Se trata de matemáticas y velocidad.</p>
                    <p>Construí este sistema para mi propia agencia, y los resultados fueron tan precisos que decidí abrirlo al público. No te prometo que te harás rico mañana, pero te aseguro que nunca más dependerás de la intuición para encontrar tu producto ganador.</p>
                </div>
                <div class="mt-10">
                    <div class="font-extrabold text-[--text-primary] text-lg">Ignacio Fraga</div>
                    <div class="text-sm font-medium text-[--text-secondary]">Fundador de TrendBase</div>
                </div>
            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer class="relative z-10 py-12 border-t border-[rgba(255,255,255,0.5)] bg-white/20 backdrop-blur-md">
        <div class="max-w-6xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-6">
            <div class="flex items-center gap-2">
                <div class="w-6 h-6 rounded-full bg-gradient-to-br from-stone-200 to-stone-400 flex items-center justify-center shadow-inner">
                    <i data-lucide="zap" class="w-3 h-3 text-white"></i>
                </div>
                <span class="font-extrabold tracking-tight">TrendBase</span>
            </div>
            <p class="text-sm text-[--text-secondary]">© 2026 TrendBase Inc. Diseñado con precisión en el borde.</p>
            <div class="flex gap-6">
                <a href="#" class="text-[--text-secondary] hover:text-[--text-primary] transition"><i data-lucide="twitter" class="w-5 h-5"></i></a>
                <a href="#" class="text-[--text-secondary] hover:text-[--text-primary] transition"><i data-lucide="instagram" class="w-5 h-5"></i></a>
                <a href="#" class="text-[--text-secondary] hover:text-[--text-primary] transition"><i data-lucide="mail" class="w-5 h-5"></i></a>
            </div>
        </div>
    </footer>

    <script>
        lucide.createIcons();
    </script>
</body>
</html>"""

    with open('/Users/nachofrag/Desktop/TrendBase_Vision.html', 'w') as f:
        f.write(html_content)
    
    print("TrendBase Vision OS Built flawlessly.")

generate_vision_os()
