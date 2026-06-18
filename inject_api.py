import re

app_js_path = '/Users/nachofrag/Downloads/trenbase_repo/app.js'
with open(app_js_path, 'r', encoding='utf-8') as f:
    app_js = f.read()

# 1. Replace the mock products initialization with a real fetch call
# Look for: if (!window.MOCK_DATA || !window.MOCK_DATA.products) ...
fetch_logic = """
  window.productsData = [];
  
  async function loadRealProducts() {
    try {
      const res = await fetch('/api/products');
      if (!res.ok) throw new Error('Failed to load products');
      window.productsData = await res.json();
      
      // Transform keys to match what the UI expects if necessary
      // Supabase format usually matches, but let's be sure.
      
      initDashboard();
    } catch (e) {
      console.error(e);
      // Fallback to MOCK_DATA if API fails in dev mode
      if (window.MOCK_DATA && window.MOCK_DATA.products) {
          window.productsData = window.MOCK_DATA.products;
          initDashboard();
      }
    }
  }
  
  loadRealProducts();
"""

app_js = re.sub(
    r'(if \(!window\.MOCK_DATA.*?const products = window\.MOCK_DATA\.products;)',
    fetch_logic,
    app_js,
    flags=re.DOTALL
)

# Also we need to replace all instances of `products` with `window.productsData` inside initDashboard and other functions where `products` is referenced globally.
app_js = app_js.replace('const total = products.length;', 'const products = window.productsData;\n    const total = products.length;')

# Wait, `products` is used in renderTable, openProduct, etc. We can just add `const products = window.productsData;` at the beginning of each function.
functions_to_patch = [
    'function renderTable() {',
    'window.openProduct = function(idx) {',
    'function calculateChange() {',
    'function updatePagination() {',
    'function applyFilters() {'
]

for func in functions_to_patch:
    app_js = app_js.replace(func, func + '\n    const products = window.productsData;')

# 2. Add Marketing IA Logic
# We need to add generateMarketingCopy
marketing_logic = """
// ─── MARKETING IA INTEGRATION ───
let aiHistory = [];
const AI_SYS = "Sos un copywriter experto de comercio electrónico.";

window.generateMarketingCopy = async function() {
    const p = window.productsData[currentProdIndex];
    if (!p) return;
    
    // UI Loading state
    document.getElementById('mkt-generate-wrap').classList.add('hidden');
    document.getElementById('mkt-loading').classList.remove('hidden');
    document.getElementById('mkt-error').classList.add('hidden');
    document.getElementById('mkt-content').classList.add('hidden');
    
    const productName = p.name || 'Producto';
    
    try {
        const res = await fetch('/api/describe', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ product: productName, features: p.features || 'Producto ganador' })
        });
        
        if (!res.ok) throw new Error('Error al conectar con Claude Haiku');
        const data = await res.json();
        
        // Populate the UI
        document.getElementById('mkt-ml-titulo').textContent = data.ml_title || productName;
        document.getElementById('mkt-ml-desc').textContent = data.ml_desc || 'Descripción generada por IA';
        document.getElementById('mkt-tiktok').textContent = data.tiktok_script || 'Guion de TikTok...';
        document.getElementById('mkt-instagram').textContent = data.ig_caption || 'Caption IG...';
        
        if(document.getElementById('mkt-precio')) document.getElementById('mkt-precio').textContent = '$' + (p.price_min || p.price);
        
        const kwContainer = document.getElementById('mkt-keywords');
        if(kwContainer) {
            kwContainer.innerHTML = '';
            const keywords = data.keywords || ['viral', 'tendencia'];
            keywords.forEach(kw => {
                const badge = document.createElement('span');
                badge.className = 'px-2 py-1 bg-white/5 border border-white/10 rounded text-[10px] text-white/50';
                badge.textContent = kw;
                kwContainer.appendChild(badge);
            });
        }
        
        // Hide loading, show content
        document.getElementById('mkt-loading').classList.add('hidden');
        document.getElementById('mkt-content').classList.remove('hidden');
        
    } catch(e) {
        document.getElementById('mkt-loading').classList.add('hidden');
        document.getElementById('mkt-error').classList.remove('hidden');
        document.getElementById('mkt-error-msg').textContent = e.message;
        document.getElementById('mkt-generate-wrap').classList.remove('hidden');
    }
}
"""
app_js = app_js + '\n' + marketing_logic

with open(app_js_path, 'w', encoding='utf-8') as f:
    f.write(app_js)

print("Injected API logic into app.js")
