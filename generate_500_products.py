import json
import random
import re

categories = ["Mascotas", "Tecnología", "Belleza", "Hogar", "Moda", "Deportes"]
platforms = ["TikTok", "Facebook", "Instagram", "Pinterest", "Amazon", "Shopee"]
regions = ["MX", "CO", "AR", "BR", "US", "CL", "ES", "PE"]
suppliers = ["AliExpress", "CJ Dropshipping", "Alibaba", "Droppi", "Dropdeal"]

adjectives = ["Inteligente", "Automático", "Mágico", "Portátil", "Inalámbrico", "Láser", "Ultrasónico", "LED", "Magnético", "Avanzado", "Pro", "Ultra", "Max", "Premium", "Ergonómico", "Multifunción", "Digital", "Invisible", "Relajante", "Anti-gravedad", "Viral", "Aesthetic"]

nouns = {
    "Mascotas": ["Cama", "Cepillo", "Collar GPS", "Rascador", "Juguete Interactivo", "Fuente de Agua", "Correa Retráctil", "Dispensador de Comida", "Transportadora", "Cortaúñas", "Pelota de Silicona", "Chaqueta Impermeable"],
    "Tecnología": ["Proyector Galaxia", "Auriculares", "Cámara de Seguridad", "Organizador de Cables", "Smartwatch", "Cargador", "Soporte para Coche", "Altavoz", "Humidificador", "Gafas VR", "Teclado", "Anillo", "Trípode", "Luz RGB"],
    "Belleza": ["Rizador de Pelo", "Limpiador Facial", "Rodillo de Masaje", "Depiladora", "Espejo", "Set de Brochas", "Masajeador de Cuello", "Lámpara de Uñas", "Plancha de Pelo", "Secador", "Sérum", "Mascarilla LED"],
    "Hogar": ["Humidificador", "Dispensador de Agua", "Aspiradora", "Lámpara Atrapamosquitos", "Proyector de Estrellas", "Mopa", "Purificador de Aire", "Almohada", "Cortador de Verduras", "Organizador de Zapatos", "Tira LED", "Ventilador"],
    "Moda": ["Faja Moldeadora", "Gafas de Sol", "Bolso Antirrobo", "Zapatillas Transpirables", "Chaqueta Calefactable", "Reloj Minimalista", "Mochila Impermeable", "Leggings Push-Up", "Cinturón Táctico", "Collar Personalizado"],
    "Deportes": ["Banda Elástica", "Botella de Agua", "Esterilla de Yoga", "Rodillera", "Rodillo Abdominal", "Cuerda de Saltar", "Soporte Lumbar", "Gorro de Natación", "Mancuernas Ajustables", "Pistola de Masaje"]
}

def generate_products(count=500):
    products = []
    names_generated = set()
    
    for i in range(count):
        cat = random.choice(categories)
        noun = random.choice(nouns[cat])
        adj = random.choice(adjectives)
        
        name = f"{noun} {adj}"
        if random.random() > 0.5:
            name += f" {random.choice(['2.0', '360', 'HD', 'Smart', 'Gamer', 'Fitness'])}"
            
        # Ensure unique names
        while name in names_generated:
            noun = random.choice(nouns[cat])
            adj = random.choice(adjectives)
            name = f"{noun} {adj} {random.randint(1,99)}"
        names_generated.add(name)
        
        score = random.randint(40, 99)
        hot = score >= 85
        
        # History curve should end at score
        history = [max(10, min(100, score - random.randint(10, 40))),
                   max(10, min(100, score - random.randint(5, 20))),
                   max(10, min(100, score - random.randint(-5, 15))),
                   score]
                   
        change_num = round(score - history[-2], 1)
        change_dir = "up" if change_num >= 0 else "down"
        
        margin = random.randint(30, 85)
        price = random.randint(10, 150)
        price_str = f"${price} - ${price + random.randint(10, 30)}"
        
        comp_choices = ["Baja", "Media", "Alta", "Muy Alta"]
        weights = [0.4, 0.3, 0.2, 0.1]
        comp = random.choices(comp_choices, weights=weights)[0]
        
        num_plts = random.randint(1, 3)
        plts = random.sample(platforms, num_plts)
        
        num_regs = random.randint(1, 4)
        regs = random.sample(regions, num_regs)
        
        supplier = random.choice(suppliers)
        sup_price = max(2, int(price * (1 - (margin/100))))
        
        p = {
            "name": name,
            "cat": cat,
            "score": score,
            "change": change_dir,
            "change_num": change_num,
            "margin": margin,
            "price_min": price,
            "price_str": price_str,
            "hot": hot,
            "comp": comp,
            "plts": plts,
            "regions": regs,
            "history": history,
            "rank": i + 1,
            "suppliers": [{"name": supplier, "price": sup_price}]
        }
        products.append(p)
        
    # Sort by score descending to assign correct ranks
    products.sort(key=lambda x: x["score"], reverse=True)
    for i, p in enumerate(products):
        p["rank"] = i + 1
        
    return products

def inject_to_html(products):
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
    # Find the products array
    # We look for "const mockData = { ... products: [ ... ], count: 47250"
    
    products_json_str = json.dumps(products, ensure_ascii=False, indent=10)
    # The JSON string puts everything on multiple lines. We can compress it so it doesn't take 10k lines in HTML
    
    compressed_lines = []
    for p in products:
        # manual serialization for a single line per product
        plts_str = '["' + '", "'.join(p['plts']) + '"]'
        regs_str = '["' + '", "'.join(p['regions']) + '"]'
        hist_str = '[' + ', '.join(map(str, p['history'])) + ']'
        sup_str = '[{"name":"' + p['suppliers'][0]['name'] + '", "price": ' + str(p['suppliers'][0]['price']) + '}]'
        
        line = f'{{ name: "{p["name"]}", cat: "{p["cat"]}", score: {p["score"]}, change: "{p["change"]}", change_num: {p["change_num"]}, margin: {p["margin"]}, price_min: {p["price_min"]}, price_str: "{p["price_str"]}", hot: {"true" if p["hot"] else "false"}, comp: "{p["comp"]}", plts: {plts_str}, regions: {regs_str}, history: {hist_str}, rank: {p["rank"]}, suppliers: {sup_str} }}'
        compressed_lines.append(line)
        
    final_array_str = "[\n          " + ",\n          ".join(compressed_lines) + "\n        ]"
    
    # Replace the existing array
    pattern = r'products:\s*\[.*?\],\s*count:\s*47250'
    replacement = f'products: {final_array_str},\n        count: 47250'
    
    new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
        
if __name__ == "__main__":
    prods = generate_products(500)
    inject_to_html(prods)
    print("Injected 500 products into index.html")
