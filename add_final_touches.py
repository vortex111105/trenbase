import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. ADD BACKGROUND BUBBLES
bubbles_css = """
  <style>
    /* 3D Realistic Animated Bubbles / Globos */
    .bg-bubble {
      position: fixed;
      border-radius: 50%;
      filter: blur(8px);
      z-index: -1;
      opacity: 0.6;
      animation: floatBubble 20s infinite ease-in-out alternate;
      /* 3D Glassy Effect */
      box-shadow: 
        inset -20px -20px 40px rgba(0,0,0,0.05),
        inset 20px 20px 40px rgba(255,255,255,0.8),
        20px 40px 60px rgba(0,0,0,0.05);
    }
    
    .bg-bubble-1 {
      width: 40vw; height: 40vw;
      top: -10%; left: -10%;
      background: radial-gradient(circle at 30% 30%, #ffffff, #e0e7ff 60%, #c7d2fe);
      animation-delay: 0s;
    }
    
    .bg-bubble-2 {
      width: 30vw; height: 30vw;
      bottom: -10%; right: -5%;
      background: radial-gradient(circle at 30% 30%, #ffffff, #ffedd5 60%, #fed7aa);
      animation-delay: -5s;
      animation-duration: 25s;
    }
    
    .bg-bubble-3 {
      width: 20vw; height: 20vw;
      top: 40%; left: 60%;
      background: radial-gradient(circle at 30% 30%, #ffffff, #fce7f3 60%, #fbcfe8);
      animation-delay: -10s;
      animation-duration: 18s;
    }

    @keyframes floatBubble {
      0% { transform: translate(0, 0) scale(1) rotate(0deg); }
      33% { transform: translate(50px, -50px) scale(1.05) rotate(15deg); }
      66% { transform: translate(-30px, 30px) scale(0.95) rotate(-10deg); }
      100% { transform: translate(0, 0) scale(1) rotate(0deg); }
    }
  </style>
"""

bubbles_html = """
  <!-- Background 3D Bubbles -->
  <div class="fixed inset-0 overflow-hidden pointer-events-none z-[-1]">
    <div class="bg-bubble bg-bubble-1"></div>
    <div class="bg-bubble bg-bubble-2"></div>
    <div class="bg-bubble bg-bubble-3"></div>
  </div>
"""

if 'bg-bubble' not in html:
    html = html.replace('</head>', bubbles_css + '\n</head>')
    html = html.replace('<body class="bg-gray-50 text-gray-900 font-sans antialiased overflow-x-hidden">', '<body class="bg-gray-50 text-gray-900 font-sans antialiased overflow-x-hidden">\n' + bubbles_html)
    html = html.replace('<body class="bg-[#F4F5F7] text-gray-900 font-sans antialiased overflow-x-hidden">', '<body class="bg-[#F4F5F7] text-gray-900 font-sans antialiased overflow-x-hidden">\n' + bubbles_html)


# 2. ADD MISSING ANALYSIS GRID
# Find the end of the AI Assistant div in sec-analisis
ai_pattern = r'(<!-- Asistente de IA -->.*?</div>\s*</div>)'

