import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Body
content = content.replace('body class="bg-obsidian text-ivory', 'body class="bg-[var(--bg-wall)] text-[var(--text-dark)]')

# 2. Make env-bg active by default
content = content.replace('<div id="vision-env-bg" class="environment-bg"></div>', '<div id="vision-env-bg" class="environment-bg active"></div>')

# 3. Remove JS env-bg toggling (just replace with empty strings to avoid breaking other logic)
content = content.replace("const envBg = document.getElementById('vision-env-bg');", "")
content = content.replace("if(envBg) envBg.classList.remove('active');", "")
content = content.replace("if(envBg) envBg.classList.add('active');", "")

# 4. Global Dark Mode replacements
# We need to replace bg-obsidian with matte-card (except in the body class which is already handled, wait, if I replace bg-obsidian globally, it will replace it everywhere. The body is already replaced).
content = re.sub(r'\bbg-obsidian\b', 'matte-card', content)
content = re.sub(r'\bbg-black/40\b', 'bg-[rgba(255,255,255,0.4)]', content)
content = re.sub(r'\bbg-black/60\b', 'bg-[rgba(255,255,255,0.6)]', content)
content = re.sub(r'\bbg-black/80\b', 'bg-[rgba(255,255,255,0.8)]', content)
content = re.sub(r'\bbg-black/20\b', 'bg-[rgba(255,255,255,0.2)]', content)
content = re.sub(r'bg-\[\#0A0A0A\]', 'matte-card', content)
content = re.sub(r'bg-\[\#111\]', 'matte-card', content)

# 5. Text colors
# To avoid replacing text-white inside class="... text-white ..." incorrectly, we use word boundaries.
# We skip text-white inside hover:text-white by targeting just text-white. Wait, hover:text-white should become hover:text-[--text-dark].
content = re.sub(r'\btext-white/30\b', 'text-[var(--text-muted)]', content)
content = re.sub(r'\btext-white/40\b', 'text-[var(--text-muted)]', content)
content = re.sub(r'\btext-white/50\b', 'text-[var(--text-muted)]', content)
content = re.sub(r'\btext-white/60\b', 'text-[var(--text-muted)]', content)
content = re.sub(r'\btext-white/70\b', 'text-[var(--text-dark)] font-medium', content)
content = re.sub(r'\btext-white/80\b', 'text-[var(--text-dark)] font-semibold', content)
content = re.sub(r'\btext-white\b', 'text-[var(--text-dark)]', content)
content = re.sub(r'\bhover:text-white\b', 'hover:text-[var(--text-dark)]', content)

# 6. Borders and other backgrounds
content = re.sub(r'\bborder-white/10\b', 'border-[rgba(200,190,180,0.3)]', content)
content = re.sub(r'\bborder-white/20\b', 'border-[rgba(200,190,180,0.4)]', content)
content = re.sub(r'\bborder-white/5\b', 'border-[rgba(200,190,180,0.2)]', content)

content = re.sub(r'\bbg-white/5\b', 'bg-[rgba(255,255,255,0.4)]', content)
content = re.sub(r'\bbg-white/10\b', 'bg-[rgba(255,255,255,0.6)]', content)
content = re.sub(r'\bhover:bg-white/5\b', 'hover:bg-[rgba(255,255,255,0.6)]', content)
content = re.sub(r'\bhover:bg-white/10\b', 'hover:bg-[rgba(255,255,255,0.8)]', content)

# 7. Navbar specific
# The navbar uses `border border-white/10 bg-transparent` originally.
# Let's change `bg-transparent` inside `#nav-container` to `sidebar-panel` to give it the frosted look.
content = content.replace('id="nav-container" class="mx-auto flex items-center justify-between px-6 py-4 rounded-full border border-[rgba(200,190,180,0.3)] bg-transparent', 'id="nav-container" class="mx-auto flex items-center justify-between px-6 py-4 rounded-full border border-[rgba(255,255,255,0.6)] sidebar-panel')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Migration of Landing Page and global styles complete!")
