import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_render = """  function renderOpportunities() {
    const el = document.getElementById('oppList');
    if(!el) return;
    
    // Sort by low competition and high score
    const sorted = [...products].sort((a,b) => {
      const aComp = a.comp === 'Baja' ? 3 : (a.comp === 'Media' ? 2 : 1);
      const bComp = b.comp === 'Baja' ? 3 : (b.comp === 'Media' ? 2 : 1);
      const aScore = a.score * a.margin * aComp;
      const bScore = b.score * b.margin * bComp;
      return bScore - aScore;
    }).slice(0, 4);
    
    el.innerHTML = sorted.map((p, i) => {
      const isLow = p.comp === 'Baja';
      const badgeBg = isLow ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700';
      const originalIdx = products.indexOf(p);
      return `
        <div class="flex items-center justify-between p-3 border border-gray-100 rounded-xl hover:border-gray-200 hover:bg-gray-50 transition cursor-pointer" onclick="openProduct(${originalIdx})">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center font-bold text-gray-400 text-xs">${i+1}</div>
            <div>
              <div class="font-bold text-sm text-gray-900 truncate max-w-[120px]">${p.name}</div>
              <div class="text-[10px] text-gray-400 font-mono mt-0.5">${p.cat}</div>
            </div>
          </div>
          <div class="text-right flex flex-col items-end">
            <div class="text-sm font-extrabold text-green-500">${p.margin}% ROI</div>
            <div class="text-[9px] font-bold px-1.5 py-0.5 rounded mt-1 ${badgeBg} uppercase tracking-wider">Comp ${p.comp}</div>
          </div>
        </div>
      `;
    }).join('');
  }"""

new_render = """  function renderOpportunities() {
    const el = document.getElementById('oppList');
    if(!el) return;
    
    // Sort by low competition and high score
    const sorted = [...products].sort((a,b) => {
      const aComp = a.comp === 'Baja' ? 3 : (a.comp === 'Media' ? 2 : 1);
      const bComp = b.comp === 'Baja' ? 3 : (b.comp === 'Media' ? 2 : 1);
      const aScore = a.score * a.margin * aComp;
      const bScore = b.score * b.margin * bComp;
      return bScore - aScore;
    }).slice(0, 10);
    
    const cards = sorted.map((p, i) => {
      const isLow = p.comp === 'Baja';
      const badgeBg = isLow ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700';
      const originalIdx = products.indexOf(p);
      return `
        <div class="min-w-[280px] flex items-center justify-between p-3 border border-gray-100 rounded-xl hover:border-gray-200 hover:bg-gray-50 transition cursor-pointer flex-shrink-0 bg-white saas-shadow-sm" onclick="openProduct(${originalIdx})">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center font-bold text-gray-400 text-xs">${i+1}</div>
            <div>
              <div class="font-bold text-sm text-gray-900 truncate w-[100px]">${p.name}</div>
              <div class="text-[10px] text-gray-500 font-mono mt-0.5">${p.cat || 'General'}</div>
            </div>
          </div>
          <div class="text-right flex flex-col items-end justify-center">
            <div class="text-sm font-extrabold text-green-500">${p.margin}% ROI</div>
            <div class="text-[9px] font-bold px-1.5 py-0.5 rounded mt-1 ${badgeBg} uppercase tracking-wider">Comp ${p.comp}</div>
          </div>
        </div>
      `;
    });
    
    // Duplicate multiple times for seamless infinite scroll
    el.innerHTML = [...cards, ...cards, ...cards].join('');
  }"""

js = js.replace(old_render, new_render)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Render Opportunities fixed!")
