def undo_window_style():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Undo the giant wrapper
    giant_wrapper_start = '<!-- Giant Glass Window -->\n    <div class="apple-widget w-[96vw] h-[96vh] flex flex-col overflow-hidden shadow-2xl">\n        '
    if giant_wrapper_start in html:
        html = html.replace(giant_wrapper_start, '')
        
        # Remove the closing div of the wrapper
        # The wrapper ends right before </body>
        wrapper_end = '    </div>\n    \n\n    <script>'
        html = html.replace(wrapper_end, '\n    <script>')
    
    # Restore the body class
    html = html.replace('<body class="antialiased h-screen w-screen flex flex-col items-center justify-center overflow-hidden">', '<body class="antialiased min-h-screen flex flex-col">')
    
    # Restore nav class
    html = html.replace('class="w-full px-6 py-4 flex items-center justify-between border-b border-black/5"', 'class="apple-nav sticky top-0 z-50 w-full px-6 py-4 flex items-center justify-between"')
    
    # Make main reach the edges closer
    html = html.replace('<main class="flex-1 p-6 md:p-10 w-full overflow-y-auto">', '<main class="flex-1 px-4 py-4 md:px-8 md:py-6 w-full max-w-[1600px] mx-auto flex flex-col">')
    
    # Remove sticky thead
    html = html.replace('<thead class="sticky top-0 bg-white/80 backdrop-blur-md z-10">', '<thead>')
    
    # Make the table widget grow to fill the rest of the height
    html = html.replace('<div class="apple-widget p-8">', '<div class="apple-widget p-8 flex-1 flex flex-col mb-4">')
    html = html.replace('<div class="overflow-x-auto">', '<div class="overflow-x-auto flex-1">')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    undo_window_style()
