import re

# 1. Update app.js (Table padding and Marquee for Opportunities)
with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Reduce padding in table cells to prevent horizontal scroll
js = js.replace('td class="p-4', 'td class="px-2 py-3 text-xs')
js = js.replace('td class="p-4 pr-6', 'td class="px-2 py-3 pr-4 text-xs')
js = js.replace('<td class="p-4">', '<td class="px-2 py-3 text-xs">')

# Modify renderOpportunities to create a marquee effect
# The original code just mapped and joined. We will duplicate the array to allow infinite scroll.
old_opp = """elOpp.innerHTML = topOpps.map((p, i) => {
      const isLow = p.comp === 'Baja';
      const badgeBg = isLow ? 'bg-green-100 text-green-700' : 'bg-yellow-100 text-yellow-700';
      const originalIdx = products.indexOf(p);
      return `
        <div class="flex items-center justify-between p-3 border border-gray-100 rounded-xl hover:border-gray-200 hover:bg-gray-50 transition cursor-pointer" onclick="openProduct(${originalIdx})">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center font-bold text-gray-400 text-xs">${i+1}</div>
            <div>
              <div class="font-bold text-sm text-gray-900 truncate max-w-[120px]">${p.name}</div>
              <div class="text-[10px] text-gray-500 font-mono mt-0.5">${p.cat || 'General'}</div>
            </div>
          </div>
          <div class="text-right flex flex-col items-end justify-center">
            <div class="text-xs font-bold text-green-500 bg-green-50 px-2 py-0.5 rounded-md mb-1">${p.margin}% ROI</div>
            <div class="text-[9px] font-bold uppercase tracking-wider text-green-600">COMP ${p.comp}</div>
          </div>
        </div>
      `;
    }).join('');"""

# If the old_opp is not exactly matching, let's just use regex
js = re.sub(r'elOpp\.innerHTML = sorted\.map.*?\)\.join\(\'\'\);', '''
    const cards = sorted.map((p, i) => {
      const isLow = p.comp === 'Baja';
      const originalIdx = products.indexOf(p);
      return `
        <div class="min-w-[280px] flex items-center justify-between p-3 border border-gray-100 rounded-xl hover:border-gray-200 hover:bg-gray-50 transition cursor-pointer flex-shrink-0 bg-white saas-shadow-sm" onclick="openProduct(${originalIdx})">
          <div class="flex items-center gap-3">
            <div class="w-8 h-8 bg-gray-100 rounded-lg flex items-center justify-center font-bold text-gray-400 text-xs">${i+1}</div>
            <div>
              <div class="font-bold text-sm text-gray-900 truncate w-[100px]">${p.name}</div>
              <div class="text-[10px] text-gray-500 font-mono mt-0.5">${p.cat || 'General'}</div>
            </div>
          </div>
          <div class="text-right flex flex-col items-end justify-center">
            <div class="text-xs font-bold text-green-500 bg-green-50 px-2 py-0.5 rounded-md mb-1">${p.margin}% ROI</div>
            <div class="text-[9px] font-bold uppercase tracking-wider text-green-600">COMP ${p.comp}</div>
          </div>
        </div>
      `;
    });
    // Duplicate to make a seamless marquee loop
    elOpp.innerHTML = [...cards, ...cards].join('');
''', js, flags=re.DOTALL)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)

# 2. Update dashboard.html (CSS for Marquee, Table Padding, Eyebrow)
with open('dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add marquee CSS
if '@keyframes marquee-opp' not in html:
    marquee_css = """
    @keyframes marquee-opp {
      0% { transform: translateX(0); }
      100% { transform: translateX(-50%); }
    }
    .animate-marquee-opp {
      display: flex;
      width: max-content;
      animation: marquee-opp 20s linear infinite;
    }
    .animate-marquee-opp:hover {
      animation-play-state: paused;
    }
"""
    html = html.replace('</style>', marquee_css + '\n  </style>')

# Update oppList classes
html = html.replace('id="oppList" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4"', 'id="oppList" class="animate-marquee-opp gap-4"')
# We also need to add a wrapper with overflow-hidden
html = html.replace('<div id="oppList"', '<div class="overflow-hidden w-full relative"><div class="absolute left-0 top-0 bottom-0 w-8 bg-gradient-to-r from-white to-transparent z-10 pointer-events-none"></div><div class="absolute right-0 top-0 bottom-0 w-8 bg-gradient-to-l from-white to-transparent z-10 pointer-events-none"></div><div id="oppList"')
html = html.replace('</div>\n        </div>\n\n        <!-- Products Table -->', '</div></div>\n        </div>\n\n        <!-- Products Table -->')

# Reduce Table Header Padding
html = html.replace('th class="p-4', 'th class="px-2 py-4 text-[10px]')
html = html.replace('th class="p-4 pr-6', 'th class="px-2 py-4 pr-4 text-[10px]')

# Add "Ceja" (Eyebrow) to main cards
# We will target <div class="bg-white rounded-[2rem] p-6 saas-shadow saas-card-hover flex flex-col w-full">
html = re.sub(r'class="bg-white rounded-\[2rem\](.*?)saas-shadow', r'class="bg-white rounded-[2rem]\1saas-shadow border-t-8 border-t-gray-900', html)
# also for the table container
html = html.replace('class="bg-white rounded-[2rem] saas-shadow h-[600px]', 'class="bg-white rounded-[2rem] saas-shadow border-t-8 border-t-gray-900 h-[600px]')
# also for analysis cards
html = re.sub(r'class="bg-white border border-gray-100 rounded-\[2rem\](.*?)saas-shadow', r'class="bg-white border border-gray-100 rounded-[2rem]\1saas-shadow border-t-8 border-t-gray-900', html)

with open('dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("UI updates applied!")
