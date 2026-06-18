import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# We need to replace the old renderTable with a full 10-column renderTable
old_render_table_pattern = r'window\.renderTable = function\(\) \{.*?(?=window\.quickSale = function\(idx\))'

new_render_table = """window.renderTable = function() {
    const tbody = document.getElementById('tableBody');
    if(!tbody) return;
    
    let filtered = window.MOCK_DATA.products.filter(p => {
      if(window.filterParams.cat && p.cat !== window.filterParams.cat) return false;
      if(window.filterParams.plt && !p.plts.includes(window.filterParams.plt)) return false;
      if(window.filterParams.region && !p.regions.includes(window.filterParams.region)) return false;
      if(window.filterParams.text && !p.name.toLowerCase().includes(window.filterParams.text)) return false;
      return true;
    });

    if(window.filterParams.sort === 'score') filtered.sort((a,b) => b.score - a.score);
    if(window.filterParams.sort === 'change') filtered.sort((a,b) => parseFloat(b.change) - parseFloat(a.change));
    if(window.filterParams.sort === 'margin') filtered.sort((a,b) => b.margin - a.margin);

    const start = (window.currentPage - 1) * window.PAGE_SIZE;
    const list = filtered.slice(start, start + window.PAGE_SIZE);
    
    const savedIds = window.getSavedProducts ? window.getSavedProducts().map(s => s.name) : [];

    tbody.innerHTML = list.map((p, i) => {
      const idx = window.MOCK_DATA.products.indexOf(p);
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
                  <span class="bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded uppercase">${p.cat}</span>
                  ${p.plts.map(plt => `<span class="bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded uppercase">${plt}</span>`).join('')}
                </div>
              </div>
            </div>
          </td>
          <td class="p-4">
            <span class="font-black text-gray-900 text-lg flex items-center">${p.score} ${badgeHtml}</span>
          </td>
          <td class="p-4 font-mono font-bold ${changeColor}">${p.change}</td>
          <td class="p-4 font-mono font-bold text-green-500">${p.marginStr || (p.margin + '%')}</td>
          <td class="p-4">
            <span class="text-xs font-bold text-gray-900 bg-gray-100 px-2 py-1 rounded-md">${p.comp}</span>
          </td>
          <td class="p-4 font-mono font-bold text-gray-900">${p.priceStr || ('$'+p.priceMin)}</td>
          <td class="p-4">
            <div class="text-xs text-gray-900 font-bold max-w-[120px] truncate" title="${p.suppliers && p.suppliers[0] ? p.suppliers[0].name : 'AliExpress'}">
              ${p.suppliers && p.suppliers[0] ? p.suppliers[0].name : 'AliExpress'}
            </div>
            <div class="text-[10px] text-gray-500 font-mono">${p.suppliers && p.suppliers[0] ? p.suppliers[0].price : 'Varía'}</div>
          </td>
          <td class="p-4 pr-6 text-right flex items-center justify-end gap-3 h-[73px]">
            <button onclick="event.stopPropagation(); toggleSave(${idx})" class="${isSaved ? 'text-black fill-current' : 'text-gray-400'} hover:text-black transition flex items-center justify-center h-full"><i data-lucide="bookmark" class="w-5 h-5"></i></button>
            <button onclick="event.stopPropagation(); openProduct(${idx})" class="bg-black hover:-translate-y-0.5 text-white text-xs font-extrabold px-5 py-2.5 rounded-xl transition saas-shadow">Ver</button>
          </td>
        </tr>
      `;
    }).join('');
    
    document.getElementById('pageInfo').textContent = `Mostrando ${start + 1}-${Math.min(start + window.PAGE_SIZE, filtered.length)} de ${filtered.length}`;
    if (window.lucide) window.lucide.createIcons();
}

"""

app_js = re.sub(old_render_table_pattern, new_render_table, app_js, flags=re.DOTALL)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

print("RenderTable fixed!")
