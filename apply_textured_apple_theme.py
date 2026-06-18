import re

def apply_textured_theme():
    with open('index.html', 'r') as f:
        content = f.read()

    custom_css = """
  <style id="premium-apple-textured-theme">
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    :root {
      /* Rich, warm, textured colors */
      --aw-bg-base: #E8E3DD;
      --aw-card-bg: rgba(250, 248, 245, 0.55);
      --aw-text-main: #2A2826;
      --aw-text-muted: #7D7873;
      --aw-green: #3F754D;
      --aw-red: #A34848;
      
      /* Complex Multi-layered Shadows */
      --aw-shadow: 
        0 40px 80px rgba(130, 120, 110, 0.12), 
        0 12px 24px rgba(130, 120, 110, 0.08), 
        0 4px 8px rgba(130, 120, 110, 0.04),
        inset 0 1px 1px rgba(255, 255, 255, 1),
        inset 0 0 4px rgba(255, 255, 255, 0.5);
        
      --aw-shadow-hover: 
        0 50px 100px rgba(130, 120, 110, 0.18), 
        0 16px 32px rgba(130, 120, 110, 0.12), 
        0 4px 12px rgba(130, 120, 110, 0.06),
        inset 0 1px 1px rgba(255, 255, 255, 1),
        inset 0 0 6px rgba(255, 255, 255, 0.6);
        
      --aw-btn-primary: linear-gradient(180deg, #3D3B3A 0%, #1A1918 100%);
    }
    
    /* 1. Body Mesh Gradient & Noise */
    body {
      background-color: var(--aw-bg-base) !important;
      background-image: 
        /* Noise Texture SVG */
        url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.04'/%3E%3C/svg%3E"),
        /* Warm Light Glows */
        radial-gradient(circle at 15% 10%, rgba(255, 253, 250, 0.8) 0%, transparent 40%),
        radial-gradient(circle at 85% 90%, rgba(230, 220, 210, 0.6) 0%, transparent 40%),
        radial-gradient(circle at 50% 50%, rgba(255, 250, 245, 0.4) 0%, transparent 60%) !important;
      background-attachment: fixed !important;
      color: var(--aw-text-main) !important;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
      letter-spacing: -0.02em;
    }
    
    /* 2. Glassmorphism Squircles */
    .aw-card {
      background: var(--aw-card-bg) !important;
      border-radius: 36px !important;
      box-shadow: var(--aw-shadow) !important;
      border: 1px solid rgba(255, 255, 255, 0.4) !important;
      backdrop-filter: blur(40px) saturate(140%) !important;
      -webkit-backdrop-filter: blur(40px) saturate(140%) !important;
      transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1) !important;
      color: var(--aw-text-main) !important;
    }
    
    .aw-card:hover {
      box-shadow: var(--aw-shadow-hover) !important;
      transform: translateY(-4px) !important;
      border: 1px solid rgba(255, 255, 255, 0.7) !important;
    }
    
    /* Buttons */
    button, .btn {
      transition: all 0.3s ease !important;
    }
    
    .aw-btn-primary {
      background: var(--aw-btn-primary) !important;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2), inset 0 1px 1px rgba(255,255,255,0.15) !important;
      color: #F5F5F7 !important;
      border-radius: 999px !important;
      font-weight: 600 !important;
      border: 1px solid rgba(0,0,0,0.8) !important;
    }
    .aw-btn-primary:hover {
      transform: scale(1.02) !important;
      box-shadow: 0 8px 24px rgba(0,0,0,0.3), inset 0 1px 1px rgba(255,255,255,0.2) !important;
    }
    
    /* Utility Classes */
    .text-stone-800, .text-stone-900, .text-white { color: var(--aw-text-main) !important; }
    .text-stone-500, .text-stone-400, .text-white\/50, .text-white\/60, .text-white\/40 { color: var(--aw-text-muted) !important; }
    .text-green-400, .text-green-600 { color: var(--aw-green) !important; }
    .text-red-400, .text-red-600 { color: var(--aw-red) !important; }
    
    .bg-obsidian { background: transparent !important; } /* Replaced by body mesh */
    
    /* Force form elements to be elegant */
    input, select, textarea {
      background: rgba(255, 255, 255, 0.5) !important;
      border: 1px solid rgba(0, 0, 0, 0.05) !important;
      color: var(--aw-text-main) !important;
      border-radius: 16px !important;
      box-shadow: inset 0 2px 4px rgba(0,0,0,0.02) !important;
    }
    
    /* Reset text-white inside primary buttons so it doesn't get turned to dark gray */
    .aw-btn-primary .text-white { color: #F5F5F7 !important; }
  </style>
"""

    if 'premium-apple-textured-theme' not in content:
        content = content.replace('</head>', custom_css + '\n</head>')

    replacements = [
        # Cards
        (r'\bbg-white/5\b', 'aw-card'),
        (r'\bbg-white/10\b', 'aw-card'),
        (r'\bbackdrop-blur-xl\b', ''), # Handled by aw-card
        (r'\bborder-white/10\b', ''), # Handled by aw-card
        
        # Badges
        (r'\bbg-green-500/10\b', 'bg-[rgba(63,117,77,0.1)] border border-[rgba(63,117,77,0.2)]'),
        (r'\bbg-red-500/10\b', 'bg-[rgba(163,72,72,0.1)] border border-[rgba(163,72,72,0.2)]'),
        
        # Primary Buttons (the big ones like Signup, Login, etc)
        (r'\bbg-champagne text-black\b', 'aw-btn-primary'),
        (r'\bhover:bg-white\b', ''),
        (r'\btext-champagne\b', 'text-[#2A2826]'),
        (r'\bborder-champagne\b', 'border-[#2A2826]'),
    ]

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
        
    # Extra fix: make sure the specific big landing buttons get aw-btn-primary
    content = content.replace('px-6 py-2 bg-white/10 hover:bg-white/20 text-white rounded-lg font-medium transition', 'aw-btn-primary px-6 py-2')
    content = content.replace('w-full py-3 bg-champagne text-black rounded-lg font-bold hover:bg-white transition flex items-center justify-center gap-2 mt-4', 'aw-btn-primary w-full py-3 flex items-center justify-center gap-2 mt-4')

    with open('index.html', 'w') as f:
        f.write(content)
    print("Perfect Textured Apple Theme applied to original HTML!")

apply_textured_theme()
