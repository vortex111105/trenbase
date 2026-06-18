import re

# Read dashboard.html
with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. ADD GOOGLE FONTS & CUSTOM CSS
google_fonts = """
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  
  <style>
    /* Premium Typography */
    body { font-family: 'Outfit', sans-serif; }
    
    /* Scrollbar minimalista */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.1); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(0,0,0,0.2); }

    /* Micro-animations */
    .saas-card-hover {
      transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .saas-card-hover:hover {
      transform: translateY(-4px);
      box-shadow: 0 20px 40px -10px rgba(0,0,0,0.08), 0 0 0 1px rgba(0,0,0,0.03);
    }

    /* Glassmorphism Sidebar */
    .sidebar-glass {
      background: rgba(17, 17, 17, 0.95);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-right: 1px solid rgba(255,255,255,0.05);
    }

    /* Animated Background Orbs */
    .bg-orb {
      position: absolute;
      border-radius: 50%;
      filter: blur(80px);
      z-index: 0;
      animation: floatOrb 20s infinite ease-in-out alternate;
      pointer-events: none;
    }
    .orb-1 { width: 400px; height: 400px; background: rgba(255, 215, 0, 0.15); top: -10%; left: -10%; animation-delay: 0s; }
    .orb-2 { width: 300px; height: 300px; background: rgba(0, 200, 255, 0.1); bottom: 10%; right: -5%; animation-delay: -5s; }
    .orb-3 { width: 350px; height: 350px; background: rgba(255, 100, 150, 0.1); top: 40%; left: 30%; animation-delay: -10s; }

    @keyframes floatOrb {
      0% { transform: translate(0, 0) scale(1); }
      50% { transform: translate(50px, 30px) scale(1.1); }
      100% { transform: translate(-30px, 50px) scale(0.9); }
    }
    
    /* Table hover glow */
    tbody tr { transition: all 0.2s ease; }
    tbody tr:hover { background-color: rgba(255,255,255,0.8); box-shadow: inset 0 0 0 1px rgba(0,0,0,0.05); transform: scale(1.002); z-index: 10; position: relative; }
  </style>
</head>
"""

html = html.replace('</head>', google_fonts)

# 2. Add Background Orbs inside main content area
orbs_html = """
    <!-- Animated Orbs -->
    <div class="fixed inset-0 pointer-events-none overflow-hidden z-0">
      <div class="bg-orb orb-1"></div>
      <div class="bg-orb orb-2"></div>
      <div class="bg-orb orb-3"></div>
    </div>
"""

# Find the start of the main section. It's inside `<main class="flex-1 ...">`
main_start_pattern = r'(<main[^>]*>)'
html = re.sub(main_start_pattern, r'\\1\n' + orbs_html, html, count=1)

# Make sure the main inner wrapper has z-10 so it stays above orbs
html = html.replace('<div class="p-8 pb-32">', '<div class="p-8 pb-32 relative z-10">')
html = html.replace('<div class="max-w-7xl mx-auto space-y-8">', '<div class="max-w-7xl mx-auto space-y-8 relative z-10">')

# 3. Upgrade Sidebar
# Currently: <aside class="w-64 bg-black text-white p-6 flex flex-col m-4 rounded-[2.5rem] shadow-2xl z-20">
sidebar_old = '<aside class="w-64 bg-black text-white p-6 flex flex-col m-4 rounded-[2.5rem] shadow-2xl z-20">'
sidebar_new = '<aside class="w-64 sidebar-glass text-white p-6 flex flex-col m-4 rounded-[2.5rem] shadow-2xl z-20 shadow-black/20">'
html = html.replace(sidebar_old, sidebar_new)

# Upgrade top search bar area to be slightly translucent
html = html.replace('<header class="flex justify-between items-center bg-white/80 backdrop-blur-md sticky top-0 z-30 py-4 px-2 -mx-2">',
                    '<header class="flex justify-between items-center bg-white/60 backdrop-blur-xl sticky top-0 z-30 py-4 px-2 -mx-2 border-b border-white/40">')

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Aesthetics upgraded successfully!")
