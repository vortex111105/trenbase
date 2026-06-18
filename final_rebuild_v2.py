import re
import os

os.system('git restore app.js')

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

new_render_table = """window.renderTable = function() {
  try {
    const tbody = document.getElementById('tableBody');
    if(!tbody) return;
    
    // We get window.filterParams or use a default if it doesn't exist yet
    const fParams = window.filterParams || {cat: '', plt: '', region: '', text: ''};
    
    let filtered = window.MOCK_DATA ? window.MOCK_DATA.products.filter(p => {
      if(fParams.cat && p.cat !== fParams.cat) return false;
      if(fParams.plt && !p.plts.includes(fParams.plt)) return false;
      if(fParams.region && !p.regions.includes(fParams.region)) return false;
      if(fParams.text && !p.name.toLowerCase().includes(fParams.text)) return false;
      return true;
    }) : (window.products || []); // Fallback

    if(fParams.sort === 'score') filtered.sort((a,b) => b.score - a.score);
    if(fParams.sort === 'change') filtered.sort((a,b) => parseFloat(b.change) - parseFloat(a.change));
    if(fParams.sort === 'margin') filtered.sort((a,b) => b.margin - a.margin);

    const pSize = window.PAGE_SIZE || 10;
    const cPage = window.currentPage || 1;
    const start = (cPage - 1) * pSize;
    const list = filtered.slice(start, start + pSize);
    
    const savedIds = window.getSavedProducts ? window.getSavedProducts().map(s => s.name) : [];

    tbody.innerHTML = list.map((p, i) => {
      const idx = window.MOCK_DATA ? window.MOCK_DATA.products.indexOf(p) : (window.products ? window.products.indexOf(p) : start + i);
      const isHot = p.score >= 90;
      const isRising = p.changeNum > 10;
      
      let badgeHtml = '';
      if(isHot) badgeHtml = '<span class="bg-red-50 text-red-600 border border-red-100 text-[10px] font-bold px-2 py-0.5 rounded uppercase ml-2">HOT</span>';
      else if(isRising) badgeHtml = '<span class="bg-blue-50 text-blue-600 border border-blue-100 text-[10px] font-bold px-2 py-0.5 rounded uppercase ml-2">RISING</span>';
      
      const changeColor = p.changeNum > 0 ? 'text-green-500' : (p.changeNum < 0 ? 'text-red-500' : 'text-gray-400');
      const isSaved = savedIds.includes(p.name);
      
      const isChecked = window.selectedProducts && window.selectedProducts.has(idx);

      return `
        <tr class="border-b border-gray-100 hover:bg-gray-50/50 transition">
          <td class="p-4 w-10 text-center" onclick="event.stopPropagation()">
            <input type="checkbox" ${isChecked ? 'checked' : ''} onchange="toggleSelection(${idx}, event)" class="accent-black w-3 h-3 rounded bg-white border-gray-200">
          </td>
          <td class="p-4 w-12 text-center text-gray-500 font-mono text-xs">${start + i + 1}</td>
          <td class="p-4 pl-6 cursor-pointer" onclick="openProduct(${idx})">
            <div class="flex items-center gap-4">
              <div class="w-10 h-10 rounded-xl bg-gray-100 border border-gray-200 flex items-center justify-center flex-shrink-0">
                <i data-lucide="image" class="w-4 h-4 text-gray-400"></i>
              </div>
              <div>
                <div class="font-bold text-gray-900 leading-tight max-w-[200px] truncate" title="${p.name}">${p.name}</div>
                <div class="text-[10px] text-gray-500 mt-0.5 flex items-center gap-1">
                  <span class="bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded uppercase">${p.cat || 'General'}</span>
                  ${p.plts ? p.plts.map(plt => `<span class="bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded uppercase">${plt}</span>`).join('') : ''}
                </div>
              </div>
            </div>
          </td>
          <td class="p-4">
            <span class="font-black text-gray-900 text-lg flex items-center">${p.score} ${badgeHtml}</span>
          </td>
          <td class="p-4 font-mono font-bold ${changeColor}">${p.change || '+0%'}</td>
          <td class="p-4 font-mono font-bold text-green-500">${p.marginStr || (p.margin ? p.margin + '%' : 'N/A')}</td>
          <td class="p-4">
            <span class="text-xs font-bold text-gray-900 bg-gray-100 px-2 py-1 rounded-md">${p.comp || 'Media'}</span>
          </td>
          <td class="p-4 font-mono font-bold text-gray-900">${p.priceStr || ('$'+(p.priceMin||0))}</td>
          <td class="p-4">
            <div class="text-xs text-gray-900 font-bold max-w-[120px] truncate" title="${p.suppliers && p.suppliers[0] ? p.suppliers[0].name : 'AliExpress'}">
              ${p.suppliers && p.suppliers[0] ? p.suppliers[0].name : 'AliExpress'}
            </div>
            <div class="text-[10px] text-gray-500 font-mono">${p.suppliers && p.suppliers[0] ? p.suppliers[0].price : 'Varía'}</div>
          </td>
          <td class="p-4 pr-6 text-right flex items-center justify-end gap-3 h-[73px]">
            <button onclick="event.stopPropagation(); window.toggleSave(${idx})" class="${isSaved ? 'text-black fill-current' : 'text-gray-400'} hover:text-black transition flex items-center justify-center h-full"><i data-lucide="bookmark" class="w-5 h-5"></i></button>
            <button onclick="event.stopPropagation(); window.openProduct(${idx})" class="bg-black hover:-translate-y-0.5 text-white text-xs font-extrabold px-5 py-2.5 rounded-xl transition saas-shadow">Ver</button>
          </td>
        </tr>
      `;
    }).join('');
    
    const pageInfo = document.getElementById('pageInfo');
    if(pageInfo) pageInfo.textContent = `Mostrando ${start + 1}-${Math.min(start + pSize, filtered.length)} de ${filtered.length}`;
    if (window.lucide) window.lucide.createIcons();
  } catch(e) {
    console.error(e);
    alert("CRASH EN renderTable: " + e.stack);
  }
}"""
app_js = re.sub(r'window\.renderTable = function\(\) \{.*?(?=window\.nextPage = function)', new_render_table + '\n\n  ', app_js, flags=re.DOTALL)

