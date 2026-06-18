import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Helper to inject content right after a matched class string
def inject_aurora(html, search_str, aurora_html):
    return html.replace(search_str, search_str + '\\n    ' + aurora_html)

# 1. Features Section (Light Aurora)
aurora_features = '<div class="absolute top-[-10%] right-[-5%] w-[500px] h-[500px] bg-blue-400/20 rounded-full blur-[120px] pointer-events-none z-0"></div><div class="absolute bottom-[-10%] left-[-5%] w-[600px] h-[600px] bg-purple-400/10 rounded-full blur-[120px] pointer-events-none z-0"></div>'
html = html.replace('<section id="features" class="py-32 bg-white relative z-20">', '<section id="features" class="py-32 bg-white relative z-20 overflow-hidden">')
html = inject_aurora(html, '<section id="features" class="py-32 bg-white relative z-20 overflow-hidden">\\n    <div class="max-w-7xl mx-auto px-6 md:px-12">', aurora_features)

# 2. Protocol Section (Light Aurora)
aurora_protocol = '<div class="absolute top-[20%] left-[20%] w-[800px] h-[800px] bg-indigo-400/10 rounded-full blur-[150px] pointer-events-none z-0"></div>'
html = html.replace('<section id="protocol" class="py-32 bg-[#E4E5E9] relative z-20">', '<section id="protocol" class="py-32 bg-[#E4E5E9] relative z-20 overflow-hidden">')
html = inject_aurora(html, '<section id="protocol" class="py-32 bg-[#E4E5E9] relative z-20 overflow-hidden">\\n    <div class="max-w-7xl mx-auto px-6 md:px-12">', aurora_protocol)

# 3. Leaderboard Section (Light Aurora)
aurora_leaderboard = '<div class="absolute bottom-0 right-0 w-[600px] h-[600px] bg-rose-400/10 rounded-full blur-[120px] pointer-events-none z-0"></div>'
html = html.replace('<section id="leaderboard" class="py-24 bg-white relative z-20">', '<section id="leaderboard" class="py-24 bg-white relative z-20 overflow-hidden">')
html = inject_aurora(html, '<section id="leaderboard" class="py-24 bg-white relative z-20 overflow-hidden">\\n    <div class="max-w-7xl mx-auto px-6 md:px-12">', aurora_leaderboard)

# 4. Ecommerce vs Dropshipping (Already has overflow-hidden)
aurora_ecom = '<div class="absolute top-[10%] left-[-10%] w-[500px] h-[500px] bg-blue-300/20 rounded-full blur-[120px] pointer-events-none z-0"></div>'
html = inject_aurora(html, '<section class="py-32 bg-[#E4E5E9] relative z-20 overflow-hidden">\\n    <div class="max-w-7xl mx-auto px-6 md:px-12">', aurora_ecom)

# 5. Wall of Love (Light Aurora)
aurora_wall = '<div class="absolute top-[30%] right-[10%] w-[700px] h-[700px] bg-purple-300/15 rounded-full blur-[150px] pointer-events-none z-0"></div>'
html = html.replace('<section id="wall-of-love" class="py-24 bg-[#E4E5E9] relative z-20">', '<section id="wall-of-love" class="py-24 bg-[#E4E5E9] relative z-20 overflow-hidden">')
html = inject_aurora(html, '<section id="wall-of-love" class="py-24 bg-[#E4E5E9] relative z-20 overflow-hidden">\\n    <div class="max-w-7xl mx-auto px-6">', aurora_wall)

# 6. Pricing Section (Dark Aurora)
aurora_pricing = '<div class="absolute top-[10%] left-[20%] w-[1000px] h-[1000px] bg-indigo-900/30 rounded-full blur-[200px] pointer-events-none z-0"></div>'
html = html.replace('<section id="pricing" class="py-32 bg-[#0A0A0C] text-slate relative z-20">', '<section id="pricing" class="py-32 bg-[#0A0A0C] text-slate relative z-20 overflow-hidden">')
html = inject_aurora(html, '<section id="pricing" class="py-32 bg-[#0A0A0C] text-slate relative z-20 overflow-hidden">\\n    <div class="max-w-6xl mx-auto px-6">', aurora_pricing)

# 7. FAQ Section (Dark Aurora)
aurora_faq = '<div class="absolute bottom-[-10%] right-[-10%] w-[800px] h-[800px] bg-violet-900/20 rounded-full blur-[150px] pointer-events-none z-0"></div>'
html = html.replace('<section id="faq" class="py-32 bg-[#0A0A0C] relative z-20">', '<section id="faq" class="py-32 bg-[#0A0A0C] relative z-20 overflow-hidden">')
html = inject_aurora(html, '<section id="faq" class="py-32 bg-[#0A0A0C] relative z-20 overflow-hidden">\\n    <div class="max-w-3xl mx-auto px-6">', aurora_faq)


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
