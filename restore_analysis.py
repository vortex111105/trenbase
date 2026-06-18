import re

def migrate_classes(html):
    # Colors and borders
    html = html.replace('bg-white/5', 'bg-white')
    html = html.replace('bg-black/30', 'bg-gray-50')
    html = html.replace('bg-black/20', 'bg-gray-50')
    html = html.replace('bg-black/10', 'bg-gray-50')
    html = html.replace('bg-obsidian', 'bg-white')
    html = html.replace('border-white/10', 'border-gray-100')
    html = html.replace('border-white/5', 'border-gray-100')
    html = html.replace('border-b border-white/5', 'border-b border-gray-100')
    html = html.replace('border-t border-white/10', 'border-t border-gray-100')
    html = html.replace('border-t border-white/5', 'border-t border-gray-100')
    
    # Text colors
    html = html.replace('text-white/70', 'text-gray-700')
    html = html.replace('text-white/60', 'text-gray-600')
    html = html.replace('text-white/50', 'text-gray-500')
    html = html.replace('text-white/40', 'text-gray-400')
    html = html.replace('text-white/30', 'text-gray-400')
    html = html.replace('text-white', 'text-gray-900')
    html = html.replace('text-champagne', 'text-gray-900')
    
    # Specific elements
    html = html.replace('bg-champagne text-obsidian', 'bg-black text-white saas-shadow')
    html = html.replace('bg-white/10 text-white', 'bg-black text-white saas-shadow')
    html = html.replace('text-green-400', 'text-green-500')
    html = html.replace('text-blue-400', 'text-blue-500')
    html = html.replace('shadow-[0_0_10px_rgba(255,255,255,0.8)]', 'shadow-md')
    html = html.replace('bg-green-500/10', 'bg-green-100')
    html = html.replace('bg-yellow-500/10', 'bg-yellow-100')
    html = html.replace('bg-red-500/10', 'bg-red-100')
    
    # Add saas-shadow to cards
    html = html.replace('rounded-[2rem]', 'rounded-[2rem] saas-shadow saas-card-hover')
    html = html.replace('rounded-[2.5rem]', 'rounded-[2.5rem] saas-shadow saas-card-hover')
    
    return html

# 1. Read original section HTML
with open('original_index.html', 'r', encoding='utf-8') as f:
    orig = f.read()

# Extract sec-analisis
match = re.search(r'<!-- SECTION: ANÁLISIS -->(.*?)</section>', orig, flags=re.DOTALL)
if not match:
    print("Could not find sec-analisis in original_index.html")
    exit(1)

sec_analisis_html = match.group(0)
migrated_html = migrate_classes(sec_analisis_html)


# 2. Replace in dashboard.html
with open('dashboard.html', 'r', encoding='utf-8') as f:
    dash = f.read()

# Find the existing sec-analisis and replace
dash = re.sub(r'<!-- ANALISIS SECTION -->.*?</section>', '<!-- ANALISIS SECTION -->\n' + migrated_html, dash, flags=re.DOTALL)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(dash)

# 3. Extract missing JS functions from original_index.html and append to app.js
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

# We also need window.renderAnalysis which calls these sub-renders
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

// Make functions global
window.exportDataCSV = exportDataCSV;
window.setAnalysisPeriod = setAnalysisPeriod;
window.playSimulatedAd = playSimulatedAd;
window.askAI = askAI;

setTimeout(() => {
  if (window.renderAnalysis) window.renderAnalysis();
}, 1500);
"""

with open('app.js', 'a', encoding='utf-8') as f:
    f.write('\\n// --- RESTORED ANALYSIS FUNCTIONS ---\\n')
    f.write('\\n\\n'.join(extracted_js))
    f.write('\\n' + render_analysis_js)

print("Migration completed.")
