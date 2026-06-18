import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the entire openProduct function
# from "window.openProduct = function(idx) {" to "window.closeModal = function(e) {"

open_product_pattern = re.compile(r'window\.openProduct\s*=\s*function\(idx\)\s*\{.*?window\.closeModalDirect\s*=\s*function\(\)\s*\{', re.DOTALL)

new_open_product = """window.openProduct = function(idx) {
    window.currentProductIndex = idx;
    const product = products[idx];
    if(!product) return;
    
    // Guardamos la info del producto en variable global para las pestañas
    window.currentProductData = product;
    window.currentProductIdx = idx;

    // Remover modal viejo si existe
    const existing = document.getElementById('productModal');
    if (existing) existing.remove();

    const modal = `
    <div id="productModal" class="fixed inset-0 z-50 bg-[#0D0D12]/90 backdrop-blur-md flex items-center justify-center p-4 sm:p-6 opacity-0 transition-opacity duration-300">
      <div class="bg-[#1E1E26] w-full max-w-4xl rounded-3xl saas-shadow-2xl relative flex flex-col md:flex-row overflow-hidden border border-gray-800 transform scale-95 transition-transform duration-300" id="productModalContent">
        
        <button onclick="closeModalDirect()" class="absolute top-4 right-4 bg-gray-800 text-gray-400 hover:text-white p-2 rounded-full z-10 transition"><i data-lucide="x" class="w-4 h-4"></i></button>

        <div class="w-full md:w-2/5 h-64 md:h-auto bg-gray-900 relative">
          <img src="${product.image}" class="w-full h-full object-cover opacity-80" alt="${product.name}">
          <div class="absolute inset-0 bg-gradient-to-t from-[#1E1E26] to-transparent"></div>
        </div>
        
        <div class="w-full md:w-3/5 p-8 flex flex-col h-[600px] overflow-y-auto custom-scrollbar">
          
          <h2 class="text-2xl font-extrabold text-white mb-6 leading-tight">${product.name}</h2>
          
          <div class="flex items-end gap-3 mb-8">
            <span class="text-5xl font-black text-white">${product.score}</span>
            <div class="pb-1 flex items-center gap-2">
              <span class="text-xs text-gray-400 font-bold tracking-widest uppercase">Trendscore</span>
              <span class="bg-champagne text-black text-[10px] font-black px-2 py-0.5 rounded-sm uppercase tracking-wider">HOT</span>
            </div>
          </div>

          <div class="flex gap-6 border-b border-gray-800 mb-6 relative">
            <button onclick="switchModalTab('info')" id="tab-info" class="pb-2 text-sm font-bold text-champagne border-b-2 border-champagne transition-colors">Información</button>
            <button onclick="switchModalTab('historial')" id="tab-historial" class="pb-2 text-sm font-bold text-gray-500 border-b-2 border-transparent hover:text-gray-300 transition-colors">Historial 90 días</button>
            <button onclick="switchModalTab('proveedores')" id="tab-proveedores" class="pb-2 text-sm font-bold text-gray-500 border-b-2 border-transparent hover:text-gray-300 transition-colors">Proveedores</button>
            <button onclick="switchModalTab('marketing')" id="tab-marketing" class="pb-2 text-sm font-bold text-gray-500 border-b-2 border-transparent hover:text-gray-300 flex items-center gap-1 transition-colors"><i data-lucide="sparkles" class="w-3 h-3"></i> Marketing IA</button>
          </div>

          <!-- Contenedor dinámico de pestañas -->
          <div id="modal-tab-content" class="flex-1 flex flex-col">
            ${getTabInfoHTML(product, idx)}
          </div>

        </div>
      </div>
    </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modal);
    lucide.createIcons();
    
    const m = document.getElementById('productModal');
    const content = document.getElementById('productModalContent');
    // small delay for transition
    setTimeout(() => {
      m.classList.remove('opacity-0');
      content.classList.remove('scale-95');
    }, 10);
  }
  
  window.closeModalDirect = function() {"""

js = re.sub(open_product_pattern, new_open_product, js)

# Fix closeModalDirect
close_modal_direct_pattern = re.compile(r'window\.closeModalDirect\s*=\s*function\(\)\s*\{.*?\}\s*window\.closeModal', re.DOTALL)
new_close_modal_direct = """window.closeModalDirect = function() {
    const modal = document.getElementById('productModal');
    const content = document.getElementById('productModalContent');
    if(!modal) {
        // Fallback for old modal
        const oldModal = document.getElementById('prodModal');
        if(oldModal) {
            document.getElementById('modalContent').classList.add('scale-95', 'opacity-0');
            setTimeout(() => oldModal.classList.add('hidden'), 300);
        }
        return;
    }
    content.classList.add('scale-95');
    modal.classList.add('opacity-0');
    setTimeout(() => {
      modal.remove();
    }, 300);
  }
  
  window.closeModal"""

js = re.sub(close_modal_direct_pattern, new_close_modal_direct, js)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed modal injection!")
