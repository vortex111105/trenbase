import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Helper function to extract a section
def get_section(name_start, name_end):
    start = html.find(name_start)
    if name_end:
        end = html.find(name_end, start)
    else:
        end = len(html)
    if start == -1 or (name_end and end == -1):
        print(f"Warning: could not find {name_start} to {name_end}")
        return ""
    return html[start:end]

# Extract all sections
head_to_hero = html[:html.find('<!-- Video Demo Section -->')]
video_demo = get_section('<!-- Video Demo Section -->', '<!-- Trust Element: Integration Banner -->')
integrations = get_section('<!-- Trust Element: Integration Banner -->', '<!-- Stats Bar -->')
stats = get_section('<!-- Stats Bar -->', '<!-- Features Section -->')
features = get_section('<!-- Features Section -->', '<!-- Protocol Section -->')
protocol = get_section('<!-- Protocol Section -->', '<!-- Leaderboard Section -->')
leaderboard = get_section('<!-- Leaderboard Section -->', '<!-- NEW ECOMMERCE VS DROPSHIPPING SECTION -->')
ecom = get_section('<!-- NEW ECOMMERCE VS DROPSHIPPING SECTION -->', '<!-- Trust Element: Wall of Love -->')
wall_of_love = get_section('<!-- Trust Element: Wall of Love -->', '<!-- FOUNDER NOTE -->')
founder = get_section('<!-- FOUNDER NOTE -->', '<!-- FAQ Section -->')
faq = get_section('<!-- FAQ Section -->', '<!-- Manifesto Section')
manifesto = get_section('<!-- Manifesto Section', '<!-- Pricing Section')
pricing = get_section('<!-- Pricing Section', '<!-- Footer Section -->')
footer_onwards = html[html.find('<!-- Footer Section -->'):]

# Modifications

# 1. Stats Bar: move to Gray background and make glass cards
stats = stats.replace('bg-[#0A0A0C]', 'bg-[#E4E5E9]')
stats = stats.replace('bg-[#141416] border border-white/5', 'bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)]')
stats = stats.replace('text-white', 'text-gray-900') # Numbers to dark
# Except the 100% text-green-500, leave it.

# 2. Features: move to Gray background and make glass cards
features = features.replace('bg-white relative', 'bg-[#E4E5E9] relative')
features = features.replace('bg-gray-50', 'bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)]')

# 3. Leaderboard: Ensure it is white
leaderboard = leaderboard.replace('bg-[#E4E5E9]', 'bg-white')
leaderboard = leaderboard.replace('border border-white/80', 'border border-gray-100')

# 4. Wall of Love: Keep gray background
wall_of_love = wall_of_love.replace('bg-[#E4E5E9]', 'bg-transparent') # We will put it in a gradient wrapper if needed, or just keep bg-[#E4E5E9]

# 5. Integrations: keep Black

# 6. Founder Note: Black background, dark glass card
founder = founder.replace('bg-[#E4E5E9]', 'bg-transparent')
founder = founder.replace('text-gray-900', 'text-white')
founder = founder.replace('text-gray-500', 'text-gray-400')
founder = founder.replace('text-gray-400', 'text-gray-500')
founder = founder.replace('bg-white saas-shadow', 'bg-[#141416] border border-white/10 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.5)]')
founder = founder.replace('bg-gray-200', 'bg-[#262626]')

# 7. Pricing: Ensure Black background
pricing = pricing.replace('bg-ivory', 'bg-[#0A0A0C]')
pricing = pricing.replace('text-obsidian', 'text-white')
pricing = pricing.replace('bg-white border border-slate/10', 'bg-[#141416] border border-white/5')
pricing = pricing.replace('text-slate/40', 'text-gray-500')
pricing = pricing.replace('text-slate/60', 'text-gray-400')
pricing = pricing.replace('text-slate/80', 'text-gray-300')
pricing = pricing.replace('bg-obsidian hover:bg-slate text-gray-900', 'bg-white text-black hover:bg-gray-200')

# 8. FAQ: Black background, dark glass cards
faq = faq.replace('bg-[#E4E5E9]', 'bg-transparent')
faq = faq.replace('text-gray-900', 'text-white')
faq = faq.replace('text-gray-500', 'text-gray-400')
faq = faq.replace('bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)]', 'bg-[#141416] border border-white/5 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.5)]')
faq = faq.replace('hover:bg-white/90', 'hover:bg-[#1C1C1E]')

# Assembly with Gradient Spacers
new_html = head_to_hero + video_demo + leaderboard

# Transition: White to Gray
new_html += '\\n  <div class="w-full h-32 bg-gradient-to-b from-white to-[#E4E5E9]"></div>\\n'

new_html += stats + features + protocol + ecom + wall_of_love

# Transition: Gray to Black
new_html += '\\n  <div class="w-full h-48 bg-gradient-to-b from-[#E4E5E9] to-[#0A0A0C]"></div>\\n'

# Wrap Black sections in a black container so background is solid
new_html += '<div class="bg-[#0A0A0C] w-full pb-20">\\n'
new_html += integrations + founder + pricing + faq + manifesto 
new_html += '</div>\\n'

# Fix the Integrations which currently has a py-12 class
new_html = new_html.replace('class="py-12 bg-[#0A0A0C] overflow-hidden relative z-20"', 'class="py-12 bg-transparent overflow-hidden relative z-20"')

new_html += footer_onwards

# Write back
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)
