import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

def get_section(start_marker, end_marker):
    start = html.find(start_marker)
    end = html.find(end_marker, start) if end_marker else len(html)
    if start == -1 or end == -1:
        print(f"Failed to extract {start_marker} to {end_marker}")
        return ""
    return html[start:end]

# Extract precisely
nav = html[:html.find('<!-- Hero Section -->')]
hero = get_section('<!-- Hero Section -->', '<!-- Demo Video Section (SaaS Style) -->')
video = get_section('<!-- Demo Video Section (SaaS Style) -->', '<!-- Trust Element: Integration Banner -->')
integrations = get_section('<!-- Trust Element: Integration Banner -->', '<!-- Stats Bar -->')
stats = get_section('<!-- Stats Bar -->', '<!-- Features Section -->')
features = get_section('<!-- Features Section -->', '<!-- Protocol Section -->')
protocol = get_section('<!-- Protocol Section -->', '<!-- Leaderboard Section -->')
leaderboard = get_section('<!-- Leaderboard Section -->', '<!-- NEW ECOMMERCE VS DROPSHIPPING SECTION -->')
ecom = get_section('<!-- NEW ECOMMERCE VS DROPSHIPPING SECTION -->', '<!-- Trust Element: Wall of Love -->')
wall_of_love = get_section('<!-- Trust Element: Wall of Love -->', '<!-- FOUNDER NOTE -->')
founder = get_section('<!-- FOUNDER NOTE -->', '<!-- Manifesto Section (Transition to dark) -->')
manifesto = get_section('<!-- Manifesto Section (Transition to dark) -->', '<!-- Pricing Section (Dark Glassmorphism) -->')
pricing = get_section('<!-- Pricing Section (Dark Glassmorphism) -->', '<!-- FAQ Section -->')
faq = get_section('<!-- FAQ Section -->', '<!-- Footer Section -->')
footer = html[html.find('<!-- Footer Section -->'):]

# Adjust colors and styles based on the new logic
# We want: 
# Hero (White) -> Video (White) -> Gradient (White to Gray) -> Leaderboard (Gray)
# -> Stats (Gray) -> Features (Gray) -> Protocol (Gray) -> Ecom (Gray)
# -> Gradient (Gray to Black)
# -> Wall of Love (Black) -> Founder (Black) -> Integrations (Black) 
# -> Pricing (Black) -> FAQ (Black) -> Manifesto (Black) -> Footer (Black)

# Leaderboard: from Gray to Gray (it was White but we want it Gray now to flow from Video to Leaderboard using gradient)
leaderboard = leaderboard.replace('bg-white relative', 'bg-[#E4E5E9] relative')
leaderboard = leaderboard.replace('border border-gray-100', 'border border-white/80')
leaderboard = leaderboard.replace('bg-white border-none rounded-[2.5rem] p-8 saas-shadow', 'bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] rounded-[2.5rem] p-8')

# Stats: Gray
stats = stats.replace('bg-[#E4E5E9]', 'bg-[#E4E5E9]') # already gray

# Features: Gray
features = features.replace('bg-[#E4E5E9] relative', 'bg-[#E4E5E9] relative')

# Wall of Love: Black with Dark Glass Cards
wall_of_love = wall_of_love.replace('bg-[#E4E5E9]', 'bg-transparent')
wall_of_love = wall_of_love.replace('text-gray-900', 'text-white')
wall_of_love = wall_of_love.replace('text-gray-600', 'text-gray-300')
wall_of_love = wall_of_love.replace('text-gray-500', 'text-gray-400')
wall_of_love = wall_of_love.replace('text-gray-400', 'text-gray-500')
wall_of_love = wall_of_love.replace('bg-white shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] border border-white/80', 'bg-[#141416] shadow-[0_20px_60px_-15px_rgba(0,0,0,0.5)] border border-white/5')

# Founder Note: Black
founder = founder.replace('bg-[#E4E5E9]', 'bg-transparent')
founder = founder.replace('text-gray-900', 'text-white')
founder = founder.replace('text-gray-500', 'text-gray-400')
founder = founder.replace('text-gray-400', 'text-gray-500')
founder = founder.replace('bg-[#141416] border border-white/5 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.5)]', 'bg-[#141416] border border-white/5 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.5)]')

# Integrations: Keep Black
integrations = integrations.replace('bg-[#0A0A0C]', 'bg-transparent')

# Pricing: Ensure it uses transparent bg since it will be in the black container
pricing = pricing.replace('bg-[#0A0A0C]', 'bg-transparent')

# FAQ: Ensure it uses transparent bg
faq = faq.replace('bg-[#E4E5E9]', 'bg-transparent')

# Assemble
new_html = nav + hero + video

# Transition to Gray
new_html += '\\n  <div class="w-full h-48 bg-gradient-to-b from-white to-[#E4E5E9] relative z-20 -mb-1"></div>\\n'

new_html += leaderboard + stats + features + protocol + ecom

# Transition to Black
new_html += '\\n  <div class="w-full h-48 bg-gradient-to-b from-[#E4E5E9] to-[#0A0A0C] relative z-20 -mb-1"></div>\\n'

# Wrap Black Sections
new_html += '<div class="bg-[#0A0A0C] w-full pt-10">\\n'
new_html += wall_of_love + integrations + founder + pricing + faq + manifesto
new_html += '</div>\\n'

new_html += footer

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
