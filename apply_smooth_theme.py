import re

def enhance_theme():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Tailwind config colors to be softer and more visual
    html = html.replace("obsidian: '#0D0D12',", "obsidian: '#161821', /* Smoother, elegant dark blue-grey */")
    html = html.replace("champagne: '#C9A84C',", "champagne: '#E5C471', /* More visual, less muddy gold */")
    html = html.replace("slate: '#2A2A35',", "slate: '#262836',")

    # 2. Add realistic glassmorphism CSS
    glass_css = """
    /* --- Realistic Glassmorphism & Depth --- */
    .glass-panel {
      background: linear-gradient(135deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.01) 100%) !important;
      backdrop-filter: blur(30px) !important;
      -webkit-backdrop-filter: blur(30px) !important;
      border: 1px solid rgba(255,255,255,0.08) !important;
      border-top: 1px solid rgba(255,255,255,0.15) !important;
      border-left: 1px solid rgba(255,255,255,0.15) !important;
      box-shadow: 0 24px 48px rgba(0,0,0,0.25), inset 0 1px 0 rgba(255,255,255,0.05) !important;
    }
    
    .glass-btn {
      background: linear-gradient(180deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.02) 100%);
      box-shadow: inset 0 1px 1px rgba(255,255,255,0.2), 0 4px 12px rgba(0,0,0,0.1);
      border: 1px solid rgba(255,255,255,0.1);
    }
    .glass-btn:hover {
      background: linear-gradient(180deg, rgba(255,255,255,0.15) 0%, rgba(255,255,255,0.05) 100%);
    }

    .neon-badge-green {
      background: rgba(52, 199, 89, 0.15);
      color: #55E079;
      border: 1px solid rgba(52, 199, 89, 0.3);
      padding: 2px 8px;
      border-radius: 12px;
      box-shadow: 0 0 10px rgba(52, 199, 89, 0.2);
    }

    .neon-badge-red {
      background: rgba(255, 59, 48, 0.15);
      color: #FF6B60;
      border: 1px solid rgba(255, 59, 48, 0.3);
      padding: 2px 8px;
      border-radius: 12px;
      box-shadow: 0 0 10px rgba(255, 59, 48, 0.2);
    }
    """
    
    if "/* --- Realistic Glassmorphism & Depth --- */" not in html:
        html = html.replace("</style>", glass_css + "\n  </style>")

    # 3. Replace generic "bg-white/5 border border-white/5 rounded-2xl" with glass-panel for realistic design
    # It appears in dashboard cards, modal sections, etc.
    html = re.sub(r'bg-white/5 border border-white/(?:5|10) rounded-2xl', r'glass-panel rounded-2xl', html)
    html = re.sub(r'bg-obsidian border border-white/10 rounded-\[2\.5rem\]', r'glass-panel rounded-[2.5rem]', html)
    
    # Update auth modal to look like real glass
    html = html.replace('bg-obsidian border border-white/10 rounded-[2.5rem]', 'glass-panel rounded-[2.5rem]')

    # 4. Smooth out flashy text colors (green-400 and red-400) to badges
    html = re.sub(r'text-green-400', r'neon-badge-green font-bold text-xs', html)
    html = re.sub(r'text-red-400', r'neon-badge-red font-bold text-xs', html)

    # 5. Buttons: make them glass buttons where appropriate
    html = html.replace('bg-white/5 hover:bg-white/10 border border-white/10', 'glass-btn rounded-xl transition')
    html = html.replace('bg-white/5 border border-white/10 text-white font-semibold', 'glass-btn text-white font-semibold')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    enhance_theme()
