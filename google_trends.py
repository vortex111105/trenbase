import os
import time
import json
from pytrends.request import TrendReq

pytrend = TrendReq(hl='es-US', tz=360)

def fetch_trend_data(keywords):
    """
    Fetch 90-day trend data for a list of keywords.
    Returns a dict mapping each keyword to a list of weekly trend scores (0-100).
    """
    results = {}

    for i in range(0, len(keywords), 5):
        chunk = keywords[i:i+5]
        print(f"Fetching trends for: {chunk}")
        try:
            pytrend.build_payload(kw_list=chunk, cat=0, timeframe='today 3-m', geo='')
            df = pytrend.interest_over_time()
            if not df.empty:
                for kw in chunk:
                    results[kw] = df[kw].tolist() if kw in df.columns else []
            else:
                for kw in chunk:
                    results[kw] = []
        except Exception as e:
            print(f"Error fetching {chunk}: {e}")
            for kw in chunk:
                results[kw] = []

        time.sleep(2)

    return results


def _normalize_to_16(values):
    """Resample or pad a list of values to exactly 16 data points."""
    if not values:
        return [0] * 16
    if len(values) == 16:
        return values
    if len(values) > 16:
        step = len(values) / 16
        return [int(values[int(i * step)]) for i in range(16)]
    last = values[-1]
    return [int(v) for v in values] + [int(last)] * (16 - len(values))


def update_supabase_history():
    """Fetch real Google Trends data for every product in Supabase and update the history field."""
    try:
        from supabase import create_client
    except ImportError:
        print("ERROR: Install supabase-py:  pip install supabase")
        return

    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set in environment")

    supabase = create_client(url, key)

    result = supabase.table("products").select("id, name").execute()
    products = result.data
    print(f"Updating history for {len(products)} products…")

    names = [p["name"] for p in products]
    trend_data = fetch_trend_data(names)

    updated = 0
    for p in products:
        raw = trend_data.get(p["name"], [])
        history = _normalize_to_16(raw)
        supabase.table("products").update({"history": history}).eq("id", p["id"]).execute()
        updated += 1
        print(f"  ✓ {p['name']} — {sum(1 for v in history if v > 0)} non-zero points")
        time.sleep(0.3)

    print(f"Done. Updated {updated}/{len(products)} products.")


def get_trending_searches(geo='AR'):
    """
    Returns a list of current trending search terms for a given country.
    Uses pytrends' trending_searches endpoint.
    geo: 'AR' (Argentina), 'UY' (Uruguay), 'CL' (Chile), etc.
    Returns list of strings (search terms), up to 20.
    """
    geo_map = {'AR': 'argentina', 'UY': 'uruguay', 'CL': 'chile', 'MX': 'mexico'}
    country_name = geo_map.get(geo, 'argentina')
    try:
        df = pytrend.trending_searches(pn=country_name)
        terms = df[0].tolist()[:20]
        print(f"Trending searches in {geo}: {terms[:5]}...")
        return terms
    except Exception as e:
        print(f"Error fetching trending searches for {geo}: {e}")
        return []


if __name__ == "__main__":
    import sys
    if "--supabase" in sys.argv:
        update_supabase_history()
    elif "--trending" in sys.argv:
        terms = get_trending_searches('AR')
        print(json.dumps(terms, indent=2, ensure_ascii=False))
    else:
        sample = ["masajeador facial", "cinturon lumbar", "luces led", "cepillo mascotas"]
        data = fetch_trend_data(sample)
        print(json.dumps(data, indent=2))
