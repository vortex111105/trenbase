import re

def apply_skin():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # The ultimate, bulletproof CSS skin that maps Tailwind dark theme to Apple Vision Liquid Glass
    css_skin = """
  <!-- ─── APPLE VISION "LIQUID GLASS" SKIN (NO HTML CHANGES) ─── -->
  <style id="apple-vision-skin">
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    :root {
        --bg-wall: #E6DCD1;
        --glass-container: rgba(245, 240, 230, 0.65);
        --matte-card: #FDFBFA;
        --card-shadow: 0 12px 30px rgba(170, 150, 130, 0.15);
        --text-dark: #2E2B2A;
        --text-muted: #807A75;
        --soft-green: #599B62;
        --soft-red: #C76B6B;
    }

    /* 1. PROCEDURAL ENVIRONMENT BACKGROUND */
    body {
        background-color: var(--bg-wall) !important;
        background-image: 
            radial-gradient(circle at 30% 20%, #F5EEE6 0%, transparent 60%),
            linear-gradient(to bottom, transparent 65%, #DBCDC0 65%, #C2B3A3 100%),
            url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E") !important;
        background-blend-mode: normal, normal, overlay !important;
        background-attachment: fixed !important;
        color: var(--text-dark) !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* Hide any old background images that were used for the dark theme */
    body > img.absolute.inset-0,
    section > img.absolute.inset-0 {
        display: none !important;
    }

    /* 2. THE GLASS CONTAINER (Overrides bg-obsidian on the main wrapper) */
    .bg-obsidian.glass-app-container,
    .bg-obsidian,
    .bg-black {
        background: transparent !important;
    }

    /* Specifically target the app's main container */
    .app-view > div.w-full.max-w-\\[1400px\\],
    .app-view > div.w-full.max-w-7xl,
    #view-dash > div {
        background: var(--glass-container) !important;
        backdrop-filter: blur(50px) saturate(120%) !important;
        -webkit-backdrop-filter: blur(50px) saturate(120%) !important;
        border-radius: 40px !important;
        box-shadow: 0 40px 80px rgba(140, 120, 100, 0.25), inset 0 1px 1px rgba(255,255,255,0.7) !important;
        border: 1px solid rgba(255,255,255,0.4) !important;
    }

    /* 3. MATTE CERAMIC CARDS (Overrides bg-white/5, bg-white/10) */
    .bg-white\\/5, .bg-white\\/10, .bg-white\\/20,
    .bg-black\\/30, .bg-black\\/50 {
        background: var(--matte-card) !important;
        border-radius: 24px !important;
        box-shadow: var(--card-shadow), inset 0 2px 4px rgba(255,255,255,1), inset 0 0 0 1px rgba(255,255,255,0.8) !important;
        border: none !important;
        color: var(--text-dark) !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }

    .bg-white\\/5:hover, .bg-white\\/10:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 20px 50px rgba(170, 150, 130, 0.25), 0 8px 20px rgba(170, 150, 130, 0.1) !important;
    }

    /* 4. TYPOGRAPHY AND TEXT COLORS */
    .text-white, .text-ivory, .text-white\\/80, .text-white\\/90 {
        color: var(--text-dark) !important;
    }
    .text-white\\/60, .text-white\\/70, .text-white\\/40, .text-slate-300, .text-slate-400 {
        color: var(--text-muted) !important;
    }
    h1, h2, h3, h4, .font-extrabold {
        color: var(--text-dark) !important;
        letter-spacing: -0.04em !important;
        font-weight: 800 !important;
    }

    /* 5. BORDERS & DIVIDERS */
    .border-white\\/10, .border-white\\/5, .border-slate-800, .divide-white\\/5 > * {
        border-color: rgba(200, 190, 180, 0.3) !important;
    }

    /* 6. BUTTONS */
    .bg-champagne {
        background: linear-gradient(180deg, #3A3A3C 0%, #1C1C1E 100%) !important;
        color: #FDFBFA !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15), inset 0 1px 1px rgba(255,255,255,0.25) !important;
        border-radius: 999px !important;
        border: 1px solid rgba(0,0,0,0.8) !important;
        text-shadow: none !important;
    }
    .bg-champagne:hover {
        transform: scale(1.02) !important;
        background: linear-gradient(180deg, #2E2B2A 0%, #0D0D12 100%) !important;
    }
    .text-champagne {
        color: var(--text-dark) !important;
        font-weight: 800 !important;
    }

    /* ACCENT COLORS */
    .text-green-400, .text-green-500, .bg-green-500 {
        color: var(--soft-green) !important;
    }
    .bg-green-500 { background-color: var(--soft-green) !important; color: white !important; }
    .text-red-400, .text-red-500, .bg-red-500 {
        color: var(--soft-red) !important;
    }
    .bg-red-500 { background-color: var(--soft-red) !important; color: white !important; }

    /* Fix Sidebar items active state */
    .active-sidebar-item {
        background: rgba(255,255,255,0.8) !important;
        color: var(--text-dark) !important;
        box-shadow: inset 0 2px 4px rgba(255,255,255,1), 0 4px 8px rgba(0,0,0,0.05) !important;
        border: none !important;
    }

    /* Inputs */
    input, select {
        background: var(--matte-card) !important;
        color: var(--text-dark) !important;
        border: 1px solid rgba(200, 190, 180, 0.4) !important;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05) !important;
    }
    input::placeholder {
        color: var(--text-muted) !important;
    }
  </style>
  <!-- ─────────────────────────────────────────────────────────── -->
"""

    # Inject the skin right before </head>
    if 'id="apple-vision-skin"' not in html:
        html = html.replace('</head>', f'{css_skin}\n</head>')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Apple Vision CSS Skin successfully injected!")

if __name__ == "__main__":
    apply_skin()
