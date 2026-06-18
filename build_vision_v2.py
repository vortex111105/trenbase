def build_v2():
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
            --app-shadow: 0 40px 80px rgba(140, 120, 100, 0.25), 0 10px 30px rgba(140, 120, 100, 0.1);
            --card-shadow: 0 12px 30px rgba(170, 150, 130, 0.15), 0 4px 10px rgba(170, 150, 130, 0.05);
            
            /* Bevels */
            --card-bevel: inset 0 2px 5px rgba(255, 255, 255, 1), inset 0 0 0 1px rgba(255, 255, 255, 0.6);
            --glass-bevel: inset 0 1px 1px rgba(255,255,255,0.8), inset 1px 0 1px rgba(255,255,255,0.5);
        }

        body {
            font-family: 'Inter', -apple-system, sans-serif;
            background-color: var(--bg-wall);
            color: var(--text-dark);
            overflow-x: hidden;
            letter-spacing: -0.02em; /* Tighter letter spacing globally */
        }
        
        ::-webkit-scrollbar { display: none; }
        * { -ms-overflow-style: none; scrollbar-width: none; }

        .environment-bg {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -2;
            /* Using a real photographic background so the glass actually has something to blur and refract */
            background-color: #E6DCD1;
            background-image: url('https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?q=80&w=2000&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
        }
        
        /* Photographic Grain Overlay for realism + slight dimming of the background photo */
        .environment-bg::after {
            content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(230, 220, 209, 0.4); /* Soft warm overlay to keep text legible */
            background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.08'/%3E%3C/svg%3E");
            pointer-events: none;
        }

        .glass-app-container {
            background: var(--glass-container);
            backdrop-filter: blur(60px) saturate(140%);
            -webkit-backdrop-filter: blur(60px) saturate(140%);
            border-radius: 40px; /* Even rounder like the image */
            box-shadow: var(--app-shadow), var(--glass-bevel);
            border: 1px solid rgba(255,255,255,0.4);
            overflow: hidden;
            position: relative;
        }
        
        /* Make the sidebar stand out distinctly instead of blending */
        .sidebar-panel {
            background: rgba(255, 250, 245, 0.35);
            backdrop-filter: blur(10px);
            border-right: 1px solid rgba(255,255,255,0.7);
            box-shadow: 4px 0 20px rgba(170, 150, 130, 0.1);
        }

        .matte-card {
            background: var(--matte-card);
            border-radius: 28px; /* Softer radius for cards */
            box-shadow: var(--card-shadow), var(--card-bevel);
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            color: var(--text-dark);
            position: relative;
        }
        .matte-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 50px rgba(170, 150, 130, 0.25), 0 8px 20px rgba(170, 150, 130, 0.1), var(--card-bevel);
        }

        /* Typography Polish */
        h1, h2, h3, h4, .font-heading { letter-spacing: -0.05em; color: var(--text-dark); font-weight: 800; }
        .text-data { font-size: 2.75rem; font-weight: 700; letter-spacing: -0.05em; line-height: 1; color: var(--text-dark); }
        p, .text-muted { color: var(--text-muted); font-weight: 500; }
        .text-accent-green { color: var(--soft-green); font-weight: 800; letter-spacing: -0.02em; }
        .text-accent-red { color: var(--soft-red); font-weight: 800; letter-spacing: -0.02em; }

        /* Small Pills */
        .pill-gray {
            background: #EAE6E1; color: var(--text-dark); border-radius: 999px; font-weight: 700;
            padding: 4px 14px; font-size: 0.8rem; box-shadow: inset 0 1px 3px rgba(255,255,255,1), 0 1px 2px rgba(0,0,0,0.05);
            letter-spacing: -0.01em;
        }
        
        .pill-active {
            background: rgba(255,255,255,0.9); box-shadow: inset 0 1px 2px white, 0 2px 5px rgba(0,0,0,0.05); color: var(--text-dark); font-weight: 800;
        }

        /* Buttons */
        .btn-solid {
            background: linear-gradient(180deg, #3A3A3C 0%, #1C1C1E 100%); color: #FDFBFA; border-radius: 999px; font-weight: 700;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15), inset 0 1px 1px rgba(255,255,255,0.25); transition: all 0.3s ease; letter-spacing: -0.02em;
            border: 1px solid rgba(0,0,0,0.8);
        }
        .btn-solid:hover { transform: scale(1.02); box-shadow: 0 8px 24px rgba(0,0,0,0.25), inset 0 1px 1px rgba(255,255,255,0.3); }
        
        .sidebar-item {
            color: var(--text-muted); transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .sidebar-item:hover { color: var(--text-dark); background: rgba(255,255,255,0.4); transform: translateX(4px); }
        .sidebar-item.active {
            background: rgba(255,255,255,0.8); color: var(--text-dark); box-shadow: inset 0 2px 4px rgba(255,255,255,1), 0 4px 8px rgba(0,0,0,0.05);
        }
    </style>
</head>
<body class="antialiased min-h-screen py-6 px-4 md:px-10 flex items-center justify-center">

    <!-- The 3D Environment Background with Grain -->
    <div class="environment-bg"></div>
    
    <!-- View Switcher (For Demo Purposes) -->
    <div class="fixed top-4 left-1/2 -translate-x-1/2 z-50 flex gap-2 bg-[rgba(255,255,255,0.5)] backdrop-blur-md p-1.5 rounded-full shadow-sm border border-white/50">
        <button onclick="showView('landing')" id="btn-landing" class="px-4 py-1.5 rounded-full text-xs font-bold bg-white shadow-sm text-[--text-dark]">Landing Page</button>
        <button onclick="showView('dashboard')" id="btn-dashboard" class="px-4 py-1.5 rounded-full text-xs font-bold text-[--text-muted] hover:text-[--text-dark] transition">Dashboard</button>
    </div>

    <!-- MAIN APP CONTAINER -->
    <div class="w-full max-w-[1280px] mx-auto glass-app-container min-h-[85vh] flex flex-col md:flex-row shadow-2xl relative mt-8">
        
        <!-- SIDEBAR (Matches the original app sections with Apple aesthetic) -->
        <aside class="w-full md:w-[240px] py-8 px-6 flex md:flex-col items-start gap-8 border-b md:border-b-0 md:border-r border-[rgba(200,190,180,0.1)] relative z-10 sidebar-panel">
            <!-- App Icon & Logo -->
            <div class="flex items-center gap-3 w-full mb-4 cursor-pointer hover:opacity-80 transition" onclick="showView('landing')">
                <div class="w-10 h-10 rounded-xl bg-[#3E3C3A] shadow-[0_4px_10px_rgba(0,0,0,0.2),inset_0_2px_2px_rgba(255,255,255,0.2)] flex items-center justify-center">
                    <div class="w-4 h-4 rounded-md bg-[--bg-wall] shadow-inner"></div>
                </div>
                <span class="font-heading text-lg tracking-tight">TrendBase</span>
            </div>
            
            <!-- Nav Menu -->
            <nav class="flex md:flex-col gap-2 w-full">
                <button onclick="showView('dashboard')" id="nav-dash" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl sidebar-item active">
                    <i data-lucide="layout-grid" class="w-5 h-5"></i>
                    <span class="font-bold text-sm">Resumen</span>
                </button>
                <button onclick="showView('products')" id="nav-tendencias" class="w-full flex items-center gap-3 px-4 py-3 rounded-xl sidebar-item">
                    <i data-lucide="flame" class="w-5 h-5"></i>
                    <span class="font-bold text-sm">Tendencias</span>
                </button>
                <button class="w-full flex items-center gap-3 px-4 py-3 rounded-xl sidebar-item">
                    <i data-lucide="bar-chart-2" class="w-5 h-5"></i>
                    <span class="font-bold text-sm">Análisis</span>
                </button>
                <button class="w-full flex justify-between items-center px-4 py-3 rounded-xl sidebar-item">
                    <div class="flex items-center gap-3">
                        <i data-lucide="bell" class="w-5 h-5"></i>
                        <span class="font-bold text-sm">Alertas</span>
                    </div>
                    <span class="bg-red-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full">3</span>
                </button>
                <button class="w-full flex justify-between items-center px-4 py-3 rounded-xl sidebar-item">
                    <div class="flex items-center gap-3">
                        <i data-lucide="bookmark" class="w-5 h-5"></i>
                        <span class="font-bold text-sm">Guardados</span>
                    </div>
                </button>
            </nav>
            
            <div class="mt-auto w-full">
                <button class="w-full flex items-center gap-3 px-4 py-3 rounded-xl sidebar-item">
                    <i data-lucide="user" class="w-5 h-5"></i>
                    <span class="font-bold text-sm">Mi Perfil</span>
                </button>
            </div>
        </aside>

        <!-- ========================================== -->
        <!-- LANDING PAGE VIEW                          -->
        <!-- ========================================== -->
        <main id="view-landing" class="flex-1 p-8 md:p-12 overflow-y-auto hidden">
            <!-- Header -->
            <header class="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-4">
                <h1 class="text-3xl font-heading">TrendBase Overview</h1>
                <div class="flex items-center gap-4">
                    <span class="text-sm font-medium text-[--text-muted]">V2.0 Active</span>
                    <div class="pill-gray flex items-center gap-2">ES <i data-lucide="chevron-down" class="w-4 h-4"></i></div>
                    <button onclick="showView('dashboard')" class="btn-solid px-6 py-2.5 text-sm ml-4">Abrir App</button>
                </div>
            </header>

            <!-- Hero Section -->
            <section class="mb-16">
                <div class="matte-card p-10 md:p-16 mb-8 flex flex-col items-center text-center">
                    <h2 class="text-5xl md:text-7xl font-heading max-w-4xl leading-[1.05] mb-6 tracking-tight">
                        Domina el E-Commerce con precisión absoluta.
                    </h2>
                    <p class="text-lg md:text-xl text-[--text-muted] max-w-2xl mb-10">
                        Descubre productos virales antes de que saturen, conéctalos a tu tienda y visualiza tus ganancias en un solo workspace increíblemente hermoso.
                    </p>
                    <div class="flex gap-4">
                        <button onclick="showView('dashboard')" class="btn-solid px-8 py-4 text-lg">Comenzar Gratis</button>
                    </div>
                </div>

                <!-- 3 Feature Cards -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="matte-card p-8">
                        <div class="flex justify-between items-start mb-6">
                            <h3 class="font-heading text-lg font-medium">Detección Virales</h3>
                            <i data-lucide="more-horizontal" class="text-muted w-5 h-5"></i>
                        </div>
                        <div class="text-data mb-2 tracking-tight">24/7</div>
                        <p class="text-muted text-sm">Escaneo de patrones de crecimiento antes de la competencia.</p>
                    </div>
                    <div class="matte-card p-8">
                        <div class="flex justify-between items-start mb-6">
                            <h3 class="font-heading text-lg font-medium">Océano Azul</h3>
                            <i data-lucide="more-horizontal" class="text-muted w-5 h-5"></i>
                        </div>
                        <div class="text-data mb-2 tracking-tight">Score</div>
                        <div class="flex gap-2 w-full h-3 mb-2">
                            <div class="w-1/3 bg-[#807A75] rounded-full"></div>
                            <div class="w-1/3 bg-[#807A75] rounded-full opacity-60"></div>
                            <div class="w-1/3 bg-[#807A75] rounded-full opacity-30"></div>
                        </div>
                        <p class="text-muted text-sm">Alto margen <span class="font-bold text-[--text-dark]">Comprobado</span></p>
                    </div>
                    <div class="matte-card p-8">
                        <div class="flex justify-between items-start mb-6">
                            <h3 class="font-heading text-lg font-medium">Control Financiero</h3>
                            <i data-lucide="more-horizontal" class="text-muted w-5 h-5"></i>
                        </div>
                        <div class="text-data mb-2 text-accent-green flex items-center gap-2 tracking-tight">ROI <i data-lucide="arrow-up-right" class="w-6 h-6"></i></div>
                        <p class="text-muted text-sm">Mide tu retorno exacto cruzando ventas reales con gastos.</p>
                    </div>
                </div>
            </section>
        </main>


        <!-- ========================================== -->
        <!-- DASHBOARD VIEW (EXACT IMAGE REPLICA)       -->
        <!-- ========================================== -->
        <main id="view-dashboard" class="flex-1 p-8 md:p-10 overflow-y-auto block relative z-10">
            <!-- Header (Exact Replica with Actions) -->
            <header class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4 relative z-50">
                <h1 class="text-[28px] font-heading tracking-tight">Dashboard Overview</h1>
                <div class="flex items-center gap-5 text-sm">
                    <span class="text-[--text-dark] font-medium tracking-tight hidden md:block">Monday, Oct 23, 10:09 AM</span>
                    <div class="pill-gray flex items-center gap-2 font-bold bg-[#E8E1D9] shadow-sm cursor-pointer hover:bg-white transition">ES <i data-lucide="chevron-down" class="w-3 h-3"></i></div>
                    
                    <!-- Nuevas Acciones a la Derecha (Notificaciones y Perfil) -->
                    <div class="flex items-center gap-3 ml-2 border-l border-[rgba(200,190,180,0.3)] pl-5">
                        <button class="relative w-10 h-10 rounded-full bg-[rgba(255,255,255,0.4)] shadow-[inset_0_1px_2px_white] flex items-center justify-center text-[--text-dark] hover:bg-white transition" onclick="toggleMenu('notif-menu')">
                            <i data-lucide="bell" class="w-5 h-5"></i>
                            <span class="absolute top-0 right-0 w-3 h-3 bg-red-500 border-2 border-[#E6DCD1] rounded-full"></span>
                        </button>
                        <button class="w-10 h-10 rounded-full bg-gradient-to-tr from-[#3A3A3C] to-[#1C1C1E] shadow-md flex items-center justify-center text-white font-bold text-sm border-2 border-white cursor-pointer hover:scale-105 transition" onclick="toggleMenu('profile-menu')">
                            NF
                        </button>
                    </div>

                    <!-- Menú de Notificaciones (Frosted Glass) -->
                    <div id="notif-menu" class="hidden absolute top-full right-[60px] mt-2 w-64 glass-app-container p-2 flex flex-col gap-1 shadow-2xl z-50 transform origin-top-right transition-all">
                        <div class="px-3 py-2 border-b border-[rgba(200,190,180,0.2)] mb-1">
                            <span class="font-bold text-[--text-dark] text-sm">Notificaciones</span>
                        </div>
                        <button class="w-full text-left px-3 py-2 rounded-xl text-sm font-medium text-[--text-dark] hover:bg-[rgba(255,255,255,0.6)] transition flex items-start gap-3">
                            <div class="w-2 h-2 rounded-full bg-blue-500 mt-1.5"></div>
                            <div>
                                <span class="block font-bold">Nueva Alerta Viral</span>
                                <span class="block text-xs text-muted">Producto "Glow Serum" subiendo 40%</span>
                            </div>
                        </button>
                    </div>

                    <!-- Menú de Perfil (Frosted Glass) -->
                    <div id="profile-menu" class="hidden absolute top-full right-0 mt-2 w-48 glass-app-container p-2 flex flex-col gap-1 shadow-2xl z-50 transform origin-top-right transition-all">
                        <button class="w-full text-left px-4 py-2.5 rounded-xl text-sm font-medium text-[--text-dark] hover:bg-[rgba(255,255,255,0.6)] transition flex items-center gap-3">
                            <i data-lucide="user" class="w-4 h-4"></i> Mi Cuenta
                        </button>
                        <button class="w-full text-left px-4 py-2.5 rounded-xl text-sm font-medium text-[--text-dark] hover:bg-[rgba(255,255,255,0.6)] transition flex items-center gap-3">
                            <i data-lucide="settings" class="w-4 h-4"></i> Preferencias
                        </button>
                        <div class="h-px bg-[rgba(200,190,180,0.2)] my-1"></div>
                        <button class="w-full text-left px-4 py-2.5 rounded-xl text-sm font-bold text-red-500 hover:bg-[rgba(255,0,0,0.1)] transition flex items-center gap-3">
                            <i data-lucide="log-out" class="w-4 h-4"></i> Cerrar Sesión
                        </button>
                    </div>
                </div>
            </header>

            <!-- Dashboard Content Grid -->
            <div class="flex flex-col gap-6">
                
                <!-- TOP ROW -->
                <div class="grid grid-cols-1 md:grid-cols-[1.4fr_1fr_1fr] gap-6">
                    
                    <!-- Performance Summary -->
                    <div class="matte-card p-6 flex flex-col justify-between">
                        <div class="flex justify-between items-center mb-6">
                            <h3 class="font-medium text-[--text-dark] text-sm tracking-tight">Performance Summary</h3>
                        </div>
                        <div class="mb-5">
                            <div class="text-xs text-[--text-dark] font-medium mb-1">Total Revenue</div>
                            <div class="flex items-baseline gap-3">
                                <div class="text-data">$87,450.00</div>
                                <div class="text-xs text-accent-green flex items-center tracking-tight">↗ +12.4%</div>
                            </div>
                        </div>
                        <div class="mb-5">
                            <div class="text-xs text-[--text-dark] font-medium mb-1">New MRR</div>
                            <div class="flex items-baseline gap-3">
                                <div class="text-[28px] font-semibold tracking-tight leading-none text-[--text-dark]">$14,210.00</div>
                                <div class="text-xs text-accent-green flex items-center tracking-tight">↗ +8.2%</div>
                            </div>
                        </div>
                        <div>
                            <div class="text-xs text-[--text-dark] font-medium mb-1">Active Users</div>
                            <div class="flex items-baseline gap-3">
                                <div class="text-2xl font-semibold tracking-tight leading-none text-[--text-dark]">1,894</div>
                                <div class="text-xs text-accent-red flex items-center tracking-tight">↘ -1.1%</div>
                            </div>
                        </div>
                    </div>

                    <!-- Key Metrics -->
                    <div class="matte-card p-6 flex flex-col">
                        <div class="flex justify-between items-center mb-6">
                            <h3 class="font-medium text-[--text-dark] text-sm tracking-tight">Key Metrics</h3>
                            <i data-lucide="more-horizontal" class="text-muted w-4 h-4"></i>
                        </div>
                        <div class="mb-8">
                            <div class="text-xs text-[--text-dark] font-medium mb-1">Project Pulse</div>
                            <div class="text-base font-semibold tracking-tight mb-3">84% Complete</div>
                            <!-- Bar -->
                            <div class="flex gap-1 w-full h-3 mb-1">
                                <div class="w-1/4 bg-[#6F757D] rounded-full"></div>
                                <div class="w-1/4 bg-[#6F757D] rounded-full"></div>
                                <div class="w-1/4 bg-[#6F757D] rounded-full"></div>
                                <div class="w-1/4 bg-[#D1CECB] rounded-full shadow-inner"></div>
                            </div>
                            <div class="flex justify-between text-[10px] text-muted font-mono px-1">
                                <span>I</span><span></span><span></span><span>80%</span>
                            </div>
                        </div>
                        <div class="mt-auto">
                            <div class="text-xs text-[--text-dark] font-medium mb-1">Client Health</div>
                            <div class="text-2xl font-semibold tracking-tight text-[--text-dark]">Healthy</div>
                        </div>
                    </div>

                    <!-- Recent Activity -->
                    <div class="matte-card p-6 flex flex-col">
                        <div class="flex justify-between items-center mb-6">
                            <h3 class="font-medium text-[--text-dark] text-sm tracking-tight">Recent Activity</h3>
                            <i data-lucide="more-horizontal" class="text-muted w-4 h-4"></i>
                        </div>
                        <div class="space-y-5">
                            <div class="flex justify-between items-start text-sm border-b border-[rgba(200,190,180,0.2)] pb-4">
                                <div><div class="text-xs text-[--text-dark] font-medium">Onboarded:</div><div class="font-medium text-[--text-dark]">Alice Chen</div></div>
                                <span class="text-[11px] text-[--text-dark] font-medium">4h ago</span>
                            </div>
                            <div class="flex justify-between items-start text-sm border-b border-[rgba(200,190,180,0.2)] pb-4">
                                <div><div class="text-xs text-[--text-dark] font-medium">Milestone:</div><div class="font-medium text-[--text-dark]">Gamma launched</div></div>
                                <span class="text-[11px] text-[--text-dark] font-medium">6h ago</span>
                            </div>
                            <div class="flex justify-between items-start text-sm">
                                <div><div class="text-xs text-[--text-dark] font-medium">Task:</div><div class="font-medium text-[--text-dark]">Project Review</div></div>
                                <span class="text-[11px] text-[--text-dark] font-medium">8h ago</span>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- BOTTOM ROW -->
                <div class="grid grid-cols-1 md:grid-cols-[2.4fr_1fr] gap-6">
                    
                    <!-- Growth Chart -->
                    <div class="matte-card p-6 h-64 relative flex flex-col">
                        <div class="flex justify-between items-start mb-2">
                            <div>
                                <h3 class="font-medium text-[--text-dark] text-sm tracking-tight">Growth Chart</h3>
                                <p class="text-xs text-[--text-dark] font-medium">Monthly Growth</p>
                            </div>
                            <i data-lucide="more-horizontal" class="text-muted w-4 h-4"></i>
                        </div>
                        
                        <!-- Chart Mockup exactly like image -->
                        <div class="flex-1 w-full relative mt-4 flex">
                            <!-- Y Axis -->
                            <div class="flex flex-col justify-between text-[11px] text-[--text-dark] font-medium w-6 py-2">
                                <span>18k</span><span>16k</span><span>14k</span><span>12k</span>
                            </div>
                            <!-- Graph Area -->
                            <div class="flex-1 relative border-l border-b border-[rgba(200,190,180,0.3)] ml-2">
                                <!-- Grid Lines -->
                                <div class="absolute top-1/3 w-full h-[1px] bg-[rgba(200,190,180,0.2)]"></div>
                                <div class="absolute top-2/3 w-full h-[1px] bg-[rgba(200,190,180,0.2)]"></div>
                                <!-- Vertical Line -->
                                <div class="absolute right-[20%] h-full w-[1px] bg-[rgba(200,190,180,0.3)]"></div>
                                
                                <!-- The Waveform (Enhanced) -->
                                <svg viewBox="0 0 1000 200" class="absolute inset-0 w-full h-full preserve-3d overflow-visible" preserveAspectRatio="none">
                                    <defs>
                                        <linearGradient id="chartGrad" x1="0" y1="0" x2="0" y2="1">
                                            <stop offset="0%" stop-color="rgba(100,110,120,0.35)" />
                                            <stop offset="50%" stop-color="rgba(100,110,120,0.15)" />
                                            <stop offset="100%" stop-color="rgba(100,110,120,0)" />
                                        </linearGradient>
                                        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
                                            <feGaussianBlur stdDeviation="4" result="blur" />
                                            <feComposite in="SourceGraphic" in2="blur" operator="over" />
                                        </filter>
                                    </defs>
                                    <!-- Fill -->
                                    <path d="M0,160 Q150,90 250,130 T500,100 T700,130 T850,40 L1000,20 L1000,200 L0,200 Z" fill="url(#chartGrad)"></path>
                                    <!-- Line -->
                                    <path d="M0,160 Q150,90 250,130 T500,100 T700,130 T850,40 L1000,20" fill="none" stroke="#2E2B2A" stroke-width="5" filter="url(#glow)"></path>
                                    <!-- Dots -->
                                    <circle cx="250" cy="130" r="6" fill="#FDFBFA" stroke="#2E2B2A" stroke-width="4"></circle>
                                    <circle cx="500" cy="100" r="6" fill="#FDFBFA" stroke="#2E2B2A" stroke-width="4"></circle>
                                    <circle cx="700" cy="130" r="6" fill="#FDFBFA" stroke="#2E2B2A" stroke-width="4"></circle>
                                    <circle cx="850" cy="40" r="7" fill="#FDFBFA" stroke="#2E2B2A" stroke-width="4"></circle>
                                </svg>

                                <!-- Tooltip -->
                                <div class="absolute right-[12%] top-[10%] bg-white px-3 py-1 rounded-md shadow-[0_2px_10px_rgba(0,0,0,0.1),inset_0_1px_1px_white] font-bold text-sm tracking-tight text-[--text-dark]">$16.8k</div>
                            </div>
                        </div>
                        
                        <!-- X Axis -->
                        <div class="flex justify-between text-[11px] text-[--text-dark] font-medium ml-8 mt-2 pr-4">
                            <span>Jul</span><span>Aug</span><span>Sep</span><span>Oct</span>
                        </div>
                    </div>

                    <!-- Team Overview -->
                    <div class="matte-card p-6 h-64 flex flex-col">
                        <div class="flex justify-between items-center mb-6">
                            <h3 class="font-medium text-[--text-dark] text-sm tracking-tight">Team Overview</h3>
                            <i data-lucide="more-horizontal" class="text-muted w-4 h-4"></i>
                        </div>
                        <div class="space-y-4 flex-1 overflow-y-auto">
                            <!-- Team Member -->
                            <div class="flex items-center gap-4">
                                <div class="w-10 h-10 rounded-full bg-[#E8E1D9] flex items-center justify-center font-bold text-sm shadow-inner">ES</div>
                                <div><div class="font-medium text-sm text-[--text-dark]">Active</div><div class="text-[11px] text-[--text-dark] font-medium">Online</div></div>
                            </div>
                            <!-- Team Member -->
                            <div class="flex items-center gap-4">
                                <div class="w-10 h-10 rounded-full bg-[#E8E1D9] flex items-center justify-center font-bold text-sm shadow-inner">AB</div>
                                <div><div class="font-medium text-sm text-[--text-dark]">Active</div><div class="text-[11px] text-[--text-dark] font-medium">Online</div></div>
                            </div>
                            <!-- Team Member -->
                            <div class="flex items-center gap-4">
                                <div class="w-10 h-10 rounded-full bg-[#E8E1D9] flex items-center justify-center font-bold text-sm shadow-inner">CJ</div>
                                <div><div class="font-medium text-sm text-[--text-dark]">Members</div><div class="text-[11px] text-[--text-dark] font-medium">Online</div></div>
                            </div>
                            <!-- Team Member -->
                            <div class="flex items-center gap-4">
                                <div class="w-10 h-10 rounded-full bg-[#E8E1D9] flex items-center justify-center font-bold text-sm shadow-inner">ML</div>
                                <div><div class="font-medium text-sm text-[--text-dark]">Roles</div><div class="text-[11px] text-[--text-dark] font-medium">Online</div></div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </main>
        <!-- ========================================== -->
        <!-- TENDENCIAS / PRODUCTS VIEW                 -->
        <!-- ========================================== -->
        <main id="view-products" class="flex-1 p-8 md:p-10 overflow-y-auto hidden relative z-10">
            <header class="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4 relative z-50">
                <h1 class="text-[28px] font-heading tracking-tight">Tendencias Virales</h1>
                <div class="flex items-center gap-4">
                    <input type="text" placeholder="Buscar productos..." class="px-4 py-2 rounded-xl bg-[rgba(255,255,255,0.5)] border border-[rgba(255,255,255,0.8)] shadow-[inset_0_1px_2px_rgba(0,0,0,0.02)] text-sm focus:outline-none focus:ring-2 focus:ring-[#807A75]">
                    <button class="btn-solid px-4 py-2 text-sm flex items-center gap-2"><i data-lucide="filter" class="w-4 h-4"></i> Filtrar</button>
                </div>
            </header>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <!-- Product Card 1 -->
                <div class="matte-card p-4 flex flex-col group cursor-pointer">
                    <div class="w-full h-48 rounded-2xl bg-[--bg-wall] mb-4 overflow-hidden relative shadow-inner">
                        <!-- Simulated Image Placeholder -->
                        <div class="absolute inset-0 bg-gradient-to-tr from-[#DBCDC0] to-[#E6DCD1] flex items-center justify-center">
                            <i data-lucide="image" class="w-10 h-10 text-[rgba(200,190,180,0.5)]"></i>
                        </div>
                        <div class="absolute top-3 left-3 bg-white/90 backdrop-blur-md px-2 py-1 rounded-lg text-[10px] font-bold shadow-sm flex items-center gap-1"><i data-lucide="flame" class="w-3 h-3 text-orange-500"></i> Viral</div>
                    </div>
                    <div class="flex justify-between items-start mb-2">
                        <h3 class="font-heading text-lg">Glow Serum Pro</h3>
                        <div class="text-accent-green font-bold text-sm tracking-tight">ROI 450%</div>
                    </div>
                    <p class="text-sm text-muted mb-4">Cosmética facial con ácido hialurónico.</p>
                    <div class="flex items-center justify-between mt-auto pt-4 border-t border-[rgba(200,190,180,0.2)]">
                        <div class="text-xs text-muted font-medium">CPA: <span class="text-[--text-dark] font-bold">$3.50</span></div>
                        <div class="text-xs text-muted font-medium">Margen: <span class="text-[--text-dark] font-bold">$15.00</span></div>
                    </div>
                </div>

                <!-- Product Card 2 -->
                <div class="matte-card p-4 flex flex-col group cursor-pointer">
                    <div class="w-full h-48 rounded-2xl bg-[--bg-wall] mb-4 overflow-hidden relative shadow-inner">
                        <div class="absolute inset-0 bg-gradient-to-tr from-[#DBCDC0] to-[#E6DCD1] flex items-center justify-center">
                            <i data-lucide="image" class="w-10 h-10 text-[rgba(200,190,180,0.5)]"></i>
                        </div>
                        <div class="absolute top-3 left-3 bg-white/90 backdrop-blur-md px-2 py-1 rounded-lg text-[10px] font-bold shadow-sm flex items-center gap-1"><i data-lucide="trending-up" class="w-3 h-3 text-blue-500"></i> Estable</div>
                    </div>
                    <div class="flex justify-between items-start mb-2">
                        <h3 class="font-heading text-lg">Corrector Postura Inteligente</h3>
                        <div class="text-accent-green font-bold text-sm tracking-tight">ROI 320%</div>
                    </div>
                    <p class="text-sm text-muted mb-4">Wearable con sensor de vibración.</p>
                    <div class="flex items-center justify-between mt-auto pt-4 border-t border-[rgba(200,190,180,0.2)]">
                        <div class="text-xs text-muted font-medium">CPA: <span class="text-[--text-dark] font-bold">$6.20</span></div>
                        <div class="text-xs text-muted font-medium">Margen: <span class="text-[--text-dark] font-bold">$22.00</span></div>
                    </div>
                </div>
                
                <!-- Product Card 3 -->
                <div class="matte-card p-4 flex flex-col group cursor-pointer">
                    <div class="w-full h-48 rounded-2xl bg-[--bg-wall] mb-4 overflow-hidden relative shadow-inner">
                        <div class="absolute inset-0 bg-gradient-to-tr from-[#DBCDC0] to-[#E6DCD1] flex items-center justify-center">
                            <i data-lucide="image" class="w-10 h-10 text-[rgba(200,190,180,0.5)]"></i>
                        </div>
                        <div class="absolute top-3 left-3 bg-[#2E2B2A] px-2 py-1 rounded-lg text-[10px] font-bold shadow-sm flex items-center gap-1 text-white"><i data-lucide="sparkles" class="w-3 h-3"></i> Nuevo</div>
                    </div>
                    <div class="flex justify-between items-start mb-2">
                        <h3 class="font-heading text-lg">Lámpara Cristal Touch</h3>
                        <div class="text-accent-green font-bold text-sm tracking-tight">ROI 280%</div>
                    </div>
                    <p class="text-sm text-muted mb-4">Iluminación decorativa recargable.</p>
                    <div class="flex items-center justify-between mt-auto pt-4 border-t border-[rgba(200,190,180,0.2)]">
                        <div class="text-xs text-muted font-medium">CPA: <span class="text-[--text-dark] font-bold">$4.10</span></div>
                        <div class="text-xs text-muted font-medium">Margen: <span class="text-[--text-dark] font-bold">$18.50</span></div>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        lucide.createIcons();

        function showView(viewId) {
            document.getElementById('view-landing').classList.add('hidden');
            document.getElementById('view-landing').classList.remove('block');
            document.getElementById('view-dashboard').classList.add('hidden');
            document.getElementById('view-dashboard').classList.remove('block');
            document.getElementById('view-products').classList.add('hidden');
            document.getElementById('view-products').classList.remove('block');

            document.getElementById('btn-landing').className = 'px-4 py-1.5 rounded-full text-xs font-bold text-[--text-muted] hover:text-[--text-dark] transition';
            document.getElementById('btn-dashboard').className = 'px-4 py-1.5 rounded-full text-xs font-bold text-[--text-muted] hover:text-[--text-dark] transition';
            
            // Sidebar resets
            document.getElementById('nav-dash').classList.remove('active');
            document.getElementById('nav-tendencias').classList.remove('active');
            
            if(viewId === 'landing') {
                document.getElementById('view-landing').classList.add('block');
                document.getElementById('view-landing').classList.remove('hidden');
                document.getElementById('btn-landing').className = 'px-4 py-1.5 rounded-full text-xs font-bold bg-white shadow-sm text-[--text-dark]';
            } else if(viewId === 'products') {
                document.getElementById('view-products').classList.add('block');
                document.getElementById('view-products').classList.remove('hidden');
                document.getElementById('btn-dashboard').className = 'px-4 py-1.5 rounded-full text-xs font-bold bg-white shadow-sm text-[--text-dark]';
                document.getElementById('nav-tendencias').classList.add('active');
            } else {
                document.getElementById('view-dashboard').classList.add('block');
                document.getElementById('view-dashboard').classList.remove('hidden');
                document.getElementById('btn-dashboard').className = 'px-4 py-1.5 rounded-full text-xs font-bold bg-white shadow-sm text-[--text-dark]';
                document.getElementById('nav-dash').classList.add('active');
            }
        }
        
        function toggleMenu(menuId) {
            // Close the other menu if open
            if(menuId === 'notif-menu') {
                document.getElementById('profile-menu').classList.add('hidden');
            } else {
                document.getElementById('notif-menu').classList.add('hidden');
            }
            
            // Toggle the requested menu
            const menu = document.getElementById(menuId);
            if (menu.classList.contains('hidden')) {
                menu.classList.remove('hidden');
            } else {
                menu.classList.add('hidden');
            }
        }
        
        // Default View
        showView('dashboard');
    </script>
</body>
</html>"""

    with open('/Users/nachofrag/Desktop/TrendBase_Vision.html', 'w') as f:
        f.write(html_content)
    
    print("TrendBase Vision OS V2 Built flawlessly.")

build_v2()
