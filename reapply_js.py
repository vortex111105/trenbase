import re

# 1. Grab Analysis logic
with open('original_index.html', 'r', encoding='utf-8') as f:
    orig = f.read()

js_functions = [
    r'function exportDataCSV\(\) \{.*?\}',
    r'function setAnalysisPeriod.*?\}',
    r'function renderAnalysisKPIs\(\) \{.*?\}',
    r'function renderRegionHeatmap\(\) \{.*?\}',
    r'function renderTopMargin\(\) \{.*?\}',
    r'function renderAnalysisCatChart\(\) \{.*?\}',
    r'function renderAnalysisHistory\(\) \{.*?\}',
    r'function populateAnalysisSelect\(\) \{.*?\}',
    r'function playSimulatedAd\(\) \{.*?\}',
    r'function renderAnalysisChart\(labels, data, name\) \{.*?\}',
    r'function askAI\(\) \{.*?\}'
]

extracted_js = []
for pattern in js_functions:
    m = re.search(pattern, orig, flags=re.DOTALL)
    if m:
        extracted_js.append(m.group(0))

render_analysis_js = """
window.renderAnalysis = function() {
  if (typeof renderAnalysisKPIs === 'function') renderAnalysisKPIs();
  if (typeof renderRegionHeatmap === 'function') renderRegionHeatmap();
  if (typeof renderTopMargin === 'function') renderTopMargin();
  if (typeof renderAnalysisCatChart === 'function') renderAnalysisCatChart();
  if (typeof renderAnalysisHistory === 'function') renderAnalysisHistory();
  if (typeof populateAnalysisSelect === 'function') populateAnalysisSelect();
}

// Hook into showSection to call renderAnalysis
const oldShowSec = window.showSection;
window.showSection = function(id, el) {
  if(oldShowSec) oldShowSec(id, el);
  if(id === 'sec-analisis' && window.renderAnalysis) window.renderAnalysis();
}

window.exportDataCSV = exportDataCSV;
window.setAnalysisPeriod = setAnalysisPeriod;
window.playSimulatedAd = playSimulatedAd;
window.askAI = askAI;

setTimeout(() => {
  if (window.renderAnalysis) window.renderAnalysis();
}, 1500);
"""

# 2. Grab Checkbox logic
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
  window.updateMasterCheckbox();
};

window.toggleAllSelection = function(e) {
  e.stopPropagation();
  const checked = e.target.checked;
  const tbody = document.getElementById('tableBody');
  if(!tbody) return;
  
  const fParams = window.filterParams || {cat: '', plt: '', region: '', text: ''};
  
  let filtered = window.MOCK_DATA ? window.MOCK_DATA.products.filter(p => {
    if(fParams.cat && p.cat !== fParams.cat) return false;
    if(fParams.plt && !p.plts.includes(fParams.plt)) return false;
    if(fParams.region && !p.regions.includes(fParams.region)) return false;
    if(fParams.text && !p.name.toLowerCase().includes(fParams.text)) return false;
    return true;
  }) : window.products;

  if(checked) {
    filtered.forEach(p => window.selectedProducts.add((window.MOCK_DATA?window.MOCK_DATA.products:window.products).indexOf(p)));
  } else {
    window.selectedProducts.clear();
  }
  window.renderTable();
};

window.updateMasterCheckbox = function() {
  const cb = document.getElementById('masterCheckbox');
  if(!cb) return;
  const total = window.MOCK_DATA ? window.MOCK_DATA.products.length : window.products.length;
  cb.checked = window.selectedProducts.size > 0 && window.selectedProducts.size === total;
};
"""

with open('app.js', 'a', encoding='utf-8') as f:
    f.write('\\n// --- RESTORED ANALYSIS FUNCTIONS ---\\n')
    f.write('\\n\\n'.join(extracted_js))
    f.write('\\n' + render_analysis_js)
    f.write('\\n' + toggle_logic)

print("JS restored correctly!")
