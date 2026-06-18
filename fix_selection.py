with open('app.js', 'r', encoding='utf-8') as f:
    app = f.read()

toggle_logic = """
// --- SELECTION LOGIC ---
window.selectedProducts = new Set();

window.toggleSelection = function(idx, e) {
  e.stopPropagation();
  if(window.selectedProducts.has(idx)) {
    window.selectedProducts.delete(idx);
  } else {
    window.selectedProducts.add(idx);
  }
  updateMasterCheckbox();
};

window.toggleAllSelection = function(e) {
  e.stopPropagation();
  const checked = e.target.checked;
  // We need to get the currently filtered products
  const tbody = document.getElementById('tableBody');
  if(!tbody) return;
  
  let filtered = window.MOCK_DATA.products.filter(p => {
    if(window.filterParams.cat && p.cat !== window.filterParams.cat) return false;
    if(window.filterParams.plt && !p.plts.includes(window.filterParams.plt)) return false;
    if(window.filterParams.region && !p.regions.includes(window.filterParams.region)) return false;
    if(window.filterParams.text && !p.name.toLowerCase().includes(window.filterParams.text)) return false;
    return true;
  });

  if(checked) {
    filtered.forEach(p => window.selectedProducts.add(window.MOCK_DATA.products.indexOf(p)));
  } else {
    window.selectedProducts.clear();
  }
  window.renderTable();
};

window.updateMasterCheckbox = function() {
  const cb = document.getElementById('masterCheckbox');
  if(!cb) return;
  cb.checked = window.selectedProducts.size > 0 && window.selectedProducts.size === window.MOCK_DATA.products.length;
};
"""

with open('app.js', 'a', encoding='utf-8') as f:
    f.write('\\n' + toggle_logic)
