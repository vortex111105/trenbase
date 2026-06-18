import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Darken the background of specific sections to make glass pop
# Replace bg-[#F4F5F8] with bg-[#E4E5E9]
html = html.replace('bg-[#F4F5F8]', 'bg-[#E4E5E9]')

# 2. Upgrade the Glass effect (more blur, more shadow)
old_glass = 'bg-white/60 backdrop-blur-2xl border border-white saas-shadow'
new_glass = 'bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)]'
html = html.replace(old_glass, new_glass)

# Upgrade for the Dropshipping vs Ecommerce cards
old_glass_xl = 'bg-white/60 backdrop-blur-xl border border-white saas-shadow'
html = html.replace(old_glass_xl, new_glass)

# Upgrade for Wall of Love (they were pure bg-white, let's make them glass too if we want, or keep pure white. Let's keep pure white but add the premium shadow)
old_white_card = 'bg-white saas-shadow border-none rounded-[2.5rem]'
new_white_card = 'bg-white shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] border border-white/80 rounded-[2.5rem]'
html = html.replace(old_white_card, new_white_card)

# 3. Replace bright colors in Protocol with Premium Neutrals
# Step 1: Indigo to Slate/Graphite
html = html.replace('text-indigo-500 bg-indigo-50', 'text-gray-900 bg-gray-100/50 border border-gray-200')
html = html.replace('stroke="#6366F1"', 'stroke="#111827"')

# Step 2: Rose to Slate/Graphite
html = html.replace('text-rose-500 bg-rose-50', 'text-gray-900 bg-gray-100/50 border border-gray-200')
html = html.replace('bg-rose-50 rounded', 'bg-gray-100 rounded')
html = html.replace('bg-rose-100 rounded', 'bg-gray-200 rounded')
html = html.replace('bg-rose-200 rounded', 'bg-gray-300 rounded')
html = html.replace('bg-rose-500 shadow-[0_0_15px_#F43F5E]', 'bg-gray-900 shadow-[0_0_15px_#111827]')
html = html.replace('border-rose-100', 'border-gray-200')

# Step 3: Emerald to Slate/Graphite
html = html.replace('text-emerald-500 bg-emerald-50', 'text-gray-900 bg-gray-100/50 border border-gray-200')
html = html.replace('stroke="#10B981"', 'stroke="#111827"')

# Remove colored icons from Dropshipping vs Ecommerce (Indigo, Rose, etc.)
html = html.replace('text-indigo-500', 'text-gray-900')
html = html.replace('from-indigo-50', 'from-gray-100')
html = html.replace('bg-indigo-50/50 border-indigo-100/50', 'bg-gray-50/50 border-gray-100')

html = html.replace('text-rose-500', 'text-gray-900')
html = html.replace('from-rose-50', 'from-gray-100')
html = html.replace('bg-rose-50/50 border-rose-100/50', 'bg-gray-50/50 border-gray-100')


# 4. Inject FAQ Section just before Footer
footer_start = html.find('<!-- Footer Section -->')

faq_section = """
  <!-- FAQ Section -->
  <section id="faq" class="py-32 bg-[#E4E5E9] relative z-20">
    <div class="max-w-3xl mx-auto px-6">
      <div class="text-center mb-16">
        <span class="text-[10px] font-mono text-gray-500 font-bold uppercase tracking-widest block mb-4">Dudas Comunes</span>
        <h2 class="text-3xl md:text-5xl font-black tracking-tight text-gray-900">Preguntas Frecuentes</h2>
      </div>
      
      <div class="space-y-4">
        <details class="group bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] rounded-3xl p-6 md:p-8 cursor-pointer hover:bg-white/90 transition duration-300">
          <summary class="flex justify-between items-center font-bold text-gray-900 text-lg list-none">
            ¿Necesito experiencia previa en Dropshipping?
            <span class="transition group-open:rotate-180">
              <i data-lucide="chevron-down" class="w-5 h-5 text-gray-400"></i>
            </span>
          </summary>
          <p class="text-gray-500 font-medium mt-4 leading-relaxed text-sm">
            No. TrendBase te da los datos digeridos (ventas, competidores, precios) para que cualquier persona pueda tomar decisiones basadas en datos reales, sin necesidad de ser un experto en análisis.
          </p>
        </details>
        
        <details class="group bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] rounded-3xl p-6 md:p-8 cursor-pointer hover:bg-white/90 transition duration-300">
          <summary class="flex justify-between items-center font-bold text-gray-900 text-lg list-none">
            ¿Es fácil cancelar mi suscripción?
            <span class="transition group-open:rotate-180">
              <i data-lucide="chevron-down" class="w-5 h-5 text-gray-400"></i>
            </span>
          </summary>
          <p class="text-gray-500 font-medium mt-4 leading-relaxed text-sm">
            Sí, completamente. Desde tu panel de control puedes cancelar con un solo clic. Sin correos, sin llamadas y sin preguntas.
          </p>
        </details>

        <details class="group bg-white/70 backdrop-blur-3xl border border-white/80 shadow-[0_20px_60px_-15px_rgba(0,0,0,0.05)] rounded-3xl p-6 md:p-8 cursor-pointer hover:bg-white/90 transition duration-300">
          <summary class="flex justify-between items-center font-bold text-gray-900 text-lg list-none">
            ¿De dónde sacan los datos?
            <span class="transition group-open:rotate-180">
              <i data-lucide="chevron-down" class="w-5 h-5 text-gray-400"></i>
            </span>
          </summary>
          <p class="text-gray-500 font-medium mt-4 leading-relaxed text-sm">
            Nuestro motor escanea múltiples fuentes, proveedores y tiendas en tiempo real en toda Latinoamérica, estructurando y validando miles de transacciones diarias.
          </p>
        </details>
      </div>
    </div>
  </section>
"""

html = html[:footer_start] + faq_section + html[footer_start:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
