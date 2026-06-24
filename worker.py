#!/usr/bin/env python3
"""
TrendBase Data Pipeline Worker
Ejecutar diariamente (cron job en Render.com o Railway).

Uso local:
  export SUPABASE_URL=...
  export SUPABASE_SERVICE_KEY=...
  export APIFY_API_TOKEN=...   # opcional — si no está, se omite TikTok
  python worker.py

Deploy en Render.com:
  1. New → Background Worker
  2. Build command: pip install supabase pytrends requests
  3. Start command: python worker.py
  4. Add env vars: SUPABASE_URL, SUPABASE_SERVICE_KEY, APIFY_API_TOKEN
  5. Configurar Cron Schedule: 0 4 * * * (4am UTC diariamente)
"""

import os
import sys
import time

import requests
from google_trends import fetch_trend_data, _normalize_to_16, get_trending_searches
from tiktok_scraper import fetch_tiktok_ads


def get_supabase():
    try:
        from supabase import create_client
    except ImportError:
        print("ERROR: Instala supabase-py:  pip install supabase")
        sys.exit(1)

    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not url or not key:
        print("ERROR: Define SUPABASE_URL y SUPABASE_SERVICE_KEY en el entorno.")
        sys.exit(1)

    return create_client(url, key)


def detect_and_create_new_products(supabase):
    """
    Busca trending searches en AR y crea productos nuevos en Supabase
    para términos que aún no existen en la base de datos.
    Llama a /api/generate con el keyword para que Claude Haiku lo estructure.
    """
    vercel_url = os.environ.get("VERCEL_URL", "").rstrip("/")
    cron_secret = os.environ.get("CRON_SECRET", "")

    if not vercel_url or not cron_secret:
        print("  Skipping (VERCEL_URL o CRON_SECRET no configurados)")
        return 0

    # Términos trending actuales en Argentina
    trending = get_trending_searches(geo='AR')
    if not trending:
        print("  Sin resultados de trending searches")
        return 0

    # Nombres existentes en Supabase (minúsculas para comparación)
    existing = {p["name"].lower() for p in supabase.table("products").select("name").execute().data}

    # Filtrar términos que no tengan match con productos existentes
    new_terms = []
    for term in trending:
        term_lower = term.lower()
        # Fuzzy: el término no aparece en ningún nombre existente y viceversa
        is_new = not any(term_lower in e or e in term_lower for e in existing)
        if is_new:
            new_terms.append(term)

    # Crear hasta 3 productos nuevos por run para no sobrecargar la API
    created = 0
    for term in new_terms[:3]:
        try:
            r = requests.post(
                f"{vercel_url}/api/generate",
                params={"keyword": term},
                headers={"Authorization": f"Bearer {cron_secret}"},
                timeout=30,
            )
            if r.ok:
                print(f"  ✓ Nuevo producto creado: {term}")
                created += 1
            else:
                print(f"  ✗ Error creando {term}: {r.status_code}")
        except Exception as e:
            print(f"  ✗ Error para '{term}': {e}")
        time.sleep(2)

    return created


def run_pipeline():
    print("=" * 50)
    print("TrendBase Data Pipeline")
    print("=" * 50)

    supabase = get_supabase()

    # ── 1. Cargar todos los productos ──────────────────
    result = supabase.table("products").select("id, name, score, cat").execute()
    products = result.data
    if not products:
        print("No hay productos en Supabase. Ejecuta /api/generate primero.")
        sys.exit(0)

    print(f"\nProductos encontrados: {len(products)}")

    # ── 2. Google Trends → actualiza campo history ─────
    print("\n--- Google Trends ---")
    names = [p["name"] for p in products]
    trend_data = fetch_trend_data(names)

    scores_updated = 0
    for p in products:
        raw = trend_data.get(p["name"], [])
        history = _normalize_to_16(raw)
        # Deriva score del promedio de las últimas 3 semanas (si hay datos reales)
        real_score = int(sum(history[-3:]) / 3) if any(v > 0 for v in history) else p["score"]

        supabase.table("products").update({
            "history": history,
            "score": real_score,
        }).eq("id", p["id"]).execute()

        scores_updated += 1
        print(f"  ✓ {p['name']} → score {real_score}")
        time.sleep(0.3)

    print(f"Trends actualizados: {scores_updated}/{len(products)}")

    # ── 3. TikTok Ads → actualiza campo ads ────────────
    print("\n--- TikTok Ads (top 30 por score) ---")
    result2 = supabase.table("products").select("id, name, score").order("score", desc=True).limit(30).execute()
    top_products = result2.data

    ads_updated = 0
    for p in top_products:
        ads = fetch_tiktok_ads(p["name"], max_videos=5)
        if ads:
            supabase.table("products").update({"ads": ads}).eq("id", p["id"]).execute()
            ads_updated += 1
            print(f"  ✓ {p['name']} → {len(ads)} videos")
        else:
            print(f"  - {p['name']} → sin datos (token no configurado o sin resultados)")
        time.sleep(1)

    print(f"TikTok actualizado: {ads_updated}/{len(top_products)}")

    # ── 4. Auto-detectar productos nuevos en tendencia ──
    print("\n--- Auto-detección de nuevos trending products ---")
    new_detected = detect_and_create_new_products(supabase)
    print(f"Nuevos términos enviados a /api/generate: {new_detected}")

    # ── 5. Resumen ─────────────────────────────────────
    print("\n" + "=" * 50)
    print(f"Pipeline completado.")
    print(f"  • Trends:  {scores_updated} productos")
    print(f"  • TikTok:  {ads_updated} productos")
    print(f"  • Nuevos:  {new_detected} términos detectados")
    print("=" * 50)


if __name__ == "__main__":
    run_pipeline()
