import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

globals_to_add = """
window.aiHistory = [];
window.aiLoading = false;
"""

if 'window.aiHistory =' not in js:
    # Insert right after window.AI_SYS
    js = js.replace("window.AI_SYS = 'Sos el asistente IA", globals_to_add + "window.AI_SYS = 'Sos el asistente IA")

js = re.sub(r'\baiHistory\b', 'window.aiHistory', js)
js = re.sub(r'\baiLoading\b', 'window.aiLoading', js)
js = js.replace('window.window.', 'window.')

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("AI globals fixed!")
