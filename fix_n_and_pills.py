import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Clean up literal '\\n' characters causing the weird bars
html = html.replace('\\n', '\n')

# 2. Upgrade the pill badges to look "3D y realista" (Ultra-premium 3D glass pill)
premium_pill_classes = "inline-block border border-white/40 bg-white/40 backdrop-blur-xl rounded-full px-5 py-2 mb-8 shadow-[0_10px_20px_-10px_rgba(0,0,0,0.1),inset_0_2px_4px_rgba(255,255,255,0.8),inset_0_-2px_4px_rgba(0,0,0,0.05)] transform hover:scale-105 transition-all"
premium_pill_dark = "inline-block border border-white/10 bg-[#18181B]/80 backdrop-blur-xl rounded-full px-5 py-2 mb-8 shadow-[0_10px_20px_-10px_rgba(0,0,0,0.5),inset_0_2px_4px_rgba(255,255,255,0.1),inset_0_-2px_4px_rgba(0,0,0,0.4)] transform hover:scale-105 transition-all"

html = html.replace(
    '<div class="inline-block border border-black/10 bg-white/50 backdrop-blur-md rounded-full px-5 py-2 mb-6 shadow-sm"><span class="text-[10px] font-mono text-gray-600 font-bold uppercase tracking-widest">Un Software, Dos Caminos</span></div>',
    f'<div class="{premium_pill_classes}"><span class="text-[10px] font-mono text-gray-800 font-extrabold uppercase tracking-widest flex items-center gap-2"><i data-lucide="git-branch" class="w-3 h-3"></i> Un Software, Dos Caminos</span></div>'
)

html = html.replace(
    '<div class="inline-block border border-black/10 bg-white/50 backdrop-blur-md rounded-full px-5 py-2 mb-6 shadow-sm"><span class="text-[10px] font-bold text-gray-600 uppercase tracking-widest">Métrica y Precisión</span></div>',
    f'<div class="{premium_pill_classes}"><span class="text-[10px] font-bold text-gray-800 font-extrabold uppercase tracking-widest flex items-center gap-2"><i data-lucide="crosshair" class="w-3 h-3"></i> Métrica y Precisión</span></div>'
)

html = html.replace(
    '<div class="inline-block border border-white/10 bg-black/50 backdrop-blur-md rounded-full px-5 py-2 mb-8 shadow-sm"><span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">El Manifiesto TrendBase</span></div>',
    f'<div class="{premium_pill_dark}"><span class="text-[10px] font-bold text-gray-300 font-extrabold uppercase tracking-widest flex items-center gap-2"><i data-lucide="scroll-text" class="w-3 h-3"></i> El Manifiesto TrendBase</span></div>'
)

html = html.replace(
    '<div class="inline-block border border-black/10 bg-white/50 backdrop-blur-md rounded-full px-5 py-2 mb-6 shadow-sm"><span class="text-[10px] font-bold text-gray-600 uppercase tracking-widest">Comunidad Activa</span></div>',
    f'<div class="{premium_pill_classes}"><span class="text-[10px] font-bold text-gray-800 font-extrabold uppercase tracking-widest flex items-center gap-2"><i data-lucide="users" class="w-3 h-3"></i> Comunidad Activa</span></div>'
)

html = html.replace(
    '<div class="inline-block border border-black/10 bg-white/50 backdrop-blur-md rounded-full px-5 py-2 mb-6 shadow-sm"><span class="text-[10px] font-bold text-gray-600 uppercase tracking-widest">El Protocolo TrendBase</span></div>',
    f'<div class="{premium_pill_classes}"><span class="text-[10px] font-bold text-gray-800 font-extrabold uppercase tracking-widest flex items-center gap-2"><i data-lucide="cpu" class="w-3 h-3"></i> El Protocolo TrendBase</span></div>'
)

# And the title in pricing:
html = html.replace(
    '<span class="text-[10px] font-bold text-gray-500 uppercase tracking-widest block mb-4">Membresías</span>',
    f'<div class="{premium_pill_dark}"><span class="text-[10px] font-bold text-gray-300 font-extrabold uppercase tracking-widest flex items-center gap-2"><i data-lucide="credit-card" class="w-3 h-3"></i> Membresías</span></div>'
)

# Replace any lingering <div class="text-center mb-16 relative z-10 w-full"> span tags that I missed
# Just in case

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
