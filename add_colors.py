import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Navbar to Floating Pill
old_nav = """  <!-- Navbar -->
  <nav class="w-full max-w-7xl mx-auto px-6 py-6 flex justify-between items-center relative z-20">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 bg-black rounded-xl flex items-center justify-center saas-shadow">
        <i data-lucide="zap" class="w-5 h-5 text-white"></i>
      </div>
      <span class="text-xl font-extrabold tracking-tight">TrendBase</span>
    </div>
    
    <div class="flex items-center gap-6">
      <a href="#" class="text-sm font-medium text-gray-500 hover:text-black transition">Características</a>
      <a href="#" class="text-sm font-medium text-gray-500 hover:text-black transition">Precios</a>
      <a href="dashboard.html" class="bg-white px-6 py-2.5 rounded-full text-sm font-bold saas-shadow hover:shadow-lg transition">Ingresar</a>
    </div>
  </nav>"""

new_nav = """  <!-- Floating Navbar -->
  <header class="fixed top-6 left-1/2 -translate-x-1/2 w-[95%] max-w-5xl z-50">
    <div class="bg-white/80 backdrop-blur-xl border border-white/50 rounded-full px-6 py-4 flex justify-between items-center saas-shadow">
      <a href="#" class="flex items-center gap-2">
        <div class="w-8 h-8 bg-black rounded-lg flex items-center justify-center">
          <i data-lucide="zap" class="w-4 h-4 text-white"></i>
        </div>
        <span class="font-black text-lg tracking-tight">TrendBase</span>
      </a>
      
      <nav class="hidden md:flex items-center gap-8">
        <a href="#features" class="text-sm font-bold text-gray-500 hover:text-black transition">Características</a>
        <a href="#protocol" class="text-sm font-bold text-gray-500 hover:text-black transition">Protocolo</a>
        <a href="#leaderboard" class="text-sm font-bold text-gray-500 hover:text-black transition">Comunidad</a>
        <a href="#pricing" class="text-sm font-bold text-gray-500 hover:text-black transition">Precios</a>
      </nav>

      <a href="dashboard.html" class="bg-black text-white px-6 py-2.5 rounded-full text-sm font-bold hover:-translate-y-1 transition-transform saas-shadow">Ingresar</a>
    </div>
  </header>"""

html = html.replace(old_nav, new_nav)

# Add padding to main so content is not hidden by fixed header
html = html.replace('<main class="flex-1 flex flex-col items-center justify-center text-center px-6 relative z-20 pb-20">', '<main class="flex-1 flex flex-col items-center justify-center text-center px-6 relative z-20 pt-40 pb-20">')

# 2. Add Pastel colors to Features icons
# Feature 1: Flame (Orange)
html = html.replace('<div class="w-14 h-14 rounded-[1.2rem] bg-gray-50 flex items-center justify-center mb-8">\n              <i data-lucide="flame" class="w-6 h-6 text-black"></i>', 
                    '<div class="w-14 h-14 rounded-[1.2rem] bg-orange-50 flex items-center justify-center mb-8">\n              <i data-lucide="flame" class="w-6 h-6 text-orange-500"></i>')
# Feature 2: Globe (Blue)
html = html.replace('<div class="w-14 h-14 rounded-[1.2rem] bg-gray-50 flex items-center justify-center mb-8">\n              <i data-lucide="globe" class="w-6 h-6 text-black"></i>', 
                    '<div class="w-14 h-14 rounded-[1.2rem] bg-blue-50 flex items-center justify-center mb-8">\n              <i data-lucide="globe" class="w-6 h-6 text-blue-500"></i>')
# Feature 3: Calculator (Purple)
html = html.replace('<div class="w-14 h-14 rounded-[1.2rem] bg-gray-50 flex items-center justify-center mb-8">\n              <i data-lucide="calculator" class="w-6 h-6 text-black"></i>', 
                    '<div class="w-14 h-14 rounded-[1.2rem] bg-purple-50 flex items-center justify-center mb-8">\n              <i data-lucide="calculator" class="w-6 h-6 text-purple-500"></i>')

