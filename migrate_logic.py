import re

def merge_logic():
    with open('original_index.html', 'r', encoding='utf-8') as f:
        old_html = f.read()
        
    with open('app.js', 'r', encoding='utf-8') as f:
        app_js = f.read()

    # Functions to extract from old_html
    funcs_to_extract = [
        r'(function getNegocioProducts\(\) \{.*?\n    \})',
        r'(function saveNegocioProducts\(arr\) \{.*?\n    \})',
        r'(function renderNegocio\(\) \{.*?\n    \})',
        r'(function showNegocioModal\(idx\) \{.*?\n    \})',
        r'(function saveNegocioProduct\(\) \{.*?\n    \})',
        r'(function deleteNegocioProduct\(idx\) \{.*?\n    \})',
        r'(function updateStatus\(idx, st\) \{.*?\n    \})',
        r'(function updateRating\(idx, rt\) \{.*?\n    \})',
        r'(function switchModalTab\(tabId, btn\) \{.*?\n    \})',
        r'(function saveCurrentProduct\(\) \{.*?\n    \})',
        r'(function markAsSold\(\) \{.*?\n    \})',
        r'(function analyzeProduct\(\) \{.*?\n    \})',
        r'(function clearMarketingCache\(\) \{.*?\n    \})',
        r'(function copyMktSection\(t,d\) \{.*?\n    \})',
        r'(function copyMktField\(id\) \{.*?\n    \})'
    ]

    extracted = "\n\n// --- MIGRATED MISSING LOGIC FROM OLD UI ---\n"
    for pattern in funcs_to_extract:
        # We need a robust regex to extract whole functions. 
        # Since standard regex is hard for nested braces, we'll extract by keyword until the end of the function.
        # A simpler way: we just read original_logic.js which has all this! Wait, does original_logic.js exist?
        pass

    # Let's use Python to extract the function bodies from original_index.html by finding the function name, then tracking braces.
    def extract_function(name):
        idx = old_html.find(f"function {name}(")
        if idx == -1: return ""
        start = idx
        brace_count = 0
        in_string = False
        string_char = ''
        i = old_html.find('{', start)
        if i == -1: return ""
        brace_count = 1
        i += 1
        while i < len(old_html) and brace_count > 0:
            c = old_html[i]
            if not in_string:
                if c in ('"', "'", '`'):
                    in_string = True
                    string_char = c
                elif c == '{':
                    brace_count += 1
                elif c == '}':
                    brace_count -= 1
            else:
                if c == '\\':
                    i += 1 # skip escaped
                elif c == string_char:
                    in_string = False
            i += 1
        return old_html[start:i]

    functions = [
        'getNegocioProducts', 'saveNegocioProducts', 'renderNegocio', 
        'showNegocioModal', 'saveNegocioProduct', 'deleteNegocioProduct',
        'updateStatus', 'updateRating', 'switchModalTab', 
        'saveCurrentProduct', 'markAsSold', 'analyzeProduct',
        'clearMarketingCache', 'copyMktSection', 'copyMktField', 'openProduct'
    ]

    for f_name in functions:
        if f_name == 'openProduct': continue # We'll handle this manually
        func_code = extract_function(f_name)
        if func_code:
            extracted += f"window.{f_name} = " + func_code + "\n\n"

    # We also need to fix app.js openProduct to populate the missing modal fields like pmChange, pmPrice, etc.
    open_prod_addition = """
    // Extra fields for the advanced modal
    if(document.getElementById('pmChange')) {
        document.getElementById('pmChange').textContent = (p.change_num > 0 ? '+' : '') + p.change_num + '%';
        document.getElementById('pmChange').className = 'text-base font-bold ' + (p.change_num >= 0 ? 'text-green-600' : 'text-red-500');
    }
    if(document.getElementById('pmMargin')) document.getElementById('pmMargin').textContent = p.margin + '%';
    if(document.getElementById('pmCat')) document.getElementById('pmCat').textContent = p.cat;
    if(document.getElementById('pmPrice')) document.getElementById('pmPrice').textContent = p.price_str || ('$' + p.price_min);
    if(document.getElementById('pmComp')) document.getElementById('pmComp').textContent = p.comp;
    if(document.getElementById('pmTag')) {
        document.getElementById('pmTag').style.display = p.hot ? 'inline-block' : 'none';
    }
    
    // Switch to Info tab by default
    if(window.switchModalTab) window.switchModalTab('info', document.querySelector('.modal-tab'));
"""
    
    app_js = app_js.replace("window.openProduct = function(idx) {", "window.openProduct = function(idx) {")
    # Actually just append the addition inside the openProduct function in app.js
    # We will find the end of the openProduct function and insert it.
    app_js = app_js.replace("document.getElementById('prodModal').classList.remove('hidden');", open_prod_addition + "\n    document.getElementById('prodModal').classList.remove('hidden');")

    app_js += extracted

    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(app_js)
    
    print("Migrated logic successfully")

if __name__ == '__main__':
    merge_logic()
