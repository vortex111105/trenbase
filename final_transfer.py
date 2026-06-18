import re

with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add AI Assistant to Sidebar
nav_button = """          <button onclick="showSection('sec-analisis', this)" class="nav-item group flex items-center justify-center lg:justify-start w-full px-4 py-3 text-sm font-bold rounded-2xl text-gray-400 hover:text-black hover:bg-white transition-all duration-300">"""
ia_button = """          <button onclick="showSection('sec-ia', this)" class="nav-item group flex items-center justify-center lg:justify-start w-full px-4 py-3 text-sm font-bold rounded-2xl text-gray-400 hover:text-black hover:bg-white transition-all duration-300">
            <i data-lucide="bot" class="w-5 h-5 flex-shrink-0 transition-transform duration-300 group-hover:scale-110"></i>
            <span class="opacity-0 w-0 group-hover:opacity-100 group-hover:w-auto transition-all duration-300 group-hover:ml-3">Asistente IA</span>
          </button>\n""" + nav_button
html = html.replace(nav_button, ia_button)

# 2. Add Login Button in Top Header
top_right = """<div class="flex items-center gap-4">"""
auth_btn = top_right + """
          <button onclick="document.getElementById('authModal').classList.remove('hidden')" class="hidden sm:flex text-xs font-bold text-gray-500 hover:text-black transition">Iniciar Sesión</button>
"""
html = html.replace(top_right, auth_btn, 1)

# 3. Fix sec-guardados
old_guardados = """      <div class="flex justify-between items-center mb-6">
        <button onclick="markAllRead()" class="text-xs text-gray-500 font-bold uppercase tracking-wider hover:text-gray-900 transition flex items-center gap-2"><i data-lucide="check-check" class="w-4 h-4"></i> Marcar todas como leídas</button>
      </div>
      <div class="bg-white rounded-[2rem] saas-shadow overflow-hidden divide-y divide-gray-100 border border-gray-100">
        <!-- Alerta 1 -->
        <div class="p-6 flex items-start gap-4 hover:bg-gray-50 transition cursor-pointer group">
          <div class="w-10 h-10 rounded-full bg-red-50 flex items-center justify-center flex-shrink-0 group-hover:bg-red-100 transition">
            <i data-lucide="alert-triangle" class="w-5 h-5 text-red-500"></i>
          </div>
          <div class="flex-1">
            <div class="text-sm font-bold text-gray-900">Alerta de Stock Bajo: Humidificador de Llama</div>
            <p class="text-xs text-gray-500 mt-1 leading-relaxed">Quedan solo 2 unidades disponibles en CJ Dropshipping a precio promocional.</p>
            <span class="text-[9px] font-mono text-gray-400 uppercase mt-2 block font-bold tracking-wider">Hace 15 minutos</span>
          </div>
        </div>
        <!-- Alerta 2 -->
        <div class="p-6 flex items-start gap-4 hover:bg-gray-50 transition cursor-pointer group">
          <div class="w-10 h-10 rounded-full bg-orange-50 flex items-center justify-center flex-shrink-0 group-hover:bg-orange-100 transition">
            <i data-lucide="trending-up" class="w-5 h-5 text-orange-500"></i>
          </div>
          <div class="flex-1">
            <div class="text-sm font-bold text-gray-900">Pico de Tendencia: Trípode Inteligente con IA</div>
            <p class="text-xs text-gray-500 mt-1 leading-relaxed">El score del producto subió +18% en las últimas 24 horas debido a alta viralidad en TikTok Chile.</p>
            <span class="text-[9px] font-mono text-gray-400 uppercase mt-2 block font-bold tracking-wider">Hace 2 horas</span>
          </div>
        </div>
        <!-- Alerta 3 -->
        <div class="p-6 flex items-start gap-4 hover:bg-gray-50 transition cursor-pointer group">
          <div class="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center flex-shrink-0 group-hover:bg-blue-100 transition">
            <i data-lucide="rocket" class="w-5 h-5 text-blue-500"></i>
          </div>
          <div class="flex-1">
            <div class="text-sm font-bold text-gray-900">Nuevo Producto Viral Detectado</div>
            <p class="text-xs text-gray-500 mt-1 leading-relaxed">Agregado al catálogo: Depiladora Láser IPL Pro con estimación de margen superior al 55%.</p>
            <span class="text-[9px] font-mono text-gray-400 uppercase mt-2 block font-bold tracking-wider">Hace 1 día</span>
          </div>
        </div>
      </div>"""

