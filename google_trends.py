import time
import json
from pytrends.request import TrendReq

# Connect to Google
pytrend = TrendReq(hl='es-US', tz=360)

def fetch_trend_data(keywords):
    """
    Fetch 90-day trend data for a list of keywords.
    Returns a dictionary mapping each keyword to an array of trend scores.
    """
    results = {}
    
    # Pytrends can process 5 keywords at a time
    for i in range(0, len(keywords), 5):
        chunk = keywords[i:i+5]
        print(f"Fetching data for: {chunk}")
        
        try:
            # timeframe='today 3-m' means last 90 days
            pytrend.build_payload(kw_list=chunk, cat=0, timeframe='today 3-m', geo='')
            
            # Interest over time
            df = pytrend.interest_over_time()
            
            if not df.empty:
                for kw in chunk:
                    if kw in df.columns:
                        # Extract list of values and scale to 0-100
                        values = df[kw].tolist()
                        results[kw] = values
                    else:
                        results[kw] = []
            else:
                for kw in chunk:
                    results[kw] = []
                    
        except Exception as e:
            print(f"Error fetching {chunk}: {e}")
            for kw in chunk:
                results[kw] = []
                
        # Sleep to avoid hitting rate limits
        time.sleep(2)
        
    return results

if __name__ == "__main__":
    # Example usage
    sample_keywords = ["masajeador facial", "cinturon lumbar", "luces led", "cepillo mascotas"]
    data = fetch_trend_data(sample_keywords)
    print(json.dumps(data, indent=2))
