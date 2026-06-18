import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix CSS background
css_target = r"background-image:\s*url\('https://images\.unsplash\.com/[^']+'\);\s*background-size:\s*cover;\s*background-position:\s*center;"
css_replacement = "background-image: radial-gradient(circle at 20% 0%, rgba(255, 255, 255, 0.8) 0%, rgba(255, 255, 255, 0) 50%), radial-gradient(circle at 80% 100%, rgba(201, 168, 76, 0.08) 0%, rgba(201, 168, 76, 0) 50%);"
content = re.sub(css_target, css_replacement, content)

# Fix features section transparency
# We want to change the feature cards from bg-[rgba(255,255,255,0.4)] to matte-card
# Let's just do a blanket replacement in the Landing Page sections for large cards.
# Wait, it's easier to just replace all bg-[rgba(255,255,255,0.4)] with matte-card globally!
# It will make the UI look very solid and ceramic, which is exactly what Apple Vision does (panels inside panels).
content = content.replace('bg-[rgba(255,255,255,0.4)]', 'matte-card')
content = content.replace('bg-[rgba(255,255,255,0.6)]', 'matte-card')
content = content.replace('bg-[rgba(255,255,255,0.8)]', 'matte-card')

# Except for the navbar container, which I manually set to `sidebar-panel` and `border border-[rgba(255,255,255,0.6)]` (no background class). 
# Wait, `clean_pricing.py` added `bg-[rgba(255,255,255,0.4)]` to pricing buttons. Those will become matte-card, which is perfect (white button).

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Background and transparencies fixed!")
