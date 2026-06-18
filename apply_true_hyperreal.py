import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update CSS for Spotlight Card to have hyper-realistic multi-layered shadows and bevels
old_css = """    .spotlight-card {
      box-shadow: inset 0 2px 4px rgba(255, 255, 255, 0.7), inset 0 -4px 6px rgba(0, 0, 0, 0.03), 0 20px 40px -10px rgba(0, 0, 0, 0.08) !important;
    }
    .spotlight-dark {
      box-shadow: inset 0 2px 4px rgba(255, 255, 255, 0.1), inset 0 -4px 6px rgba(0, 0, 0, 0.4), 0 20px 60px -15px rgba(0, 0, 0, 0.6) !important;
    }"""

new_css = """    .spotlight-card {
      box-shadow: 
        inset 0 1px 1px rgba(255, 255, 255, 0.9), 
        inset 1px 0 1px rgba(255, 255, 255, 0.5), 
        inset 0 -2px 4px rgba(0, 0, 0, 0.05),
        inset -1px 0 2px rgba(0, 0, 0, 0.02),
        0 20px 40px -10px rgba(0, 0, 0, 0.08), 
        0 40px 80px -20px rgba(0, 0, 0, 0.15) !important;
    }
    .spotlight-dark {
      box-shadow: 
        inset 0 1px 1px rgba(255, 255, 255, 0.15), 
        inset 1px 0 1px rgba(255, 255, 255, 0.05), 
        inset 0 -2px 4px rgba(0, 0, 0, 0.4),
        inset -1px 0 2px rgba(0, 0, 0, 0.2),
        0 20px 40px -10px rgba(0, 0, 0, 0.4), 
        0 40px 80px -20px rgba(0, 0, 0, 0.7) !important;
    }"""

if old_css in html:
    html = html.replace(old_css, new_css)
else:
    # Just in case the CSS is different, insert it directly
    html = html.replace('</style>', new_css + '\\n  </style>')

# 2. Add volumetric gradients to all cards without breaking translucency
# Features Cards
html = html.replace('bg-gray-50 rounded-[2.5rem]', 'bg-gradient-to-br from-white via-gray-50 to-gray-100/90 rounded-[3rem]')
# Protocol Bubbles
html = html.replace('bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] rounded-[3rem]', 'bg-gradient-to-br from-white/90 via-white/60 to-white/30 backdrop-blur-3xl border border-white/80 rounded-[3rem]')
# Ecommerce vs Dropshipping
html = html.replace('bg-white/70 backdrop-blur-3xl border border-white/80 p-10 rounded-[3rem]', 'bg-gradient-to-br from-white/90 via-white/60 to-white/30 backdrop-blur-3xl border border-white/80 p-10 rounded-[3rem]')
html = html.replace('bg-white/40 backdrop-blur-3xl border border-white/40 p-10 rounded-[3rem]', 'bg-gradient-to-br from-white/60 via-white/30 to-white/10 backdrop-blur-3xl border border-white/40 p-10 rounded-[3rem]')
# Wall of Love
html = html.replace('bg-white shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] border border-white/80 rounded-[2.5rem]', 'bg-gradient-to-br from-white via-white/90 to-white/70 border border-white/80 rounded-[3rem]')
# Leaderboard cards
html = html.replace('bg-white/80 backdrop-blur-md rounded-3xl', 'bg-gradient-to-br from-white/90 via-white/70 to-white/40 backdrop-blur-xl rounded-[2.5rem]')

# Pricing (Dark Mode)
html = html.replace('bg-[#18181B]/80 backdrop-blur-3xl rounded-[2.5rem]', 'bg-gradient-to-br from-[#2A2A2E]/90 via-[#18181B]/70 to-[#0A0A0C]/50 backdrop-blur-3xl rounded-[3rem]')
html = html.replace('bg-[#1F1F22] rounded-[2.5rem]', 'bg-gradient-to-br from-[#303036] via-[#1F1F22] to-[#141416] rounded-[3rem]')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
