def fix_colors():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace the Unsplash image with a minimal wood texture
    html = html.replace(
        "background-image: url('https://images.unsplash.com/photo-1550684848-fac1c5b4e853?q=80&w=1600');",
        "background-color: #EFEBE5; background-image: url('https://www.transparenttextures.com/patterns/wood-pattern.png');"
    )
    # Remove the 140% saturation that makes things gaudy
    html = html.replace(
        "backdrop-filter: blur(60px) saturate(140%);",
        "backdrop-filter: blur(40px);"
    )
    html = html.replace(
        "-webkit-backdrop-filter: blur(60px) saturate(140%);",
        "-webkit-backdrop-filter: blur(40px);"
    )

    # Mute flashy colors in the UI
    html = html.replace('bg-green-500', 'bg-[#3A3A3C]')
    html = html.replace('text-green-500', 'text-[#3A3A3C]')
    html = html.replace('text-accent-green', 'text-[#2E2B2A]')
    html = html.replace('bg-red-500', 'bg-[#2E2B2A]')
    html = html.replace('bg-[#D3E8D6]', 'bg-[#EAE6E1]')
    html = html.replace('text-blue-500', 'text-[#2E2B2A]')
    
    # Change the gradient on the buttons to be strictly black/dark grey
    html = html.replace(
        "background: linear-gradient(180deg, #3A3A3C 0%, #1C1C1E 100%);",
        "background: #1C1C1E;"
    )

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("Colors muted to minimal wood/black/white successfully.")

if __name__ == "__main__":
    fix_colors()
