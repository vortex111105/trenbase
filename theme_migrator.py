import re

def migrate_theme(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 1. Global structural changes
    replacements = [
        # Body and generic colors
        (r'\bbg-obsidian\b', 'bg-[#F5F5F7]'),
        (r'\btext-ivory\b', 'text-stone-800'),
        
        # Cards and Glassmorphism
        (r'\bbg-white/5\b', 'bg-white/60 backdrop-blur-xl shadow-[0_8px_30px_rgb(0,0,0,0.04)]'),
        (r'\bbg-white/10\b', 'bg-white/80 backdrop-blur-xl shadow-[0_8px_30px_rgb(0,0,0,0.06)]'),
        (r'\bbg-white/20\b', 'bg-white'),
        
        # Borders and Dividers
        (r'\bborder-obsidian\b', 'border-[#F5F5F7]'),
        (r'\bborder-white/5\b', 'border-white/60'),
        (r'\bborder-white/10\b', 'border-white/80'),
        (r'\bborder-white/20\b', 'border-stone-200'),
        (r'\bdivide-white/5\b', 'divide-stone-200'),
        (r'\bdivide-white/10\b', 'divide-stone-200'),
        
        # Placeholders
        (r'\bplaceholder-white/30\b', 'placeholder-stone-400'),
        (r'\bplaceholder-white/40\b', 'placeholder-stone-400'),
        
        # Text opacities
        (r'\btext-white/40\b', 'text-stone-500'),
        (r'\btext-white/50\b', 'text-stone-500'),
        (r'\btext-white/60\b', 'text-stone-600'),
        (r'\btext-white/70\b', 'text-stone-600'),
        (r'\btext-white/80\b', 'text-stone-700'),
        (r'\btext-white/90\b', 'text-stone-700'),
        
        # Hover text
        (r'\bhover:text-white\b', 'hover:text-stone-900'),
        (r'\bgroup-hover:text-white\b', 'group-hover:text-stone-900'),
        
        # Squircles (Apple Widget style)
        (r'\brounded-\[2rem\]\b', 'rounded-[32px]'),
        (r'\brounded-3xl\b', 'rounded-[32px]'),
        (r'\brounded-2xl\b', 'rounded-[32px]'),
        
        # Functional Colors
        (r'\btext-green-400\b', 'text-green-600'),
        (r'\btext-red-400\b', 'text-red-600'),
        (r'\bbg-green-500/10\b', 'bg-green-600/10'),
        (r'\bborder-green-500/20\b', 'border-green-600/20'),
        (r'\bbg-red-500/10\b', 'bg-red-600/10'),
        (r'\bborder-red-500/20\b', 'border-red-600/20'),
        
        # Modals / Overlay backgrounds
        (r'\bbg-black/20\b', 'bg-stone-200/50'),
        (r'\bbg-black/40\b', 'bg-stone-300/50'),
        (r'\bbg-black/80\b', 'bg-stone-800/80'),
    ]

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)

    # 2. General text-white replacements (Careful not to overwrite button text)
    # Replaces text-white with text-stone-800 UNLESS it's preceded by hover: or group-hover:
    content = re.sub(r'(?<!hover:)(?<!group-hover:)\btext-white\b', 'text-stone-800', content)
    
    # Re-fix buttons that legitimately need white text because they have a dark/colored background
    buttons_to_fix = [
        ('bg-green-600 hover:bg-green-700 text-stone-800', 'bg-green-600 hover:bg-green-700 text-white'),
        ('bg-blue-600 flex items-center justify-center text-stone-800', 'bg-blue-600 flex items-center justify-center text-white'),
        ('bg-purple-600 flex items-center justify-center text-stone-800', 'bg-purple-600 flex items-center justify-center text-white'),
        ('bg-red-500 text-stone-800', 'bg-red-500 text-white'),
        ('bg-red-600 text-stone-800', 'bg-red-600 text-white'),
        ('bg-champagne hover:bg-yellow-600 text-stone-800', 'bg-champagne hover:bg-yellow-600 text-white'),
    ]
    for old, new in buttons_to_fix:
        content = content.replace(old, new)
        
    # 3. Apply the Subtle Apple Widget design philosophy: 
    # Large numbers should NOT be brightly colored, they should be dark. Only small indicators stay colored.

    # My Business (Dashboard Dashboard)
    content = content.replace('text-2xl font-extrabold text-green-600 mt-1', 'text-3xl font-extrabold text-stone-900 mt-1 tracking-tight')
    content = content.replace('text-2xl font-extrabold mt-1 ${totalProfit>=0?\'text-green-600\':\'text-red-600\'}', 'text-3xl font-extrabold text-stone-900 mt-1 tracking-tight')

    # Analysis KPI avg margin
    content = content.replace('class="text-3xl font-extrabold text-green-600 mt-1">${avgMargin}%</div>', 'class="text-4xl tracking-tight font-extrabold text-stone-900 mt-1">${avgMargin}%</div>')
    
    # Saturation UI
    content = content.replace('id="satText" class="text-3xl font-extrabold text-green-600 transition-colors duration-500"', 'id="satText" class="text-4xl font-extrabold text-stone-900 tracking-tight transition-colors duration-500"')
    content = content.replace('elSatText.className = `text-3xl font-extrabold ${satColor} transition-colors duration-500`;', 'elSatText.className = `text-4xl font-extrabold text-stone-900 tracking-tight transition-colors duration-500`;')

    # Product detail margin and price
    content = content.replace('id="pmMargin" class="text-base font-bold text-green-600"', 'id="pmMargin" class="text-xl font-extrabold tracking-tight text-stone-900"')
    
    # Product Table margin column
    content = content.replace('<td class="p-4 font-mono text-green-600">${p.marginStr}</td>', '<td class="p-4 font-mono font-bold text-stone-900">${p.marginStr}</td>')
    content = content.replace('<td class="p-4 text-right font-mono font-bold ${profit>=0?\'text-green-600\':\'text-red-600\'}">$${profit.toFixed(0)}</td>', '<td class="p-4 text-right font-mono font-extrabold text-stone-900">$${profit.toFixed(0)}</td>')

    # 4. Chart Colors (JavaScript Canvas)
    content = content.replace("color: 'rgba(255, 255, 255, 0.1)'", "color: 'rgba(0, 0, 0, 0.05)'")
    content = content.replace("color: 'rgba(255, 255, 255, 0.5)'", "color: 'rgba(0, 0, 0, 0.4)'")
    content = content.replace("color: '#FAF8F5'", "color: '#1c1917'") # text-ivory to text-stone-900 in charts
    content = content.replace("color: 'rgba(250, 248, 245, 0.5)'", "color: 'rgba(28, 25, 23, 0.5)'")

    # 5. UI Avatars fallback
    content = content.replace("background=1a1a1a&color=C9A84C", "background=F5F5F7&color=C9A84C")

    with open(filepath, 'w') as f:
        f.write(content)
    print("Migration complete!")

migrate_theme('/Users/nachofrag/Downloads/trenbase_repo/index.html')
