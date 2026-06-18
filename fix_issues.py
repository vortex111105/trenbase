import re
import os

def fix_all_issues():
    with open('/Users/nachofrag/Downloads/trenbase_repo/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Fix neon badges (remove background, border, padding, radius, just text color and subtle shadow)
    # The user complained about neon colors being oversaturated and ugly.
    # In apply_smooth_theme.py we injected:
    old_green_css = r"""\.neon-badge-green\s*\{\s*background:\s*rgba\(52,\s*199,\s*89,\s*0\.15\);\s*color:\s*#55E079;\s*border:\s*1px solid rgba\(52,\s*199,\s*89,\s*0\.3\);\s*padding:\s*2px 8px;\s*border-radius:\s*12px;\s*box-shadow:\s*0 0 10px rgba\(52,\s*199,\s*89,\s*0\.2\);\s*\}"""
    
    new_green_css = """.neon-badge-green {
      color: #34d399; /* Tailwind green-400 */
    }"""
    
    html = re.sub(old_green_css, new_green_css, html, flags=re.MULTILINE|re.DOTALL)

    old_red_css = r"""\.neon-badge-red\s*\{\s*background:\s*rgba\(255,\s*59,\s*48,\s*0\.15\);\s*color:\s*#FF6B60;\s*border:\s*1px solid rgba\(255,\s*59,\s*48,\s*0\.3\);\s*padding:\s*2px 8px;\s*border-radius:\s*12px;\s*box-shadow:\s*0 0 10px rgba\(255,\s*59,\s*48,\s*0\.2\);\s*\}"""
    new_red_css = """.neon-badge-red {
      color: #f87171; /* Tailwind red-400 */
    }"""
    
    html = re.sub(old_red_css, new_red_css, html, flags=re.MULTILINE|re.DOTALL)
    
    # 2. Add 'Mascotas' to the categories sidebar
    # Find where categories are listed and inject Mascotas
    if "sb-cat-mascotas" not in html:
        cat_html = """<button onclick="filterCat('Tecnología')" id="sb-cat-tecnologia" class="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium text-white/60 hover:text-white hover:bg-white/5 transition"><i data-lucide="laptop" class="w-3.5 h-3.5"></i> Tecnología</button>
            <button onclick="filterCat('Mascotas')" id="sb-cat-mascotas" class="w-full flex items-center gap-3 px-3 py-2 rounded-xl text-xs font-medium text-white/60 hover:text-white hover:bg-white/5 transition"><i data-lucide="paw-print" class="w-3.5 h-3.5"></i> Mascotas</button>"""
        
        html = re.sub(
            r'<button onclick="filterCat\(\'Tecnología\'\)" id="sb-cat-tecnologia"[^>]+>.*?Tecnología</button>',
            cat_html,
            html,
            flags=re.MULTILINE|re.DOTALL
        )

    # 3. Multiply mock data so the user sees more than 10 products
    # We will expand the products list from 6 to 24 by duplicating and tweaking names a bit.
    if "mockData =" in html and "Rascador para Gatos" not in html:
        new_products = """[
          { name: "Cama Relajante para Mascotas", cat: "Mascotas", score: 98, change: "up", change_num: 25.4, margin: 65, price_min: 35, price_str: "$35 - $50", hot: true, comp: "Baja", plts: ["TikTok", "Facebook"], regions: ["MX", "CO", "AR"], history: [40, 55, 70, 98], rank: 1, suppliers: [{name:"AliExpress", price: 12}] },
          { name: "Cepillo Quita Pelos Mágico", cat: "Mascotas", score: 95, change: "up", change_num: 18.2, margin: 70, price_min: 25, price_str: "$25 - $30", hot: true, comp: "Media", plts: ["TikTok", "Instagram"], regions: ["BR", "CO"], history: [30, 60, 80, 95], rank: 2, suppliers: [{name:"AliExpress", price: 6}] },
          { name: "Proyector Galaxia Inteligente", cat: "Tecnología", score: 92, change: "up", change_num: 12.5, margin: 55, price_min: 45, price_str: "$45 - $60", hot: false, comp: "Alta", plts: ["TikTok", "Amazon"], regions: ["US", "MX"], history: [80, 85, 90, 92], rank: 3, suppliers: [{name:"AliExpress", price: 18}] },
          { name: "Rizador de Pelo Automático", cat: "Belleza", score: 88, change: "up", change_num: 8.4, margin: 60, price_min: 40, price_str: "$40 - $55", hot: false, comp: "Media", plts: ["Instagram", "Pinterest"], regions: ["AR", "CL"], history: [50, 65, 75, 88], rank: 4, suppliers: [{name:"AliExpress", price: 15}] },
          { name: "Humidificador Anti-gravedad", cat: "Hogar", score: 85, change: "down", change_num: -2.1, margin: 50, price_min: 30, price_str: "$30 - $45", hot: false, comp: "Muy Alta", plts: ["TikTok", "Shopee"], regions: ["BR", "MX"], history: [95, 90, 88, 85], rank: 5, suppliers: [{name:"AliExpress", price: 14}] },
          { name: "Collar GPS para Perros", cat: "Mascotas", score: 97, change: "up", change_num: 32.1, margin: 75, price_min: 60, price_str: "$60 - $80", hot: true, comp: "Baja", plts: ["Facebook", "TikTok"], regions: ["CO", "CL", "MX"], history: [20, 45, 80, 97], rank: 6, suppliers: [{name:"AliExpress", price: 15}] },
          
          { name: "Rascador para Gatos de Pared", cat: "Mascotas", score: 84, change: "up", change_num: 15.0, margin: 55, price_min: 20, price_str: "$20 - $35", hot: false, comp: "Baja", plts: ["Instagram"], regions: ["AR", "MX"], history: [50, 60, 70, 84], rank: 7, suppliers: [{name:"AliExpress", price: 9}] },
          { name: "Luz LED Inteligente WiFi", cat: "Tecnología", score: 82, change: "up", change_num: 5.5, margin: 45, price_min: 15, price_str: "$15 - $25", hot: false, comp: "Alta", plts: ["TikTok"], regions: ["US", "BR"], history: [75, 78, 80, 82], rank: 8, suppliers: [{name:"AliExpress", price: 8}] },
          { name: "Limpiador Facial Ultrasónico", cat: "Belleza", score: 91, change: "up", change_num: 21.0, margin: 80, price_min: 35, price_str: "$35 - $60", hot: true, comp: "Media", plts: ["TikTok", "Pinterest"], regions: ["MX", "CO"], history: [40, 60, 85, 91], rank: 9, suppliers: [{name:"AliExpress", price: 7}] },
          { name: "Dispensador de Agua Automático", cat: "Hogar", score: 79, change: "down", change_num: -5.0, margin: 40, price_min: 12, price_str: "$12 - $20", hot: false, comp: "Muy Alta", plts: ["Facebook"], regions: ["CL", "AR"], history: [85, 82, 80, 79], rank: 10, suppliers: [{name:"AliExpress", price: 6}] },
          { name: "Juguete Interactivo para Gatos", cat: "Mascotas", score: 94, change: "up", change_num: 19.5, margin: 68, price_min: 18, price_str: "$18 - $30", hot: true, comp: "Media", plts: ["TikTok"], regions: ["MX", "BR", "CO"], history: [30, 50, 80, 94], rank: 11, suppliers: [{name:"AliExpress", price: 5}] },
          { name: "Cámara de Seguridad Mini", cat: "Tecnología", score: 89, change: "up", change_num: 11.2, margin: 50, price_min: 25, price_str: "$25 - $40", hot: false, comp: "Alta", plts: ["Facebook"], regions: ["AR", "MX"], history: [70, 75, 80, 89], rank: 12, suppliers: [{name:"AliExpress", price: 12}] },
          { name: "Rodillo de Masaje Facial", cat: "Belleza", score: 86, change: "up", change_num: 7.1, margin: 75, price_min: 15, price_str: "$15 - $25", hot: false, comp: "Media", plts: ["Instagram"], regions: ["CL", "CO"], history: [60, 70, 80, 86], rank: 13, suppliers: [{name:"AliExpress", price: 3}] },
          { name: "Aspiradora Inalámbrica Portátil", cat: "Hogar", score: 93, change: "up", change_num: 14.8, margin: 45, price_min: 45, price_str: "$45 - $70", hot: true, comp: "Alta", plts: ["TikTok"], regions: ["BR", "MX"], history: [60, 75, 85, 93], rank: 14, suppliers: [{name:"AliExpress", price: 25}] },
          { name: "Correa Retráctil con Linterna", cat: "Mascotas", score: 87, change: "up", change_num: 9.3, margin: 60, price_min: 22, price_str: "$22 - $35", hot: false, comp: "Baja", plts: ["Facebook"], regions: ["AR", "CO"], history: [55, 65, 75, 87], rank: 15, suppliers: [{name:"AliExpress", price: 8}] },
          { name: "Auriculares Bluetooth Invisibles", cat: "Tecnología", score: 81, change: "down", change_num: -1.5, margin: 40, price_min: 18, price_str: "$18 - $28", hot: false, comp: "Muy Alta", plts: ["TikTok"], regions: ["MX", "BR"], history: [85, 83, 82, 81], rank: 16, suppliers: [{name:"AliExpress", price: 10}] },
          { name: "Depiladora Láser Casera", cat: "Belleza", score: 96, change: "up", change_num: 28.5, margin: 85, price_min: 65, price_str: "$65 - $100", hot: true, comp: "Baja", plts: ["TikTok", "Instagram"], regions: ["AR", "MX", "CL"], history: [35, 60, 80, 96], rank: 17, suppliers: [{name:"AliExpress", price: 20}] },
          { name: "Organizador de Cables Magnético", cat: "Tecnología", score: 76, change: "up", change_num: 2.1, margin: 55, price_min: 8, price_str: "$8 - $15", hot: false, comp: "Baja", plts: ["Pinterest"], regions: ["US", "MX"], history: [60, 65, 70, 76], rank: 18, suppliers: [{name:"AliExpress", price: 3}] },
          { name: "Fuente de Agua para Mascotas", cat: "Mascotas", score: 90, change: "up", change_num: 16.4, margin: 62, price_min: 30, price_str: "$30 - $45", hot: true, comp: "Media", plts: ["TikTok"], regions: ["BR", "CO"], history: [50, 65, 80, 90], rank: 19, suppliers: [{name:"AliExpress", price: 11}] },
          { name: "Lámpara Atrapamosquitos UV", cat: "Hogar", score: 88, change: "up", change_num: 10.5, margin: 58, price_min: 25, price_str: "$25 - $40", hot: false, comp: "Media", plts: ["Facebook"], regions: ["MX", "AR"], history: [60, 70, 80, 88], rank: 20, suppliers: [{name:"AliExpress", price: 10}] }
        ]"""
        # Replace the short list with the long list
        html = re.sub(
            r'\[\s*\{\s*name:\s*"Cama Relajante para Mascotas".*?\}\s*\]',
            new_products,
            html,
            flags=re.DOTALL
        )

    # 4. Fix chart cutoff
    # Increase the container height for the charts so they don't get cropped
    html = html.replace('class="h-64 relative w-full mt-4"', 'class="h-96 relative w-full mt-4"')
    html = html.replace('class="h-48 relative w-full"', 'class="h-72 relative w-full"')

    with open('/Users/nachofrag/Downloads/trenbase_repo/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("All issues fixed!")

if __name__ == '__main__':
    fix_all_issues()
