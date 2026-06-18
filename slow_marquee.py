with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('marquee-opp 20s linear infinite;', 'marquee-opp 80s linear infinite;')

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Marquee speed reduced!")