missing_grid = """
      <!-- Oportunidades y Tendencias por región -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-6">
        <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover space-y-4 border border-gray-100 flex flex-col">
          <h3 class="text-xs font-mono text-gray-400 uppercase tracking-widest border-b border-gray-100 pb-2 font-bold">Oportunidades</h3>
          <div class="divide-y divide-gray-100 flex-1">
            <div class="py-3 flex justify-between items-center">
              <div>
                <div class="text-xs font-bold text-gray-900">Proyector Galaxia</div>
                <div class="text-[9px] text-green-500 font-bold uppercase mt-0.5">Alto Margen</div>
              </div>
              <i data-lucide="arrow-up-right" class="w-4 h-4 text-gray-400"></i>
            </div>
            <div class="py-3 flex justify-between items-center">
              <div>
                <div class="text-xs font-bold text-gray-900">Cepillo Secador</div>
                <div class="text-[9px] text-orange-500 font-bold uppercase mt-0.5">Alta Demanda</div>
              </div>
              <i data-lucide="arrow-up-right" class="w-4 h-4 text-gray-400"></i>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover space-y-4 border border-gray-100 flex flex-col">
          <h3 class="text-xs font-mono text-gray-400 uppercase tracking-widest border-b border-gray-100 pb-2 font-bold">Por País</h3>
          <div class="flex flex-col gap-3 flex-1">
            <div class="flex items-center gap-3">
              <span class="text-xl">🇦🇷</span>
              <div class="flex-1">
                <div class="flex justify-between text-[10px] font-bold text-gray-600 mb-1"><span>Argentina</span><span>45%</span></div>
                <div class="w-full bg-gray-100 rounded-full h-1.5"><div class="bg-black h-1.5 rounded-full" style="width: 45%"></div></div>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <span class="text-xl">🇨🇱</span>
              <div class="flex-1">
                <div class="flex justify-between text-[10px] font-bold text-gray-600 mb-1"><span>Chile</span><span>30%</span></div>
                <div class="w-full bg-gray-100 rounded-full h-1.5"><div class="bg-black h-1.5 rounded-full" style="width: 30%"></div></div>
              </div>
            </div>
            <div class="flex items-center gap-3">
              <span class="text-xl">🇺🇾</span>
              <div class="flex-1">
                <div class="flex justify-between text-[10px] font-bold text-gray-600 mb-1"><span>Uruguay</span><span>25%</span></div>
                <div class="w-full bg-gray-100 rounded-full h-1.5"><div class="bg-black h-1.5 rounded-full" style="width: 25%"></div></div>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover space-y-4 border border-gray-100 flex flex-col">
          <h3 class="text-xs font-mono text-gray-400 uppercase tracking-widest border-b border-gray-100 pb-2 font-bold">Top Márgenes</h3>
          <div class="divide-y divide-gray-100 flex-1 flex flex-col justify-center">
            <div class="py-2.5 flex justify-between items-center">
              <span class="text-xs font-bold text-gray-800">1. Belleza</span>
              <span class="text-xs font-black text-green-500">65%</span>
            </div>
            <div class="py-2.5 flex justify-between items-center">
              <span class="text-xs font-bold text-gray-800">2. Hogar</span>
              <span class="text-xs font-black text-green-500">52%</span>
            </div>
            <div class="py-2.5 flex justify-between items-center">
              <span class="text-xs font-bold text-gray-800">3. Tech</span>
              <span class="text-xs font-black text-green-500">48%</span>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover space-y-4 border border-gray-100 flex flex-col items-center justify-center text-center">
          <h3 class="text-xs font-mono text-gray-400 uppercase tracking-widest border-b border-gray-100 pb-2 font-bold w-full text-left">Distribución</h3>
          <div class="relative w-24 h-24 mt-2">
            <!-- Simulated CSS Pie Chart for Categories -->
            <div class="absolute inset-0 rounded-full border-[12px] border-black" style="clip-path: polygon(50% 50%, 100% 0, 100% 100%, 0 100%, 0 0, 50% 0);"></div>
            <div class="absolute inset-0 rounded-full border-[12px] border-gray-300" style="clip-path: polygon(50% 50%, 50% 0, 100% 0);"></div>
          </div>
          <div class="flex gap-3 text-[9px] font-bold text-gray-500 uppercase mt-4 tracking-wider">
            <div class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-black"></span> 75% Tech</div>
            <div class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-gray-300"></span> 25% Otros</div>
          </div>
        </div>
      </div>
"""

if 'Oportunidades y Tendencias por región' not in html:
    html = re.sub(ai_pattern, r'\1\n' + missing_grid, html, flags=re.DOTALL)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
