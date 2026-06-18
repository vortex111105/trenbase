import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

def get_section(start_marker, end_marker):
    start = html.find(start_marker)
    end = html.find(end_marker, start) if end_marker else len(html)
    if start == -1 or end == -1:
        return ""
    return html[start:end]

# 1. Reorder FAQ and Pricing
manifesto = get_section('<!-- Manifesto Section (Transition to dark) -->', '<!-- Pricing Section (Dark Glassmorphism) -->')
pricing = get_section('<!-- Pricing Section (Dark Glassmorphism) -->', '<!-- FAQ Section -->')
faq = get_section('<!-- FAQ Section -->', '<!-- Footer Section -->')

if manifesto and pricing and faq:
    # Remove them from the HTML temporarily
    html = html.replace(manifesto, '')
    html = html.replace(pricing, '')
    html = html.replace(faq, '')

    # 2. Add Title to Pricing
    pricing_title = """
    <div class="text-center mb-16 relative z-10 w-full">
      <span class="text-[10px] font-bold text-gray-500 uppercase tracking-widest block mb-4">Membresías</span>
      <h2 class="text-4xl md:text-6xl font-black text-white tracking-tight mb-4">Planes diseñados para escalar</h2>
      <p class="text-gray-400 font-medium text-lg max-w-xl mx-auto">Comienza gratis y sube de nivel cuando encuentres tu primer producto ganador.</p>
    </div>
    """
    pricing = pricing.replace('<!-- Toggle -->', pricing_title + '<!-- Toggle -->')

    # Add a premium grid background to pricing
    grid_bg = """
    <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI0MCIgaGVpZ2h0PSI0MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSA0MCAwIEwgMCAwIDAgNDAiIGZpbGw9Im5vbmUiIHN0cm9rZT0icmdiYSgyNTUsIDI1NSwgMjU1LCAwLjAzKSIgc3Ryb2tlLXdpZHRoPSIxIi8+PC9wYXR0ZXJuPjwvZGVmcz48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSJ1cmwoI2dyaWQpIi8+PC9zdmc+')] z-0 pointer-events-none [mask-image:linear-gradient(to_bottom,transparent,black,transparent)]"></div>
    """
    pricing = pricing.replace('<!-- Huge blurred background text -->', grid_bg + '\\n    <!-- Huge blurred background text -->')

    # Put them back in new order: Manifesto -> FAQ -> Pricing
    footer_idx = html.find('<!-- Footer Section -->')
    new_bottom = manifesto + faq + pricing
    html = html[:footer_idx] + new_bottom + html[footer_idx:]

# 3. Add inset shadow (beveled glass effect) to CSS
beveled_css = """
    .spotlight-card {
      box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.4), 0 20px 60px -15px rgba(0,0,0,0.05) !important;
    }
    .spotlight-dark {
      box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1), 0 20px 60px -15px rgba(0,0,0,0.5) !important;
    }
"""
html = html.replace('.spotlight-card {', beveled_css + '\\n    .spotlight-card {')

# 4. Give the features and pricing cards an extra aesthetic touch
# Let's make the Pricing "Standard Plan" more premium by adding an outer glow.
html = html.replace('<!-- Standard Plan (Highlighted) -->', '<!-- Standard Plan (Highlighted) -->\\n        <div class="absolute -inset-0.5 bg-gradient-to-b from-white/20 to-transparent rounded-[3rem] blur opacity-50 z-0"></div>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
