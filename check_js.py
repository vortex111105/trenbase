import re
import json

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract the entire mockData object
match = re.search(r'const mockData = (\{.*?\n      \});', html, re.DOTALL)
if match:
    data_str = match.group(1)
    
    # Try to transform to JSON
    # 1. Add quotes around keys
    data_str = re.sub(r'([a-zA-Z0-9_]+):', r'"\1":', data_str)
    
    # 2. Fix trailing commas if any (before } or ])
    data_str = re.sub(r',\s*\}', '}', data_str)
    data_str = re.sub(r',\s*\]', ']', data_str)

    try:
        j = json.loads(data_str)
        print("Valid JSON transformation! Contains", len(j.get("products", [])), "products")
    except Exception as e:
        print("JSON Error:", str(e))
        
        # Let's find the approximate location of the error
        import traceback
        traceback.print_exc()
else:
    print("Could not find mockData")