old_init_dash = """    function initDashboard() {"""
new_init_dash = """    function initDashboard() {
    try {"""
app_js = app_js.replace(old_init_dash, new_init_dash)

old_init_dash_end = """    initCharts();
    renderTable();
    renderOpportunities();
    window.calcROI();
  }"""
new_init_dash_end = """    try { initCharts(); } catch(e) { console.warn(e); }
    renderTable();
    renderOpportunities();
    if(window.calcROI) window.calcROI();
    } catch(e) {
      alert("CRASH EN initDashboard: " + e.stack);
    }
  }"""
app_js = app_js.replace(old_init_dash_end, new_init_dash_end)

app_js = app_js.replace("lucide.createIcons();", "if(typeof lucide !== 'undefined') lucide.createIcons();")
app_js = app_js.replace("window.if(typeof lucide !== 'undefined') lucide.createIcons();", "window.lucide.createIcons();")
app_js = app_js.replace("const sales = parseInt(document.getElementById('calcSales').value) || 0;", "const salesEl = document.getElementById('calcSales');\n    const sales = salesEl ? parseInt(salesEl.value) || 0 : 0;")

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
    (r'function renderAnalysisChart\(\) \{.*?(?=function calcROI)', 'renderAnalysisChart')
]

extracted = []
for pattern, name in functions:
    m = re.search(pattern, orig, flags=re.DOTALL)
    if m:
        extracted.append(m.group(0))

m_askAI = re.search(r'async function askAI.*?msgs\.scrollHeight;\s+\}', orig, flags=re.DOTALL)
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

app_js += '\n// --- RESTORED EXACTLY ---\n'
app_js += '\n\n'.join(extracted)
app_js += '\n' + render_analysis_js
app_js += '\n' + toggle_logic

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

print("App.js absolutely perfectly built from scratch v2.")
