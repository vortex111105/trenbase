import re

with open('app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Replace literal \n with actual newlines
app_js = app_js.replace('\\n', '\n')

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

print("Fixed literal newlines in app.js!")
