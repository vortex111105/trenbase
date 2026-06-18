import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add Social Proof under the hero buttons
social_proof_html = """    <div class="mt-10 flex flex-col sm:flex-row gap-4 items-center">
      <a href="dashboard.html" class="btn-3d px-10 py-4 rounded-full font-extrabold text-lg flex items-center gap-3 transition">
        Entrar al Dashboard <i data-lucide="arrow-right" class="w-5 h-5"></i>
      </a>
      <a href="#demo" class="px-10 py-4 rounded-full text-lg font-bold text-gray-600 hover:text-black transition flex items-center gap-2">
        <i data-lucide="play-circle" class="w-5 h-5"></i> Ver Demo
      </a>
    </div>

    <!-- Social Proof (Info agregada) -->
    <div class="mt-8 flex flex-col items-center sm:flex-row gap-4 opacity-0 animate-[fadeIn_1s_ease-out_1s_forwards]">
      <div class="flex -space-x-3">
        <img class="w-10 h-10 rounded-full border-2 border-white shadow-md" src="https://i.pravatar.cc/100?img=11" alt="User">
        <img class="w-10 h-10 rounded-full border-2 border-white shadow-md" src="https://i.pravatar.cc/100?img=32" alt="User">
        <img class="w-10 h-10 rounded-full border-2 border-white shadow-md" src="https://i.pravatar.cc/100?img=33" alt="User">
        <img class="w-10 h-10 rounded-full border-2 border-white shadow-md" src="https://i.pravatar.cc/100?img=44" alt="User">
        <div class="w-10 h-10 rounded-full border-2 border-white shadow-md bg-gray-900 flex items-center justify-center text-[10px] text-white font-bold tracking-tighter">+2k</div>
      </div>
      <div class="text-sm text-gray-500 font-medium text-left leading-tight">
        Respaldado por <span class="font-bold text-gray-900">+2,450 dropshippers</span><br>
        <div class="flex items-center gap-1 text-yellow-500 mt-1">
          <i data-lucide="star" class="w-3 h-3 fill-current"></i>
          <i data-lucide="star" class="w-3 h-3 fill-current"></i>
          <i data-lucide="star" class="w-3 h-3 fill-current"></i>
          <i data-lucide="star" class="w-3 h-3 fill-current"></i>
          <i data-lucide="star" class="w-3 h-3 fill-current"></i>
          <span class="text-gray-400 text-xs ml-1">(4.9/5)</span>
        </div>
      </div>
    </div>
"""

# Find the buttons block and replace it to inject the social proof
old_buttons = """    <div class="mt-10 flex flex-col sm:flex-row gap-4 items-center">
      <a href="dashboard.html" class="btn-3d px-10 py-4 rounded-full font-extrabold text-lg flex items-center gap-3 transition">
        Entrar al Dashboard <i data-lucide="arrow-right" class="w-5 h-5"></i>
      </a>
      <a href="#demo" class="px-8 py-4 rounded-full text-lg font-bold text-gray-600 hover:text-black transition">
        Ver Demo
      </a>
    </div>"""

if old_buttons in html:
    html = html.replace(old_buttons, social_proof_html)
else:
    # Try a more fuzzy replace in case the button code changed slightly
    pattern = re.compile(r'<div class="mt-10 flex flex-col sm:flex-row gap-4 items-center">.*?Ver Demo\s*</a>\s*</div>', re.DOTALL)
    html = pattern.sub(social_proof_html, html)


# Add CSS for fadeIn animation if not present
fade_in_css = """
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
"""
if 'keyframes fadeIn' not in html:
    html = html.replace('</style>', fade_in_css + '\\n  </style>', 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
