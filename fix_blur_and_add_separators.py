import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove aggressive blur and opacity from the Two Paths cards
html = html.replace('group-hover/paths:[&:not(:hover)]:opacity-30 group-hover/paths:[&:not(:hover)]:blur-[4px]', 'group-hover/paths:[&:not(:hover)]:opacity-70')

# 2. Add black separators between major white sections to break up the distance.
# The user wants "detalles en negro como separadores"
separator_html = """
  <!-- Black aesthetic separator -->
  <div class="w-full flex justify-center -mt-8 relative z-30">
    <div class="h-16 w-[1px] bg-gradient-to-b from-transparent via-black to-transparent opacity-30"></div>
    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-3 h-3 bg-black rounded-full shadow-[0_0_15px_rgba(0,0,0,0.2)]"></div>
  </div>
"""

# Let's insert separators between major light sections
# Features -> Protocol
if '<!-- Protocol Section -->' in html:
    html = html.replace('<!-- Protocol Section -->', separator_html + '\\n<!-- Protocol Section -->')

# Protocol -> Leaderboard
if '<!-- Leaderboard Section -->' in html:
    html = html.replace('<!-- Leaderboard Section -->', separator_html + '\\n<!-- Leaderboard Section -->')

# Leaderboard -> Ecommerce vs Dropshipping
if '<!-- NEW ECOMMERCE VS DROPSHIPPING SECTION -->' in html:
    html = html.replace('<!-- NEW ECOMMERCE VS DROPSHIPPING SECTION -->', separator_html + '\\n<!-- NEW ECOMMERCE VS DROPSHIPPING SECTION -->')

# Ecommerce -> Wall of Love
if '<!-- Trust Element: Wall of Love -->' in html:
    html = html.replace('<!-- Trust Element: Wall of Love -->', separator_html + '\\n<!-- Trust Element: Wall of Love -->')


with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
