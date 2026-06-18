def apply_window_style():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # We want to wrap the entire content (Nav + Main) inside a giant window
    
    # Remove the background glass from nav
    html = html.replace('class="apple-nav sticky top-0 z-50 w-full px-6 py-4 flex items-center justify-between"', 'class="w-full px-6 py-4 flex items-center justify-between border-b border-black/5"')
    
    # Wrap everything in a giant apple-widget window
    start_body = '<body class="antialiased min-h-screen flex flex-col items-center justify-center">'
    
    # Find <nav>
    nav_idx = html.find('<!-- Top Navigation -->')
    
    # Find end of <main>
    main_end_idx = html.find('</main>') + len('</main>')
    
    content = html[nav_idx:main_end_idx]
    
    window_wrapper = f"""
    <!-- Giant Glass Window -->
    <div class="apple-widget w-[96vw] h-[96vh] flex flex-col overflow-hidden shadow-2xl">
        {content}
    </div>
    """
    
    # Make the body center the window
    html = html.replace('<body class="antialiased min-h-screen flex flex-col">', '<body class="antialiased h-screen w-screen flex flex-col items-center justify-center overflow-hidden">')
    
    html = html.replace(content, window_wrapper)
    
    # Make the main section scrollable since it's now inside a fixed height window
    html = html.replace('<main class="flex-1 p-6 md:p-10 max-w-[1400px] mx-auto w-full">', '<main class="flex-1 p-6 md:p-10 w-full overflow-y-auto">')
    
    # Ensure the table header stays sticky
    html = html.replace('<thead>', '<thead class="sticky top-0 bg-white/80 backdrop-blur-md z-10">')
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    apply_window_style()