new_guardados = """      <!-- Filtros de guardados -->
      <div class="flex gap-2 overflow-x-auto pb-4 hide-scrollbar">
        <button class="px-5 py-2.5 bg-black text-white text-xs font-bold rounded-full whitespace-nowrap saas-shadow-sm hover:-translate-y-0.5 transition">Todos</button>
        <button class="px-5 py-2.5 bg-white border border-gray-200 text-gray-600 text-xs font-bold rounded-full whitespace-nowrap hover:bg-gray-50 hover:text-black transition hover:-translate-y-0.5">Colección Q4</button>
      </div>

      <!-- Empty State / Grid -->
      <div id="savedGrid" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        <div class="col-span-full py-20 flex flex-col items-center justify-center text-center bg-white rounded-[2rem] border border-dashed border-gray-200">
          <div class="w-16 h-16 bg-gray-50 rounded-2xl flex items-center justify-center mb-4"><i data-lucide="bookmark" class="w-8 h-8 text-gray-400"></i></div>
          <h3 class="text-lg font-bold text-gray-800">No tienes productos guardados</h3>
          <p class="text-xs text-gray-500 mt-2 max-w-xs">Explora las tendencias y haz clic en el ícono de marcador para guardar productos en tu catálogo.</p>
          <button onclick="showSection('sec-tendencias', null)" class="mt-6 px-6 py-3 bg-black text-white text-xs font-bold uppercase tracking-wider rounded-full saas-shadow hover:-translate-y-0.5 transition">Explorar Tendencias</button>
        </div>
      </div>"""

html = html.replace(old_guardados, new_guardados)

# 4. Add sec-ia
sec_ia = """
    <!-- IA SECTION -->
    <section id="sec-ia" class="dash-section space-y-6">
      <div class="flex justify-between items-center mb-2">
        <div>
          <h2 class="text-2xl font-extrabold text-gray-900 tracking-tight">Asistente TrendBase</h2>
          <p class="text-xs text-gray-500 mt-1">Impulsado por IA avanzada para E-Commerce</p>
        </div>
      </div>
      
      <div class="bg-white rounded-[2rem] saas-shadow h-[600px] flex flex-col overflow-hidden border border-gray-100 relative">
        <div class="flex-1 p-6 overflow-y-auto space-y-6" id="chatArea">
          <!-- Bot Welcome -->
          <div class="flex gap-4">
            <div class="w-10 h-10 rounded-xl bg-black flex items-center justify-center flex-shrink-0 saas-shadow-sm"><i data-lucide="bot" class="w-5 h-5 text-white"></i></div>
            <div class="bg-gray-50 p-4 rounded-2xl rounded-tl-sm text-sm text-gray-800 max-w-[80%] border border-gray-100 shadow-sm leading-relaxed">
              <p class="font-bold mb-2">¡Hola! Soy tu asistente de rentabilidad.</p>
              <p>Puedo ayudarte a buscar proveedores alternativos, escribir descripciones SEO para tu tienda, o darte ideas de campañas para TikTok. ¿En qué trabajamos hoy?</p>
            </div>
          </div>
        </div>
        <div class="p-4 bg-white border-t border-gray-100">
          <div class="relative flex items-center">
            <input type="text" id="chatInput" placeholder="Escribe tu consulta o pide un copy SEO..." class="w-full bg-gray-50 border border-gray-200 rounded-full py-4 pl-6 pr-14 text-sm font-medium text-gray-800 focus:outline-none focus:ring-2 focus:ring-black/5 focus:border-gray-400 transition" onkeypress="if(event.key==='Enter') sendChat()">
            <button onclick="sendChat()" class="absolute right-2 w-10 h-10 bg-black text-white rounded-full flex items-center justify-center hover:bg-gray-800 transition transform hover:scale-105 saas-shadow-sm"><i data-lucide="send" class="w-4 h-4 ml-0.5"></i></button>
          </div>
        </div>
      </div>
    </section>
"""
html = html.replace('</main>', sec_ia + '\n  </main>')

