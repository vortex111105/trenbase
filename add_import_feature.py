import re

# 1. Update dashboard.html
with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make Tiendanube active
old_tn = """            <!-- Tiendanube -->
            <div class="border border-gray-200 rounded-2xl p-4 flex items-center justify-between hover:border-gray-400 transition cursor-pointer">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-blue-50 rounded-xl flex items-center justify-center text-blue-600 font-bold">Tn</div>
                <div>
                  <h4 class="font-bold text-sm text-gray-900">Tiendanube</h4>
                  <p class="text-[10px] text-gray-500">Próximamente</p>
                </div>
              </div>
              <button class="bg-gray-50 text-gray-400 px-3 py-1.5 rounded-lg text-xs font-bold cursor-not-allowed">Pronto</button>
            </div>"""

new_tn = """            <!-- Tiendanube -->
            <div class="border border-gray-200 rounded-2xl p-4 flex items-center justify-between hover:border-gray-400 transition cursor-pointer" onclick="alert('Conexión OAuth con Tiendanube simulada exitosamente. ¡Tu tienda ahora está vinculada!')">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 bg-blue-50 rounded-xl flex items-center justify-center text-blue-600 font-bold">Tn</div>
                <div>
                  <h4 class="font-bold text-sm text-gray-900">Tiendanube</h4>
                  <p class="text-[10px] text-gray-500">Sincronización a 1-Clic</p>
                </div>
              </div>
              <button class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1.5 rounded-lg text-xs font-bold transition saas-shadow-sm">Conectar</button>
            </div>"""

html = html.replace(old_tn, new_tn)

# Add Import Modal at the end of the body (before <script>)
import_modal = """
  <!-- Importador Mágico Modal -->
  <div id="importModal" class="hidden fixed inset-0 z-50 bg-gray-900/40 backdrop-blur-sm flex items-center justify-center p-4 opacity-0 transition-opacity duration-300">
    <div class="bg-white w-full max-w-md rounded-3xl p-8 saas-shadow-lg relative transform scale-95 transition-transform duration-300" id="importModalContent">
      <button onclick="closeImportModal()" class="absolute top-4 right-4 text-gray-400 hover:text-gray-900"><i data-lucide="x" class="w-5 h-5"></i></button>
      
      <div class="text-center mb-6">
        <div class="w-16 h-16 bg-blue-50 rounded-2xl flex items-center justify-center mx-auto mb-4 relative overflow-hidden">
           <i data-lucide="cloud-lightning" class="w-8 h-8 text-blue-600 relative z-10"></i>
        </div>
        <h2 class="text-2xl font-extrabold text-gray-900 tracking-tight">Importador Mágico</h2>
        <p class="text-xs text-gray-500 mt-1">Sincronizando producto con Tiendanube</p>
      </div>
      
      <div id="importSteps" class="space-y-4">
        <!-- Steps will be injected here by JS -->
      </div>
      
      <div id="importProgress" class="mt-6 hidden">
        <div class="w-full h-2 bg-gray-100 rounded-full overflow-hidden">
          <div id="importProgressBar" class="h-full bg-blue-600 w-0 transition-all duration-300 ease-out"></div>
        </div>
      </div>
    </div>
  </div>
"""
html = html.replace('</main>', '</main>\n' + import_modal)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)


# 2. Update app.js
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add button in openProduct modal
old_modal_footer = """            </div>
          </div>
        </div>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', modal);"""

new_modal_footer = """            </div>
            
            <div class="mt-6 pt-6 border-t border-gray-100 flex flex-col gap-3">
              <button onclick="window.startImportWorkflow(${idx})" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-extrabold text-sm py-4 rounded-xl saas-shadow transition hover:-translate-y-0.5 flex items-center justify-center gap-2">
                <i data-lucide="cloud-lightning" class="w-5 h-5"></i> Importar a Tiendanube
              </button>
              <div class="text-center text-[10px] text-gray-400 font-bold uppercase tracking-widest flex items-center justify-center gap-1">
                <i data-lucide="zap" class="w-3 h-3"></i> Proveedor: Droppi / Dropdeal
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', modal);"""

