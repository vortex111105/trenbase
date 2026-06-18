import os
import re

def sync_affiliate_links():
    affiliates_file = "/Users/nachofrag/Desktop/TrendBase_Afiliados/MIS_ENLACES_AFILIADOS.txt"
    index_file = "/Users/nachofrag/Downloads/trenbase_repo/index.html"
    
    if not os.path.exists(affiliates_file):
        print("El archivo de afiliados no existe.")
        return

    affiliate_links = {}
    with open(affiliates_file, 'r', encoding='utf-8') as f:
        for line in f:
            if ':' in line and not line.startswith('#'):
                parts = line.split(':', 1)
                platform = parts[0].strip()
                link = parts[1].strip()
                if link:
                    affiliate_links[platform] = link

    if not affiliate_links:
        print("No se encontraron enlaces de afiliados llenados en el archivo. Mantenemos los de por defecto.")
        return

    # Mapeo de plataforma en archivo -> nombre en SUPPLIERS_BUY
    print(f"Detectados {len(affiliate_links)} enlaces de afiliados. Integrando a index.html...")
    
    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for platform, link in affiliate_links.items():
        # Update the aff:'...' in SUPPLIERS_BUY
        pattern = re.compile(r"(\{ name:'" + platform + r"',[^}]+aff:')([^']*)(' \})")
        
        # If the user put a full URL like https://s.click.aliexpress.com/e/_D..., we should just replace the whole URL logic or just inject it.
        # Since SUPPLIERS_BUY builds href like s.url + q + s.aff, if user provides a full link, maybe we just use that link if it's a redirect, or append it.
        # For simplicity, we just inject whatever they put into `aff`.
        if "&" not in link and "?" not in link:
            # If they just put 'trendbase123', prepend &af= or &ref=
            link = "&ref=" + link
            
        content = pattern.sub(r"\g<1>" + link + r"\g<3>", content)

    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("¡Enlaces de afiliado integrados con éxito!")

if __name__ == '__main__':
    sync_affiliate_links()
