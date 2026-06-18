import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove the bad vertical separators
bad_separator = """
  <!-- Black aesthetic separator -->
  <div class="w-full flex justify-center -mt-8 relative z-30">
    <div class="h-16 w-[1px] bg-gradient-to-b from-transparent via-black to-transparent opacity-30"></div>
    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-3 h-3 bg-black rounded-full shadow-[0_0_15px_rgba(0,0,0,0.2)]"></div>
  </div>
"""
html = html.replace(bad_separator, '')

# 2. Add rounded pill badges to the section subtitles instead to act as beautiful separators
html = html.replace(
    '<span class="text-[10px] font-mono text-gray-400 font-bold uppercase tracking-widest block mb-4">Un Software, Dos Caminos</span>',
    '<div class="inline-block border border-black/10 bg-white/50 backdrop-blur-md rounded-full px-5 py-2 mb-6 shadow-sm"><span class="text-[10px] font-mono text-gray-600 font-bold uppercase tracking-widest">Un Software, Dos Caminos</span></div>'
)

html = html.replace(
    '<span class="text-[10px] font-bold text-gray-500 uppercase tracking-widest block mb-4">Métrica y Precisión</span>',
    '<div class="inline-block border border-black/10 bg-white/50 backdrop-blur-md rounded-full px-5 py-2 mb-6 shadow-sm"><span class="text-[10px] font-bold text-gray-600 uppercase tracking-widest">Métrica y Precisión</span></div>'
)

html = html.replace(
    '<span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest block mb-8">El Manifiesto TrendBase</span>',
    '<div class="inline-block border border-white/10 bg-black/50 backdrop-blur-md rounded-full px-5 py-2 mb-8 shadow-sm"><span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest">El Manifiesto TrendBase</span></div>'
)

html = html.replace(
    '<span class="text-[10px] font-bold text-gray-400 uppercase tracking-widest block mb-4">Comunidad Activa</span>',
    '<div class="inline-block border border-black/10 bg-white/50 backdrop-blur-md rounded-full px-5 py-2 mb-6 shadow-sm"><span class="text-[10px] font-bold text-gray-600 uppercase tracking-widest">Comunidad Activa</span></div>'
)

html = html.replace(
    '<span class="text-[10px] font-bold text-gray-500 uppercase tracking-widest block mb-4">El Protocolo TrendBase</span>',
    '<div class="inline-block border border-black/10 bg-white/50 backdrop-blur-md rounded-full px-5 py-2 mb-6 shadow-sm"><span class="text-[10px] font-bold text-gray-600 uppercase tracking-widest">El Protocolo TrendBase</span></div>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
