import os
import json
import requests

APIFY_API_TOKEN = os.environ.get("APIFY_API_TOKEN")
# Free actor: clockworks/free-tiktok-scraper
# Paid / more results: clockworks/tiktok-scraper
APIFY_ACTOR_ID = os.environ.get("APIFY_ACTOR_ID", "clockworks/free-tiktok-scraper")


def fetch_tiktok_ads(keyword, max_videos=5):
    """
    Fetch top TikTok videos for a keyword using Apify.
    Returns a list of dicts: [{id, views, likes, url}]
    Returns [] if APIFY_API_TOKEN is not set.
    """
    if not APIFY_API_TOKEN:
        print(f"[tiktok] APIFY_API_TOKEN not set — skipping '{keyword}'")
        return []

    try:
        url = f"https://api.apify.com/v2/acts/{APIFY_ACTOR_ID}/run-sync-get-dataset-items"
        params = {"token": APIFY_API_TOKEN, "timeout": 120}
        payload = {
            "hashtags": [keyword.replace(" ", "")],
            "resultsPerPage": max_videos,
            "proxyConfig": {"useApifyProxy": True},
        }
        res = requests.post(url, json=payload, params=params, timeout=130)
        res.raise_for_status()
        items = res.json()

        return [
            {
                "id": str(item.get("id", "")),
                "views": item.get("playCount", 0),
                "likes": item.get("diggCount", 0),
                "url": item.get("webVideoUrl", ""),
            }
            for item in items[:max_videos]
            if item.get("webVideoUrl")
        ]
    except Exception as e:
        print(f"[tiktok] Error fetching '{keyword}': {e}")
        return []


if __name__ == "__main__":
    ads = fetch_tiktok_ads("masajeador facial")
    print(json.dumps(ads, indent=2))
