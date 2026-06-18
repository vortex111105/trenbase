import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Make PRODUCTS global just in case
if 'window.PRODUCTS =' not in js:
    js = js.replace("const products = window.MOCK_DATA.products;", "const products = window.MOCK_DATA.products;\n  window.PRODUCTS = products;\n  window.products = products;")

# Replace literal PRODUCTS with window.PRODUCTS in the global scope functions
js = re.sub(r'\bPRODUCTS\b', 'window.PRODUCTS', js)

# Since we replaced ALL 'PRODUCTS', we might have replaced window.PRODUCTS to window.window.PRODUCTS
js = js.replace('window.window.PRODUCTS', 'window.PRODUCTS')

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("PRODUCTS fixed!")
