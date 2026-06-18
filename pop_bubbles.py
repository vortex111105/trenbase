import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update CSS for stronger shadows (pop effect) and add dot patterns
css_to_add = """
    .bg-dot-pattern {
      background-image: radial-gradient(rgba(0, 0, 0, 0.05) 1.5px, transparent 1.5px);
      background-size: 32px 32px;
    }
    .bg-dot-pattern-dark {
      background-image: radial-gradient(rgba(255, 255, 255, 0.04) 1.5px, transparent 1.5px);
      background-size: 32px 32px;
    }
"""

if 'bg-dot-pattern' not in html:
    html = html.replace('</style>', css_to_add + '\\n  </style>', 1)

# Enhance spotlight-card shadows
old_shadow = "0 20px 40px -10px rgba(0, 0, 0, 0.08),"
new_shadow = "0 20px 40px -10px rgba(0, 0, 0, 0.2),"
html = html.replace(old_shadow, new_shadow)

old_shadow2 = "0 40px 80px -20px rgba(0, 0, 0, 0.15) !important;"
new_shadow2 = "0 40px 80px -20px rgba(0, 0, 0, 0.3) !important;"
html = html.replace(old_shadow2, new_shadow2)

# 2. Darken backgrounds slightly to make the white bubbles pop
html = html.replace('<section id="features" class="py-32 bg-white relative z-20 overflow-hidden">', '<section id="features" class="py-32 bg-[#F3F4F6] bg-dot-pattern relative z-20 overflow-hidden">')
html = html.replace('<section id="protocol" class="py-32 bg-[#E4E5E9] relative z-20 overflow-hidden">', '<section id="protocol" class="py-32 bg-[#E5E7EB] bg-dot-pattern relative z-20 overflow-hidden">')
html = html.replace('<section id="leaderboard" class="py-24 bg-white relative z-20 overflow-hidden">', '<section id="leaderboard" class="py-24 bg-[#F3F4F6] bg-dot-pattern relative z-20 overflow-hidden">')
html = html.replace('<section class="py-32 bg-[#E4E5E9] relative z-20 overflow-hidden">', '<section class="py-32 bg-[#E5E7EB] bg-dot-pattern relative z-20 overflow-hidden">')
html = html.replace('<section id="wall-of-love" class="py-24 bg-[#E4E5E9] relative z-20 overflow-hidden">', '<section id="wall-of-love" class="py-24 bg-[#E5E7EB] bg-dot-pattern relative z-20 overflow-hidden">')

html = html.replace('<section id="pricing" class="bg-[#0A0A0C] w-full py-40 relative overflow-hidden flex flex-col items-center justify-center min-h-screen border-t border-white/5">', '<section id="pricing" class="bg-[#0A0A0C] bg-dot-pattern-dark w-full py-40 relative overflow-hidden flex flex-col items-center justify-center min-h-screen border-t border-white/5">')
html = html.replace('<section id="philosophy" class="py-32 bg-[#0A0A0C] relative z-20 border-t border-white/5">', '<section id="philosophy" class="py-32 bg-[#0A0A0C] bg-dot-pattern-dark relative z-20 border-t border-white/5 overflow-hidden">')
html = html.replace('<section id="faq" class="py-32 bg-[#0A0A0C] relative z-20 overflow-hidden">', '<section id="faq" class="py-32 bg-[#0A0A0C] bg-dot-pattern-dark relative z-20 overflow-hidden">')


# 3. Add huge watermark texts
if 'watermark' not in html:
    protocol_watermark = '<div class="absolute inset-0 flex items-center justify-center pointer-events-none z-0 overflow-hidden"><h2 class="text-[20rem] font-black text-black opacity-[0.03] select-none whitespace-nowrap tracking-tighter">PROTOCOL</h2></div>'
    html = html.replace('<section id="protocol" class="py-32 bg-[#E5E7EB] bg-dot-pattern relative z-20 overflow-hidden">\\n    <div class="max-w-7xl', f'<section id="protocol" class="py-32 bg-[#E5E7EB] bg-dot-pattern relative z-20 overflow-hidden">\\n    {protocol_watermark}\\n    <div class="max-w-7xl')

    caminos_watermark = '<div class="absolute inset-0 flex items-center justify-center pointer-events-none z-0 overflow-hidden"><h2 class="text-[20rem] font-black text-black opacity-[0.03] select-none whitespace-nowrap tracking-tighter">DECISION</h2></div>'
    html = html.replace('<section class="py-32 bg-[#E5E7EB] bg-dot-pattern relative z-20 overflow-hidden">\\n    <div class="max-w-7xl', f'<section class="py-32 bg-[#E5E7EB] bg-dot-pattern relative z-20 overflow-hidden">\\n    {caminos_watermark}\\n    <div class="max-w-7xl')

# 4. Enhance Auroras heavily
# Find absolute divs with bg-[color]-400/10 or similar and make them HUGE and colorful
html = re.sub(r'bg-blue-[34]00/[0-9]+', 'bg-cyan-500/40 w-[800px] h-[800px] blur-[100px]', html)
html = re.sub(r'bg-purple-[34]00/[0-9]+', 'bg-fuchsia-500/40 w-[800px] h-[800px] blur-[100px]', html)
html = re.sub(r'bg-indigo-[34]00/[0-9]+', 'bg-violet-500/40 w-[800px] h-[800px] blur-[100px]', html)
html = re.sub(r'bg-rose-[34]00/[0-9]+', 'bg-rose-500/40 w-[800px] h-[800px] blur-[100px]', html)

# Fix duplicate width/height/blur if the regex appended it to existing
html = re.sub(r'w-\[40%\] h-\[40%\] bg-([a-z]+-500/40) w-\[800px\] h-\[800px\] blur-\[100px\] rounded-full blur-\[150px\]', r'\1 w-[800px] h-[800px] rounded-full blur-[100px]', html)
html = re.sub(r'w-\[30%\] h-\[30%\] bg-([a-z]+-500/40) w-\[800px\] h-\[800px\] blur-\[100px\] rounded-full blur-\[120px\]', r'\1 w-[800px] h-[800px] rounded-full blur-[100px]', html)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
