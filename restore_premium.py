import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Body background
html = html.replace('bg-bgmain', 'bg-white')
html = html.replace('from-bgmain', 'from-[#0A0A0C]') # Integrations gradient will be black

# 2. Integrations to Black
integrations_start = html.find('<!-- Trust Element: Integration Banner -->')
integrations_end = html.find('<!-- Stats Bar -->')
old_integrations = html[integrations_start:integrations_end]
new_integrations = old_integrations.replace('class="py-12 overflow-hidden relative z-20"', 'class="py-12 bg-[#0A0A0C] overflow-hidden relative z-20"')
html = html.replace(old_integrations, new_integrations)

# 3. Stats to Black
stats_start = html.find('<!-- Stats Bar -->')
stats_end = html.find('<!-- Features Section -->')
old_stats = html[stats_start:stats_end]
new_stats = old_stats.replace('class="py-16 relative z-20"', 'class="py-16 bg-[#0A0A0C] relative z-20"')
new_stats = new_stats.replace('bg-white', 'bg-[#141416] border border-white/5')
new_stats = new_stats.replace('text-gray-900', 'text-white')
html = html.replace(old_stats, new_stats)

# 4. Features Section (Restore interactive UI)
features_start = html.find('<!-- Features Section -->')
features_end = html.find('<!-- Protocol Section -->')

