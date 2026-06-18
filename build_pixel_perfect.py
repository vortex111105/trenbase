def build_pixel_perfect():
    html_content = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrendBase - Dashboard Apple</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    
    <style>
        body {
            font-family: 'Inter', -apple-system, sans-serif;
            color: #1A1A1A;
            background-color: #FDFBF8;
            /* To make it stretch to the top/bottom */
            height: 100vh; 
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        
        /* The exact warm office background from the sketch */
        body::before {
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background-image: url('https://images.unsplash.com/photo-1497366216548-37526070297c?q=80&w=2000&auto=format&fit=crop');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            z-index: -2;
        }
        
        /* Gentle soft white overlay to make text readable but keep the office vibe */
        body::after {
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: rgba(255, 255, 255, 0.75); 
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            z-index: -1;
        }

        /* Glassmorphism bubbles exactly like Apple Widgets */
        .apple-widget {
            background: rgba(255, 255, 255, 0.65);
            backdrop-filter: blur(40px) saturate(200%);
            -webkit-backdrop-filter: blur(40px) saturate(200%);
            border-radius: 36px; /* Strong Squircles */
            border: 1px solid rgba(255, 255, 255, 1);
            box-shadow: 
                0 20px 40px rgba(0, 0, 0, 0.05),
                0 10px 20px rgba(0, 0, 0, 0.03),
                inset 0 2px 4px rgba(255, 255, 255, 0.9),
                inset 0 0 0 1px rgba(255, 255, 255, 0.5);
            transition: all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1);
            overflow: hidden;
        }

        .apple-widget:hover {
            transform: translateY(-4px) scale(1.02);
            box-shadow: 
                0 30px 60px rgba(0, 0, 0, 0.08), 
                0 15px 30px rgba(0, 0, 0, 0.05),
                inset 0 2px 4px rgba(255, 255, 255, 1),
                inset 0 0 0 1px rgba(255, 255, 255, 0.6);
            background: rgba(255, 255, 255, 0.85);
        }
        
        .apple-nav {
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(40px) saturate(200%);
            -webkit-backdrop-filter: blur(40px) saturate(200%);
            border-bottom: 1px solid rgba(255, 255, 255, 0.8);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
        }

        /* Subtle Functional Colors - No aggressive glows */
        .text-green-functional { color: #34C759; font-weight: 800; }
        .text-red-functional { color: #FF3B30; font-weight: 800; }

        .widget-title {
            font-size: 0.85rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: rgba(0, 0, 0, 0.5);
        }
        
        /* Big numbers in carbon gray */
        .big-number {
            color: #1A1A1A;
            font-weight: 900;
            letter-spacing: -0.05em;
        }

        /* Minimalist Scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.1); border-radius: 10px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(0,0,0,0.2); }
    </style>
</head>
<body>

    <!-- Top Navigation -->
    <nav class="apple-nav w-full px-8 py-4 flex items-center justify-between flex-shrink-0 z-50 relative">
        <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-2xl bg-white shadow-sm border border-gray-100 flex items-center justify-center">
                <i data-lucide="zap" class="w-5 h-5 text-black"></i>
            </div>
            <span class="font-extrabold tracking-tight text-xl">TrendBase</span>
        </div>
        
        <div class="hidden md:flex items-center gap-2 p-1.5 rounded-full bg-white/40 border border-white/60 shadow-sm">
            <button class="px-6 py-2 rounded-full bg-white shadow-sm font-bold text-sm">Dashboard</button>
            <button class="px-6 py-2 rounded-full font-bold text-sm text-black/60 hover:text-black transition">Tendencias</button>
            <button class="px-6 py-2 rounded-full font-bold text-sm text-black/60 hover:text-black transition">Análisis</button>
        </div>
        
        <div class="flex items-center gap-4">
            <button class="w-10 h-10 rounded-full bg-white/80 border border-white shadow-sm flex items-center justify-center relative hover:scale-105 transition">
                <i data-lucide="bell" class="w-5 h-5 text-black"></i>
                <span class="absolute top-0 right-0 w-3 h-3 bg-[#FF3B30] border-2 border-white rounded-full"></span>
            </button>
            <div class="w-10 h-10 rounded-full bg-black flex items-center justify-center text-white font-bold border-2 border-white shadow-md cursor-pointer hover:scale-105 transition">NF</div>
        </div>
    </nav>

    <!-- Main Dashboard Workspace - Stretching fully to edges -->
    <main class="flex-1 w-full max-w-[1600px] mx-auto px-4 md:px-8 py-6 flex flex-col overflow-hidden relative z-10 gap-6">
        
        <!-- Header with Date (Requested by user) -->
        <div class="flex flex-col md:flex-row justify-between items-start md:items-end flex-shrink-0">
            <div>
                <h1 class="text-4xl md:text-5xl font-extrabold tracking-tight mb-2 text-black">Panel de Control</h1>
                <p class="text-black/60 font-semibold flex items-center gap-2">
                    <i data-lucide="calendar" class="w-4 h-4"></i> Lunes, 23 Octubre • Actualizado hace instantes
                </p>
            </div>
            <div class="flex gap-3 mt-4 md:mt-0">
                <button class="bg-white/60 hover:bg-white/90 text-black border border-white/80 shadow-sm rounded-full px-5 py-2.5 flex items-center gap-2 font-bold transition">
                    <i data-lucide="filter" class="w-4 h-4"></i> Filtros
                </button>
                <button class="bg-black text-white rounded-full px-6 py-2.5 flex items-center gap-2 font-bold shadow-lg hover:scale-105 transition">
                    <i data-lucide="plus" class="w-4 h-4"></i> Conectar Tienda
                </button>
            </div>
        </div>

        <!-- Apple Widgets Grid (Stretches to fill vertical space) -->
        <div class="grid grid-cols-1 md:grid-cols-4 lg:grid-cols-4 grid-rows-[auto_1fr] gap-6 flex-1 overflow-y-auto pb-8 pr-2">
            
            <!-- Top Row: Small Stat Widgets -->
            <div class="apple-widget p-6 flex flex-col justify-between">
                <div class="flex justify-between items-start mb-6">
                    <span class="widget-title">Facturación Total</span>
                    <div class="w-10 h-10 rounded-full bg-white flex items-center justify-center shadow-sm border border-gray-100"><i data-lucide="dollar-sign" class="w-5 h-5 text-black"></i></div>
                </div>
                <div>
                    <div class="text-4xl big-number mb-1">$124,500</div>
                    <div class="flex items-center gap-1.5 text-sm text-green-functional bg-[#34C759]/10 px-3 py-1.5 rounded-full w-max border border-[#34C759]/20">
                        <i data-lucide="trending-up" class="w-4 h-4"></i> +24.5% este mes
                    </div>
                </div>
            </div>

            <div class="apple-widget p-6 flex flex-col justify-between">
                <div class="flex justify-between items-start mb-6">
                    <span class="widget-title">CPA Promedio</span>
                    <div class="w-10 h-10 rounded-full bg-white flex items-center justify-center shadow-sm border border-gray-100"><i data-lucide="target" class="w-5 h-5 text-black"></i></div>
                </div>
                <div>
                    <div class="text-4xl big-number mb-1">$12.40</div>
                    <div class="flex items-center gap-1.5 text-sm text-red-functional bg-[#FF3B30]/10 px-3 py-1.5 rounded-full w-max border border-[#FF3B30]/20">
                        <i data-lucide="trending-up" class="w-4 h-4"></i> +5.2% subida (FB)
                    </div>
                </div>
            </div>

            <div class="apple-widget p-6 flex flex-col justify-between">
                <div class="flex justify-between items-start mb-6">
                    <span class="widget-title">ROI Global</span>
                    <div class="w-10 h-10 rounded-full bg-white flex items-center justify-center shadow-sm border border-gray-100"><i data-lucide="pie-chart" class="w-5 h-5 text-black"></i></div>
                </div>
                <div>
                    <div class="text-4xl big-number mb-1">320%</div>
                    <div class="flex items-center gap-1.5 text-sm text-green-functional bg-[#34C759]/10 px-3 py-1.5 rounded-full w-max border border-[#34C759]/20">
                        <i data-lucide="check-circle" class="w-4 h-4"></i> Margen Óptimo
                    </div>
                </div>
            </div>

            <div class="apple-widget p-6 flex flex-col justify-between">
                <div class="flex justify-between items-start mb-6">
                    <span class="widget-title">Productos Testeados</span>
                    <div class="w-10 h-10 rounded-full bg-white flex items-center justify-center shadow-sm border border-gray-100"><i data-lucide="package" class="w-5 h-5 text-black"></i></div>
                </div>
                <div>
                    <div class="text-4xl big-number mb-1">14</div>
                    <div class="flex items-center gap-1.5 text-sm font-bold text-black/60 bg-black/5 px-3 py-1.5 rounded-full w-max border border-black/5">
                        3 ganadores activos
                    </div>
                </div>
            </div>

            <!-- Bottom Row: Huge Table Widget spanning all 4 columns -->
            <div class="apple-widget col-span-1 md:col-span-4 flex flex-col min-h-[400px]">
                <div class="p-6 md:p-8 border-b border-black/5 bg-white/20 flex flex-col md:flex-row justify-between items-center gap-4">
                    <h2 class="text-2xl font-extrabold tracking-tight text-black">Monitoreo de Productos Virales</h2>
                    <div class="relative w-full md:w-auto">
                        <i data-lucide="search" class="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-black/40"></i>
                        <input type="text" placeholder="Buscar producto..." class="w-full md:w-72 bg-white/80 border border-white rounded-full pl-11 pr-6 py-3 text-sm font-bold text-black placeholder-black/40 outline-none focus:bg-white transition shadow-sm">
                    </div>
                </div>

                <div class="flex-1 overflow-auto">
                    <table class="w-full text-left border-collapse">
                        <thead class="sticky top-0 bg-white/90 backdrop-blur-md z-10 shadow-sm">
                            <tr class="text-black/50 font-extrabold uppercase text-[10px] tracking-widest border-b border-black/5">
                                <th class="p-5 w-12 text-center">#</th>
                                <th class="p-5">Producto</th>
                                <th class="p-5">TrendScore</th>
                                <th class="p-5">Margen</th>
                                <th class="p-5">Competencia</th>
                                <th class="p-5 text-right">Venta Est.</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-black/5 font-bold text-sm">
                            
                            <!-- Row 1 -->
                            <tr class="hover:bg-white/60 transition cursor-pointer group">
                                <td class="p-5 text-center text-black/30 group-hover:text-black transition">1</td>
                                <td class="p-5">
                                    <div class="flex items-center gap-4">
                                        <div class="w-12 h-12 rounded-2xl bg-white border border-gray-100 flex items-center justify-center shadow-sm">
                                            <i data-lucide="smartphone" class="w-6 h-6 text-black/60"></i>
                                        </div>
                                        <span class="text-base text-black font-extrabold">Corrector Postura Inteligente</span>
                                    </div>
                                </td>
                                <td class="p-5">
                                    <span class="bg-black text-white px-3 py-1.5 rounded-full text-xs font-black shadow-md">98/100</span>
                                </td>
                                <td class="p-5 text-base text-black font-extrabold">$22.00</td>
                                <td class="p-5">
                                    <span class="bg-[#34C759]/10 text-green-functional px-3 py-1.5 rounded-full text-xs border border-[#34C759]/20 flex items-center gap-1.5 w-max">
                                        <div class="w-1.5 h-1.5 rounded-full bg-[#34C759]"></div> Baja
                                    </span>
                                </td>
                                <td class="p-5 text-right text-black/60">$35.00</td>
                            </tr>

                            <!-- Row 2 -->
                            <tr class="hover:bg-white/60 transition cursor-pointer group">
                                <td class="p-5 text-center text-black/30 group-hover:text-black transition">2</td>
                                <td class="p-5">
                                    <div class="flex items-center gap-4">
                                        <div class="w-12 h-12 rounded-2xl bg-white border border-gray-100 flex items-center justify-center shadow-sm">
                                            <i data-lucide="sun" class="w-6 h-6 text-black/60"></i>
                                        </div>
                                        <span class="text-base text-black font-extrabold">Lámpara Cristal Touch</span>
                                    </div>
                                </td>
                                <td class="p-5">
                                    <span class="bg-black/80 text-white px-3 py-1.5 rounded-full text-xs font-black shadow-sm">92/100</span>
                                </td>
                                <td class="p-5 text-base text-black font-extrabold">$18.50</td>
                                <td class="p-5">
                                    <span class="bg-[#34C759]/10 text-green-functional px-3 py-1.5 rounded-full text-xs border border-[#34C759]/20 flex items-center gap-1.5 w-max">
                                        <div class="w-1.5 h-1.5 rounded-full bg-[#34C759]"></div> Baja
                                    </span>
                                </td>
                                <td class="p-5 text-right text-black/60">$25.00</td>
                            </tr>

                            <!-- Row 3 -->
                            <tr class="hover:bg-white/60 transition cursor-pointer group">
                                <td class="p-5 text-center text-black/30 group-hover:text-black transition">3</td>
                                <td class="p-5">
                                    <div class="flex items-center gap-4">
                                        <div class="w-12 h-12 rounded-2xl bg-white border border-gray-100 flex items-center justify-center shadow-sm">
                                            <i data-lucide="activity" class="w-6 h-6 text-black/60"></i>
                                        </div>
                                        <span class="text-base text-black font-extrabold">Depiladora Láser IPL</span>
                                    </div>
                                </td>
                                <td class="p-5">
                                    <span class="bg-black/40 text-white px-3 py-1.5 rounded-full text-xs font-black">85/100</span>
                                </td>
                                <td class="p-5 text-base text-black font-extrabold">$8.00</td>
                                <td class="p-5">
                                    <span class="bg-[#FF3B30]/10 text-red-functional px-3 py-1.5 rounded-full text-xs border border-[#FF3B30]/20 flex items-center gap-1.5 w-max">
                                        <div class="w-1.5 h-1.5 rounded-full bg-[#FF3B30]"></div> Alta Saturación
                                    </span>
                                </td>
                                <td class="p-5 text-right text-black/60">$45.00</td>
                            </tr>

                        </tbody>
                    </table>
                </div>
                
                <!-- Footer of table widget -->
                <div class="p-4 border-t border-black/5 bg-white/30 flex justify-center mt-auto">
                    <button class="bg-white hover:bg-gray-50 text-black border border-gray-200 shadow-sm rounded-full px-6 py-2 text-sm font-bold flex items-center gap-2 transition">
                        Ver 150+ productos <i data-lucide="arrow-right" class="w-4 h-4"></i>
                    </button>
                </div>
                
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
    build_pixel_perfect()
