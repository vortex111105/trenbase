import re

def extract_section(content, start_marker, end_marker):
    start = content.find(start_marker)
    end = content.find(end_marker, start)
    if start != -1 and end != -1:
        return content[start:end]
    return ""

def rebuild():
    with open('index.html', 'r', encoding='utf-8') as f:
        idx = f.read()
    
    with open('/Users/nachofrag/Desktop/TrendBase_Vision.html', 'r', encoding='utf-8') as f:
        vision = f.read()

    # We want to use vision as the base.
    # 1. Grab CSS and JS from index.html that are not in vision.
    js_start = idx.find('<!-- ─── JAVASCRIPT APP ENGINE ───────────────────────────────────────────── -->')
    js_content = idx[js_start:idx.rfind('</body>')]

    # Get modals
    modals = extract_section(idx, '<!-- Toast Notification Container -->', '<!-- ─── APP VIEW: LANDING ────────────────────────────────────────────────── -->')
    
    # Get Landing Page Inner Content
    landing_inner = extract_section(idx, '<!-- Hero Section -->', '<!-- ─── APP VIEW: DASHBOARD ─────────────────────────────────────────────── -->')
    
    # Get Dashboard Sections
    dash_content = extract_section(idx, '<!-- Dashboard Content View Area -->', '<!-- Mobile Navigation Bar -->')

    # Replace the landing view inner content in Vision
    vision_landing_start = vision.find('<main id="view-landing"')
    vision_landing_end = vision.find('</main>', vision_landing_start) + 7
    
    # The new landing view should have id="view-landing" class="app-view active-view flex-1 p-8 md:p-12 overflow-y-auto"
    new_landing = f"""
        <main id="view-landing" class="app-view active-view flex-1 p-8 md:p-12 overflow-y-auto">
            {landing_inner}
        </main>
    """
    vision = vision[:vision_landing_start] + new_landing + vision[vision_landing_end:]
    
    # Replace the dashboard view inner content in Vision
    # Wait, index.html has a single view for dash, but toggles inside it.
    # Let's just put all dashboard content inside `view-dash` in Vision.
    # Remove `view-dashboard` and `view-products` from Vision, and insert `view-dash`.
    vision_dash_start = vision.find('<!-- ========================================== -->\n        <!-- DASHBOARD VIEW (EXACT IMAGE REPLICA)       -->')
    vision_products_end = vision.find('</main>', vision.find('<main id="view-products"')) + 7
    
    new_dash = f"""
        <!-- DASHBOARD VIEW -->
        <main id="view-dash" class="app-view flex-1 overflow-y-auto hidden">
            {dash_content}
        </main>
    """
    vision = vision[:vision_dash_start] + new_dash + vision[vision_products_end:]
    
    # Insert Modals before the container
    container_start = vision.find('<!-- MAIN APP CONTAINER -->')
    vision = vision[:container_start] + modals + vision[container_start:]
    
    # Replace the JS
    vision_js_start = vision.find('<script>')
    vision_js_end = vision.rfind('</body>')
    
    vision = vision[:vision_js_start] + js_content + "\n" + vision[vision_js_end:]
    
    # We need to copy head tags (Firebase, Stripe, etc)
    head_start = idx.find('<head>') + 6
    head_end = idx.find('</head>')
    idx_head = idx[head_start:head_end]
    
    # Extract just the <style> from vision
    vision_style_start = vision.find('<style>')
    vision_style_end = vision.find('</style>') + 8
    vision_style = vision[vision_style_start:vision_style_end]
    
    # Combine head
    new_head = f"""<head>
    {idx_head}
    {vision_style}
    </head>"""
    
    vision_real_head_start = vision.find('<head>')
    vision_real_head_end = vision.find('</head>') + 7
    vision = vision[:vision_real_head_start] + new_head + vision[vision_real_head_end:]
    
    with open('index_v3.html', 'w', encoding='utf-8') as f:
        f.write(vision)
        
    print("Rebuild completed into index_v3.html")

rebuild()
