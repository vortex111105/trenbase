import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

if 'lucide.createIcons();' not in html:
    html = html.replace('</body>', '  <script>lucide.createIcons();</script>\\n</body>')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Restored lucide script!")
else:
    print("Script already there")