# 3. Add Pastel colors to Protocol Steps
# Step 1
html = html.replace('<div class="w-16 h-16 rounded-full bg-white border border-gray-200 saas-shadow flex items-center justify-center flex-shrink-0 relative">\n            <span class="font-black text-xl text-gray-900">01</span>',
                    '<div class="w-16 h-16 rounded-full bg-indigo-50 flex items-center justify-center flex-shrink-0 relative saas-shadow">\n            <span class="font-black text-xl text-indigo-600">01</span>')
# Step 2
html = html.replace('<div class="w-16 h-16 rounded-full bg-black border-4 border-gray-100 shadow-xl flex items-center justify-center flex-shrink-0 relative">\n            <span class="font-black text-xl text-white">02</span>',
                    '<div class="w-16 h-16 rounded-full bg-rose-50 flex items-center justify-center flex-shrink-0 relative saas-shadow">\n            <span class="font-black text-xl text-rose-500">02</span>')
# Step 3
html = html.replace('<div class="w-16 h-16 rounded-full bg-white border border-gray-200 saas-shadow flex items-center justify-center flex-shrink-0 relative">\n            <span class="font-black text-xl text-gray-900">03</span>',
                    '<div class="w-16 h-16 rounded-full bg-emerald-50 flex items-center justify-center flex-shrink-0 relative saas-shadow">\n            <span class="font-black text-xl text-emerald-600">03</span>')

# 4. Add Pastel colors to Leaderboard Stats & Badges
html = html.replace('<div class="text-4xl font-extrabold text-gray-900 mb-2">12,450</div>', '<div class="text-4xl font-extrabold text-indigo-500 mb-2">12,450</div>')
html = html.replace('<div class="text-4xl font-extrabold text-gray-900 mb-2">842</div>', '<div class="text-4xl font-extrabold text-rose-500 mb-2">842</div>')
html = html.replace('<div class="text-xl font-black text-gray-900 mt-2 mb-3">Cortador Invisible</div>', '<div class="text-xl font-black text-emerald-500 mt-2 mb-3">Cortador Invisible</div>')

# Fix grey badges in product 3 and 4
html = html.replace('<span class="absolute top-3 right-3 bg-gray-100 text-gray-600 text-[10px] font-bold px-2 py-1 rounded-lg">Score: 98</span>\n            <i data-lucide="image" class="w-8 h-8 text-gray-300"></i>',
                    '<span class="absolute top-3 right-3 bg-emerald-100 text-emerald-700 text-[10px] font-bold px-2 py-1 rounded-lg">Score: 98</span>\n            <i data-lucide="image" class="w-8 h-8 text-emerald-300"></i>', 1)
html = html.replace('<span class="absolute top-3 right-3 bg-gray-100 text-gray-600 text-[10px] font-bold px-2 py-1 rounded-lg">Score: 98</span>\n            <i data-lucide="image" class="w-8 h-8 text-gray-300"></i>',
                    '<span class="absolute top-3 right-3 bg-blue-100 text-blue-700 text-[10px] font-bold px-2 py-1 rounded-lg">Score: 98</span>\n            <i data-lucide="image" class="w-8 h-8 text-blue-300"></i>', 1)

# Also fix the pink icons to match the pink badges
html = html.replace('<i data-lucide="image" class="w-8 h-8 text-gray-300"></i>', '<i data-lucide="image" class="w-8 h-8 text-pink-300"></i>', 2)

# 5. Add Footer Section
footer = """
  <!-- Footer Section -->
  <footer class="bg-[#0A0A0C] text-gray-400 py-12 border-t border-white/10 w-full flex flex-col items-center">
    <div class="max-w-7xl mx-auto px-6 w-full flex flex-col md:flex-row justify-between items-center gap-6">
      <div class="flex items-center gap-2">
        <div class="w-8 h-8 bg-white/10 rounded-lg flex items-center justify-center">
          <i data-lucide="zap" class="w-4 h-4 text-white"></i>
        </div>
        <span class="font-black text-lg tracking-tight text-white">TrendBase</span>
      </div>
      <div class="flex gap-6 text-sm font-medium">
        <a href="#" class="hover:text-white transition">Términos de Servicio</a>
        <a href="#" class="hover:text-white transition">Política de Privacidad</a>
        <a href="#" class="hover:text-white transition">Contacto</a>
      </div>
      <div class="text-sm">
        &copy; 2024 TrendBase. Todos los derechos reservados.
      </div>
    </div>
  </footer>
"""

html = html.replace('</body>', footer + '\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
