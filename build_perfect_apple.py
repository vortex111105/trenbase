def build_perfect_apple():
    html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrendBase - Apple Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <style>
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            color: #1A1A1A;
            /* Warm, light office aesthetic (creams, subtle wood textures) */
            background-image: url('https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?q=80&w=2000&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            min-height: 100vh;
        }

        /* Glassmorphism bubbles with smooth rounded corners (squircles), soft drop shadows, and white translucent backgrounds. */
        .apple-widget {
            background: rgba(255, 255, 255, 0.45);
            backdrop-filter: blur(24px) saturate(150%);
            -webkit-backdrop-filter: blur(24px) saturate(150%);
            border-radius: 36px;
            border: 1px solid rgba(255, 255, 255, 0.6);
            border-top: 1px solid rgba(255, 255, 255, 0.9);
            box-shadow: 
                0 20px 40px rgba(0, 0, 0, 0.08), 
                inset 0 2px 4px rgba(255, 255, 255, 0.8),
                inset 0 -2px 4px rgba(255, 255, 255, 0.2);
            transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        }

        .apple-widget:hover {
            transform: translateY(-4px) scale(1.01);
            box-shadow: 
                0 30px 60px rgba(0, 0, 0, 0.12), 
                inset 0 2px 4px rgba(255, 255, 255, 0.9);
            background: rgba(255, 255, 255, 0.55);
        }
        
        .apple-nav {
            background: rgba(255, 255, 255, 0.45);
            backdrop-filter: blur(24px) saturate(150%);
            -webkit-backdrop-filter: blur(24px) saturate(150%);
            border-bottom: 1px solid rgba(255, 255, 255, 0.6);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        }

        /* Neon Green and Striking Red for Financials */
        .neon-green { color: #00D33B; text-shadow: 0 0 10px rgba(0, 211, 59, 0.3); }
        .neon-red { color: #FF3B30; text-shadow: 0 0 10px rgba(255, 59, 48, 0.3); }

        .widget-title {
            font-size: 0.85rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: rgba(26, 26, 26, 0.6);
        }

        .btn-black {
            background: #1A1A1A;
            color: white;
            border-radius: 999px;
            font-weight: 600;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2), inset 0 1px 1px rgba(255,255,255,0.2);
            transition: all 0.2s;
        }
        .btn-black:hover {
            transform: scale(1.05);
            background: #000;
        }
        
        .btn-glass {
            background: rgba(255,255,255,0.6);
            color: #1A1A1A;
            border-radius: 999px;
            font-weight: 600;
            border: 1px solid rgba(255,255,255,0.8);
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            transition: all 0.2s;
        }
        .btn-glass:hover {
            background: rgba(255,255,255,0.9);
            transform: scale(1.05);
        }
        
        /* Thin beautiful scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.1); border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(0,0,0,0.2); }
    </style>
</head>
<body class="antialiased min-h-screen flex flex-col">

    <!-- Top Navigation -->
    <nav class="apple-nav sticky top-0 z-50 w-full px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-2xl bg-white/80 shadow-sm border border-white flex items-center justify-center">
                <i data-lucide="zap" class="w-5 h-5 text-black"></i>
            </div>
            <span class="font-extrabold tracking-tight text-xl">TrendBase</span>
        </div>
        
        <div class="hidden md:flex items-center gap-2 p-1 rounded-full bg-white/30 border border-white/50 backdrop-blur-md">
            <button class="px-6 py-2 rounded-full bg-white shadow-sm font-bold text-sm">Dashboard</button>
            <button class="px-6 py-2 rounded-full font-bold text-sm text-black/60 hover:text-black transition">Tendencias</button>
            <button class="px-6 py-2 rounded-full font-bold text-sm text-black/60 hover:text-black transition">Análisis</button>
        </div>
        
        <div class="flex items-center gap-4">
            <button class="w-10 h-10 rounded-full bg-white/60 border border-white shadow-sm flex items-center justify-center relative">
                <i data-lucide="bell" class="w-5 h-5 text-black"></i>
                <span class="absolute top-0 right-0 w-3 h-3 bg-[#FF3B30] border-2 border-white rounded-full"></span>
            </button>
            <div class="w-10 h-10 rounded-full bg-[#1A1A1A] flex items-center justify-center text-white font-bold border-2 border-white shadow-md cursor-pointer">NF</div>
        </div>
    </nav>

    <!-- Main Dashboard Workspace -->
    <main class="flex-1 p-6 md:p-10 max-w-[1400px] mx-auto w-full">
        
        <!-- Header -->
        <div class="flex flex-col md:flex-row justify-between items-start md:items-end mb-10 gap-4">
            <div>
                <h1 class="text-4xl md:text-5xl font-extrabold tracking-tight mb-2">Panel de Control</h1>
                <p class="text-black/60 font-medium">Lunes, 23 Octubre • Actualizado hace instantes</p>
            </div>
            <div class="flex gap-3">
                <button class="btn-glass px-5 py-2.5 flex items-center gap-2"><i data-lucide="filter" class="w-4 h-4"></i> Filtros</button>
                <button class="btn-black px-6 py-2.5 flex items-center gap-2"><i data-lucide="plus" class="w-4 h-4"></i> Conectar Tienda</button>
            </div>
        </div>

        <!-- Apple Widgets Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            
            <!-- Widget 1: Revenue -->
            <div class="apple-widget p-8 flex flex-col justify-between h-48">
                <div class="flex justify-between items-start">
                    <span class="widget-title">Facturación Total</span>
                    <div class="w-8 h-8 rounded-full bg-white/50 flex items-center justify-center"><i data-lucide="dollar-sign" class="w-4 h-4"></i></div>
                </div>
                <div>
                    <div class="text-4xl font-extrabold tracking-tight mb-2">$124,500</div>
                    <div class="flex items-center gap-2 font-bold neon-green">
                        <i data-lucide="trending-up" class="w-4 h-4"></i> +24.5% este mes
                    </div>
                </div>
            </div>

            <!-- Widget 2: CPA -->
            <div class="apple-widget p-8 flex flex-col justify-between h-48">
                <div class="flex justify-between items-start">
                    <span class="widget-title">CPA Promedio</span>
                    <div class="w-8 h-8 rounded-full bg-white/50 flex items-center justify-center"><i data-lucide="target" class="w-4 h-4"></i></div>
                </div>
                <div>
                    <div class="text-4xl font-extrabold tracking-tight mb-2">$12.40</div>
                    <div class="flex items-center gap-2 font-bold neon-red">
                        <i data-lucide="trending-up" class="w-4 h-4"></i> +5.2% subida en FB
                    </div>
                </div>
            </div>

            <!-- Widget 3: ROI -->
            <div class="apple-widget p-8 flex flex-col justify-between h-48">
                <div class="flex justify-between items-start">
                    <span class="widget-title">ROI Global</span>
                    <div class="w-8 h-8 rounded-full bg-white/50 flex items-center justify-center"><i data-lucide="pie-chart" class="w-4 h-4"></i></div>
                </div>
                <div>
                    <div class="text-4xl font-extrabold tracking-tight mb-2">320%</div>
                    <div class="flex items-center gap-2 font-bold neon-green">
                        <i data-lucide="trending-up" class="w-4 h-4"></i> Óptimo
                    </div>
                </div>
            </div>

            <!-- Widget 4: Active Products -->
            <div class="apple-widget p-8 flex flex-col justify-between h-48">
                <div class="flex justify-between items-start">
                    <span class="widget-title">Productos Testeados</span>
                    <div class="w-8 h-8 rounded-full bg-white/50 flex items-center justify-center"><i data-lucide="package" class="w-4 h-4"></i></div>
                </div>
                <div>
                    <div class="text-4xl font-extrabold tracking-tight mb-2">14</div>
                    <div class="flex items-center gap-2 font-bold text-black/60">
                        3 ganadores activos
                    </div>
                </div>
            </div>

        </div>

        <!-- Big Section: Tendencias -->
        <div class="apple-widget p-8">
            <div class="flex justify-between items-center mb-8">
                <h2 class="text-2xl font-extrabold tracking-tight">Monitoreo de Productos Virales</h2>
                <div class="relative">
                    <i data-lucide="search" class="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-black/40"></i>
                    <input type="text" placeholder="Buscar producto..." class="bg-white/50 border border-white/80 rounded-full pl-12 pr-6 py-3 text-sm font-bold text-black placeholder-black/40 outline-none focus:bg-white/80 transition shadow-sm w-64">
                </div>
            </div>

            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr class="border-b border-black/10 text-black/40 font-bold uppercase text-[10px] tracking-wider">
                            <th class="p-4 w-12 text-center">#</th>
                            <th class="p-4">Producto</th>
                            <th class="p-4">TrendScore</th>
                            <th class="p-4">Margen</th>
                            <th class="p-4">Competencia</th>
                            <th class="p-4 text-right">Venta Est.</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-black/5 font-semibold">
                        <!-- Row 1 -->
                        <tr class="hover:bg-white/40 transition cursor-pointer">
                            <td class="p-4 text-center text-black/40">1</td>
                            <td class="p-4">
                                <div class="flex items-center gap-4">
                                    <div class="w-10 h-10 rounded-xl bg-white/80 border border-white flex items-center justify-center shadow-sm">
                                        <i data-lucide="image" class="w-5 h-5 text-black/20"></i>
                                    </div>
                                    <span class="text-base text-black">Corrector Postura Inteligente</span>
                                </div>
                            </td>
                            <td class="p-4">
                                <span class="bg-black text-white px-3 py-1 rounded-full text-xs">98/100</span>
                            </td>
                            <td class="p-4 neon-green text-base">$22.00</td>
                            <td class="p-4">
                                <span class="bg-[#00D33B]/10 text-[#00D33B] px-3 py-1 rounded-full text-xs border border-[#00D33B]/20">Baja</span>
                            </td>
                            <td class="p-4 text-right text-black/60">$35.00</td>
                        </tr>

                        <!-- Row 2 -->
                        <tr class="hover:bg-white/40 transition cursor-pointer">
                            <td class="p-4 text-center text-black/40">2</td>
                            <td class="p-4">
                                <div class="flex items-center gap-4">
                                    <div class="w-10 h-10 rounded-xl bg-white/80 border border-white flex items-center justify-center shadow-sm">
                                        <i data-lucide="image" class="w-5 h-5 text-black/20"></i>
                                    </div>
                                    <span class="text-base text-black">Lámpara Cristal Touch</span>
                                </div>
                            </td>
                            <td class="p-4">
                                <span class="bg-black/70 text-white px-3 py-1 rounded-full text-xs">92/100</span>
                            </td>
                            <td class="p-4 neon-green text-base">$18.50</td>
                            <td class="p-4">
                                <span class="bg-[#00D33B]/10 text-[#00D33B] px-3 py-1 rounded-full text-xs border border-[#00D33B]/20">Baja</span>
                            </td>
                            <td class="p-4 text-right text-black/60">$25.00</td>
                        </tr>

                        <!-- Row 3 -->
                        <tr class="hover:bg-white/40 transition cursor-pointer">
                            <td class="p-4 text-center text-black/40">3</td>
                            <td class="p-4">
                                <div class="flex items-center gap-4">
                                    <div class="w-10 h-10 rounded-xl bg-white/80 border border-white flex items-center justify-center shadow-sm">
                                        <i data-lucide="image" class="w-5 h-5 text-black/20"></i>
                                    </div>
                                    <span class="text-base text-black">Depiladora Láser IPL</span>
                                </div>
                            </td>
                            <td class="p-4">
                                <span class="bg-black/40 text-white px-3 py-1 rounded-full text-xs">85/100</span>
                            </td>
                            <td class="p-4 neon-red text-base">$8.00</td>
                            <td class="p-4">
                                <span class="bg-[#FF3B30]/10 neon-red px-3 py-1 rounded-full text-xs border border-[#FF3B30]/20">Alta Saturación</span>
                            </td>
                            <td class="p-4 text-right text-black/60">$45.00</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="mt-6 flex justify-center">
                <button class="btn-glass px-6 py-2 text-sm flex items-center gap-2">Ver 150+ productos <i data-lucide="arrow-right" class="w-4 h-4"></i></button>
            </div>
        </div>
    </main>

    <script>
        lucide.createIcons();
    </script>
</body>
</html>"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == '__main__':
    build_perfect_apple()
