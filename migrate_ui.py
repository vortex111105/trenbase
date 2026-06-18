import re

def migrate():
    # Read the original HTML containing the missing features
    with open('original_index.html', 'r', encoding='utf-8') as f:
        old_html = f.read()
        
    # Read the new Dashboard HTML
    with open('dashboard.html', 'r', encoding='utf-8') as f:
        new_html = f.read()

    # 1. Extract the old advanced Product Modal
    modal_match = re.search(r'(<!-- PRODUCT DETAIL MODAL.*?</div>\s*</div>\s*</div>)', old_html, re.DOTALL)
    if not modal_match:
        print("Could not extract old modal")
        return
    old_modal = modal_match.group(1)

    # Restyle old modal to Light Glassmorphism
    old_modal = old_modal.replace('bg-obsidian border border-white/10 rounded-[2.5rem]', 'bg-white rounded-[2.5rem]')
    old_modal = old_modal.replace('text-white', 'text-gray-900')
    old_modal = old_modal.replace('text-white/40', 'text-gray-400')
    old_modal = old_modal.replace('text-white/50', 'text-gray-500')
    old_modal = old_modal.replace('text-white/60', 'text-gray-600')
    old_modal = old_modal.replace('bg-white/5 border border-white/5 rounded-2xl', 'bg-gray-50 border border-gray-100 rounded-2xl')
    old_modal = old_modal.replace('bg-white/5 border border-white/10 rounded-2xl', 'bg-gray-50 border border-gray-100 rounded-2xl')
    old_modal = old_modal.replace('border-white/10', 'border-gray-100')
    old_modal = old_modal.replace('bg-white/5 hover:bg-white/10', 'bg-gray-50 hover:bg-gray-100')
    old_modal = old_modal.replace('bg-black/20', 'bg-gray-100')
    
    # 2. Replace the new modal with the advanced restyled modal
    new_modal_match = re.search(r'(<div id="prodModal" class="hidden.*?</div>\s*</div>\s*</div>)', new_html, re.DOTALL)
    if new_modal_match:
        new_html = new_html.replace(new_modal_match.group(1), old_modal)
    else:
        print("Could not find new modal to replace")

    # 3. Extract the old Mi Negocio section
    negocio_match = re.search(r'(<!-- SECTION: MI NEGOCIO -->\s*<section id="sec-negocio" class="dash-section space-y-6">.*?</section>)', old_html, re.DOTALL)
    if not negocio_match:
        print("Could not extract old negocio")
        return
    old_negocio = negocio_match.group(1)

    # Restyle old Mi Negocio to Light Glassmorphism
    old_negocio = old_negocio.replace('text-white', 'text-gray-900')
    old_negocio = old_negocio.replace('text-white/40', 'text-gray-400')
    old_negocio = old_negocio.replace('text-white/50', 'text-gray-500')
    old_negocio = old_negocio.replace('text-white/60', 'text-gray-600')
    old_negocio = old_negocio.replace('text-white/70', 'text-gray-700')
    old_negocio = old_negocio.replace('bg-white/5 border border-white/10', 'bg-white saas-shadow')
    old_negocio = old_negocio.replace('bg-obsidian border border-white/10 rounded-[2.5rem]', 'bg-white rounded-[2.5rem] saas-shadow')
    old_negocio = old_negocio.replace('border-white/10', 'border-gray-100')
    old_negocio = old_negocio.replace('bg-white/5', 'bg-gray-50')
    old_negocio = old_negocio.replace('bg-white/10', 'bg-gray-100')

    # 4. Replace the new Mi Negocio with the advanced restyled one
    new_negocio_match = re.search(r'(<!-- NEGOCIO SECTION -->\s*<section id="sec-negocio" class="dash-section space-y-6">.*?</section>)', new_html, re.DOTALL)
    if new_negocio_match:
        new_html = new_html.replace(new_negocio_match.group(1), old_negocio)
    else:
        print("Could not find new negocio to replace")
        
    with open('dashboard.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Merged UI successfully.")

if __name__ == '__main__':
    migrate()