# 5. Add Auth Modal
auth_modal = """
  <!-- Auth Modal -->
  <div id="authModal" class="hidden fixed inset-0 z-50 bg-gray-900/60 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white w-full max-w-sm rounded-[2rem] p-8 saas-shadow-lg relative overflow-hidden">
      <button onclick="document.getElementById('authModal').classList.add('hidden')" class="absolute top-4 right-4 text-gray-400 hover:text-gray-900 z-10"><i data-lucide="x" class="w-5 h-5"></i></button>
      <div class="text-center relative z-10">
        <h2 class="text-2xl font-black text-gray-900 tracking-tight">Bienvenido</h2>
        <p class="text-xs text-gray-500 mt-2">Inicia sesión en TrendBase</p>
        
        <div class="space-y-4 mt-8">
          <button onclick="alert('Google Auth simulado')" class="w-full flex items-center justify-center gap-3 py-3 px-4 border border-gray-200 rounded-xl hover:bg-gray-50 transition text-sm font-bold text-gray-700">
            <svg class="w-5 h-5" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/></svg>
            Continuar con Google
          </button>
          
          <div class="relative flex items-center justify-center my-4">
            <div class="border-t border-gray-100 w-full"></div>
            <span class="bg-white px-3 text-[10px] uppercase font-bold text-gray-300 absolute">O email</span>
          </div>
          
          <input type="email" placeholder="tu@email.com" class="w-full bg-gray-50 border border-gray-200 rounded-xl py-3 px-4 text-sm font-medium focus:outline-none focus:border-black transition">
          <input type="password" placeholder="Contraseña" class="w-full bg-gray-50 border border-gray-200 rounded-xl py-3 px-4 text-sm font-medium focus:outline-none focus:border-black transition">
          <button onclick="document.getElementById('authModal').classList.add('hidden')" class="w-full bg-black text-white font-bold text-sm py-3 rounded-xl saas-shadow hover:-translate-y-0.5 transition">Entrar</button>
        </div>
      </div>
    </div>
  </div>
"""
html = html.replace('</body>', auth_modal + '\n</body>')

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 6. Update app.js (Chat Logic & Compare Button)
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add Comparar button in product modal
old_import_btn = """              <button onclick="window.startImportWorkflow(${idx})" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-sm py-4 rounded-xl saas-shadow transition hover:-translate-y-0.5 flex items-center justify-center gap-2">
                <i data-lucide="cloud-lightning" class="w-5 h-5"></i> Importar a Tiendanube
              </button>"""

new_import_btn = """              <div class="grid grid-cols-2 gap-3">
                <button onclick="alert('Comparador de precios LATAM abierto')" class="w-full bg-white border-2 border-gray-200 hover:border-gray-900 text-gray-900 font-extrabold text-sm py-4 rounded-xl transition flex items-center justify-center gap-2">
                  <i data-lucide="git-compare" class="w-5 h-5"></i> Comparar
                </button>
                <button onclick="window.startImportWorkflow(${idx})" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-sm py-4 rounded-xl saas-shadow transition hover:-translate-y-0.5 flex items-center justify-center gap-2">
                  <i data-lucide="cloud-lightning" class="w-5 h-5"></i> Importar
                </button>
              </div>"""

js = js.replace(old_import_btn, new_import_btn)

# Add sendChat logic
chat_js = """
  // Asistente IA Chat
  window.sendChat = function() {
    const input = document.getElementById('chatInput');
    const area = document.getElementById('chatArea');
    if(!input || !area || !input.value.trim()) return;
    
    // User message
    const userMsg = input.value.trim();
    area.insertAdjacentHTML('beforeend', `
      <div class="flex gap-4 flex-row-reverse">
        <div class="w-10 h-10 rounded-xl bg-gray-200 flex items-center justify-center flex-shrink-0"><i data-lucide="user" class="w-5 h-5 text-gray-600"></i></div>
        <div class="bg-black text-white p-4 rounded-2xl rounded-tr-sm text-sm max-w-[80%] saas-shadow-sm leading-relaxed">
          <p>${userMsg}</p>
        </div>
      </div>
    `);
    
    input.value = '';
    lucide.createIcons();
    area.scrollTop = area.scrollHeight;
    
    // Bot loading
    const loadId = 'load-' + Date.now();
    area.insertAdjacentHTML('beforeend', `
      <div id="${loadId}" class="flex gap-4 opacity-50 transition-opacity">
        <div class="w-10 h-10 rounded-xl bg-black flex items-center justify-center flex-shrink-0"><i data-lucide="bot" class="w-5 h-5 text-white animate-pulse"></i></div>
        <div class="bg-gray-50 p-4 rounded-2xl rounded-tl-sm text-sm text-gray-800 border border-gray-100 flex items-center gap-2">
          <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
          <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
          <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
        </div>
      </div>
    `);
    area.scrollTop = area.scrollHeight;
    
    // Bot response simulate
    setTimeout(() => {
      document.getElementById(loadId)?.remove();
      area.insertAdjacentHTML('beforeend', `
        <div class="flex gap-4">
          <div class="w-10 h-10 rounded-xl bg-black flex items-center justify-center flex-shrink-0 saas-shadow-sm"><i data-lucide="bot" class="w-5 h-5 text-white"></i></div>
          <div class="bg-gray-50 p-4 rounded-2xl rounded-tl-sm text-sm text-gray-800 max-w-[80%] border border-gray-100 shadow-sm leading-relaxed">
            <p><strong>[Conexión a Anthropic Simulada]</strong><br>He analizado tu consulta. Para ese nicho te recomiendo centrarte en videos POV orgánicos en TikTok mostrando el uso del producto, y en cuanto a proveedores, CJ Dropshipping tiene un almacén local con envío rápido para esa categoría.</p>
          </div>
        </div>
      `);
      lucide.createIcons();
      area.scrollTop = area.scrollHeight;
    }, 1500);
  }
"""
js += '\n' + chat_js

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Final transfer complete!")