features_content = """<!-- Features Section -->
  <section id="features" class="py-32 bg-white relative z-20">
    <div class="max-w-7xl mx-auto px-6 md:px-12">
      <div class="mb-20 text-center">
        <span class="text-[10px] font-bold text-gray-500 uppercase tracking-widest block mb-4">Métrica y Precisión</span>
        <h2 class="text-4xl md:text-6xl font-black text-gray-900 tracking-tight">Todo para vender en tendencia</h2>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        <!-- Card 1 — "Diagnostic Shuffler" -->
        <div class="bg-gray-50 rounded-[2.5rem] p-8 flex flex-col justify-between h-[500px] border border-gray-200 shadow-xl overflow-hidden relative group">
          <div>
            <div class="w-14 h-14 rounded-2xl bg-black flex items-center justify-center text-white mb-6 shadow-lg">
              <i data-lucide="flame"></i>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-2">Monitoreo en tiempo real</h3>
            <p class="text-gray-500 text-sm font-medium leading-relaxed">
              Rastreo continuo de 47k+ productos en 9 plataformas líderes como TikTok, Amazon y Mercado Libre.
            </p>
          </div>
          <!-- Shuffler Live UI Interface -->
          <div class="relative w-full h-[240px] mt-6 flex items-center justify-center">
            <div class="absolute w-[90%] bg-black border border-gray-800 rounded-2xl p-4 shadow-2xl transition-all duration-500 z-30 transform translate-y-0 scale-100">
              <div class="flex items-center justify-between mb-2">
                <span class="text-[10px] font-mono text-white font-bold uppercase bg-white/10 px-2 py-0.5 rounded">TikTok Viral</span>
                <span class="text-xs font-mono text-green-400 font-bold">+240%</span>
              </div>
              <p class="font-bold text-sm text-white mb-2">Humidificador de Llama</p>
              <div class="flex justify-between items-center text-[10px] font-mono text-gray-400">
                <span>Score: <b class="text-white">98/100</b></span>
                <span>Plat: <b class="text-white">TikTok</b></span>
              </div>
            </div>
            <div class="absolute w-[90%] bg-gray-900 border border-gray-800 rounded-2xl p-4 shadow-xl transition-all duration-500 z-20 transform translate-y-4 scale-95 opacity-80">
              <div class="flex items-center justify-between mb-2">
                <span class="text-[10px] font-mono text-white font-bold uppercase bg-blue-500/20 px-2 py-0.5 rounded">Mercado Libre</span>
                <span class="text-xs font-mono text-green-400 font-bold">+180%</span>
              </div>
              <p class="font-bold text-sm text-white mb-2">Trípode Auto-Rastreo</p>
              <div class="flex justify-between items-center text-[10px] font-mono text-gray-400">
                <span>Score: <b class="text-white">95/100</b></span>
                <span>Plat: <b class="text-white">Meli</b></span>
              </div>
            </div>
          </div>
        </div>

        <!-- Card 2 — "Telemetry Typewriter" -->
        <div class="bg-gray-50 rounded-[2.5rem] p-8 flex flex-col justify-between h-[500px] border border-gray-200 shadow-xl overflow-hidden relative group">
          <div>
            <div class="w-14 h-14 rounded-2xl bg-black flex items-center justify-center text-white mb-6 shadow-lg">
              <i data-lucide="globe"></i>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-2">Precios localizados</h3>
            <p class="text-gray-500 text-sm font-medium leading-relaxed">
              Datos específicos para latam en ARS, UYU y CLP con historial de tendencia de 90 días para mitigar riesgos.
            </p>
          </div>
          <!-- Typewriter Telemetry Interface -->
          <div class="w-full bg-[#0A0A0C] border border-gray-800 rounded-2xl p-6 h-[220px] flex flex-col justify-between font-mono text-[11px] text-gray-300 shadow-inner">
            <div class="flex items-center justify-between border-b border-gray-800 pb-2 mb-3">
              <div class="flex items-center gap-2">
                <span class="w-2.5 h-2.5 rounded-full bg-green-500 animate-ping"></span>
                <span class="text-[10px] uppercase font-bold text-white">Telemetry Feed</span>
              </div>
              <span class="text-[9px] text-gray-600">v2.1_STABLE</span>
            </div>
            <div class="flex-1 overflow-y-auto leading-relaxed text-green-400 font-bold text-xs font-mono">
              > CONECTANDO A DB_LATAM...<br>
              > EXTRACCION DE PRECIOS OK.<br>
              > CALCULO DE TENDENCIA: +45%<br>
              _
            </div>
            <div class="text-[9px] text-gray-600 border-t border-gray-800 pt-2 mt-2 flex justify-between">
              <span>DB: CONNECTED</span>
              <span>PING: 24ms</span>
            </div>
          </div>
        </div>

        <!-- Card 3 — "Cursor Protocol Scheduler" -->
        <div class="bg-gray-50 rounded-[2.5rem] p-8 flex flex-col justify-between h-[500px] border border-gray-200 shadow-xl overflow-hidden relative group">
          <div>
            <div class="w-14 h-14 rounded-2xl bg-black flex items-center justify-center text-white mb-6 shadow-lg">
              <i data-lucide="calculator"></i>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 mb-2">Rentabilidad avanzada</h3>
            <p class="text-gray-500 text-sm font-medium leading-relaxed">
              Cálculo automático de margen estimado, nivel de competencia del nicho y calculadora de retorno.
            </p>
          </div>
          <!-- Interactive Scheduler Simulation Grid -->
          <div class="relative w-full bg-[#0A0A0C] border border-gray-800 rounded-2xl p-4 h-[240px] flex flex-col justify-between overflow-hidden shadow-inner">
            <div class="text-[9px] font-mono text-gray-400 uppercase mb-2 flex justify-between">
              <span>Rentabilidad</span>
              <span class="text-white font-bold">READY</span>
            </div>
            <div class="grid grid-cols-7 gap-1.5 my-auto z-10">
              <!-- Animated days -->
              <div class="border border-gray-800 bg-gray-900 rounded-lg p-1.5 text-center"><div class="text-[7px] text-gray-500 font-mono">L</div><div class="text-[10px] font-bold text-white mt-0.5">09</div></div>
              <div class="border border-white/20 bg-white/10 rounded-lg p-1.5 text-center animate-pulse"><div class="text-[7px] text-gray-400 font-mono">M</div><div class="text-[10px] font-bold text-white mt-0.5">10</div></div>
              <div class="border border-gray-800 bg-gray-900 rounded-lg p-1.5 text-center"><div class="text-[7px] text-gray-500 font-mono">M</div><div class="text-[10px] font-bold text-white mt-0.5">11</div></div>
              <div class="border border-gray-800 bg-gray-900 rounded-lg p-1.5 text-center"><div class="text-[7px] text-gray-500 font-mono">J</div><div class="text-[10px] font-bold text-white mt-0.5">12</div></div>
              <div class="border border-gray-800 bg-gray-900 rounded-lg p-1.5 text-center"><div class="text-[7px] text-gray-500 font-mono">V</div><div class="text-[10px] font-bold text-white mt-0.5">13</div></div>
            </div>
            <button class="w-full bg-white text-black font-mono text-[9px] font-bold py-2 rounded-lg transition-all z-10">
              CALCULAR RETORNO
            </button>
            <svg class="absolute w-5 h-5 pointer-events-none z-30 transform translate-x-16 translate-y-10" viewBox="0 0 24 24" fill="none">
              <path d="M4.5 3V17L9 12.5L14.5 21L17.5 19L12.5 11L18.5 10L4.5 3Z" fill="#FFF" stroke="#000" stroke-width="1.5"/>
            </svg>
          </div>
        </div>

      </div>
    </div>
  </section>
"""
html = html[:features_start] + features_content + html[features_end:]

# 5. Protocol Section (Black BG + Animated SVGs)
protocol_start = html.find('<!-- Protocol Section -->')
protocol_end = html.find('<!-- Leaderboard Section -->')

