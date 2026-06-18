import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Inject CSS for dot patterns
dot_css = """
    .bg-dot-pattern {
      background-image: radial-gradient(rgba(0, 0, 0, 0.04) 1.5px, transparent 1.5px);
      background-size: 32px 32px;
    }
    .bg-dot-pattern-dark {
      background-image: radial-gradient(rgba(255, 255, 255, 0.04) 1.5px, transparent 1.5px);
      background-size: 32px 32px;
    }
"""

if 'bg-dot-pattern' not in html:
    html = html.replace('</style>', dot_css + '\\n  </style>', 1)

# 2. Add dot pattern to sections
html = html.replace('<section id="features" class="py-32 bg-white relative z-20 overflow-hidden">', '<section id="features" class="py-32 bg-white bg-dot-pattern relative z-20 overflow-hidden">')
html = html.replace('<section id="protocol" class="py-32 bg-[#E4E5E9] relative z-20 overflow-hidden">', '<section id="protocol" class="py-32 bg-[#F8F9FA] bg-dot-pattern relative z-20 overflow-hidden">')
html = html.replace('<section id="leaderboard" class="py-24 bg-white relative z-20 overflow-hidden">', '<section id="leaderboard" class="py-24 bg-white bg-dot-pattern relative z-20 overflow-hidden">')
html = html.replace('<section class="py-32 bg-[#E4E5E9] relative z-20 overflow-hidden">', '<section class="py-32 bg-[#F8F9FA] bg-dot-pattern relative z-20 overflow-hidden">')
html = html.replace('<section id="wall-of-love" class="py-24 bg-[#E4E5E9] relative z-20 overflow-hidden">', '<section id="wall-of-love" class="py-24 bg-[#F8F9FA] bg-dot-pattern relative z-20 overflow-hidden">')
html = html.replace('<section id="pricing" class="bg-[#0A0A0C] w-full py-40 relative overflow-hidden flex flex-col items-center justify-center min-h-screen border-t border-white/5">', '<section id="pricing" class="bg-[#0A0A0C] bg-dot-pattern-dark w-full py-40 relative overflow-hidden flex flex-col items-center justify-center min-h-screen border-t border-white/5">')
html = html.replace('<section id="philosophy" class="py-32 bg-[#0A0A0C] relative z-20 border-t border-white/5">', '<section id="philosophy" class="py-32 bg-[#0A0A0C] bg-dot-pattern-dark relative z-20 border-t border-white/5 overflow-hidden">')
html = html.replace('<section id="faq" class="py-32 bg-[#0A0A0C] relative z-20 overflow-hidden">', '<section id="faq" class="py-32 bg-[#0A0A0C] bg-dot-pattern-dark relative z-20 overflow-hidden">')

# 3. Enhance Aurora colors
html = html.replace('bg-blue-400/20', 'bg-blue-500/30')
html = html.replace('bg-purple-400/10', 'bg-fuchsia-500/20')
html = html.replace('bg-indigo-400/10', 'bg-indigo-500/20')
html = html.replace('bg-rose-400/10', 'bg-rose-500/20')
html = html.replace('bg-blue-300/20', 'bg-cyan-500/25')
html = html.replace('bg-purple-300/15', 'bg-purple-500/25')

# 4. Add huge watermark to empty sections (like Protocol and Dos Caminos)
if 'watermark' not in html:
    protocol_watermark = '<div class="absolute inset-0 flex items-center justify-center pointer-events-none z-0 overflow-hidden"><h2 class="text-[20rem] font-black text-black opacity-[0.02] select-none whitespace-nowrap tracking-tighter">PROTOCOL</h2></div>'
    html = html.replace('<section id="protocol" class="py-32 bg-[#F8F9FA] bg-dot-pattern relative z-20 overflow-hidden">\\n    <div class="max-w-7xl', f'<section id="protocol" class="py-32 bg-[#F8F9FA] bg-dot-pattern relative z-20 overflow-hidden">\\n    {protocol_watermark}\\n    <div class="max-w-7xl')

    caminos_watermark = '<div class="absolute inset-0 flex items-center justify-center pointer-events-none z-0 overflow-hidden"><h2 class="text-[20rem] font-black text-black opacity-[0.02] select-none whitespace-nowrap tracking-tighter">DECISION</h2></div>'
    html = html.replace('<section class="py-32 bg-[#F8F9FA] bg-dot-pattern relative z-20 overflow-hidden">\\n    <div class="max-w-7xl', f'<section class="py-32 bg-[#F8F9FA] bg-dot-pattern relative z-20 overflow-hidden">\\n    {caminos_watermark}\\n    <div class="max-w-7xl')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
