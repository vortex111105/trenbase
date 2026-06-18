import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Sidebar submenus
content = re.sub(r'text-white/50 hover:text-white', 'text-muted hover:text-[--text-dark]', content)
content = re.sub(r'text-white/60 hover:text-white hover:bg-white/5', 'sidebar-item', content)

# 2. Main Dashboard text colors
content = re.sub(r'text-white/30', 'text-muted', content)
content = re.sub(r'text-white/40', 'text-muted', content)
content = re.sub(r'text-white/70', 'text-[--text-dark] font-medium', content)
content = re.sub(r'text-white/80', 'text-[--text-dark] font-semibold', content)
content = re.sub(r'text-white\b', 'text-[--text-dark]', content)

# 3. Borders and Backgrounds in table and inputs
content = re.sub(r'border-white/10', 'border-[rgba(200,190,180,0.2)]', content)
content = re.sub(r'border-white/20', 'border-[rgba(200,190,180,0.4)]', content)
content = re.sub(r'bg-white/5', 'bg-[rgba(255,255,255,0.4)]', content)
content = re.sub(r'bg-black/40', 'bg-[rgba(240,230,220,0.3)]', content)
content = re.sub(r'bg-black/20', 'bg-[rgba(255,255,255,0.5)]', content)
content = re.sub(r'hover:bg-white/5', 'hover:bg-[rgba(255,255,255,0.6)]', content)

# 4. Modals and Product View backgrounds
content = re.sub(r'bg-\[\#0A0A0A\]', 'matte-card', content)
content = re.sub(r'bg-\[\#111\]', 'matte-card', content)

# 5. Fix text-champagne and green/red variants
content = re.sub(r'text-champagne', 'text-[--text-dark] font-bold', content)
content = re.sub(r'text-green-400', 'text-accent-green', content)
content = re.sub(r'text-red-400', 'text-accent-red', content)

# 6. Buttons
content = re.sub(r'bg-white text-black', 'btn-solid', content)
content = re.sub(r'bg-champagne text-obsidian', 'btn-solid', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("index.html successfully migrated to Liquid Glass design!")
