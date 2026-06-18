import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update .saas-shadow to Apple Widget style
old_shadow = """    .saas-shadow {
      box-shadow: 0 0 30px rgba(0,0,0,0.06), 0 4px 6px -1px rgba(0,0,0,0.05);
      border: 1px solid rgba(0,0,0,0.04);
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }"""
new_shadow = """    .saas-shadow {
      box-shadow: 0 20px 40px -10px rgba(0,0,0,0.08), 0 0 20px rgba(0,0,0,0.02);
      transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }"""
html = html.replace(old_shadow, new_shadow)

# 2. Update Integrations section
html = html.replace('class="py-12 bg-white border-y border-gray-100 overflow-hidden relative z-20"', 'class="py-12 overflow-hidden relative z-20"')
html = html.replace('from-white', 'from-bgmain') # Fix gradient masks

# 3. Update Stats section
html = html.replace('class="py-16 bg-bgmain relative z-20"', 'class="py-16 relative z-20"')
html = html.replace('bg-white rounded-3xl p-8 saas-shadow border border-gray-100', 'bg-white rounded-[2.5rem] p-8 saas-shadow border-none')

# 4. Update Features section
html = html.replace('class="py-24 bg-white relative z-20"', 'class="py-24 relative z-20"')
html = html.replace('bg-gray-50 rounded-[2.5rem] p-10 flex flex-col justify-between hover:-translate-y-2 transition-transform duration-300 border border-gray-100 saas-shadow', 'bg-white rounded-[2.5rem] p-10 flex flex-col justify-between hover:-translate-y-2 transition-transform duration-300 border-none saas-shadow')
html = html.replace('w-14 h-14 rounded-2xl bg-white saas-shadow flex items-center justify-center mb-8', 'w-14 h-14 rounded-[1.2rem] bg-gray-50 flex items-center justify-center mb-8')

# 5. Update Protocol section
html = html.replace('class="py-24 bg-bgmain border-y border-gray-100 relative z-20"', 'class="py-24 relative z-20"')
html = html.replace('bg-white rounded-[2rem] p-8 saas-shadow border border-gray-100', 'bg-white rounded-[2.5rem] p-8 saas-shadow border-none')

# 6. Update Leaderboard section
html = html.replace('class="py-24 bg-white relative z-20"', 'class="py-24 relative z-20"')
html = html.replace('bg-gray-50 border border-gray-100 rounded-3xl p-8 saas-shadow', 'bg-white border-none rounded-[2.5rem] p-8 saas-shadow')
html = html.replace('bg-white border border-gray-100 rounded-3xl overflow-hidden saas-shadow', 'bg-white border-none rounded-[2rem] overflow-hidden saas-shadow')

# 7. Update Philosophy / Manifesto section
html = html.replace('class="py-32 bg-gray-100 relative z-20 border-b border-gray-200"', 'class="py-32 relative z-20"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
