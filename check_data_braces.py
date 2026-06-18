import re

with open('data.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove string literals and comments to count braces accurately
text = re.sub(r'//.*', '', text)
text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
text = re.sub(r'(["\'])(?:(?=(\\?))\2.)*?\1', '', text, flags=re.DOTALL)
text = re.sub(r'`[^`]*`', '', text, flags=re.DOTALL)

open_braces = text.count('{')
close_braces = text.count('}')

print(f"data.js -> Open braces: {open_braces}, Close braces: {close_braces}")
if open_braces != close_braces:
    print("MISMATCHED BRACES IN DATA.JS!")
