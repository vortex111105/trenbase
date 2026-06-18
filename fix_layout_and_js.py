import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. FIX SEC-NEGOCIO OVERLAP
# The issue:
#           <div class="absolute -bottom-2 bg-black text-white text-[10px] font-bold px-2 py-0.5 rounded-full">NIVEL 1</div>
#         </div>
#       <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover flex flex-col justify-center items-center text-center">
#         <div class="w-16 h-16 bg-green-50 rounded-full flex items-center justify-center mb-4 border border-green-100">

negocio_broken_pattern = r'(<div class="absolute -bottom-2 bg-black text-white text-\[10px\] font-bold px-2 py-0\.5 rounded-full">NIVEL 1</div>\s*</div>)'
negocio_fix = r'\1\n        </div>\n      </div>'
html = re.sub(negocio_broken_pattern, negocio_fix, html)

# 2. FIX SEC-ANALISIS OVERLAP AND RESTORE AI ASSISTANT FULLY
# Remove from <!-- Asistente de IA --> to the end of sec-analisis
analisis_end_pattern = r'(<!-- Asistente de IA -->.*?</section>)'

fixed_bottom_analisis = """<!-- Oportunidades y Tendencias por región -->
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
            <div class="absolute inset-0 rounded-full border-[12px] border-black" style="clip-path: polygon(50% 50%, 100% 0, 100% 100%, 0 100%, 0 0, 50% 0);"></div>
            <div class="absolute inset-0 rounded-full border-[12px] border-gray-300" style="clip-path: polygon(50% 50%, 50% 0, 100% 0);"></div>
          </div>
          <div class="flex gap-3 text-[9px] font-bold text-gray-500 uppercase mt-4 tracking-wider">
            <div class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-black"></span> 75% Tech</div>
            <div class="flex items-center gap-1"><span class="w-2 h-2 rounded-full bg-gray-300"></span> 25% Otros</div>
          </div>
        </div>
      </div>

      <!-- Asistente de IA -->
      <div class="bg-white rounded-[2rem] saas-shadow overflow-hidden flex flex-col mt-6 border border-gray-100">
        <div class="px-6 py-4 border-b border-gray-100 bg-gray-50 flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-green-500 animate-pulse"></span>
            <span class="text-sm font-extrabold text-gray-900">Asistente IA TrendBase</span>
          </div>
          <span class="text-[9px] font-mono text-gray-400 uppercase font-bold tracking-widest bg-gray-200 px-2 py-1 rounded-md">Anthropic Claude Engine</span>
        </div>
        
        <div id="aiMessages" class="p-6 h-64 overflow-y-auto space-y-4 flex flex-col text-sm bg-white">
          <div class="bg-gray-100 text-gray-800 p-4 rounded-2xl rounded-tl-sm max-w-[85%] self-start saas-shadow-sm">
            <p class="font-medium text-xs leading-relaxed">¡Hola! Soy tu asistente de tendencias de TrendBase. ¿Sobre qué producto te gustaría que analicemos su estrategia, estimación de márgenes o canales de reventa en LATAM?</p>
          </div>
        </div>

        <div class="px-6 py-4 border-t border-gray-100 flex gap-3 items-center bg-gray-50">
          <input type="text" id="aiInput" placeholder="Pregúntame sobre estrategias de venta..." class="flex-1 bg-white border border-gray-200 rounded-xl px-4 py-3 text-sm text-gray-900 placeholder-gray-400 outline-none focus:border-gray-400 transition saas-shadow-sm" onkeydown="if(event.key==='Enter')askAI()">
          <button id="aiSend" onclick="askAI()" class="bg-black text-white px-6 py-3 rounded-xl text-xs font-extrabold uppercase tracking-wider saas-shadow hover:-translate-y-0.5 transition flex items-center gap-2">Enviar <i data-lucide="send" class="w-4 h-4"></i></button>
        </div>
      </div>
    </section>"""

html = re.sub(analisis_end_pattern, fixed_bottom_analisis, html, flags=re.DOTALL)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)


