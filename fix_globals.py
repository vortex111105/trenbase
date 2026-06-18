import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Define the missing globals
globals_to_add = """
window.WEEKS = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun'];
window.PAGE_SIZE = 10;
window.AI_SYS = 'Sos el asistente IA de TrendBase, plataforma de tendencias para dropshippers de Argentina, Uruguay y Chile. Ayudás con: productos virales, márgenes estimados, proveedores, estrategias de venta. Respondé en español, conciso y útil. Máximo 3 párrafos.';
"""

# If not already added
if 'window.WEEKS =' not in js:
    js = globals_to_add + '\n' + js

# Replace all occurrences of literal WEEKS, PAGE_SIZE, AI_SYS that are failing in global scope
# We'll use window.WEEKS, window.PAGE_SIZE, window.AI_SYS
js = re.sub(r'\bWEEKS\b', 'window.WEEKS', js)
js = re.sub(r'\bPAGE_SIZE\b', 'window.PAGE_SIZE', js)
js = re.sub(r'\bAI_SYS\b', 'window.AI_SYS', js)

# Fix double window.window if any
js = js.replace('window.window.', 'window.')

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Globals fixed!")
