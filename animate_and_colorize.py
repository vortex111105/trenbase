import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add background animations to Auroras
aurora_css = """
    @keyframes aurora-float-1 {
      0%, 100% { transform: translate(0, 0) scale(1) rotate(0deg); }
      33% { transform: translate(30px, -50px) scale(1.1) rotate(45deg); }
      66% { transform: translate(-20px, 20px) scale(0.9) rotate(-15deg); }
    }
    @keyframes aurora-float-2 {
      0%, 100% { transform: translate(0, 0) scale(1) rotate(0deg); }
      33% { transform: translate(-30px, 50px) scale(1.15) rotate(-30deg); }
      66% { transform: translate(20px, -20px) scale(0.85) rotate(20deg); }
    }
    .animate-aurora-1 { animation: aurora-float-1 15s ease-in-out infinite; }
    .animate-aurora-2 { animation: aurora-float-2 18s ease-in-out infinite reverse; }
"""
if 'aurora-float-1' not in html:
    html = html.replace('</style>', aurora_css + '\\n  </style>', 1)

# Add animation classes to existing huge auroras
html = html.replace('w-[800px] h-[800px]', 'w-[800px] h-[800px] animate-aurora-1')
# Let's make half of them animate-aurora-2 to give varied movement
html = html.replace('animate-aurora-1', 'animate-aurora-2', 2) # replace first 2 occurrences

# 2. Colorize Protocol Steps
# Currently they are all identical bg-gradient-to-br from-white/90 via-white/60 to-white/30
# We need to replace them specifically based on their step content.

# STEP 1: Cyan/Azul
step_1_old_bg = '<!-- Step 1 Bubble -->\\n        <div class="bg-gradient-to-br from-white/90 via-white/60 to-white/30 backdrop-blur-3xl border border-white/80 rounded-[3rem] p-10 md:p-16 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center spotlight-card">'
step_1_new_bg = '<!-- Step 1 Bubble -->\\n        <div class="bg-gradient-to-br from-white/90 via-cyan-50/50 to-white/30 backdrop-blur-3xl border border-white/80 rounded-[3rem] p-10 md:p-16 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center spotlight-card">'
html = html.replace(step_1_old_bg, step_1_new_bg)

step_1_old_pill = '<span class="font-mono text-xs text-gray-900 bg-gray-100/50 border border-gray-200 font-bold px-3 py-1 rounded-full">PASO 01 //'
step_1_new_pill = '<span class="font-mono text-xs text-cyan-700 bg-cyan-100/50 border border-cyan-200 font-bold px-3 py-1 rounded-full">PASO 01 //'
html = html.replace(step_1_old_pill, step_1_new_pill)

# Step 1 SVG colors: #111827 -> #0891b2
step_1_svg = """<circle cx="50" cy="50" r="45" fill="none" stroke="#111827" stroke-width="0.5" stroke-dasharray="2 6" opacity="0.5"/>
              <circle cx="50" cy="50" r="35" fill="none" stroke="#111827" stroke-width="0.5" stroke-dasharray="10 5" opacity="0.3"/>
              <circle cx="50" cy="50" r="25" fill="none" stroke="#111827" stroke-width="1"/>
              <line x1="50" y1="0" x2="50" y2="100" stroke="#111827" stroke-width="0.2" opacity="0.2"/>
              <line x1="0" y1="50" x2="100" y2="50" stroke="#111827" stroke-width="0.2" opacity="0.2"/>"""
step_1_svg_new = """<circle cx="50" cy="50" r="45" fill="none" stroke="#0891b2" stroke-width="0.5" stroke-dasharray="2 6" opacity="0.5"/>
              <circle cx="50" cy="50" r="35" fill="none" stroke="#0891b2" stroke-width="0.5" stroke-dasharray="10 5" opacity="0.3"/>
              <circle cx="50" cy="50" r="25" fill="none" stroke="#06b6d4" stroke-width="1" filter="drop-shadow(0 0 4px #22d3ee)"/>
              <line x1="50" y1="0" x2="50" y2="100" stroke="#0891b2" stroke-width="0.2" opacity="0.2"/>
              <line x1="0" y1="50" x2="100" y2="50" stroke="#0891b2" stroke-width="0.2" opacity="0.2"/>"""
html = html.replace(step_1_svg, step_1_svg_new)

# STEP 2: Purple/Fuchsia
step_2_old_bg = '<!-- Step 2 Bubble -->\\n        <div class="bg-gradient-to-br from-white/90 via-white/60 to-white/30 backdrop-blur-3xl border border-white/80 rounded-[3rem] p-10 md:p-16 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center spotlight-card">'
step_2_new_bg = '<!-- Step 2 Bubble -->\\n        <div class="bg-gradient-to-br from-white/90 via-fuchsia-50/50 to-white/30 backdrop-blur-3xl border border-white/80 rounded-[3rem] p-10 md:p-16 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center spotlight-card">'
html = html.replace(step_2_old_bg, step_2_new_bg)

step_2_old_pill = '<span class="font-mono text-xs text-gray-900 bg-gray-100/50 border border-gray-200 font-bold px-3 py-1 rounded-full">PASO 02 //'
step_2_new_pill = '<span class="font-mono text-xs text-fuchsia-700 bg-fuchsia-100/50 border border-fuchsia-200 font-bold px-3 py-1 rounded-full">PASO 02 //'
html = html.replace(step_2_old_pill, step_2_new_pill)

# Step 2 scanner:
html = html.replace('bg-gray-900 shadow-[0_0_15px_#111827] animate-[scan_3s_ease-in-out_infinite]', 'bg-fuchsia-500 shadow-[0_0_15px_#d946ef] animate-[scan_3s_ease-in-out_infinite]')


# STEP 3: Emerald/Green
step_3_old_bg = '<!-- Step 3 Bubble -->\\n        <div class="bg-gradient-to-br from-white/90 via-white/60 to-white/30 backdrop-blur-3xl border border-white/80 rounded-[3rem] p-10 md:p-16 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center spotlight-card">'
step_3_new_bg = '<!-- Step 3 Bubble -->\\n        <div class="bg-gradient-to-br from-white/90 via-emerald-50/50 to-white/30 backdrop-blur-3xl border border-white/80 rounded-[3rem] p-10 md:p-16 grid grid-cols-1 lg:grid-cols-2 gap-16 items-center spotlight-card">'
html = html.replace(step_3_old_bg, step_3_new_bg)

step_3_old_pill = '<span class="font-mono text-xs text-gray-900 bg-gray-100/50 border border-gray-200 font-bold px-3 py-1 rounded-full">PASO 03 //'
step_3_new_pill = '<span class="font-mono text-xs text-emerald-700 bg-emerald-100/50 border border-emerald-200 font-bold px-3 py-1 rounded-full">PASO 03 //'
html = html.replace(step_3_old_pill, step_3_new_pill)

# Step 3 SVG:
html = html.replace('fill="none" stroke="#111827" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="stroke-dasharray: 200; stroke-dashoffset: 200; animation: dash 4s linear infinite;"', 'fill="none" stroke="#10b981" filter="drop-shadow(0 0 6px rgba(16,185,129,0.5))" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="stroke-dasharray: 200; stroke-dashoffset: 200; animation: dash 4s linear infinite;"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