protocol_content = """<!-- Protocol Section -->
  <section id="protocol" class="py-32 bg-[#0A0A0C] relative z-20">
    <div class="max-w-7xl mx-auto px-6 md:px-12">
      <div class="mb-24 text-center">
        <span class="text-[10px] font-mono text-gray-500 font-bold uppercase tracking-widest block mb-4">Cómo Funciona</span>
        <h2 class="text-4xl md:text-6xl font-black text-white tracking-tight">El Protocolo TrendBase</h2>
      </div>

      <div class="space-y-32">
        <!-- Step 1 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <div class="space-y-6">
            <span class="font-mono text-xs text-gray-500 font-bold border border-gray-800 px-3 py-1 rounded-full">PASO 01 //</span>
            <h3 class="text-3xl md:text-5xl font-extrabold text-white tracking-tight">Extracción Multiplataforma</h3>
            <p class="text-gray-400 text-lg leading-relaxed font-medium">
              Nuestros motores analizan millones de señales en TikTok, Amazon, Instagram y Mercado Libre cada hora. Almacenamos métricas crudas listas para su evaluación estadística.
            </p>
          </div>
          <div class="h-[300px] flex items-center justify-center relative overflow-hidden bg-[#111113] rounded-[2.5rem] border border-white/5 shadow-2xl">
            <svg class="w-48 h-48 animate-[spin_20s_linear_infinite]" viewBox="0 0 100 100">
              <circle cx="50" cy="50" r="45" fill="none" stroke="#FFFFFF" stroke-width="0.5" stroke-dasharray="2 6" opacity="0.5"/>
              <circle cx="50" cy="50" r="35" fill="none" stroke="#FFFFFF" stroke-width="0.5" stroke-dasharray="10 5" opacity="0.3"/>
              <circle cx="50" cy="50" r="25" fill="none" stroke="#FFFFFF" stroke-width="1"/>
              <line x1="50" y1="0" x2="50" y2="100" stroke="#FFFFFF" stroke-width="0.2" opacity="0.2"/>
              <line x1="0" y1="50" x2="100" y2="50" stroke="#FFFFFF" stroke-width="0.2" opacity="0.2"/>
            </svg>
          </div>
        </div>

        <!-- Step 2 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <div class="order-2 lg:order-1 h-[300px] flex items-center justify-center relative overflow-hidden bg-[#111113] rounded-[2.5rem] border border-white/5 shadow-2xl">
            <div class="relative w-64 h-48 border border-white/10 rounded-xl overflow-hidden flex flex-col justify-between p-4">
              <div class="grid grid-cols-4 gap-4 h-full">
                <div class="bg-white/10 rounded"></div><div class="bg-white/20 rounded"></div><div class="bg-white/5 rounded"></div><div class="bg-white/10 rounded"></div>
                <div class="bg-white/5 rounded"></div><div class="bg-white/30 rounded"></div><div class="bg-white/10 rounded"></div><div class="bg-white/5 rounded"></div>
              </div>
              <div class="absolute left-0 w-full h-[2px] bg-white shadow-[0_0_15px_#FFF] animate-[scan_3s_ease-in-out_infinite]"></div>
            </div>
            <style>@keyframes scan { 0%, 100% { top: 0%; } 50% { top: 100%; } }</style>
          </div>
          <div class="space-y-6 order-1 lg:order-2">
            <span class="font-mono text-xs text-gray-500 font-bold border border-gray-800 px-3 py-1 rounded-full">PASO 02 //</span>
            <h3 class="text-3xl md:text-5xl font-extrabold text-white tracking-tight">Algoritmo de Tendencia</h3>
            <p class="text-gray-400 text-lg leading-relaxed font-medium">
              Combinamos datos de búsqueda, interacción y competencia publicitaria para generar un score que define el potencial viral del producto.
            </p>
          </div>
        </div>

        <!-- Step 3 -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <div class="space-y-6">
            <span class="font-mono text-xs text-gray-500 font-bold border border-gray-800 px-3 py-1 rounded-full">PASO 03 //</span>
            <h3 class="text-3xl md:text-5xl font-extrabold text-white tracking-tight">Validación y Localización</h3>
            <p class="text-gray-400 text-lg leading-relaxed font-medium">
              Convertimos las métricas a tu moneda local y te brindamos enlaces directos de proveedores validados.
            </p>
          </div>
          <div class="h-[300px] flex items-center justify-center relative overflow-hidden bg-[#111113] rounded-[2.5rem] border border-white/5 shadow-2xl">
            <svg class="w-64 h-32" viewBox="0 0 100 50">
              <path d="M 0 25 L 10 25 L 20 25 L 25 10 L 30 40 L 35 25 L 50 25 L 60 5 L 65 45 L 70 25 L 85 25 L 90 25 L 100 25" fill="none" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="stroke-dasharray: 200; stroke-dashoffset: 200; animation: dash 4s linear infinite;"/>
            </svg>
            <style>@keyframes dash { to { stroke-dashoffset: 0; } }</style>
          </div>
        </div>
      </div>
    </div>
  </section>
"""
html = html[:protocol_start] + protocol_content + html[protocol_end:]

# 6. Manifesto Section -> Black
manifesto_start = html.find('<!-- Manifesto Section')
manifesto_end = html.find('<!-- Pricing Section')
old_manifesto = html[manifesto_start:manifesto_end]
new_manifesto = old_manifesto.replace('class="py-32 relative z-20"', 'class="py-32 bg-[#0A0A0C] relative z-20 border-t border-white/5"')
new_manifesto = new_manifesto.replace('text-gray-900', 'text-white')
new_manifesto = new_manifesto.replace('from-gray-900 to-gray-500', 'from-white to-gray-500')
html = html.replace(old_manifesto, new_manifesto)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
