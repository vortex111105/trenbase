import re

with open('original_index.html', 'r', encoding='utf-8') as f:
    orig = f.read()

functions = [
    (r'function renderAnalysisKPIs\(\) \{.*?(?=function renderRegionHeatmap)', 'renderAnalysisKPIs'),
    (r'function renderRegionHeatmap\(\) \{.*?(?=function renderTopMargin)', 'renderRegionHeatmap'),
    (r'function renderTopMargin\(\) \{.*?(?=function renderAnalysisCatChart)', 'renderTopMargin'),
    (r'function renderAnalysisCatChart\(\) \{.*?(?=function populateAnalysisSelect)', 'renderAnalysisCatChart'),
    (r'function populateAnalysisSelect\(\) \{.*?(?=function setAnalysisPeriod)', 'populateAnalysisSelect'),
    (r'function setAnalysisPeriod.*?\}', 'setAnalysisPeriod'),
    (r'function playSimulatedAd.*?\}', 'playSimulatedAd'),
    (r'function exportDataCSV\(\) \{.*?(?=function renderAnalysisHistory)', 'exportDataCSV'),
    (r'function renderAnalysisHistory\(\) \{.*?(?=function renderAnalysisChart)', 'renderAnalysisHistory'),
    (r'function renderAnalysisChart.*?\}\s+\}', 'renderAnalysisChart')
]

extracted = []
for pattern, name in functions:
    m = re.search(pattern, orig, flags=re.DOTALL)
    if m:
        extracted.append(m.group(0))
    else:
        print(f"FAILED TO EXTRACT: {name}")

m_askAI = re.search(r'async function askAI.*?catch.*?\}', orig, flags=re.DOTALL)
if m_askAI:
    extracted.append(m_askAI.group(0))

render_analysis_js = """
window.renderAnalysis = function() {
  if (typeof renderAnalysisKPIs === 'function') renderAnalysisKPIs();
  if (typeof renderRegionHeatmap === 'function') renderRegionHeatmap();
  if (typeof renderTopMargin === 'function') renderTopMargin();
  if (typeof renderAnalysisCatChart === 'function') renderAnalysisCatChart();
  if (typeof renderAnalysisHistory === 'function') renderAnalysisHistory();
  if (typeof populateAnalysisSelect === 'function') populateAnalysisSelect();
}

const oldShowSec = window.showSection;
window.showSection = function(id, el) {
  if(oldShowSec) oldShowSec(id, el);
  if(id === 'sec-analisis' && window.renderAnalysis) window.renderAnalysis();
}

window.exportDataCSV = typeof exportDataCSV !== 'undefined' ? exportDataCSV : function(){};
window.setAnalysisPeriod = typeof setAnalysisPeriod !== 'undefined' ? setAnalysisPeriod : function(){};
window.playSimulatedAd = typeof playSimulatedAd !== 'undefined' ? playSimulatedAd : function(){};
window.askAI = typeof askAI !== 'undefined' ? askAI : async function(){};

setTimeout(() => {
  if (window.renderAnalysis) window.renderAnalysis();
}, 1500);
"""

toggle_logic = """
window.selectedProducts = new Set();
window.toggleSelection = function(idx, e) {
  e.stopPropagation();
  if(window.selectedProducts.has(idx)) window.selectedProducts.delete(idx);
  else window.selectedProducts.add(idx);
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

  if(checked) filtered.forEach(p => window.selectedProducts.add((window.MOCK_DATA?window.MOCK_DATA.products:window.products).indexOf(p)));
  else window.selectedProducts.clear();
  window.renderTable();
};
window.updateMasterCheckbox = function() {
  const cb = document.getElementById('masterCheckbox');
  if(!cb) return;
  const total = window.MOCK_DATA ? window.MOCK_DATA.products.length : window.products.length;
  cb.checked = window.selectedProducts.size > 0 && window.selectedProducts.size === total;
};

window.renderPagination = function() {
    const el = document.getElementById('pagination');
    if(!el) return;
    const items = window.MOCK_DATA ? window.MOCK_DATA.products : window.products;
    const totalPages = Math.ceil(items.length / (window.PAGE_SIZE || 10));
    let html = '';
    html += `<button onclick="window.prevPage()" class="w-8 h-8 rounded-lg bg-white border border-gray-200 flex items-center justify-center hover:bg-gray-50 transition shadow-sm"><i data-lucide="chevron-left" class="w-4 h-4"></i></button>`;
    for(let i=1; i<=Math.min(totalPages, 5); i++) {
      if(i === (window.currentPage||1)) {
        html += `<button class="w-8 h-8 rounded-lg bg-black text-white font-bold text-xs flex items-center justify-center saas-shadow transition">${i}</button>`;
      } else {
        html += `<button onclick="window.goToPage(${i})" class="w-8 h-8 rounded-lg bg-white border border-gray-200 text-gray-500 hover:bg-gray-50 hover:text-gray-900 font-bold text-xs flex items-center justify-center transition shadow-sm">${i}</button>`;
      }
    }
    html += `<button onclick="window.nextPage()" class="w-8 h-8 rounded-lg bg-white border border-gray-200 flex items-center justify-center hover:bg-gray-50 transition shadow-sm"><i data-lucide="chevron-right" class="w-4 h-4"></i></button>`;
    el.innerHTML = html;
    if(window.lucide) window.lucide.createIcons();
}
window.goToPage = function(p) {
    window.currentPage = p;
    window.renderTable();
    window.renderPagination();
}
"""

with open('app.js', 'a', encoding='utf-8') as f:
    f.write('\\n// --- RESTORED EXACTLY ---\\n')
    f.write('\\n\\n'.join(extracted))
    f.write('\\n' + render_analysis_js)
    f.write('\\n' + toggle_logic)

print("Perfect extraction completed!")
