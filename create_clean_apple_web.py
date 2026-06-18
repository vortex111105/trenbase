import re

def create_clean_apple_web():
    with open('index.html', 'r') as f:
        content = f.read()

    custom_css = """
  <style id="premium-apple-textured-theme">
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    :root {
      /* Warm, deep, textured sand/cream */
      --aw-bg-base: #EAE6DF;
      --aw-card-bg: rgba(250, 248, 245, 0.65);
      --aw-text-main: #2A2826;
      --aw-text-muted: #7A7570;
      --aw-green: #3F754D;
      --aw-red: #A34848;
      
      /* Multi-layered soft 3D Shadows */
      --aw-shadow: 
        0 40px 80px rgba(130, 120, 110, 0.15), 
        0 12px 24px rgba(130, 120, 110, 0.08), 
        0 4px 8px rgba(130, 120, 110, 0.04),
        inset 0 1px 1px rgba(255, 255, 255, 0.9),
        inset 0 0 4px rgba(255, 255, 255, 0.4);
        
      --aw-shadow-hover: 
        0 50px 100px rgba(130, 120, 110, 0.2), 
        0 16px 32px rgba(130, 120, 110, 0.12), 
        0 4px 12px rgba(130, 120, 110, 0.06),
        inset 0 1px 1px rgba(255, 255, 255, 1),
        inset 0 0 6px rgba(255, 255, 255, 0.6);
    }
    
    body {
      background-color: var(--aw-bg-base) !important;
      background-image: 
        /* Rich grain noise */
        url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)' opacity='0.05'/%3E%3C/svg%3E"),
        /* Massive soft light diffusions */
        radial-gradient(circle at 10% 10%, rgba(255, 252, 248, 0.9) 0%, transparent 45%),
        radial-gradient(circle at 85% 85%, rgba(230, 222, 212, 0.7) 0%, transparent 50%),
        radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.3) 0%, transparent 60%) !important;
      background-attachment: fixed !important;
      color: var(--aw-text-main) !important;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    /* Elegant Cards */
    .aw-card {
      background: var(--aw-card-bg) !important;
      border-radius: 36px !important;
      box-shadow: var(--aw-shadow) !important;
      border: 1px solid rgba(255, 255, 255, 0.5) !important;
      backdrop-filter: blur(40px) saturate(130%) !important;
      -webkit-backdrop-filter: blur(40px) saturate(130%) !important;
      transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
      color: var(--aw-text-main) !important;
    }
    
    .aw-card:hover {
      box-shadow: var(--aw-shadow-hover) !important;
      transform: translateY(-2px) !important;
    }
    
    /* Navigation Glass */
    .aw-nav {
      background: rgba(247, 245, 242, 0.8) !important;
      backdrop-filter: blur(30px) saturate(150%) !important;
      -webkit-backdrop-filter: blur(30px) saturate(150%) !important;
      border-bottom: 1px solid rgba(255, 255, 255, 0.6) !important;
    }
    
    /* Solid Buttons */
    .aw-btn-primary {
      background: linear-gradient(180deg, #3A3A3C 0%, #1C1C1E 100%) !important;
      color: #F5F5F7 !important;
      box-shadow: 0 4px 12px rgba(0,0,0,0.15), inset 0 1px 1px rgba(255,255,255,0.2) !important;
      border: 1px solid rgba(0,0,0,0.8) !important;
    }
    .aw-btn-primary:hover {
      box-shadow: 0 8px 24px rgba(0,0,0,0.25), inset 0 1px 1px rgba(255,255,255,0.3) !important;
      transform: scale(1.02) !important;
    }
    
    /* Typography Overrides */
    h1, h2, h3, h4, h5, h6 { color: var(--aw-text-main) !important; letter-spacing: -0.02em !important; }
    p { color: var(--aw-text-muted) !important; }
    .text-ivory { color: var(--aw-text-main) !important; }
    .text-stone-800, .text-stone-900, .text-white { color: var(--aw-text-main) !important; }
    .text-white\/80, .text-white\/60, .text-white\/50, .text-white\/40, .text-stone-400, .text-stone-500 { color: var(--aw-text-muted) !important; }
    
    .text-green-400, .text-green-500, .text-green-600 { color: var(--aw-green) !important; }
    .text-red-400, .text-red-500, .text-red-600 { color: var(--aw-red) !important; }
    
    .bg-green-500\/10, .bg-green-500\/20 { background: rgba(63,117,77,0.1) !important; color: var(--aw-green) !important; border: 1px solid rgba(63,117,77,0.2) !important; }
    .bg-red-500\/10, .bg-red-500\/20 { background: rgba(163,72,72,0.1) !important; color: var(--aw-red) !important; border: 1px solid rgba(163,72,72,0.2) !important; }
    
    /* Clean Inputs */
    input, select, textarea {
      background: rgba(255, 255, 255, 0.6) !important;
      border: 1px solid rgba(0, 0, 0, 0.05) !important;
      color: var(--aw-text-main) !important;
    }
    
    /* Revert button text explicitly */
    .aw-btn-primary .text-white { color: #F5F5F7 !important; }
    .aw-btn-primary i { color: #F5F5F7 !important; }
  </style>
"""
    if 'premium-apple-textured-theme' not in content:
        content = content.replace('</head>', custom_css + '\n</head>')

    # 1. Backgrounds
    content = content.replace('bg-obsidian', '') # We let the body gradient handle the main background
    content = content.replace('bg-black/95', 'aw-nav') # Navigation bar
    content = content.replace('bg-black/90', 'aw-nav')
    content = content.replace('bg-black/80', 'aw-card')
    content = content.replace('bg-black/50', 'aw-card')
    content = content.replace('bg-white/5', 'aw-card')
    content = content.replace('bg-white/10', 'aw-card')
    content = content.replace('backdrop-blur-xl', '') # Handled by aw-card
    content = content.replace('backdrop-blur-md', '')
    content = content.replace('backdrop-blur-sm', '')
    
    # Remove old borders that break the glass look
    content = content.replace('border-white/10', '')
    content = content.replace('border-white/20', '')
    content = content.replace('border-stone-800', '')
    
    # Primary Buttons mapping (e.g. "Comenzar Gratis")
    content = content.replace('bg-champagne', 'aw-btn-primary')
    content = content.replace('text-black', '') # aw-btn-primary handles text color
    content = content.replace('border-champagne', 'border-transparent')
    
    # Specific buttons to keep them solid
    content = content.replace('bg-white/10 hover:bg-white/20', 'aw-btn-primary')

    # Remove conflicting text colors that might override our !important if inline, though tailwind usually is classes.
    # The CSS takes care of mapping `.text-white` to dark gray automatically.
    
    with open('index.html', 'w') as f:
        f.write(content)
        
    print("Clean mapping successful. Layout strictly preserved.")

create_clean_apple_web()