js = js.replace(old_modal_footer, new_modal_footer)

# Add Import Workflow logic at the end
import_logic = """
  // Importador Magico Logic
  window.startImportWorkflow = function(idx) {
    // Close product modal if open
    const pm = document.getElementById('productModal');
    if(pm) {
      pm.classList.add('opacity-0');
      setTimeout(() => pm.remove(), 300);
    }
    
    const product = window.PRODUCTS[idx];
    if(!product) return;
    
    const im = document.getElementById('importModal');
    const content = document.getElementById('importModalContent');
    const stepsEl = document.getElementById('importSteps');
    const progEl = document.getElementById('importProgress');
    const progBar = document.getElementById('importProgressBar');
    
    if(!im) return;
    
    // Reset state
    im.classList.remove('hidden');
    // trigger reflow
    void im.offsetWidth;
    im.classList.remove('opacity-0');
    content.classList.remove('scale-95');
    
    progEl.classList.remove('hidden');
    progBar.style.width = '0%';
    
    stepsEl.innerHTML = `
      <div id="step1" class="flex items-center gap-3 text-sm font-bold text-gray-400 transition-colors duration-300">
        <div class="w-6 h-6 rounded-full border-2 border-current flex items-center justify-center"><i data-lucide="download" class="w-3 h-3"></i></div>
        <span>Descargando imágenes HD...</span>
      </div>
      <div id="step2" class="flex items-center gap-3 text-sm font-bold text-gray-400 transition-colors duration-300">
        <div class="w-6 h-6 rounded-full border-2 border-current flex items-center justify-center"><i data-lucide="file-text" class="w-3 h-3"></i></div>
        <span>Generando descripciones SEO...</span>
      </div>
      <div id="step3" class="flex items-center gap-3 text-sm font-bold text-gray-400 transition-colors duration-300">
        <div class="w-6 h-6 rounded-full border-2 border-current flex items-center justify-center"><i data-lucide="shopping-bag" class="w-3 h-3"></i></div>
        <span>Creando producto en Tiendanube...</span>
      </div>
    `;
    lucide.createIcons();
    
    // Simulation sequence
    setTimeout(() => {
      document.getElementById('step1').classList.replace('text-gray-400', 'text-blue-600');
      progBar.style.width = '33%';
    }, 500);
    
    setTimeout(() => {
      document.getElementById('step1').classList.replace('text-blue-600', 'text-green-500');
      document.getElementById('step2').classList.replace('text-gray-400', 'text-blue-600');
      progBar.style.width = '66%';
    }, 1500);
    
    setTimeout(() => {
      document.getElementById('step2').classList.replace('text-blue-600', 'text-green-500');
      document.getElementById('step3').classList.replace('text-gray-400', 'text-blue-600');
      progBar.style.width = '95%';
    }, 3000);
    
    setTimeout(() => {
      document.getElementById('step3').classList.replace('text-blue-600', 'text-green-500');
      progBar.style.width = '100%';
      progEl.classList.add('hidden');
      
      stepsEl.innerHTML = `
        <div class="bg-green-50 text-green-700 p-4 rounded-xl border border-green-100 flex items-start gap-3">
          <i data-lucide="check-circle" class="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5"></i>
          <div>
            <div class="font-bold text-sm">¡Importación Exitosa!</div>
            <div class="text-xs mt-1">"${product.name}" ya está publicado y listo para vender en tu Tiendanube. Las órdenes se sincronizarán con Droppi.</div>
          </div>
        </div>
      `;
      lucide.createIcons();
    }, 4000);
  }
  
  window.closeImportModal = function() {
    const im = document.getElementById('importModal');
    if(im) {
      im.classList.add('opacity-0');
      document.getElementById('importModalContent').classList.add('scale-95');
      setTimeout(() => im.classList.add('hidden'), 300);
    }
  }
"""
js += '\n' + import_logic

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Added import functionality!")
