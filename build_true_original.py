def create_true_original():
    with open('/Users/nachofrag/Downloads/trenbase_repo/integrate_apple_vision.py', 'r', encoding='utf-8') as f:
        py_content = f.read()

    # Extract the CSS string from the python file
    css_start = py_content.find('custom_css = """') + 16
    css_end = py_content.find('"""', css_start)
    custom_css = py_content[css_start:css_end]

    # Extract the landing string from the python file
    landing_start = py_content.find('new_landing = """') + 17
    landing_end = py_content.find('"""', landing_start)
    new_landing = py_content[landing_start:landing_end]

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TrendBase Vision Original Prototype</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    {custom_css}
</head>
<body class="antialiased min-h-screen bg-[#E6DCD1] text-[#2E2B2A]">
<div class="environment-bg"></div>
{new_landing}
<script>
    lucide.createIcons();
</script>
</body>
</html>
"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
        
    print("True original prototype restored!")

if __name__ == "__main__":
    create_true_original()
