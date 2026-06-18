import re

def apply_apple_theme():
    with open('index.html', 'r') as f:
        content = f.read()

    # 1. Custom CSS Block
    custom_css = """
  <style id="premium-apple-theme">
    /* Exact Colors from Mockup */
    :root {
      --aw-bg: #E8DFD5;
      --aw-card: #F3EFEA;
      --aw-text-main: #2D2B29;
      --aw-text-muted: #7A7571;
      --aw-green: #4A8B5D;
      --aw-red: #B95252;
      --aw-shadow: 0 24px 48px rgba(160, 150, 140, 0.25), 0 2px 6px rgba(160, 150, 140, 0.1), inset 0 1px 2px rgba(255, 255, 255, 0.9);
      --aw-shadow-hover: 0 32px 64px rgba(160, 150, 140, 0.3), 0 4px 12px rgba(160, 150, 140, 0.15), inset 0 1px 2px rgba(255, 255, 255, 1);
    }
    
    /* Base Body overrides */
    body {
      background-color: var(--aw-bg) !important;
      color: var(--aw-text-main) !important;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    
    /* Squircles (Cards) */
    .aw-card {
      background-color: var(--aw-card) !important;
      border-radius: 32px !important;
      box-shadow: var(--aw-shadow) !important;
      border: 1px solid rgba(255, 255, 255, 0.4) !important;
      backdrop-filter: blur(20px) !important;
      transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
      color: var(--aw-text-main) !important;
    }
    
    .aw-card:hover {
      box-shadow: var(--aw-shadow-hover) !important;
      transform: translateY(-2px) !important;
    }

    /* Functional Text */
    .aw-text-main { color: var(--aw-text-main) !important; }
    .aw-text-muted { color: var(--aw-text-muted) !important; }
    .aw-green { color: var(--aw-green) !important; }
    .aw-red { color: var(--aw-red) !important; }
    .aw-bg-green { background-color: rgba(74, 139, 93, 0.1) !important; color: var(--aw-green) !important; }
    .aw-bg-red { background-color: rgba(185, 82, 82, 0.1) !important; color: var(--aw-red) !important; }
    
    /* Inputs & Selects */
    input, select, textarea {
      background-color: rgba(255, 255, 255, 0.5) !important;
      border: 1px solid rgba(0, 0, 0, 0.05) !important;
      color: var(--aw-text-main) !important;
    }
    input::placeholder { color: var(--aw-text-muted) !important; }
  </style>
"""

    # Inject CSS
    content = content.replace('</head>', custom_css + '\n</head>')

    # 2. Tailwind Replacements (Remove Generic Tailwind, Add Custom CSS Classes)
    replacements = [
        # Base
        (r'\bbg-obsidian\b', 'aw-bg'),
        (r'\btext-ivory\b', 'aw-text-main'),
        
        # Cards
        (r'\bbg-white/5\b', 'aw-card'),
        (r'\bbg-white/10\b', 'aw-card'),
        (r'\bbg-white/70 backdrop-blur-xl border border-white shadow-\[0_8px_30px_rgb\(0,0,0,0.06\)\] rounded-\[32px\]\b', 'aw-card'),
        
        # Text
        (r'\btext-stone-800\b', 'aw-text-main'),
        (r'\btext-stone-900\b', 'aw-text-main'),
        (r'\btext-white/40\b', 'aw-text-muted'),
        (r'\btext-white/50\b', 'aw-text-muted'),
        (r'\btext-white/60\b', 'aw-text-muted'),
        (r'\btext-stone-500\b', 'aw-text-muted'),
        (r'\btext-stone-400\b', 'aw-text-muted'),
        
        # Generic text-white to main (careful with buttons)
        (r'(?<!hover:)(?<!group-hover:)\btext-white\b', 'aw-text-main'),
        
        # Colors
        (r'\btext-green-400\b', 'aw-green'),
        (r'\btext-green-600\b', 'aw-green'),
        (r'\btext-red-400\b', 'aw-red'),
        (r'\btext-red-600\b', 'aw-red'),
        (r'\bbg-green-500/10\b', 'aw-bg-green'),
        (r'\bbg-red-500/10\b', 'aw-bg-red'),
    ]

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)

    # 3. Chart Customizations
    content = content.replace("color: '#FAF8F5'", "color: '#2D2B29'")
    content = content.replace("color: 'rgba(255, 255, 255, 0.1)'", "color: 'rgba(45, 43, 41, 0.05)'")
    content = content.replace("color: 'rgba(255, 255, 255, 0.5)'", "color: 'rgba(45, 43, 41, 0.4)'")

    # Re-fix solid buttons that need white text
    buttons_to_fix = [
        ('bg-green-600 hover:bg-green-700 aw-text-main', 'bg-green-600 hover:bg-green-700 text-white'),
        ('bg-blue-600 flex items-center justify-center aw-text-main', 'bg-blue-600 flex items-center justify-center text-white'),
        ('bg-purple-600 flex items-center justify-center aw-text-main', 'bg-purple-600 flex items-center justify-center text-white'),
        ('bg-red-500 aw-text-main', 'bg-red-500 text-white'),
        ('bg-red-600 aw-text-main', 'bg-red-600 text-white'),
    ]
    for old, new in buttons_to_fix:
        content = content.replace(old, new)

    with open('index.html', 'w') as f:
        f.write(content)
    print("Perfect Apple Theme applied!")

apply_apple_theme()
