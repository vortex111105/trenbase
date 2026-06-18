def apply_transparent_widgets():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    old_css = """    .matte-card {
        background: var(--matte-card) !important;
        border-radius: 24px !important;
        box-shadow: var(--card-shadow), var(--card-bevel) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        color: var(--text-dark) !important;
    }"""

    new_css = """    .matte-card {
        background: rgba(255, 255, 255, 0.45) !important;
        backdrop-filter: blur(24px) saturate(110%) !important;
        -webkit-backdrop-filter: blur(24px) saturate(110%) !important;
        border-radius: 32px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05), inset 0 2px 4px rgba(255, 255, 255, 0.6), inset 0 0 0 1px rgba(255, 255, 255, 0.4) !important;
        border: 1px solid rgba(255, 255, 255, 0.5) !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        color: var(--text-dark) !important;
    }"""

    html = html.replace(old_css, new_css)
    
    # Also update the hover state to keep it glassy
    old_hover = """    .matte-card:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 16px 40px rgba(170, 150, 130, 0.2), 0 6px 15px rgba(170, 150, 130, 0.08), var(--card-bevel) !important;
    }"""
    
    new_hover = """    .matte-card:hover {
        transform: translateY(-2px) !important;
        background: rgba(255, 255, 255, 0.55) !important;
        box-shadow: 0 16px 40px rgba(170, 150, 130, 0.1), 0 6px 15px rgba(170, 150, 130, 0.05), inset 0 2px 4px rgba(255, 255, 255, 0.8), inset 0 0 0 1px rgba(255, 255, 255, 0.5) !important;
    }"""
    
    html = html.replace(old_hover, new_hover)

    # In the sidebar, there are some active elements that use white, let's make them translucent too
    # Like: bg-[rgba(255,255,255,0.5)] is already translucent.
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Widgets are now transparent glass!")

if __name__ == "__main__":
    apply_transparent_widgets()
