import re

with open('/Users/nachofrag/Downloads/trendbase/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the main script block
scripts = re.findall(r'<script>(.*?)</script>', content, re.DOTALL)
# The last script block is usually the main one
main_script = scripts[-1]

with open('original_logic.js', 'w', encoding='utf-8') as f:
    f.write(main_script)

print("Extracted script to original_logic.js")
