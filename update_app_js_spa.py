import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

show_section_func = """
  window.showSection = function(sectionId, btn) {
    // Hide all sections
    document.querySelectorAll('.dash-section').forEach(sec => {
      sec.classList.remove('active-section');
    });
    
    // Show target section
    const target = document.getElementById(sectionId);
    if(target) {
      target.classList.add('active-section');
    }
    
    // Update active state in sidebar
    if(btn) {
      document.querySelectorAll('#sidebarNav .nav-btn').forEach(b => {
        b.classList.remove('bg-white/10', 'text-white');
        b.classList.add('text-white/50');
      });
      btn.classList.remove('text-white/50');
      btn.classList.add('bg-white/10', 'text-white');
    }
  }
"""

if 'window.showSection =' not in js:
    js = js.replace('window.renderTable = function()', show_section_func + '\n  window.renderTable = function()')

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
