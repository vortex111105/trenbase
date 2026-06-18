import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Fix calcROI
app_js = app_js.replace("const sales = parseInt(document.getElementById('calcSales').value) || 0;",
                        "const salesEl = document.getElementById('calcSales');\n    const sales = salesEl ? parseInt(salesEl.value) || 0 : 0;")

# Fix renderTable wrapping in try-catch
old_render_table = """window.renderTable = function() {"""
new_render_table = """window.renderTable = function() {
  try {"""

app_js = app_js.replace(old_render_table, new_render_table)

old_render_table_end = """    const pageInfo = document.getElementById('pageInfo');
    if(pageInfo) pageInfo.textContent = `Mostrando ${start + 1}-${Math.min(start + pSize, filtered.length)} de ${filtered.length}`;
    if (window.lucide) window.lucide.createIcons();
  }"""

new_render_table_end = """    const pageInfo = document.getElementById('pageInfo');
    if(pageInfo) pageInfo.textContent = `Mostrando ${start + 1}-${Math.min(start + pSize, filtered.length)} de ${filtered.length}`;
    if (window.lucide) window.lucide.createIcons();
  } catch(e) {
    console.error(e);
    alert("CRASH EN renderTable: " + e.stack);
  }
}"""

app_js = app_js.replace(old_render_table_end, new_render_table_end)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

print("Safe wrappers added")
