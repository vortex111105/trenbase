import re

def migrate():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # CSS updates
    css_updates = {
        r'\.glass-panel\s*\{[^}]*\}': """.glass-panel {
      background: #FFFFFF !important;
      border: 1px solid rgba(0,0,0,0.08) !important;
      border-radius: 2rem !important;
      box-shadow: 0 12px 36px rgba(0,0,0,0.06) !important;
    }""",
        r'\.neon-badge-green': ".neon-badge-green { color: #059669; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.2); }",
        r'\.neon-badge-red': ".neon-badge-red { color: #DC2626; background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.2); }"
    }
    for pat, rep in css_updates.items():
        html = re.sub(pat, rep, html)

    # HTML Class replacements
    replacements = [
        # Body
        ('bg-obsidian text-white font-sans', 'bg-[#F4F5F7] text-gray-900 font-sans'),
        
        # Sidebar
        ('bg-black/40 border-r border-white/10', 'bg-[#1A1A1A] text-white border-r border-black/10'),
        
        # Text colors in main area
        ('text-white/40', 'text-gray-500'),
        ('text-white/50', 'text-gray-500'),
        ('text-white/60', 'text-gray-600'),
        ('text-white/70', 'text-gray-700'),
        ('text-white', 'text-gray-900'),
        ('border-white/10', 'border-gray-200'),
        ('border-white/5', 'border-gray-100'),
        ('bg-white/5', 'bg-gray-50'),
        ('bg-white/10', 'bg-gray-100'),
        
        # Buttons
        ('bg-champagne text-obsidian', 'bg-black text-white rounded-2xl'),
        ('text-champagne', 'text-black font-bold'),
        ('border-champagne', 'border-black'),
        
        # Modal
        ('bg-obsidian/90 backdrop-blur-md', 'bg-white/90 backdrop-blur-md border-b border-gray-100'),
        
        # Charts (replace colors)
        ("grid: { color: 'rgba(255,255,255,0.05)' }", "grid: { color: 'rgba(0,0,0,0.05)' }"),
        ("ticks: { color: 'rgba(255,255,255,0.5)'", "ticks: { color: 'rgba(0,0,0,0.5)'"),
        ("'#C9A84C'", "'#000000'"), # Lines become black
        ("'rgba(201, 168, 76, 0.1)'", "'rgba(0, 0, 0, 0.05)'"), # Fills become light gray
    ]
    
    # We must be careful because Sidebar still has text-white. 
    # Let's do replacements only in specific blocks or be aware of sidebar vs main.
    # The sidebar is `<aside ...>...</aside>`. We can protect it by splitting.
    
    parts = re.split(r'(<aside.*?</aside>)', html, flags=re.DOTALL)
    
    if len(parts) == 3:
        # parts[0] is everything before aside (header, nav)
        # parts[1] is aside
        # parts[2] is everything after aside (main content)
        
        for old, new in replacements:
            parts[0] = parts[0].replace(old, new)
            parts[2] = parts[2].replace(old, new)
            
        html = "".join(parts)
    else:
        for old, new in replacements:
            html = html.replace(old, new)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
if __name__ == '__main__':
    migrate()
    print("Migration complete.")
