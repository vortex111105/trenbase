import re
import json

def extract():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Find mockData object
    match = re.search(r'const mockData = (\{.*?\n      \});', html, re.DOTALL)
    if not match:
        print("Error: Could not find mockData")
        return
        
    data_str = match.group(1)
    
    # We will save it directly as a javascript file that defines window.MOCK_DATA
    js_content = "window.MOCK_DATA = " + data_str + ";\n"
    
    with open('data.js', 'w', encoding='utf-8') as f:
        f.write(js_content)
        
    print("Extracted data to data.js")

if __name__ == '__main__':
    extract()
