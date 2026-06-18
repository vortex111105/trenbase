import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inject CSS for Hyper-real 3D styling
css_to_inject = """
    /* Hiper-Realismo 3D Claro */
    .glass-3d {
      background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.65) 50%, rgba(255,255,255,0.4) 100%) !important;
      border: 1px solid rgba(255,255,255,0.9) !important;
      box-shadow: 
        inset 0 2px 4px rgba(255,255,255,1),
        inset 0 -4px 6px rgba(0,0,0,0.03),
        inset 2px 0 4px rgba(255,255,255,0.6),
        0 4px 6px rgba(0,0,0,0.02),
        0 20px 40px -10px rgba(0,0,0,0.08),
        0 40px 80px -20px rgba(0,0,0,0.12) !important;
      backdrop-filter: blur(32px) saturate(1.2) !important;
      border-radius: 3rem; /* Enforce extreme roundness everywhere */
    }

    /* Hiper-Realismo 3D Oscuro */
    .glass-3d-dark {
      background: linear-gradient(135deg, rgba(35,35,40,0.85) 0%, rgba(18,18,22,0.8) 100%) !important;
      border: 1px solid rgba(255,255,255,0.08) !important;
      box-shadow: 
        inset 0 2px 4px rgba(255,255,255,0.15),
        inset 0 -4px 6px rgba(0,0,0,0.5),
        inset 2px 0 4px rgba(255,255,255,0.05),
        0 4px 10px rgba(0,0,0,0.4),
        0 30px 60px -15px rgba(0,0,0,0.8) !important;
      backdrop-filter: blur(32px) saturate(1.2) !important;
      border-radius: 3rem;
    }
    
    /* Botones 3D Físicos */
    .btn-3d {
      background: linear-gradient(to bottom, #ffffff 0%, #f0f0f5 100%) !important;
      box-shadow: 
        inset 0 2px 2px rgba(255,255,255,1), 
        inset 0 -2px 4px rgba(0,0,0,0.1),
        0 4px 10px rgba(0,0,0,0.1),
        0 15px 30px -5px rgba(0,0,0,0.1) !important;
      border: 1px solid rgba(0,0,0,0.05) !important;
      color: black !important;
      transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .btn-3d:active {
      transform: scale(0.96) translateY(2px);
      box-shadow: 
        inset 0 4px 8px rgba(0,0,0,0.1),
        0 2px 4px rgba(0,0,0,0.05) !important;
    }

    .btn-3d-dark {
      background: linear-gradient(to bottom, #303036 0%, #1a1a1e 100%) !important;
      box-shadow: 
        inset 0 1px 1px rgba(255,255,255,0.15), 
        inset 0 -2px 4px rgba(0,0,0,0.4),
        0 4px 10px rgba(0,0,0,0.3),
        0 15px 30px -5px rgba(0,0,0,0.5) !important;
      border: 1px solid rgba(255,255,255,0.1) !important;
      color: white !important;
      transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    .btn-3d-dark:active {
      transform: scale(0.96) translateY(2px);
      box-shadow: 
        inset 0 4px 8px rgba(0,0,0,0.5),
        0 2px 4px rgba(0,0,0,0.2) !important;
    }
"""

if '.glass-3d' not in html:
    html = html.replace('</style>', css_to_inject + '\\n  </style>')

# 2. Replace hardcoded light card styles with `.glass-3d`
# e.g. bg-white/70 backdrop-blur-3xl border border-white/80 ... spotlight-card
html = re.sub(r'bg-(?:white|gray-50)/[0-9]+ backdrop-blur-[^ ]+ border border-white/[0-9]+[^"]*spotlight-card', 'glass-3d spotlight-card relative', html)
html = re.sub(r'bg-(?:white|gray-50) rounded-\[[^\]]+\] p-8 flex flex-col justify-between h-\[500px\] border border-gray-200 shadow-xl overflow-hidden relative group spotlight-card', 'glass-3d spotlight-card p-8 flex flex-col justify-between h-[500px] overflow-hidden relative group', html)
# Leaderboard cards
html = re.sub(r'bg-white/80 backdrop-blur-md rounded-3xl p-6 border border-white saas-shadow hover:-translate-y-2 transition-transform duration-300 relative group overflow-hidden spotlight-card', 'glass-3d spotlight-card p-6 hover:-translate-y-2 transition-transform duration-300 relative group overflow-hidden', html)

# Stats cards in the dark section
html = re.sub(r'bg-\[\#141416\] border border-white/5 rounded-\[2\.5rem\] p-8 saas-shadow border-none hover:-translate-y-1 transition-transform', 'glass-3d-dark p-8 hover:-translate-y-1 transition-transform', html)

# 3. Replace hardcoded dark card styles with `.glass-3d-dark`
# Pricing cards
html = re.sub(r'bg-\[\#18181B\]/80 backdrop-blur-3xl rounded-\[2\.5rem\] p-10 border border-white/5 flex flex-col transition-all hover:-translate-y-2 saas-shadow spotlight-card spotlight-dark', 'glass-3d-dark spotlight-card p-10 flex flex-col transition-all hover:-translate-y-2 relative overflow-hidden', html)

html = re.sub(r'bg-\[\#1F1F22\] rounded-\[2\.5rem\] p-12 border border-white/10 flex flex-col relative z-20 shadow-2xl shadow-black/50 w-full spotlight-card spotlight-dark', 'glass-3d-dark spotlight-card p-12 flex flex-col relative z-20 w-full overflow-hidden', html)

# 4. Make all buttons Hyper-real 3D
html = re.sub(r'bg-gray-900 text-white[^"]*hover:bg-gray-800[^"]*rounded-full[^"]*', 'btn-3d-dark px-10 py-5 rounded-full font-bold shadow-2xl text-lg relative', html)
html = re.sub(r'bg-white text-black font-extrabold hover:scale-105 transition shadow-\[0_0_30px_rgba\(255,255,255,0\.2\)\] relative z-10', 'btn-3d py-4 rounded-2xl relative z-10 font-bold', html)
html = re.sub(r'bg-white/5 text-white text-sm font-bold border border-white/10 hover:bg-white/10 transition', 'btn-3d-dark text-sm', html)

# Navbar buttons
html = html.replace('bg-black text-white px-8 py-3 rounded-[1.5rem] font-bold text-sm hover:scale-105 transition-transform shadow-xl', 'btn-3d-dark px-8 py-3 rounded-[1.5rem] font-bold text-sm')
html = html.replace('bg-white text-black px-10 py-4 rounded-full font-bold shadow-2xl hover:-translate-y-1 transition-transform text-lg', 'btn-3d px-10 py-4 rounded-full font-extrabold text-lg')

# Leaderboard tags/buttons
html = html.replace('bg-gray-900 text-white px-6 py-2 rounded-full text-sm font-bold', 'btn-3d-dark px-6 py-2 rounded-full text-sm font-bold')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
