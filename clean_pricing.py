import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Pricing Cards cleanup
content = re.sub(r'\bbg-white border-slate/10\b', 'matte-card border-[rgba(200,190,180,0.3)]', content)
content = re.sub(r'\bbg-slate border-slate/20\b', 'matte-card border-champagne', content)
content = re.sub(r'\btext-obsidian\b', 'text-[var(--text-dark)]', content)
content = re.sub(r'\btext-slate/40\b', 'text-[var(--text-muted)]', content)
content = re.sub(r'\btext-slate/60\b', 'text-[var(--text-muted)]', content)
content = re.sub(r'\bborder-slate/5\b', 'border-[rgba(200,190,180,0.2)]', content)
content = re.sub(r'\bborder-slate/10\b', 'border-[rgba(200,190,180,0.3)]', content)
content = re.sub(r'\btext-ivory\b', 'text-[var(--text-dark)]', content)
content = re.sub(r'\bbg-ivory\b', 'bg-transparent', content)

# Fix the buttons inside pricing
content = content.replace('bg-slate text-[var(--text-dark)] hover:bg-obsidian hover:text-[var(--text-dark)]', 'bg-[rgba(255,255,255,0.4)] text-[var(--text-dark)] hover:bg-[rgba(255,255,255,0.6)] border border-[rgba(200,190,180,0.3)]')
content = content.replace('bg-ivory text-obsidian hover:bg-white', 'bg-[rgba(255,255,255,0.4)] text-[var(--text-dark)] hover:bg-[rgba(255,255,255,0.6)] border border-[rgba(200,190,180,0.3)]')

# One missing thing: text-slate from the top section might still be there:
content = re.sub(r'\btext-slate\b', 'text-[var(--text-dark)]', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Pricing cards cleaned up!")
