def fix():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Fix the hidden class on view-dash
    # Find: <main id="view-dash" class="flex-1 overflow-y-auto hidden relative z-10 w-full flex-col p-6 md:p-10 max-w-7xl mx-auto space-y-8">
    # Replace with: <main id="view-dash" class="app-view flex-1 overflow-y-auto relative z-10 w-full flex-col p-6 md:p-10 max-w-7xl mx-auto space-y-8">
    html = html.replace(
        '<main id="view-dash" class="flex-1 overflow-y-auto hidden relative z-10 w-full flex-col p-6 md:p-10 max-w-7xl mx-auto space-y-8">',
        '<main id="view-dash" class="app-view flex-1 overflow-y-auto relative z-10 w-full flex-col p-6 md:p-10 max-w-7xl mx-auto space-y-8">'
    )

    # Also check if it was already replaced or slightly different
    if 'id="view-dash" class="flex-1' in html and 'hidden' in html:
        # Just in case
        html = html.replace('id="view-dash" class="flex-1 overflow-y-auto hidden', 'id="view-dash" class="app-view flex-1 overflow-y-auto')

    # 2. Fix the Old Apple Bevels in matte-card overrides
    # Find: box-shadow: var(--card-shadow), inset 0 2px 4px rgba(255,255,255,1), inset 0 0 0 1px rgba(255,255,255,0.8) !important;
    # Replace with a clean, flat modern shadow
    html = html.replace(
        'box-shadow: var(--card-shadow), inset 0 2px 4px rgba(255,255,255,1), inset 0 0 0 1px rgba(255,255,255,0.8) !important;',
        'box-shadow: 0 8px 24px rgba(170, 150, 130, 0.1), inset 0 1px 1px rgba(255,255,255,0.5) !important;'
    )

    # Make the active sidebar item flatter too
    html = html.replace(
        'box-shadow: inset 0 2px 4px rgba(255,255,255,1), 0 4px 8px rgba(0,0,0,0.05) !important;',
        'box-shadow: 0 4px 12px rgba(170, 150, 130, 0.1), inset 0 1px 1px rgba(255,255,255,0.5) !important;'
    )
    
    # 3. Increase matte-card borders to make it look like flat ceramic instead of a glowing bevel
    html = html.replace(
        'border: none !important;',
        'border: 1px solid rgba(255, 255, 255, 0.4) !important;'
    )

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Fixes applied successfully!")

if __name__ == "__main__":
    fix()