# 3. ADD MISSING JS FUNCTIONS to app.js
js_functions = """

// --- ROI CALCULATOR LOGIC ---
function calcROISliders() {
  const cost = parseFloat(document.getElementById('calcCost').value) || 0;
  const ads = parseFloat(document.getElementById('calcAds').value) || 0;
  const price = parseFloat(document.getElementById('calcPrice').value) || 0;
  
  document.getElementById('calcCostVal').textContent = '$' + cost.toFixed(2);
  document.getElementById('calcAdsVal').textContent = '$' + ads.toFixed(2);
  document.getElementById('calcPriceVal').textContent = '$' + price.toFixed(2);
  
  const profit = price - (cost + ads);
  const margin = price > 0 ? (profit / price) * 100 : 0;
  
  let resultHTML = '';
  if (profit > 0) {
    resultHTML = `
      <div class="col-span-1">
        <div class="text-[10px] text-gray-500 font-bold uppercase">Ganancia Neta</div>
        <div class="text-xl font-black text-green-500">+$${profit.toFixed(2)}</div>
      </div>
      <div class="col-span-1 text-right">
        <div class="text-[10px] text-gray-500 font-bold uppercase">Margen</div>
        <div class="text-xl font-black text-green-500">${margin.toFixed(0)}%</div>
      </div>
    `;
  } else {
    resultHTML = `
      <div class="col-span-2">
        <div class="text-[10px] text-gray-500 font-bold uppercase text-center">Pérdida Estimada</div>
        <div class="text-xl font-black text-red-500 text-center">-$${Math.abs(profit).toFixed(2)}</div>
      </div>
    `;
  }
  document.getElementById('calcResult').innerHTML = resultHTML;
}

// Initial calc
setTimeout(() => {
    if(document.getElementById('calcCost')) calcROISliders();
}, 500);

// --- AI ASSISTANT LOGIC ---
function askAI() {
  const input = document.getElementById('aiInput');
  const msgs = document.getElementById('aiMessages');
  if(!input || !msgs || input.value.trim() === '') return;
  
  const text = input.value.trim();
  
  // User message
  msgs.innerHTML += `
    <div class="bg-black text-white p-4 rounded-2xl rounded-tr-sm max-w-[85%] self-end saas-shadow-sm mt-4">
      <p class="font-medium text-xs leading-relaxed">${text}</p>
    </div>
  `;
  
  input.value = '';
  msgs.scrollTop = msgs.scrollHeight;
  
  // Fake typing
  const typingId = 'typing-' + Date.now();
  msgs.innerHTML += `
    <div id="${typingId}" class="bg-gray-100 text-gray-500 p-4 rounded-2xl rounded-tl-sm max-w-[85%] self-start saas-shadow-sm mt-4 flex items-center gap-2">
      <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"></span>
      <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></span>
      <span class="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></span>
    </div>
  `;
  msgs.scrollTop = msgs.scrollHeight;
  
  setTimeout(() => {
    document.getElementById(typingId).remove();
    msgs.innerHTML += `
      <div class="bg-gray-100 text-gray-800 p-4 rounded-2xl rounded-tl-sm max-w-[85%] self-start saas-shadow-sm mt-4">
        <p class="font-medium text-xs leading-relaxed">Según mis datos, ese producto tiene una alta estacionalidad. Te recomendaría preparar creativos enfocados en el ángulo de "regalo ideal" y apuntar a audiencias de 25-34 años en TikTok Ads. El CPA estimado rondará los $4.50.</p>
      </div>
    `;
    msgs.scrollTop = msgs.scrollHeight;
  }, 2000);
}

// --- ALERTS LOGIC ---
function markAllRead() {
  const sec = document.getElementById('sec-alertas');
  if(!sec) return;
  const badges = sec.querySelectorAll('.bg-red-500, .bg-orange-500, .bg-blue-500, .animate-pulse');
  badges.forEach(b => {
    b.classList.remove('bg-red-500', 'bg-orange-500', 'bg-blue-500', 'animate-pulse');
    b.classList.add('bg-gray-300');
  });
  const textAlerts = sec.querySelectorAll('.text-red-500, .text-orange-500, .text-blue-500');
  textAlerts.forEach(t => {
    t.classList.remove('text-red-500', 'text-orange-500', 'text-blue-500');
    t.classList.add('text-gray-400');
  });
  alert('Todas las alertas marcadas como leídas.');
}

// --- NEGOCIO MODAL ---
function showAddProductModal() {
  alert('Aquí se abriría el modal para registrar una nueva venta o cargar producto. (Funcionalidad Simulada)');
}
"""

with open('app.js', 'a', encoding='utf-8') as f:
    f.write(js_functions)
