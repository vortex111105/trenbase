import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Only apply replacements from line 580 onwards (where Analysis functions are)
parts = js.split('function renderAnalysisKPIs() {')
if len(parts) > 1:
    old_js = parts[0]
    new_js = parts[1]
    
    replacements = {
        'bg-white/5': 'bg-gray-50',
        'border-white/10': 'border-gray-100',
        'border-white/5': 'border-gray-100',
        'text-white/40': 'text-gray-500',
        'text-white/50': 'text-gray-500',
        'text-white/60': 'text-gray-600',
        'text-white/70': 'text-gray-600',
        'text-white/80': 'text-gray-700',
        'text-white': 'text-gray-900',
        'bg-white/10': 'bg-gray-100',
        'bg-black/40': 'bg-gray-200'
    }
    
    for old, new in replacements.items():
        new_js = new_js.replace(old, new)
    
    js = old_js + 'function renderAnalysisKPIs() {' + new_js
    
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Analysis colors fixed!")
else:
    print("Could not find renderAnalysisKPIs")
