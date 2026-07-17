# worker/update_products.py
# TrendBase — Worker de datos REALES desde MercadoLibre
# Corre cada 6 horas vía GitHub Actions (.github/workflows/update-products.yml)
#
# Fuentes:
#   - /trends/{site}: búsquedas en tendencia REALES (MLA=AR, MLU=UY, MLC=CL)
#   - /sites/{site}/search: precios y resultados reales por keyword
#
# Requiere (GitHub Secrets):
#   ML_CLIENT_ID, ML_CLIENT_SECRET  -> app en developers.mercadolibre.com
#   SUPABASE_SERVICE_KEY            -> service_role de Supabase

import os
import sys
import time
import requests

SUPABASE_URL = "https://rbrundkswmlbgkicdnty.supabase.co"
SUPABASE_KEY = os.environ["SUPABASE_SERVICE_KEY"]
ML_CLIENT_ID = os.environ["ML_CLIENT_ID"]
ML_CLIENT_SECRET = os.environ["ML_CLIENT_SECRET"]

SITES = {"MLA": "AR", "MLU": "UY", "MLC": "CL"}
TRENDS_PER_SITE = 40          # keywords de tendencia a procesar por país
RESULTS_PER_KEYWORD = 1       # producto representativo por keyword

# Mapeo de categorías ML -> categorías TrendBase
CAT_MAP = {
    "Tecnología": ["Electrónica", "Computación", "Celulares", "Cámaras", "Consolas", "Audio", "Televisores", "Accesorios para Vehículos"],
    "Hogar": ["Hogar", "Muebles", "Jardín", "Electrodomésticos", "Construcción", "Cocina"],
    "Moda": ["Ropa", "Calzado", "Accesorios de Moda", "Relojes", "Joyas", "Lentes"],
    "Belleza": ["Belleza", "Cuidado", "Salud", "Perfumes"],
    "Deportes": ["Deportes", "Fitness", "Camping", "Ciclismo"],
}

def ml_token():
    r = requests.post("https://api.mercadolibre.com/oauth/token", data={
        "grant_type": "client_credentials",
        "client_id": ML_CLIENT_ID,
        "client_secret": ML_CLIENT_SECRET,
    }, timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]

def map_cat(ml_category_name: str) -> str:
    for tb_cat, keywords in CAT_MAP.items():
        for kw in keywords:
            if kw.lower() in (ml_category_name or "").lower():
                return tb_cat
    return "Hogar"

def comp_level(total_results: int) -> str:
    if total_results < 500: return "Baja"
    if total_results < 5000: return "Media"
    return "Alta"

def fetch_existing_history(headers_sb):
    """name(lower) -> history para mantener continuidad del gráfico."""
    r = requests.get(
        f"{SUPABASE_URL}/rest/v1/products?select=name,history,score",
        headers=headers_sb, timeout=30)
    out = {}
    if r.ok:
        for p in r.json():
            out[(p.get("name") or "").lower().strip()] = p.get("history") or []
    return out

def main():
    token = ml_token()
    h_ml = {"Authorization": f"Bearer {token}"}
    h_sb = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates",
    }

    prev_history = fetch_existing_history(h_sb)
    products, seen = [], set()

    for site, region in SITES.items():
        tr = requests.get(f"https://api.mercadolibre.com/trends/{site}", headers=h_ml, timeout=30)
        if not tr.ok:
            print(f"[{site}] trends error {tr.status_code}: {tr.text[:200]}", file=sys.stderr)
            continue
        trends = tr.json()[:TRENDS_PER_SITE]

        for rank, t in enumerate(trends):
            keyword = t.get("keyword", "").strip()
            if not keyword:
                continue
            key = keyword.lower()
            if key in seen:
                # producto ya visto en otro país -> solo sumamos la región
                for p in products:
                    if p["name"].lower() == key and region not in p["regions"]:
                        p["regions"].append(region)
                continue

            sr = requests.get(
                f"https://api.mercadolibre.com/sites/{site}/search",
                params={"q": keyword, "limit": RESULTS_PER_KEYWORD},
                headers=h_ml, timeout=30)
            if not sr.ok:
                continue
            data = sr.json()
            items = data.get("results") or []
            if not items:
                continue
            it = items[0]
            total = data.get("paging", {}).get("total", 0)

            price = it.get("price") or 0
            currency = it.get("currency_id") or ""
            cat_name = ""
            try:
                cr = requests.get(f"https://api.mercadolibre.com/categories/{it.get('category_id')}", timeout=15)
                if cr.ok:
                    cat_name = cr.json().get("name", "")
            except Exception:
                pass

            # Score REAL basado en posición de tendencia (1° = 99, decrece)
            score = max(35, 99 - int(rank * (64 / max(1, TRENDS_PER_SITE - 1))))
            hist = (prev_history.get(key) or [])[-15:] + [score]

            products.append({
                "name": keyword.title()[:80],
                "cat": map_cat(cat_name),
                "score": score,
                "change": f"+{max(1, (TRENDS_PER_SITE - rank))}%",
                "change_num": max(1, TRENDS_PER_SITE - rank),
                "plts": ["ML"],
                "margin": None,               # sin dato real de costo -> no inventamos margen
                "margin_str": "s/d",
                "hot": rank < 5,
                "regions": [region],
                "comp": comp_level(total),
                "price_min": price,
                "price_str": f"{currency} {price:,.0f}" if price else "s/d",
                "history": hist,
                "rank": rank + 1,
                "suppliers": [{
                    "name": "MercadoLibre",
                    "icon": "ML",
                    "meta": f"{total:,} publicaciones activas",
                    "url": it.get("permalink") or "",
                    "aff": False,
                }],
                "img_kw": keyword,
                "updated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            })
            seen.add(key)
            time.sleep(0.25)  # rate-limit friendly

    if not products:
        print("Sin productos — abortando sin tocar la base", file=sys.stderr)
        sys.exit(1)

    # Upsert en Supabase (on_conflict por name si existe unique; si no, insert)
    r = requests.post(
        f"{SUPABASE_URL}/rest/v1/products",
        headers=h_sb, json=products, timeout=60)
    if not r.ok:
        print(f"Supabase error {r.status_code}: {r.text[:400]}", file=sys.stderr)
        sys.exit(1)

    # Purgar productos viejos (no actualizados en esta corrida) para no mezclar IA vieja con datos reales
    cutoff = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() - 26 * 3600))
    requests.delete(
        f"{SUPABASE_URL}/rest/v1/products?updated_at=lt.{cutoff}",
        headers=h_sb, timeout=60)

    print(f"OK — {len(products)} productos reales cargados")

if __name__ == "__main__":
    main()
